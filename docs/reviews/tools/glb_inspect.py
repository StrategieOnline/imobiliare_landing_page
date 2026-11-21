#!/usr/bin/env python3
"""JUDGE helper: print the contract-relevant facts of a .glb (nodes, materials, tris, world bbox, extensions).
Usage: python3 -I docs/reviews/tools/glb_inspect.py public/models/tower.glb
"""
import json, struct, sys, math

def mat_mul(a, b):
    return [sum(a[r + 4 * k] * b[k + 4 * c] for k in range(4)) for c in range(4) for r in range(4)]  # column-major

def local_matrix(n):
    if 'matrix' in n:
        return n['matrix']
    tx, ty, tz = n.get('translation', [0, 0, 0])
    x, y, z, w = n.get('rotation', [0, 0, 0, 1])
    sx, sy, sz = n.get('scale', [1, 1, 1])
    r = [1 - 2*(y*y+z*z), 2*(x*y+z*w), 2*(x*z-y*w), 0,
         2*(x*y-z*w), 1 - 2*(x*x+z*z), 2*(y*z+x*w), 0,
         2*(x*z+y*w), 2*(y*z-x*w), 1 - 2*(x*x+y*y), 0,
         0, 0, 0, 1]
    s = [sx, 0, 0, 0, 0, sy, 0, 0, 0, 0, sz, 0, 0, 0, 0, 1]
    t = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, tx, ty, tz, 1]
    return mat_mul(t, mat_mul(r, s))

def xform(m, p):
    x, y, z = p
    return [m[0]*x + m[4]*y + m[8]*z + m[12], m[1]*x + m[5]*y + m[9]*z + m[13], m[2]*x + m[6]*y + m[10]*z + m[14]]

def main(path):
    data = open(path, 'rb').read()
    magic, version, length = struct.unpack_from('<4sII', data, 0)
    print(f'file: {path}  bytes: {len(data)} ({len(data)/1048576:.2f} MB)  magic: {magic}  version: {version}')
    clen, ctype = struct.unpack_from('<I4s', data, 12)
    g = json.loads(data[20:20 + clen])
    print('extensionsUsed:', g.get('extensionsUsed', []), ' required:', g.get('extensionsRequired', []))
    acc, meshes, nodes = g.get('accessors', []), g.get('meshes', []), g.get('nodes', [])
    print('materials:')
    for m in g.get('materials', []):
        pbr = m.get('pbrMetallicRoughness', {})
        print(f"  {m.get('name')!r:18} base={pbr.get('baseColorFactor')} metal={pbr.get('metallicFactor', 1)} rough={pbr.get('roughnessFactor', 1)} "
              f"emissive={m.get('emissiveFactor')} ext={list(m.get('extensions', {}).keys())} tex={'baseColorTexture' in pbr}")
    for im in g.get('images', []):
        print('  image:', im.get('name'), im.get('mimeType'))

    def mesh_tris(mi):
        t = 0
        for p in meshes[mi]['primitives']:
            if 'indices' in p:
                t += acc[p['indices']]['count'] // 3
            else:
                t += acc[p['attributes']['POSITION']]['count'] // 3
        return t

    total = 0
    bb = [[math.inf] * 3, [-math.inf] * 3]
    rows = []

    def walk(i, parent, depth):
        nonlocal total
        n = nodes[i]
        m = mat_mul(parent, local_matrix(n))
        tris, nb = 0, None
        if 'mesh' in n:
            tris = mesh_tris(n['mesh'])
            total += tris
            for p in meshes[n['mesh']]['primitives']:
                a = acc[p['attributes']['POSITION']]
                lo, hi = a['min'], a['max']
                for cx in (lo[0], hi[0]):
                    for cy in (lo[1], hi[1]):
                        for cz in (lo[2], hi[2]):
                            w = xform(m, (cx, cy, cz))
                            nb = nb or [[math.inf] * 3, [-math.inf] * 3]
                            for k in range(3):
                                nb[0][k] = min(nb[0][k], w[k]); nb[1][k] = max(nb[1][k], w[k])
                                bb[0][k] = min(bb[0][k], w[k]); bb[1][k] = max(bb[1][k], w[k])
            mats = sorted({g['materials'][p['material']].get('name') for p in meshes[n['mesh']]['primitives'] if 'material' in p})
        else:
            mats = []
        origin = [round(v, 2) for v in xform(m, (0, 0, 0))]
        rows.append((depth, n.get('name'), tris, origin, nb, mats))
        for c in n.get('children', []):
            walk(c, m, depth + 1)

    ident = [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1]
    for s in g.get('scenes', [{'nodes': list(range(len(nodes)))}]):
        for r in s['nodes']:
            walk(r, ident, 0)
    print(f'nodes ({len(rows)}):  name | tris | world origin (pivot) | world bbox y-range | materials')
    for d, name, tris, o, nb, mats in rows:
        yr = f'y {nb[0][1]:.1f}..{nb[1][1]:.1f}' if nb else ''
        print(f"  {'  '*d}{name!r:20} {tris:7d}  pivot={o}  {yr}  {mats}")
    print(f'TOTAL tris: {total}')
    print('world bbox min', [round(v, 2) for v in bb[0]], 'max', [round(v, 2) for v in bb[1]],
          'size', [round(bb[1][k] - bb[0][k], 2) for k in range(3)])
    names = {n.get('name') for n in nodes}
    # SPEC §7.3: Seam_XX is a child of Floor_XX; there is no single full-height 'Seam'.
    want = [f'Floor_{i:02d}' for i in range(24)] + [f'Seam_{i:02d}' for i in range(24)] + ['Crown', 'Podium']
    print('missing contract nodes:', [w for w in want if w not in names] or 'none')
    parent = {c: i for i, n in enumerate(nodes) for c in n.get('children', [])}
    idx = {n.get('name'): i for i, n in enumerate(nodes)}
    def parent_name(name):
        p = parent.get(idx[name])
        return nodes[p].get('name') if p is not None else None
    bad = [f'Seam_{i:02d}' for i in range(24) if f'Seam_{i:02d}' in idx and parent_name(f'Seam_{i:02d}') != f'Floor_{i:02d}']
    print('Seam_XX not parented to Floor_XX:', bad or 'none', '| single Seam node present:', 'Seam' in names)
    want_m = ['M_Glass', 'M_Stone', 'M_WindowGlow', 'M_Frame']
    print('missing contract materials:', [w for w in want_m if w not in {m.get('name') for m in g.get('materials', [])}] or 'none')

if __name__ == '__main__':
    main(sys.argv[1])
