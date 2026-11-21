"""ORIZONT tower: one reproducible Blender build.

Run headless from the project root:
    /Applications/Blender.app/Contents/MacOS/Blender -b -P blender/build_tower.py
    ... -P blender/build_tower.py -- --no-render      (skip the preview stills)

It clears the scene, builds the tower and the low-poly city, assigns the four
contract materials (SPEC section 4), saves blender/orizont_tower.blend, exports
public/models/tower.glb + public/models/city.glb and renders EEVEE stills to
blender/renders/. The exported GLBs and textures are byte-identical between runs.

Blender is Z-up; the glTF exporter converts to Y-up, so Blender (x, y, z)
becomes three.js (x, z, -y). The tower's front (-Y here) faces three.js +Z.
The silhouette follows public/img/tower-exterior.webp (canonical): a narrow
travertine band on the front-right corner, filled by the loggia stack, whose
leading edge steps in once at mid-height.
"""

import math
import os
import random
import shutil
import sys

import bpy
import numpy as np
from mathutils import Vector

try:
    ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
except NameError:  # run through a bridge exec without __file__
    ROOT = os.environ.get("ORIZONT_ROOT", "/Volumes/Development/imobiliare_landing_page")

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
DO_RENDER = "--no-render" not in ARGS

BLEND_PATH = os.path.join(ROOT, "blender", "orizont_tower.blend")
TEX_DIR = os.path.join(ROOT, "blender", "textures")
RENDER_DIR = os.path.join(ROOT, "blender", "renders")
EXPORT_DIR = os.path.join(ROOT, "blender", "export")         # production copies (Amendment 2)
TOWER_GLB = os.path.join(EXPORT_DIR, "tower.glb")
CITY_GLB = os.path.join(EXPORT_DIR, "city.glb")
SITE_MODELS = os.path.join(ROOT, "public", "models")         # kept until RELEASE drops them

# ---------------------------------------------------------------- dimensions (metres)
HX, HY = 14.0, 10.0                 # half footprint: 28 x 20
PODIUM_H = 6.0                      # double-height lobby
FLOOR_H = 3.6
N_FLOORS = 24
SLAB_H = 0.4                        # slab edge band at the base of each floor
TOP_Z = PODIUM_H + N_FLOORS * FLOOR_H   # 92.4, roof of Floor_23
CROWN_H = 3.6                       # parapet / seam cap top = 96.0 m ("ÎNĂLȚIME 96 m")

# The seam: a travertine band on the front-right corner, proud of the glass.
SEAM_FRONT = -HY - 0.6              # outer stone face
PIER_BACK = -9.6                    # loggia piers are 1 m deep; the loggia lines the rest
CORNER_BACK = -8.6                  # the corner pier returns 2 m along the right facade
SEAM_BACK = -6.4                    # the stone band (loggia floors) runs this deep
SEAM_OUT_X = HX + 0.4               # corner pier proud of the right facade
OPEN_X0, OPEN_X1 = 7.6, 13.0        # loggia opening (5.4 m), centred on x = 10.3
LOGGIA_BACK = -7.0                  # glazed back wall of the loggia (3.6 m deep)
BAND_H = 0.55                       # stone band = loggia floor / soffit of the one below
CHAMFER = 0.4                       # plan chamfer on the band's leading edge
EDGE_LOW, EDGE_HIGH = 4.6, 6.0      # leading edge below / above the mid-height step
KINK_Z0 = PODIUM_H + 11 * FLOOR_H   # the step runs diagonally across storeys 11-12
KINK_Z1 = PODIUM_H + 13 * FLOOR_H
JOINT = 0.05                        # piers sit back from the bands: a storey joint
FACE = 0.06                         # thickness of the stone facing panels
GAP = 0.015                         # half-width of a vertical panel joint
PIER_JOINTS = (6.3,)
CAP_JOINTS = (7.6, 9.0, 10.3, 11.6, 13.0)

GLASS_MODULE = 28.0 / 19            # 1.47 m panels, same grid on front and back
SIDE_MODULE = 1.5
STONE_TILE = 1.5                    # metres per travertine texture repeat

LOGGIA_PIVOT = (10.3, -8.8)         # contract pivot (three.js x 10.3, z 8.8)
assert abs((OPEN_X0 + OPEN_X1) / 2 - LOGGIA_PIVOT[0]) < 1e-9
assert abs((SEAM_FRONT + LOGGIA_BACK) / 2 - LOGGIA_PIVOT[1]) < 1e-9


def edge_x(z):
    """Leading edge of the stone band: one deliberate step in at mid-height,
    as in the canonical photo, carried by a diagonal facet over two storeys."""
    t = min(1.0, max(0.0, (z - KINK_Z0) / (KINK_Z1 - KINK_Z0)))
    return EDGE_LOW + (EDGE_HIGH - EDGE_LOW) * t


def seam_x(z, y):
    """Leading edge at depth y: chamfered across the pier's front metre."""
    t = min(1.0, max(0.0, (PIER_BACK - y) / (PIER_BACK - SEAM_FRONT)))
    return edge_x(z) + CHAMFER * t


# ---------------------------------------------------------------- materials & textures
def srgb(hexstr, a=1.0):
    h = hexstr.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lin = [x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return (*lin, a)


def principled(name, base, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name)     # Blender 5.x: new materials come with a node tree
    bsdf = next(n for n in mat.node_tree.nodes if n.type == "BSDF_PRINCIPLED")
    bsdf.inputs["Base Color"].default_value = srgb(base)
    bsdf.inputs["Metallic"].default_value = metallic
    bsdf.inputs["Roughness"].default_value = roughness
    mat.diffuse_color = srgb(base)
    return mat, bsdf


def save_texture(name, rgb, quality):
    """Write an sRGB-encoded float array (rows bottom-up) to a JPEG and load it back."""
    h, w, _ = rgb.shape
    rgba = np.concatenate([np.clip(rgb, 0, 1), np.ones((h, w, 1))], axis=-1).astype(np.float32)
    img = bpy.data.images.new(name, w, h, alpha=False)
    img.colorspace_settings.name = "sRGB"   # byte image: pixels are stored sRGB-encoded
    img.pixels.foreach_set(rgba.ravel())
    path = os.path.join(TEX_DIR, f"{name}.jpg")
    os.makedirs(TEX_DIR, exist_ok=True)
    img.filepath_raw = path
    img.file_format = "JPEG"
    bpy.context.scene.render.image_settings.quality = quality
    img.save()
    bpy.data.images.remove(img)
    tex = bpy.data.images.load(path)
    tex.name = name
    return tex


def fft_noise(rng, h, w, sx, sy):
    """Periodic (tileable) noise: white noise low-passed in the frequency domain."""
    ky = np.fft.fftfreq(h)[:, None]
    kx = np.fft.fftfreq(w)[None, :]
    f = np.fft.fft2(rng.standard_normal((h, w)))
    n = np.real(np.fft.ifft2(f * np.exp(-((kx * sx) ** 2 + (ky * sy) ** 2))))
    return (n - n.mean()) / (n.std() + 1e-9)


def travertine_texture(size=512):
    """Tileable travertine: horizontal veining, pores, and a broad tone drift so
    panels sampling different offsets read as slightly different stones."""
    rng = np.random.default_rng(2028)
    veins = fft_noise(rng, size, size, 90, 9)
    cloud = fft_noise(rng, size, size, 14, 14)
    fine = fft_noise(rng, size, size, 2.5, 2.5)
    pores = fft_noise(rng, size, size, 6, 1.6)
    drift = fft_noise(rng, size, size, 220, 220)
    t = 0.5 + 0.13 * (0.55 * veins + 0.30 * cloud + 0.15 * fine) + 0.07 * drift
    t = np.clip(t, 0, 1)[..., None]
    light = np.array([0.87, 0.82, 0.73])
    dark = np.array([0.75, 0.69, 0.59])
    col = dark + (light - dark) * t
    col = np.where((pores < -2.1)[..., None], col * 0.80, col)
    return save_texture("travertine", col, 88)


# Eight interior "room cards" in a 2 x 4 atlas. Each lit panel maps onto one card,
# so rooms differ in warmth, brightness and content without any custom shader.
CARD_SPECS = [  # (kelvin colour, intensity, content)
    ("2700", 1.00, "sofa_lamp"),
    ("2700", 0.75, "curtain"),
    ("3000", 0.90, "shelves"),
    ("3000", 0.55, "half_curtain"),
    ("3300", 0.85, "table"),
    ("2900", 0.38, "lamp"),
    ("3100", 0.30, "flat"),      # crown lantern: one soft continuous band
    ("2700", 0.10, "away"),      # loggias of homes nobody is in
]
KELVIN = {"2700": (1.0, 0.62, 0.32), "2900": (1.0, 0.66, 0.38),
          "3000": (1.0, 0.70, 0.43), "3100": (1.0, 0.73, 0.47), "3300": (1.0, 0.78, 0.54)}
HOME_CARDS = (0, 1, 2, 3, 4, 5)
CARD_LANTERN, CARD_AWAY = 6, 7


def room_atlas(card_px=128):
    rng = np.random.default_rng(46)
    h, w = card_px * 4, card_px * 2
    out = np.zeros((h, w, 3))
    t = (np.arange(card_px)[:, None] + 0.5) / card_px * np.ones((1, card_px))   # 0 sill .. 1 ceiling
    s = (np.arange(card_px)[None, :] + 0.5) / card_px * np.ones((card_px, 1))
    for c, (kelvin, inten, content) in enumerate(CARD_SPECS):
        v = 0.42 + 0.33 * t                                   # brighter towards the ceiling
        v = np.where(t > 0.88, 1.0, v)                        # cove / ceiling band
        v = np.where(t < 0.12, 0.30, v)                       # dark sill zone
        if content == "sofa_lamp":
            v = np.where((s > 0.10) & (s < 0.60) & (t > 0.12) & (t < 0.30), 0.22, v)
            v = np.where((abs(s - 0.78) < 0.012) & (t > 0.12) & (t < 0.55), 0.25, v)
            v = np.maximum(v, 1.15 * np.exp(-(((s - 0.78) / 0.07) ** 2 + ((t - 0.60) / 0.05) ** 2)))
        elif content == "curtain":
            v = v * (0.80 + 0.20 * np.abs(np.sin(s * math.pi * 7)))
        elif content == "shelves":
            shelf = (s > 0.62) & (s < 0.95) & (t > 0.18) & (t < 0.80)
            v = np.where(shelf & ((abs(t - 0.36) < 0.012) | (abs(t - 0.56) < 0.012)
                                  | (abs(t - 0.76) < 0.012) | (abs(s - 0.62) < 0.01)), 0.2, v)
            v = np.maximum(v, 1.1 * np.exp(-(((s - 0.30) / 0.10) ** 2 + ((t - 0.74) / 0.05) ** 2)))
        elif content == "half_curtain":
            v = np.where(s < 0.45, v * (0.55 + 0.15 * np.abs(np.sin(s * math.pi * 9))), v)
        elif content == "table":
            v = np.where((s > 0.30) & (s < 0.70) & (abs(t - 0.30) < 0.015), 0.2, v)
            v = np.where(((abs(s - 0.34) < 0.01) | (abs(s - 0.66) < 0.01)) & (t > 0.12) & (t < 0.30), 0.2, v)
        elif content == "lamp":
            v = 0.35 * v + 0.9 * np.exp(-(((s - 0.25) / 0.09) ** 2 + ((t - 0.5) / 0.08) ** 2))
        elif content in ("flat", "away"):
            v = 0.75 + 0.25 * t
        v = v * (1.0 + 0.04 * rng.standard_normal(v.shape))
        rgb = np.clip(v * inten, 0, 1.2)[..., None] * np.array(KELVIN[kelvin])
        col, row = c % 2, c // 2
        out[row * card_px:(row + 1) * card_px, col * card_px:(col + 1) * card_px] = rgb
    return save_texture("room_atlas", out, 85)


def card_uv(card, j=0, n=1):
    """UVs of slice j/n of a room card, in face order (p,z0),(q,z0),(q,z1),(p,z1)."""
    col, row = card % 2, card // 2
    inset = 2 / 256
    u0, u1 = col * 0.5 + inset, col * 0.5 + 0.5 - inset
    v0, v1 = row * 0.25 + inset, row * 0.25 + 0.25 - inset
    ua, ub = u0 + (u1 - u0) * j / n, u0 + (u1 - u0) * (j + 1) / n
    return [(ua, v0), (ub, v0), (ub, v1), (ua, v1)]


def build_materials():
    mats = {}
    glass, bsdf = principled("M_Glass", "#2a2118", metallic=0.6, roughness=0.15)
    # A glossy coat (KHR_materials_clearcoat) gives the dark bronze its glassy sky
    # reflection at grazing angles without changing the contract's base/metal/rough.
    bsdf.inputs["Coat Weight"].default_value = 1.0
    bsdf.inputs["Coat Roughness"].default_value = 0.03
    mats["M_Glass"] = glass
    stone, bsdf = principled("M_Stone", "#cdbfa6", roughness=0.8)
    tex = stone.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = travertine_texture()
    stone.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    mats["M_Stone"] = stone
    glow, bsdf = principled("M_WindowGlow", "#3a2a1c", roughness=0.6)
    tex = glow.node_tree.nodes.new("ShaderNodeTexImage")
    tex.image = room_atlas()
    glow.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = 2.0
    mats["M_WindowGlow"] = glow
    mats["M_Frame"], _ = principled("M_Frame", "#33271c", metallic=0.85, roughness=0.35)
    mats["M_City"], _ = principled("M_City", "#9b948a", roughness=0.9)
    return mats


# ---------------------------------------------------------------- mesh builder
class MeshBuilder:
    """Collects faces in world space; to_object() re-bases them on a pivot.
    Faces get world-space triplanar UVs (plus an optional offset, used to vary
    stone panels) unless explicit UVs are given (room cards)."""

    def __init__(self):
        self.verts, self.faces, self.mats, self.uvs = [], [], [], []

    def face(self, pts, mat, want=None, uv=None, uv_off=(0.0, 0.0)):
        pts = [Vector(p) for p in pts]
        if want is not None:
            n = (pts[1] - pts[0]).cross(pts[2] - pts[0])
            if n.dot(Vector(want)) < 0:
                pts.reverse()
                uv = uv[::-1] if uv else uv
        i = len(self.verts)
        self.verts += pts
        self.faces.append(tuple(range(i, i + len(pts))))
        self.mats.append(mat)
        self.uvs.append(uv if uv else uv_off)

    def hexa(self, bottom, top, mat, caps=True, uv_off=(0.0, 0.0)):
        """Solid from a plan quad at two levels; each ring is [(x, y, z)] * 4.
        caps=False omits top and bottom (fins/bars that stack or hide)."""
        area = sum(bottom[i][0] * bottom[(i + 1) % 4][1] - bottom[(i + 1) % 4][0] * bottom[i][1]
                   for i in range(4))
        if area < 0:
            bottom, top = bottom[::-1], top[::-1]
        for i in range(4):
            j = (i + 1) % 4
            self.face([bottom[i], bottom[j], top[j], top[i]], mat, uv_off=uv_off)
        if caps:
            self.face(top, mat, uv_off=uv_off)
            self.face(bottom[::-1], mat, uv_off=uv_off)

    def box(self, x0, x1, y0, y1, z0, z1, mat, caps=True, uv_off=(0.0, 0.0)):
        plan = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        self.hexa([(x, y, z0) for x, y in plan], [(x, y, z1) for x, y in plan], mat, caps, uv_off)

    def to_object(self, name, pivot, materials, collection, parent=None):
        pivot = Vector(pivot)
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata([v - pivot for v in self.verts], [], self.faces)
        used = sorted(set(self.mats), key=["M_Glass", "M_Stone", "M_WindowGlow",
                                           "M_Frame", "M_City"].index)
        for m in used:
            mesh.materials.append(materials[m])
        uv = mesh.uv_layers.new(name="UVMap")
        for poly, m, fuv in zip(mesh.polygons, self.mats, self.uvs):
            poly.material_index = used.index(m)
            if isinstance(fuv, list):
                for k, li in enumerate(poly.loop_indices):
                    uv.data[li].uv = fuv[k]
                continue
            n = poly.normal
            ax, ay, az = abs(n.x), abs(n.y), abs(n.z)
            for li in poly.loop_indices:
                p = self.verts[mesh.loops[li].vertex_index]
                if az >= ax and az >= ay:
                    u, v = p.x, p.y
                elif ax >= ay:
                    u, v = p.y, p.z
                else:
                    u, v = p.x, p.z
                uv.data[li].uv = (u / STONE_TILE + fuv[0], v / STONE_TILE + fuv[1])
        mesh.validate()
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        collection.objects.link(obj)
        place(obj, pivot, parent)
        return obj


def place(obj, world_pos, parent):
    if parent is not None:
        obj.parent = parent
        obj.location = Vector(world_pos) - parent.matrix_world.translation
    else:
        obj.location = world_pos
    bpy.context.view_layer.update()


def empty(name, pos, collection, parent=None):
    e = bpy.data.objects.new(name, None)
    e.empty_display_size = 4
    collection.objects.link(e)
    place(e, Vector(pos), parent)
    return e


# ---------------------------------------------------------------- facade helpers
def glass_path(z1, inset=0.0):
    """Glazed perimeter, counter-clockwise from above: from inside the corner pier,
    round the back, to just inside the band's leading edge (which can only move
    right as z rises, so ending at the storey's top edge never leaves a gap)."""
    x_end = seam_x(z1, -HY + inset) + 0.05
    return [(HX - inset, CORNER_BACK - 0.1), (HX - inset, HY - inset), (-HX + inset, HY - inset),
            (-HX + inset, -HY + inset), (x_end, -HY + inset)]


def outward(a, b):
    d = (Vector(b) - Vector(a)).normalized()
    return Vector((d.y, -d.x)), d


def offset_path(path, off):
    """Miter-offset a polyline outward (positive) or inward (negative)."""
    out = []
    for i, p in enumerate(path):
        p = Vector(p)
        ns = []
        if i > 0:
            ns.append(outward(path[i - 1], path[i])[0])
        if i < len(path) - 1:
            ns.append(outward(path[i], path[i + 1])[0])
        if len(ns) == 1:
            out.append(p + ns[0] * off)
        else:
            m = (ns[0] + ns[1])
            out.append(p + m * (off / (1 + ns[0].dot(ns[1]))))
    return out


def panel_points(a, b, module):
    a, b = Vector(a), Vector(b)
    length = (b - a).length
    n = max(1, round(length / module))
    return [a + (b - a).normalized() * length / n * k for k in range(n + 1)]


def anchored_points(a, b, module, from_end):
    """Fixed module measured from one end; the other (sliding) end gets a partial
    panel, so mullions line up from floor to floor while the stone edge moves."""
    a, b = Vector(a), Vector(b)
    if from_end:
        return anchored_points(b, a, module, False)[::-1]
    length, d = (b - a).length, (b - a).normalized()
    n = int((length - 0.3) / module)
    return [a + d * module * k for k in range(n + 1)] + [b]


def facade_ring(mb, path, z0, z1, lights, module, fin_every=3, sliding_ends=False, glass_mb=None):
    """Glass panels with bronze fins. lights(n) returns, per panel, None (dark glass)
    or (card, j, n): panel j of an n-panel room lit with that room card.
    Panels go to glass_mb when given, so the glazing can be its own node."""
    gmb = glass_mb or mb
    panels = []
    for s in range(len(path) - 1):
        a, b = Vector(path[s]), Vector(path[s + 1])
        if sliding_ends and s == 0:
            pts = anchored_points(a, b, SIDE_MODULE, from_end=True)
        elif sliding_ends and s == len(path) - 2:
            pts = anchored_points(a, b, GLASS_MODULE, from_end=False)
        else:
            pts = panel_points(a, b, module)
        n, _ = outward(a, b)
        panels += [(pts[k], pts[k + 1], n, k == 0) for k in range(len(pts) - 1)]

    specs = lights(len(panels))
    for (p, q, n, _), spec in zip(panels, specs):
        quad = [(p.x, p.y, z0), (q.x, q.y, z0), (q.x, q.y, z1), (p.x, p.y, z1)]
        if spec is None:
            gmb.face(quad, "M_Glass", want=(n.x, n.y, 0))
        else:
            gmb.face(quad, "M_WindowGlow", want=(n.x, n.y, 0), uv=card_uv(*spec))

    # Fins at each panel joint; every third one deeper, for a slender vertical rhythm.
    for k, (p, q, n, seg_start) in enumerate(panels):
        if k == 0:
            continue
        d = (q - p).normalized()
        depth = 0.55 if k % fin_every == 0 else 0.26
        w = 0.07 if not seg_start else 0.16   # corner posts a touch heavier
        plan = [p - d * w / 2 - n * 0.05, p + d * w / 2 - n * 0.05,
                p + d * w / 2 + n * depth, p - d * w / 2 + n * depth]
        mb.hexa([(v.x, v.y, z0) for v in plan], [(v.x, v.y, z1) for v in plan], "M_Frame", caps=False)
    return sum(s is not None for s in specs), len(specs)


def slab_ring(mb, path, z0, z1, out=0.12, inn=0.35, mat="M_Frame"):
    outer, inner = offset_path(path, out), offset_path(path, -inn)
    for s in range(len(path) - 1):
        plan = [inner[s], inner[s + 1], outer[s + 1], outer[s]]
        mb.hexa([(v.x, v.y, z0) for v in plan], [(v.x, v.y, z1) for v in plan], mat)


# ---------------------------------------------------------------- lighting by occupancy
def place_rooms(span, n_rooms, rng, cards, size=(2, 4)):
    """Light n_rooms runs of adjacent panels inside an apartment's span of panels."""
    lit = {}
    for _ in range(n_rooms):
        for _attempt in range(12):
            n = rng.randint(*size)
            if n > len(span):
                break
            start = rng.randint(0, len(span) - n)
            idx = span[start:start + n]
            if any(i in lit or i - 1 in lit or i + 1 in lit for i in idx):
                continue
            card = rng.choice(cards)
            for j, i in enumerate(idx):
                lit[i] = (card, j, n)
            break
    return lit


def apartment_lights(rng, n_apts, p_home):
    """Two homes per storey (one on the penthouse storeys). About half are home at
    dusk and show 2-3 lit rooms; an empty home sometimes leaves one dim lamp on.
    Apartment 0 owns the loggia. Returns (lights callback, home flags)."""
    homes = [rng.random() < p_home for _ in range(n_apts)]
    plan = [rng.choice((2, 2, 3, 3)) if h else 0 for h in homes]
    dim = [not h and rng.random() < 0.35 for h in homes]

    def lights(n_panels):
        cut = [round(n_panels * k / n_apts) for k in range(n_apts + 1)]
        lit = {}
        for a in range(n_apts):
            span = list(range(cut[a], cut[a + 1]))
            if plan[a]:
                lit.update(place_rooms(span, plan[a], rng, HOME_CARDS))
            elif dim[a]:
                lit.update(place_rooms(span, 1, rng, (5,), size=(2, 2)))
        return [lit.get(i) for i in range(n_panels)]
    return lights, homes


def random_runs(rng, share, cards):
    def lights(n_panels):
        out, i = [None] * n_panels, 0
        while i < n_panels:
            n = rng.randint(2, 3)
            if rng.random() < share:
                card = rng.choice(cards)
                for j in range(min(n, n_panels - i)):
                    out[i + j] = (card, j, n)
            i += n
        return out
    return lights


# ---------------------------------------------------------------- the seam
def stone_wall(mb, z0, z1, x_left, x_right, y0, y1, rng, joints=()):
    """A stone mass whose left face follows x_left(z, y). Where vertical joints fall
    inside the front face it gets a recessed core plus 6 cm facing panels with
    shadow gaps; every panel samples the texture at its own offset (tone variation)."""
    def off():
        return (rng.random(), rng.random())

    def ok(x):
        return all(x_left(z, y0) + 0.25 < x < x_right - 0.25 for z in (z0, z1))
    xs = [x for x in joints if ok(x)]
    ring = lambda z, ya, yb, xa, xb: [(xa(z, ya), ya, z), (xb, ya, z), (xb, yb, z), (xa(z, yb), yb, z)]
    if not xs:
        mb.hexa(ring(z0, y0, y1, x_left, x_right), ring(z1, y0, y1, x_left, x_right), "M_Stone",
                uv_off=off())
        return
    yc = y0 + FACE
    mb.hexa(ring(z0, yc, y1, x_left, x_right), ring(z1, yc, y1, x_left, x_right), "M_Stone",
            uv_off=off())
    bounds = [None] + xs + [x_right]
    for k in range(len(bounds) - 1):
        xb = bounds[k + 1] - (GAP if k + 1 < len(bounds) - 1 else 0)
        if bounds[k] is None:
            xa = x_left
        else:
            xa = (lambda v: lambda z, y: v)(bounds[k] + GAP)
        mb.hexa(ring(z0, y0, yc, xa, xb), ring(z1, y0, yc, xa, xb), "M_Stone", uv_off=off())


def band(mb, z0, z1, rng, joints=()):
    """Full-depth stone across the seam (a loggia floor, the podium head, the cap),
    in three non-overlapping strips: chamfered front, corner return, hidden back."""
    stone_wall(mb, z0, z1, seam_x, SEAM_OUT_X, SEAM_FRONT, PIER_BACK, rng, joints)
    edge = lambda z, y: edge_x(z)
    stone_wall(mb, z0, z1, edge, SEAM_OUT_X, PIER_BACK, CORNER_BACK, rng)
    stone_wall(mb, z0, z1, edge, HX - 0.1, CORNER_BACK, SEAM_BACK, rng)


def piers(mb, z0, z1, rng):
    """Leading pier (diagonal left face, panel joints) and corner pier, 5 cm back from the bands."""
    yf = SEAM_FRONT + JOINT
    stone_wall(mb, z0, z1, seam_x, OPEN_X0, yf, PIER_BACK, rng, PIER_JOINTS)
    mb.box(OPEN_X1, SEAM_OUT_X - JOINT, yf, CORNER_BACK, z0, z1, "M_Stone",
           uv_off=(rng.random(), rng.random()))


def seam_storey(mb, z0, z1, rng):
    zb = z0 + BAND_H
    band(mb, z0, zb, rng)
    piers(mb, zb, z1, rng)


# ---------------------------------------------------------------- tower parts
STRUCT_COLUMNS = [(x, 9.1) for x in (-12.6, -6.3, 0.0, 6.3, 12.6)] + \
                 [(x, -9.1) for x in (-12.6, -6.3, 0.0)] + \
                 [(-13.1, -3.0), (-13.1, 3.0), (13.1, -2.0), (13.1, 4.0)]


def build_floor(i, mats, col, root, rng, stats):
    z0 = PODIUM_H + i * FLOOR_H
    z1 = z0 + FLOOR_H
    mb, gb, sb = MeshBuilder(), MeshBuilder(), MeshBuilder()
    path = glass_path(z1)
    slab_ring(mb, path, z0, z0 + SLAB_H)
    penthouse = i >= N_FLOORS - 2
    lights, homes = apartment_lights(rng, 1 if penthouse else 2, 0.75 if penthouse else 0.55)
    lit, total = facade_ring(mb, path, z0 + SLAB_H, z1, lights, GLASS_MODULE,
                             sliding_ends=True, glass_mb=gb)
    stats["lit"] += lit
    stats["panels"] += total
    stats["homes"] += sum(homes)
    seam_storey(sb, z0, z1, rng)
    # Structure that reads when Glass_XX is hidden (the construction look): a core and slim columns.
    mb.box(-4.0, 3.0, -1.5, 4.5, z0 + SLAB_H, z1, "M_Frame", caps=False)
    for x, y in STRUCT_COLUMNS:
        mb.box(x - 0.22, x + 0.22, y - 0.22, y + 0.22, z0 + SLAB_H, z1, "M_Frame", caps=False)
    # Lid so a partly built tower reads solid from above (hidden once the next floor lands).
    xl = edge_x(z1)
    mb.face([(-HX, -HY, z1), (xl, -HY, z1), (xl, HY, z1), (-HX, HY, z1)], "M_Frame", want=(0, 0, 1))
    mb.face([(xl, SEAM_BACK, z1), (HX, SEAM_BACK, z1), (HX, HY, z1), (xl, HY, z1)], "M_Frame",
            want=(0, 0, 1))
    # Floor_XX = slab edge, fins, core/columns and lid (the bare frame); its children carry
    # the rest, all pivoted on the storey base so the whole storey moves as one.
    floor = mb.to_object(f"Floor_{i:02d}", (0, 0, z0), mats, col, parent=root)
    gb.to_object(f"Glass_{i:02d}", (0, 0, z0), mats, col, parent=floor)
    sb.to_object(f"Seam_{i:02d}", (0, 0, z0), mats, col, parent=floor)
    build_loggia(i, z0, z1, mats, col, floor, rng, home=homes[0])
    return homes[0]


def build_loggia(i, z0, z1, mats, col, floor, rng, home):
    zf = z0 + BAND_H            # loggia floor (top of the stone band)
    mb = MeshBuilder()
    # Glazed back wall: two rooms seen through the sliding doors, dim when nobody is home.
    xm = (OPEN_X0 + OPEN_X1) / 2
    for xa, xb in ((OPEN_X0, xm), (xm, OPEN_X1)):
        card = rng.choice(HOME_CARDS[:5]) if home else CARD_AWAY
        mb.face([(xa, LOGGIA_BACK, zf), (xb, LOGGIA_BACK, zf), (xb, LOGGIA_BACK, z1),
                 (xa, LOGGIA_BACK, z1)], "M_WindowGlow", want=(0, -1, 0), uv=card_uv(card))
    # Sliding-door frames: three mullions, a head and a threshold.
    for k in range(1, 4):
        x = OPEN_X0 + (OPEN_X1 - OPEN_X0) * k / 4
        mb.box(x - 0.035, x + 0.035, LOGGIA_BACK - 0.12, LOGGIA_BACK, zf, z1, "M_Frame", caps=False)
    mb.box(OPEN_X0, OPEN_X1, LOGGIA_BACK - 0.12, LOGGIA_BACK, z1 - 0.38, z1 - 0.30, "M_Frame")
    mb.box(OPEN_X0, OPEN_X1, LOGGIA_BACK - 0.12, LOGGIA_BACK, zf, zf + 0.05, "M_Frame")
    # Stone side returns lining the recess behind the piers.
    mb.box(OPEN_X0 - 0.5, OPEN_X0, PIER_BACK, LOGGIA_BACK, zf, z1, "M_Stone", uv_off=(0.3, 0.6))
    mb.box(OPEN_X1, OPEN_X1 + 0.5, CORNER_BACK, LOGGIA_BACK, zf, z1, "M_Stone", uv_off=(0.7, 0.2))
    # Warm cove strip in the soffit along the glazing (on only when someone is home).
    mb.face([(OPEN_X0, LOGGIA_BACK - 0.45, z1 - 0.01), (OPEN_X1, LOGGIA_BACK - 0.45, z1 - 0.01),
             (OPEN_X1, LOGGIA_BACK - 0.25, z1 - 0.01), (OPEN_X0, LOGGIA_BACK - 0.25, z1 - 0.01)],
            "M_WindowGlow", want=(0, 0, -1), uv=card_uv(4 if home else CARD_AWAY))
    # Frameless glass balustrade, drawn as its slim bronze cap and base shoe: the clear
    # pane itself is left out (an opaque M_Glass pane read as a black bar).
    yb, top = SEAM_FRONT + 0.25, zf + 1.05
    mb.box(OPEN_X0, OPEN_X1, yb - 0.03, yb + 0.03, top, top + 0.05, "M_Frame")
    mb.box(OPEN_X0, OPEN_X1, yb - 0.04, yb + 0.04, zf, zf + 0.08, "M_Frame")
    mb.to_object(f"Loggia_{i:02d}", (*LOGGIA_PIVOT, z0), mats, col, parent=floor)


def build_seam_podium(mats, col, podium, rng):
    """The seam lands on the ground: piers down to the plinth framing a
    double-height glazed entrance, under a stone head band."""
    mb = MeshBuilder()
    piers(mb, 0.0, PODIUM_H - BAND_H, rng)
    band(mb, PODIUM_H - BAND_H, PODIUM_H, rng)
    return mb.to_object("Seam_Podium", (0, 0, 0), mats, col, parent=podium)


def build_seam_crown(mats, col, crown, rng):
    """The band ends in a stone cap level with the parapet (96 m), jointed like the piers."""
    mb = MeshBuilder()
    band(mb, TOP_Z, TOP_Z + CROWN_H, rng, joints=CAP_JOINTS)
    return mb.to_object("Seam_Crown", (0, 0, TOP_Z), mats, col, parent=crown)


def build_podium(mats, col, root, rng):
    mb = MeshBuilder()
    mb.box(-18.0, 19.0, -15.0, 14.0, -0.05, 0.3, "M_Stone")          # stone plinth / forecourt
    # Recessed double-height lobby glazing, warmly lit; it runs behind the seam piers too.
    i = 1.2
    ring = [(HX - i, -HY + i), (HX - i, HY - i), (-HX + i, HY - i), (-HX + i, -HY + i), (HX - i, -HY + i)]
    facade_ring(mb, ring, 0.3, PODIUM_H - 0.6, random_runs(rng, 0.6, (0, 2, 4)), 2.1, fin_every=1)
    for x in (-14.0, -7.0):                                            # bronze-clad columns
        mb.box(x - 0.3, x + 0.3, -HY - 0.3, -HY + 0.3, 0.3, PODIUM_H - 0.6, "M_Frame")
    for y in (0.0, 5.0, HY):
        for x in (-HX, HX):
            mb.box(x - 0.3, x + 0.3, y - 0.3, y + 0.3, 0.3, PODIUM_H - 0.6, "M_Frame")
    for x in (-7.0, 0.0, 7.0):
        mb.box(x - 0.3, x + 0.3, HY - 0.3, HY + 0.3, 0.3, PODIUM_H - 0.6, "M_Frame")
    slab_ring(mb, glass_path(PODIUM_H), PODIUM_H - 0.6, PODIUM_H, out=0.12, inn=1.6)
    mb.box(-11.5, -1.5, -14.0, -HY + 0.12, 4.3, 4.55, "M_Frame")      # entrance canopy
    mb.face([(-HX, -HY, PODIUM_H), (HX, -HY, PODIUM_H), (HX, HY, PODIUM_H), (-HX, HY, PODIUM_H)],
            "M_Frame", want=(0, 0, 1))
    podium = mb.to_object("Podium", (0, 0, 0), mats, col, parent=root)
    build_seam_podium(mats, col, podium, rng)


def build_crown(mats, col, root, rng):
    z0 = TOP_Z
    mb = MeshBuilder()
    path = glass_path(z0 + CROWN_H)
    slab_ring(mb, path, z0, z0 + 0.7, out=0.12, inn=0.6)
    # Set-back glass lantern (roof amenity) as one soft continuous band of light.
    lantern = [(10.5, -6.0), (10.5, 8.0), (-12.0, 8.0), (-12.0, -6.0), (10.5, -6.0)]
    facade_ring(mb, lantern, z0 + 0.7, z0 + 2.9, lambda n: [(CARD_LANTERN, 0, 1)] * n, 1.5, fin_every=2)
    mb.box(-12.3, 10.8, -6.3, 8.3, z0 + 2.9, z0 + 3.1, "M_Frame")
    # Bronze fin screen continuing the facade rhythm past the roof line.
    screen = offset_path(path, 0.1)
    for s in range(len(screen) - 1):
        a, b = screen[s], screen[s + 1]
        n, d = outward(a, b)
        for p in panel_points(a, b, GLASS_MODULE / 3)[1:-1]:
            plan = [p - d * 0.05, p + d * 0.05, p + d * 0.05 + n * 0.45, p - d * 0.05 + n * 0.45]
            mb.hexa([(v.x, v.y, z0 + 0.7) for v in plan], [(v.x, v.y, z0 + CROWN_H - 0.3) for v in plan],
                    "M_Frame", caps=False)
    slab_ring(mb, [tuple(v) for v in screen], z0 + CROWN_H - 0.4, z0 + CROWN_H, out=0.5, inn=0.1)
    mb.face([(-HX, -HY, z0 + 0.7), (HX, -HY, z0 + 0.7), (HX, HY, z0 + 0.7), (-HX, HY, z0 + 0.7)],
            "M_Frame", want=(0, 0, 1))
    crown = mb.to_object("Crown", (0, 0, z0), mats, col, parent=root)
    build_seam_crown(mats, col, crown, rng)


def build_tower(mats):
    col = bpy.data.collections.new("TOWER")
    bpy.context.scene.collection.children.link(col)
    rng = random.Random(2028)
    root = empty("Tower", (0, 0, 0), col)
    build_podium(mats, col, root, rng)
    stats = {"lit": 0, "panels": 0, "homes": 0}
    loggia_home = [build_floor(i, mats, col, root, rng, stats) for i in range(N_FLOORS)]
    build_crown(mats, col, root, rng)
    print(f"OCCUPANCY homes lit {stats['homes']}/46, facade panels lit {stats['lit']}/{stats['panels']}"
          f" = {100 * stats['lit'] / stats['panels']:.1f}%, loggias lit {sum(loggia_home)}/{N_FLOORS}")
    return col, loggia_home


# ---------------------------------------------------------------- city context
def build_city(mats, lot_filter=None):
    """lot_filter(centre, distance, height) -> height or None (skip); used by the
    motion guides to clear sightlines. Without it the city is the exported one."""
    col = bpy.data.collections.new("CITY")
    bpy.context.scene.collection.children.link(col)
    rng = random.Random(46)
    g = MeshBuilder()
    r = 700.0
    g.face([(-r, -r, -0.06), (r, -r, -0.06), (r, r, -0.06), (-r, r, -0.06)], "M_City", want=(0, 0, 1))
    g.to_object("Ground", (0, 0, 0), mats, col)

    lot, clear = 46.0, 70.0          # lot grid with streets; clear plot round the tower
    lots = []
    for ix in range(-13, 14):
        for iy in range(-13, 14):
            c = Vector((ix * lot, iy * lot))
            d = c.length
            if clear < d < 600 and rng.random() < (0.55 if d < 260 else 0.22):
                lots.append((c, d))
    rng.shuffle(lots)
    lots = sorted(lots[:110], key=lambda t: t[1])

    b = MeshBuilder()
    for c, d in lots:
        w, dp = rng.uniform(16, 34), rng.uniform(14, 30)
        if rng.random() < 0.5:
            w, dp = dp, w
        # A handful of mid-rise office towers frame the skyline; the rest is low/mid-rise.
        roll = rng.random()
        if 110 < d < 420 and roll < 0.18:
            h, w, dp = rng.uniform(55, 78), min(w, 24), min(dp, 24)
        elif roll < 0.35:
            h = rng.uniform(24, 42)
        else:
            h = rng.uniform(7, 22)
        # Keep the approach in front of the tower (-Y here, +Z in three.js) low-rise.
        ang = math.degrees(math.atan2(c.y, c.x))
        if -165 < ang < -15 and d < 320:
            h = min(h, 11.0)
        cx, cy = c.x + rng.uniform(-5, 5), c.y + rng.uniform(-5, 5)
        if lot_filter is not None:
            h = lot_filter(Vector((cx, cy)), d, h)
            if h is None:
                continue
        b.box(cx - w / 2, cx + w / 2, cy - dp / 2, cy + dp / 2, -0.05, h, "M_City")
        if h > 20 and rng.random() < 0.45:          # set-back top storeys
            s = rng.uniform(0.55, 0.8)
            b.box(cx - w * s / 2, cx + w * s / 2, cy - dp * s / 2, cy + dp * s / 2,
                  h, h + rng.uniform(3, 9), "M_City")
    b.to_object("City_Blocks", (0, 0, 0), mats, col)
    return col, len(lots)


# ---------------------------------------------------------------- export
def export_glb(col, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bpy.ops.object.select_all(action="DESELECT")
    for o in col.all_objects:
        o.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=path, export_format="GLB", use_selection=True, export_apply=True,
        export_cameras=False, export_lights=False, export_yup=True,
        export_image_format="JPEG", export_image_quality=85,
        export_draco_mesh_compression_enable=False, export_extras=False)


# ---------------------------------------------------------------- preview renders
SUN_DIR = Vector((0.6, 0.8, 0.09)).normalized()   # towards the sun: low, behind-right of the front


def setup_render_world(loggia_home):
    scene = bpy.context.scene
    scene.render.engine = "BLENDER_EEVEE"
    ee = scene.eevee
    ee.taa_render_samples = 64
    for attr, val in (("use_raytracing", True), ("use_shadows", True)):
        if hasattr(ee, attr):
            setattr(ee, attr, val)
    scene.view_settings.view_transform = "AgX"
    scene.view_settings.look = "AgX - Medium High Contrast"

    # Dusk sky: a vertical gradient (dark ground, warm horizon, blue zenith), a warm
    # glow round the sun and the pink "belt of Venus" opposite it, so the bronze glass
    # has something to reflect on every face.
    world = bpy.data.worlds.new("Dusk")
    scene.world = world
    nt = world.node_tree     # Blender 5.x worlds always have a node tree
    nt.nodes.clear()
    N = nt.nodes.new
    coord, sep = N("ShaderNodeTexCoord"), N("ShaderNodeSeparateXYZ")
    remap, ramp = N("ShaderNodeMath"), N("ShaderNodeValToRGB")
    dot, clamp, powr, glow = N("ShaderNodeVectorMath"), N("ShaderNodeMath"), N("ShaderNodeMath"), N("ShaderNodeMix")
    bg, out = N("ShaderNodeBackground"), N("ShaderNodeOutputWorld")
    L = nt.links.new
    L(coord.outputs["Generated"], sep.inputs[0])
    remap.operation = "MULTIPLY_ADD"                 # z in [-1, 1] -> [0, 1]
    L(sep.outputs["Z"], remap.inputs[0])
    remap.inputs[1].default_value, remap.inputs[2].default_value = 0.5, 0.5
    L(remap.outputs[0], ramp.inputs["Fac"])
    els = ramp.color_ramp.elements
    els[0].position, els[0].color = 0.0, srgb("#1c1a19")
    els[1].position, els[1].color = 1.0, srgb("#18233c")
    for pos, hexc in ((0.49, "#4a3e37"), (0.50, "#dba27a"), (0.53, "#c7a28c"), (0.62, "#8486a3"),
                      (0.80, "#2b3d60")):
        els.new(pos).color = srgb(hexc)
    dot.operation = "DOT_PRODUCT"
    L(coord.outputs["Generated"], dot.inputs[0])
    dot.inputs[1].default_value = SUN_DIR
    clamp.operation, clamp.use_clamp = "MAXIMUM", True
    L(dot.outputs["Value"], clamp.inputs[0])
    clamp.inputs[1].default_value = 0.0
    powr.operation = "POWER"
    L(clamp.outputs[0], powr.inputs[0])
    powr.inputs[1].default_value = 6.0
    glow.data_type, glow.blend_type = "RGBA", "ADD"
    L(powr.outputs[0], glow.inputs["Factor"])
    L(ramp.outputs["Color"], glow.inputs[6])
    glow.inputs[7].default_value = srgb("#ff9a52")
    anti, aclamp, apow, belt = N("ShaderNodeVectorMath"), N("ShaderNodeMath"), N("ShaderNodeMath"), N("ShaderNodeMix")
    anti.operation = "DOT_PRODUCT"
    L(coord.outputs["Generated"], anti.inputs[0])
    anti.inputs[1].default_value = Vector((-SUN_DIR.x, -SUN_DIR.y, 0.35)).normalized()
    aclamp.operation, aclamp.use_clamp = "MAXIMUM", True
    L(anti.outputs["Value"], aclamp.inputs[0])
    aclamp.inputs[1].default_value = 0.0
    apow.operation = "POWER"
    L(aclamp.outputs[0], apow.inputs[0])
    apow.inputs[1].default_value = 3.0
    belt.data_type, belt.blend_type = "RGBA", "ADD"
    L(apow.outputs[0], belt.inputs["Factor"])
    L(glow.outputs[2], belt.inputs[6])
    belt.inputs[7].default_value = srgb("#9c7c8a")
    L(belt.outputs[2], bg.inputs["Color"])
    bg.inputs["Strength"].default_value = 1.2
    L(bg.outputs[0], out.inputs[0])

    rig = bpy.data.collections.new("RENDER_RIG")
    scene.collection.children.link(rig)
    sun = bpy.data.objects.new("Sun", bpy.data.lights.new("Sun", "SUN"))
    sun.data.energy = 2.0
    sun.data.color = srgb("#ffc590")[:3]
    sun.data.angle = math.radians(1.5)
    sun.rotation_euler = (-SUN_DIR).to_track_quat("-Z", "Y").to_euler()
    rig.objects.link(sun)
    # A light in each occupied loggia so the warm interior spills onto the stone (render only).
    for i, home in enumerate(loggia_home):
        if not home:
            continue
        z1 = PODIUM_H + (i + 1) * FLOOR_H
        ld = bpy.data.lights.new(f"LoggiaLight_{i:02d}", "AREA")
        ld.shape, ld.size, ld.size_y = "RECTANGLE", 5.0, 1.2
        ld.energy, ld.color = 140, srgb("#ffc58a")[:3]
        lo = bpy.data.objects.new(ld.name, ld)
        lo.location = (LOGGIA_PIVOT[0], LOGGIA_BACK - 1.2, z1 - 0.05)
        rig.objects.link(lo)
    return rig


def render_still(rig, name, loc, target, lens, res, hide=()):
    scene = bpy.context.scene
    cam = bpy.data.objects.new(f"CAM_{name}", bpy.data.cameras.new(f"CAM_{name}"))
    cam.data.lens = lens
    cam.data.clip_end = 3000
    rig.objects.link(cam)
    cam.location = loc
    cam.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
    scene.camera = cam
    scene.render.resolution_x, scene.render.resolution_y = res
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    hidden = [bpy.data.objects[n] for n in hide]
    for o in hidden:
        o.hide_render = True
    os.makedirs(RENDER_DIR, exist_ok=True)
    scene.render.filepath = os.path.join(RENDER_DIR, f"{name}.png")
    bpy.ops.render.render(write_still=True)
    for o in hidden:
        o.hide_render = False
    print("RENDERED", scene.render.filepath)


# ---------------------------------------------------------------- main
def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for block in (bpy.data.meshes, bpy.data.materials, bpy.data.images, bpy.data.lights,
                  bpy.data.cameras, bpy.data.worlds):
        for item in list(block):
            block.remove(item)


def main():
    clear_scene()
    bpy.context.preferences.filepaths.save_version = 0   # no .blend1 backups in the repo
    bpy.context.scene.unit_settings.system = "METRIC"
    mats = build_materials()
    tower, loggia_home = build_tower(mats)
    city, n_blocks = build_city(mats)
    export_glb(tower, TOWER_GLB)
    export_glb(city, CITY_GLB)
    os.makedirs(SITE_MODELS, exist_ok=True)
    for path in (TOWER_GLB, CITY_GLB):
        shutil.copyfile(path, os.path.join(SITE_MODELS, os.path.basename(path)))
    print(f"EXPORTED {TOWER_GLB} ({os.path.getsize(TOWER_GLB) / 1e6:.2f} MB)")
    print(f"EXPORTED {CITY_GLB} ({os.path.getsize(CITY_GLB) / 1e6:.2f} MB, {n_blocks} lots)")
    rig = setup_render_world(loggia_home)
    bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH, compress=True)
    if DO_RENDER:
        render_still(rig, "tower_34", (125, -175, 22), (3, 0, 47), 55, (1600, 2000))
        render_still(rig, "seam_closeup", (40, -62, 46), (9, -10, 58), 50, (1600, 2000))
        render_still(rig, "loggia_closeup", (16.5, -24, 56.5), (10.3, -8, 54.2), 32, (1600, 1000))
        # Hero chapter positions: ch1 from mid-height ~250 m out, ch2 a close 3/4 on the seam.
        render_still(rig, "ch1_skyline", (40, -245, 45), (0, 0, 46), 45, (1600, 1000))
        render_still(rig, "ch2_seam", (60, -55, 52), (10, -10, 52), 35, (1600, 1000))
        # Construction look: top three storeys without glass, crown not yet built.
        render_still(rig, "construction", (70, -120, 80), (0, 0, 80), 50, (1600, 1000),
                     hide=("Glass_21", "Glass_22", "Glass_23", "Crown", "Seam_Crown"))
        bpy.ops.wm.save_as_mainfile(filepath=BLEND_PATH, compress=True)


if __name__ == "__main__":
    main()
