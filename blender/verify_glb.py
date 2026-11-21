"""Re-import the exported GLBs into an empty scene and print what three.js will get.

    /Applications/Blender.app/Contents/MacOS/Blender -b -P blender/verify_glb.py

Blender's importer converts glTF Y-up back to Z-up, so heights print as Z here
(three.js Y). Node origins are printed in glTF/three.js axes (x, y=up, z).
"""

import os

import bpy

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


def tris(obj):
    obj.data.calc_loop_triangles()
    return len(obj.data.loop_triangles)


def report(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=path)
    objs = sorted(bpy.context.scene.objects, key=lambda o: o.name)
    meshes = [o for o in objs if o.type == "MESH"]
    total = sum(tris(o) for o in meshes)
    lo = [min((o.matrix_world @ v.co)[a] for o in meshes for v in o.data.vertices) for a in range(3)]
    hi = [max((o.matrix_world @ v.co)[a] for o in meshes for v in o.data.vertices) for a in range(3)]
    print(f"\n=== {os.path.relpath(path, ROOT)}  {os.path.getsize(path) / 1e6:.2f} MB")
    print(f"nodes ({len(objs)}):")
    for o in objs:
        p = o.matrix_world.translation
        mats = sorted({s.material.name for s in o.material_slots if s.material}) if o.type == "MESH" else []
        parent = o.parent.name if o.parent else "-"
        extra = f"tris={tris(o):6d} mats={','.join(mats)}" if o.type == "MESH" else o.type
        print(f"  {o.name:12s} parent={parent:9s} origin(x,y,z)=({p.x:6.2f},{p.z:6.2f},{-p.y:6.2f})  {extra}")
    print("materials:", sorted(m.name for m in bpy.data.materials if m.users))
    print("images:", [(i.name, tuple(i.size)) for i in bpy.data.images])
    print(f"triangles: {total}")
    print(f"bbox x {lo[0]:.2f}..{hi[0]:.2f}  height {lo[2]:.2f}..{hi[2]:.2f}  depth {-hi[1]:.2f}..{-lo[1]:.2f}"
          f"  -> {hi[0] - lo[0]:.1f} x {hi[2] - lo[2]:.1f} x {hi[1] - lo[1]:.1f} m (w x h x d)")
    print("lights/cameras:", [o.name for o in objs if o.type in {"LIGHT", "CAMERA"}] or "none")


for name in ("tower.glb", "city.glb"):
    p = os.path.join(ROOT, "public", "models", name)
    if os.path.exists(p):
        report(p)
