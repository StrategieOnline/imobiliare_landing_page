"""ORIZONT hero motion guides (SPEC section 8): one scene, one continuous camera.

    /Applications/Blender.app/Contents/MacOS/Blender -b -P blender/build_guides.py
    ... -- --shots S1,S2        render only these shots (plus their 12-frame overlaps)
    ... -- --stills             only each shot's first/last frame (fast check)

Builds the round-2 tower (via build_tower.py) with keyframed floor-by-floor
stacking, the city context with a lake, a rooftop terrace for S1 and a loggia +
living-room blockout behind Loggia_14 for S4-S6. Renders EEVEE frames and encodes
blender/guides/S1.mp4 ... S6.mp4 (1280x720, 24 fps, H.264), S#_first/last.png and
guides.json. These are motion/geometry guides for the Higgsfield edit: they are
never published on the site.

World axes are Blender's (Z up, metres). The tower stands at the origin, its front
(with the travertine band and the loggias) facing -Y, i.e. south.
"""

import json
import math
import os
import shutil
import subprocess
import sys
import tempfile

import bpy
import bmesh
from mathutils import Matrix, Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_tower as bt  # noqa: E402  (the tower, materials and render world)

ARGS = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
STILLS_ONLY = "--stills" in ARGS
EXTRA = next(([int(x) for x in a.split(",")] for i, a in enumerate(ARGS) if i and ARGS[i - 1] == "--frames"), [])
ONLY = next((a.split(",") for i, a in enumerate(ARGS) if i and ARGS[i - 1] == "--shots"), None)

GUIDE_DIR = os.path.join(bt.ROOT, "blender", "guides")
VERSION = "v2"
ALT_S2 = "--alt-s2" in ARGS        # contingency S2: faster stack, base higher in frame
FRAME_DIR = os.path.join(tempfile.gettempdir(), "orizont_guide_frames_v2" + ("_s2alt" if ALT_S2 else ""))
FPS, RES = 24, (1280, 720)
OVERLAP = 12
LENS = 28.0                      # one lens throughout: no zooms, nothing optically odd

SHOTS = [  # name, seconds, note
    ("S1", 5, "RISE: eye height (1.7 m) on a 24 m rooftop terrace 340 m west of the plot; rises over the "
              "travertine parapet between the olive planters and tilts down to the empty plot."),
    ("S2", 7, "STACK: drone push toward the plot on a gentle arc while the tower stacks floor by floor "
              "(podium, 24 storeys growing up from the one below, glass trailing ~3 storeys, crown last). "
              "The travertine band faces the camera at ~50 deg (3/4, east face visible)."),
    ("S3", 7, "ORBIT: ~60 deg clockwise round the finished tower, closing from 185 m to 87 m and rising "
              "to loggia height (58.5 m), lake behind; ends 20 deg off the loggia axis, framed on the band."),
    ("S4", 5, "APPROACH: straight dolly toward Loggia_14 (storey 15) until the loggia fills the frame, "
              "finishing on its axis 4.4 m out."),
    ("S5", 5, "THRESHOLD: through the open centre of the sliding glass into the living room."),
    ("S6", 5, "DRIFT: slow lateral drift left across the living room (shelf wall, sofa, window right)."),
]
FRAMES = {}
_f = 1
for _name, _sec, _ in SHOTS:
    FRAMES[_name] = (_f, _f + _sec * FPS - 1)
    _f += _sec * FPS
LAST_FRAME = _f - 1

# ---------------------------------------------------------------- world layout
ROOF_THETA, ROOF_R, ROOF_Z = math.radians(-178), 340.0, 24.0
ROOF_C = Vector((math.cos(ROOF_THETA) * ROOF_R, math.sin(ROOF_THETA) * ROOF_R, 0))
ROOF_YAW = math.atan2(-ROOF_C.y, -ROOF_C.x)        # local +X of the terrace faces the tower
ROOF_HX, ROOF_HY = 15.0, 12.0
# The tower is turned about its axis so its travertine band faces the S1/S2 camera at 3/4.
TOWER_YAW = math.radians(224.5)
TOWER_ROT = Matrix.Rotation(TOWER_YAW, 3, "Z")
LOGGIA_HEADING = math.radians(-20)                 # S3 ends 20 deg off the loggia axis
LAKE_C, LAKE_R, LAKE_ROT = Vector((242.0, -355.0)), (300.0, 120.0), math.radians(34.3)
LOGGIA_FLOOR = 14
Z0 = bt.PODIUM_H + LOGGIA_FLOOR * bt.FLOOR_H       # storey base 56.4
ZF = Z0 + bt.BAND_H                                # loggia / living-room floor 56.95
Z1 = Z0 + bt.FLOOR_H                               # 60.0
EYE = ZF + 1.6
ROOM = dict(x0=4.6, x1=bt.HX - 0.02, y0=bt.LOGGIA_BACK, y1=1.5, ceil=Z1 - 0.15)
DOOR_X = bt.LOGGIA_PIVOT[0]                        # centre of the sliding-door opening


# Height yardsticks: 1970s Bucharest apartment slabs, 10 storeys x 2.8 m = 28 m, 12 m deep.
# (centre x, centre y, length, depth, long axis along y?)  World coordinates.
SLABS = [(-111.0, 30.0, 60.0, 12.0, True),      # front-left of the site from the S1/S2 camera
         (149.5, -70.0, 66.0, 12.0, True),      # behind-right
         (145.0, 122.0, 54.0, 12.0, False)]     # behind-left, turned
SLAB_STOREYS, SLAB_STOREY_H = 10, 2.8


def near_slab(c, margin):
    for sx, sy, ln, dp, along_y in SLABS:
        hx, hy = (dp / 2, ln / 2) if along_y else (ln / 2, dp / 2)
        if abs(c.x - sx) < hx + margin and abs(c.y - sy) < hy + margin:
            return True
    return False


def T(v):
    """Tower-local point -> world (the tower is yawed by TOWER_YAW about the origin)."""
    return TOWER_ROT @ Vector(v)


def in_lake(c, margin=0.0):
    d = c - LAKE_C.to_2d()
    cs, sn = math.cos(-LAKE_ROT), math.sin(-LAKE_ROT)
    x, y = cs * d.x - sn * d.y, sn * d.x + cs * d.y
    return (x / (LAKE_R[0] + margin)) ** 2 + (y / (LAKE_R[1] + margin)) ** 2 < 1


def roof_local(x, y, z):
    c, s = math.cos(ROOF_YAW), math.sin(ROOF_YAW)
    return Vector((ROOF_C.x + c * x - s * y, ROOF_C.y + s * x + c * y, z))


def polar(theta_deg, r, z):
    t = math.radians(theta_deg)
    return Vector((math.cos(t) * r, math.sin(t) * r, z))


def lot_filter(c, d, h):
    """Clear the sightlines: no blocks on the lake or the rooftop's own lot, low-rise
    round the lake and along the rooftop-to-plot line, low near the orbit path."""
    if in_lake(c, 25) or near_slab(c, 22):
        return None
    if (c - ROOF_C.to_2d()).length < 42:
        return None
    seg = -ROOF_C.to_2d()
    t = max(0.0, min(1.0, (c - ROOF_C.to_2d()).dot(seg) / seg.length_squared))
    if (c - (ROOF_C.to_2d() + seg * t)).length < 70:
        h = min(h, 10.0)                       # keep the tower's base in view from the rooftop
    ang = math.degrees(math.atan2(c.y, c.x))
    if -115 < ang < 5:
        h = min(h, 22.0)                       # the park and lake side, behind the tower in S3
    if (ang > 115 or ang < -170) and d < 300:
        h = min(h, 14.0)                       # under the orbit
    if -25 < ang < 40 and d < 520:
        h = min(h, 24.0)                       # behind the plot as seen from the rooftop: the tower stands alone
    return h


# ---------------------------------------------------------------- guide materials
def guide_materials():
    def mat(name, hexc, rough=0.6, metal=0.0, emit=None, strength=0.0, alpha=1.0):
        m, b = bt.principled(name, hexc, metallic=metal, roughness=rough)
        if emit:
            b.inputs["Emission Color"].default_value = bt.srgb(emit)
            b.inputs["Emission Strength"].default_value = strength
        if alpha < 1.0:
            b.inputs["Alpha"].default_value = alpha
            m.surface_render_method = "BLENDED"
        return m
    return {
        "oak": mat("G_SmokedOak", "#3a281c", 0.45),
        "fabric": mat("G_Boucle", "#d8cdb9", 0.95),
        "leather": mat("G_Leather", "#5b3a24", 0.5),
        "plaster": mat("G_Plaster", "#d8cfc3", 0.9),
        "clear": mat("G_ClearGlass", "#30261c", 0.03, alpha=0.18),
        "glow": mat("G_Practical", "#ffd7a8", 0.6, emit="#ffbf80", strength=6.0),
        "curtain": mat("G_Sheer", "#e8dfcf", 0.9, alpha=0.75),
        "water": mat("G_Water", "#1a2630", 0.14),
        "olive": mat("G_Olive", "#56633f", 0.85),
        "bark": mat("G_Bark", "#4a3d31", 0.9),
        "render": mat("G_Render", "#b9b0a3", 0.9),
        "site": mat("G_SitePad", "#a29a8e", 0.95),
        "panel": mat("G_PrefabPanel", "#bdb2a1", 0.9),
        "window": mat("G_SlabWindow", "#2b2e31", 0.25),
        "winlit": mat("G_SlabWindowLit", "#3a2a1c", 0.6, emit="#ffbf80", strength=2.5),
        "hoarding": mat("G_Hoarding", "#3e423a", 0.8),
    }


class Builder(bt.MeshBuilder):
    """bt.MeshBuilder with guide materials (any bpy material, keyed by name)."""

    def to_obj(self, name, pivot, mats, col, parent=None):
        pivot = Vector(pivot)
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata([v - pivot for v in self.verts], [], self.faces)
        used = sorted(set(self.mats))
        for m in used:
            mesh.materials.append(mats[m])
        uv = mesh.uv_layers.new(name="UVMap")
        for poly, m, fuv in zip(mesh.polygons, self.mats, self.uvs):
            poly.material_index = used.index(m)
            n = poly.normal
            for li in poly.loop_indices:
                p = self.verts[mesh.loops[li].vertex_index]
                u, v = (p.x, p.y) if abs(n.z) > 0.7 else ((p.y, p.z) if abs(n.x) > abs(n.y) else (p.x, p.z))
                off = fuv if isinstance(fuv, tuple) else (0, 0)
                uv.data[li].uv = (u / bt.STONE_TILE + off[0], v / bt.STONE_TILE + off[1])
        mesh.update()
        obj = bpy.data.objects.new(name, mesh)
        col.objects.link(obj)
        obj.location = pivot
        if parent is not None:
            obj.parent = parent
            obj.matrix_parent_inverse = parent.matrix_world.inverted()
        return obj


def cylinder(b, cx, cy, z0, z1, r, mat, n=16):
    for k in range(n):
        a0, a1 = 2 * math.pi * k / n, 2 * math.pi * (k + 1) / n
        p0 = (cx + r * math.cos(a0), cy + r * math.sin(a0))
        p1 = (cx + r * math.cos(a1), cy + r * math.sin(a1))
        b.face([(*p0, z0), (*p1, z0), (*p1, z1), (*p0, z1)], mat)
        b.face([(cx, cy, z1), (*p0, z1), (*p1, z1)], mat, want=(0, 0, 1))


def blob(b, cx, cy, cz, rx, ry, rz, mat, rings=5, seg=10):
    """Low-poly ellipsoid (olive canopies, a vase)."""
    def pt(i, j):
        th, ph = math.pi * i / rings, 2 * math.pi * j / seg
        return (cx + rx * math.sin(th) * math.cos(ph), cy + ry * math.sin(th) * math.sin(ph),
                cz + rz * math.cos(th))
    for i in range(rings):
        for j in range(seg):
            q = [pt(i, j), pt(i + 1, j), pt(i + 1, j + 1), pt(i, j + 1)]
            c = Vector((cx, cy, cz))
            n = sum((Vector(p) for p in q), Vector()) / 4 - c
            b.face(q, mat, want=n)


# ---------------------------------------------------------------- set pieces
def build_rooftop(m, col):
    """A 7-storey neighbour with a terrace: travertine parapet, olive planters, a bench."""
    b = Builder()
    hx, hy, z = ROOF_HX, ROOF_HY, ROOF_Z
    b.box(-hx, hx, -hy, hy, -0.05, z, "render")
    b.box(-hx + 0.3, hx - 0.3, -hy + 0.3, hy - 0.3, z, z + 0.05, "M_Stone")       # pavers
    t, ph = 0.32, 1.1
    for x0, x1, y0, y1 in ((hx - t, hx, -hy, hy), (-hx, -hx + t, -hy, hy),
                           (-hx, hx, hy - t, hy), (-hx, hx, -hy, -hy + t)):
        b.box(x0, x1, y0, y1, z, z + ph, "M_Stone")                               # parapet
        b.box(x0 - 0.04, x1 + 0.04, y0 - 0.04, y1 + 0.04, z + ph, z + ph + 0.06, "M_Stone")
    for y in (-8.5, -3.2, 4.2, 9.0):                                              # planters + olives
        b.box(12.9, 14.1, y - 0.6, y + 0.6, z, z + 0.8, "M_Stone")
        b.box(13.44, 13.56, y - 0.06, y + 0.06, z + 0.8, z + 2.2, "bark")
        blob(b, 13.5, y, z + 2.9, 1.0, 0.9, 0.85, "olive")
    b.box(6.0, 10.0, -6.5, -5.8, z, z + 0.45, "oak")                              # bench
    obj = b.to_obj("Guide_Rooftop", (0, 0, 0), m, col)
    obj.location = (ROOF_C.x, ROOF_C.y, 0)
    obj.rotation_euler = (0, 0, ROOF_YAW)
    return obj


def build_lake(m, col):
    b = Builder()
    n = 48
    cs, sn = math.cos(LAKE_ROT), math.sin(LAKE_ROT)
    ring = []
    for k in range(n):
        x = LAKE_R[0] * math.cos(2 * math.pi * k / n) * (1 + 0.08 * math.sin(3 * k))
        y = LAKE_R[1] * math.sin(2 * math.pi * k / n)
        ring.append((LAKE_C.x + cs * x - sn * y, LAKE_C.y + sn * x + cs * y, 0.03))
    for k in range(n):
        b.face([(LAKE_C.x, LAKE_C.y, 0.03), ring[k], ring[(k + 1) % n]], "water", want=(0, 0, 1))
    return b.to_obj("Guide_Lake", (0, 0, 0), m, col)


def build_slabs(m, col):
    """Prefab-panel slabs with banded windows (a few lit): the scale reference that
    stops a video model from stretching the 24-storey tower."""
    import random as _r
    rng = _r.Random(1974)
    b = Builder()
    for sx, sy, ln, dp, along_y in SLABS:
        hx, hy = (dp / 2, ln / 2) if along_y else (ln / 2, dp / 2)
        top = SLAB_STOREYS * SLAB_STOREY_H
        b.box(sx - hx, sx + hx, sy - hy, sy + hy, -0.05, top, "panel")
        b.box(sx - hx - 0.1, sx + hx + 0.1, sy - hy - 0.1, sy + hy + 0.1, top, top + 0.9, "panel")
        b.box(sx - 3, sx + 3, sy - 4, sy + 4, top, top + 3.2, "panel")           # lift / stair housing
        n_win = int(ln / 3.0)
        for side in (-1, 1):                                                       # the two long faces
            for st in range(1, SLAB_STOREYS):
                z0, z1 = st * SLAB_STOREY_H + 0.9, st * SLAB_STOREY_H + 2.3
                for k in range(n_win):
                    u0 = -ln / 2 + (k + 0.2) * ln / n_win
                    u1 = -ln / 2 + (k + 0.8) * ln / n_win
                    mat = "winlit" if rng.random() < 0.12 else "window"
                    if along_y:
                        x = sx + side * (hx + 0.02)
                        b.face([(x, sy + u0, z0), (x, sy + u1, z0), (x, sy + u1, z1), (x, sy + u0, z1)],
                               mat, want=(side, 0, 0))
                    else:
                        y = sy + side * (hy + 0.02)
                        b.face([(sx + u0, y, z0), (sx + u1, y, z0), (sx + u1, y, z1), (sx + u0, y, z1)],
                               mat, want=(0, side, 0))
    return b.to_obj("Guide_Slabs", (0, 0, 0), m, col)


def build_site(m, col, root):
    """The plot at grade: a concrete site pad and a 2.4 m hoarding with a gate on the
    front, so the tower is grounded from the first frame of the stack."""
    b = Builder()
    hx, hy, t, h = 38.0, 32.0, 0.12, 2.4
    b.box(-hx, hx, -hy, hy, -0.05, 0.06, "site")
    for x0, x1, y0, y1 in ((-hx, hx, hy - t, hy), (-hx, -hx + t, -hy, hy), (hx - t, hx, -hy, hy),
                           (-hx, -6.0, -hy, -hy + t), (6.0, hx, -hy, -hy + t)):
        b.box(x0, x1, y0, y1, 0.06, h, "hoarding")
    obj = b.to_obj("Guide_Site", (0, 0, 0), m, col, parent=root)
    return obj


def open_loggia_and_room(m, col):
    """Replace Loggia_14's back wall with sliding glass open at the centre, and put a
    living room (matching interior-living.webp) behind it, inside Floor_14."""
    floor = bpy.data.objects[f"Floor_{LOGGIA_FLOOR:02d}"]
    bpy.data.objects[f"Loggia_{LOGGIA_FLOOR:02d}"].hide_render = True
    # The room's window is the tower's own east facade: drop those dark panels.
    glass = bpy.data.objects[f"Glass_{LOGGIA_FLOOR:02d}"]
    bm = bmesh.new()
    bm.from_mesh(glass.data)
    kill = [f for f in bm.faces if f.normal.x > 0.9 and ROOM["y0"] - 0.6 < f.calc_center_median().y < ROOM["y1"] + 0.2]
    bmesh.ops.delete(bm, geom=kill, context="FACES")
    bm.to_mesh(glass.data)
    bm.free()

    b = Builder()
    x0, x1, yb = bt.OPEN_X0, bt.OPEN_X1, bt.LOGGIA_BACK
    # Loggia: stone returns, cove, balustrade glass with bronze cap, furniture.
    b.box(x0 - 0.5, x0, bt.PIER_BACK, yb, ZF, Z1, "M_Stone")
    b.box(x1, x1 + 0.5, bt.CORNER_BACK, yb, ZF, Z1, "M_Stone")
    b.face([(x0, yb - 0.45, Z1 - 0.01), (x1, yb - 0.45, Z1 - 0.01), (x1, yb - 0.25, Z1 - 0.01),
            (x0, yb - 0.25, Z1 - 0.01)], "glow", want=(0, 0, -1))
    ybal = bt.SEAM_FRONT + 0.25
    b.face([(x0, ybal, ZF), (x1, ybal, ZF), (x1, ybal, ZF + 1.05), (x0, ybal, ZF + 1.05)], "clear")
    b.box(x0, x1, ybal - 0.03, ybal + 0.03, ZF + 1.05, ZF + 1.1, "M_Frame")
    for x in (8.3, 12.3):                                       # lounge chairs
        b.box(x - 0.4, x + 0.4, -9.6, -8.8, ZF, ZF + 0.42, "fabric")
        b.box(x - 0.4, x + 0.4, -8.95, -8.75, ZF + 0.42, ZF + 0.85, "fabric")
    cylinder(b, DOOR_X, -9.2, ZF, ZF + 0.4, 0.55, "oak")        # round table
    for x in (7.95, 12.65):                                     # planters
        cylinder(b, x, -7.55, ZF, ZF + 0.7, 0.32, "M_Frame")
        blob(b, x, -7.55, ZF + 1.35, 0.55, 0.55, 0.7, "olive")
    # Sliding doors: four 1.35 m leaves; the two centre ones are slid behind the outer ones.
    leaf = (x1 - x0) / 4                                        # opening = 9.0 .. 11.6 m
    for xa, y in ((x0, yb - 0.06), (x0 + 0.05, yb), (x1 - leaf - 0.05, yb), (x1 - leaf, yb - 0.06)):
        b.face([(xa, y, ZF), (xa + leaf, y, ZF), (xa + leaf, y, Z1 - 0.3), (xa, y, Z1 - 0.3)], "clear")
        for xe in (xa, xa + leaf):
            b.box(xe - 0.025, xe + 0.025, y - 0.04, y + 0.04, ZF, Z1 - 0.3, "M_Frame", caps=False)
    b.box(x0, x1, yb - 0.12, yb, Z1 - 0.3, Z1 - 0.22, "M_Frame")
    b.box(x0, x1, yb - 0.12, yb, ZF, ZF + 0.03, "M_Frame")

    # Living room shell: travertine floor, plaster ceiling with a cove, smoked-oak walls.
    r = ROOM
    b.face([(r["x0"], r["y0"], ZF), (r["x1"], r["y0"], ZF), (r["x1"], r["y1"], ZF), (r["x0"], r["y1"], ZF)],
           "M_Stone", want=(0, 0, 1))
    b.face([(r["x0"], r["y0"], r["ceil"]), (r["x1"], r["y0"], r["ceil"]), (r["x1"], r["y1"], r["ceil"]),
            (r["x0"], r["y1"], r["ceil"])], "plaster", want=(0, 0, -1))
    b.box(r["x0"] - 0.1, r["x0"], r["y0"], r["y1"], ZF, r["ceil"], "oak")                  # left wall
    b.box(r["x0"], r["x1"], r["y1"], r["y1"] + 0.1, ZF, r["ceil"], "oak")                  # shelf wall
    b.box(r["x0"], x0, r["y0"] - 0.1, r["y0"], ZF, r["ceil"], "plaster")                   # front wall
    b.box(x1, r["x1"], r["y0"] - 0.1, r["y0"], ZF, r["ceil"], "plaster")
    for y0, y1 in ((r["y0"], r["y1"]),):                                                   # cove strips
        b.face([(r["x0"] + 0.05, y0, r["ceil"] - 0.02), (r["x0"] + 0.25, y0, r["ceil"] - 0.02),
                (r["x0"] + 0.25, y1, r["ceil"] - 0.02), (r["x0"] + 0.05, y1, r["ceil"] - 0.02)],
               "glow", want=(0, 0, -1))
    b.face([(r["x0"], r["y1"] - 0.25, r["ceil"] - 0.02), (r["x1"], r["y1"] - 0.25, r["ceil"] - 0.02),
            (r["x1"], r["y1"] - 0.05, r["ceil"] - 0.02), (r["x0"], r["y1"] - 0.05, r["ceil"] - 0.02)],
           "glow", want=(0, 0, -1))
    # Built-in shelves with warm strips under each board, a few stone objects.
    for hgt in (0.95, 1.55, 2.15):
        b.box(5.8, 10.6, r["y1"] - 0.38, r["y1"], ZF + hgt, ZF + hgt + 0.05, "oak")
        b.face([(5.8, r["y1"] - 0.36, ZF + hgt - 0.005), (10.6, r["y1"] - 0.36, ZF + hgt - 0.005),
                (10.6, r["y1"] - 0.02, ZF + hgt - 0.005), (5.8, r["y1"] - 0.02, ZF + hgt - 0.005)],
               "glow", want=(0, 0, -1))
    blob(b, 6.6, r["y1"] - 0.2, ZF + 1.75, 0.16, 0.16, 0.2, "M_Stone")
    blob(b, 8.4, r["y1"] - 0.2, ZF + 2.27, 0.25, 0.25, 0.07, "M_Stone")
    b.box(9.2, 9.7, r["y1"] - 0.3, r["y1"] - 0.1, ZF + 1.0, ZF + 1.12, "plaster")
    # Low boucle sofa in front of the shelves, facing the loggia.
    b.box(5.9, 11.0, -0.75, 0.25, ZF, ZF + 0.42, "fabric")
    b.box(5.9, 11.0, 0.0, 0.3, ZF + 0.42, ZF + 0.8, "fabric")
    for xa in (5.9, 10.7):
        b.box(xa, xa + 0.3, -0.75, 0.3, ZF + 0.42, ZF + 0.62, "fabric")
    b.box(7.4, 9.9, -2.55, -1.35, ZF, ZF + 0.36, "oak")                                   # coffee table
    blob(b, 8.3, -1.95, ZF + 0.42, 0.3, 0.3, 0.07, "M_Stone")
    cylinder(b, 12.0, 0.2, ZF, ZF + 0.03, 0.2, "M_Frame")                                  # floor lamp
    cylinder(b, 12.0, 0.2, ZF, ZF + 1.55, 0.015, "M_Frame", n=8)
    cylinder(b, 12.0, 0.2, ZF + 1.45, ZF + 1.8, 0.24, "glow")
    b.box(12.5, 13.4, -2.0, -1.0, ZF, ZF + 0.42, "leather")                                # armchair
    b.box(13.2, 13.4, -2.0, -1.0, ZF + 0.42, ZF + 0.9, "leather")
    b.face([(13.65, -0.6, ZF + 0.02), (13.65, 1.45, ZF + 0.02), (13.65, 1.45, r["ceil"] - 0.05),
            (13.65, -0.6, r["ceil"] - 0.05)], "curtain")                                    # sheer
    # The window: clear glass on the facade line with bronze mullions.
    b.face([(13.97, r["y0"], ZF), (13.97, r["y1"], ZF), (13.97, r["y1"], r["ceil"]),
            (13.97, r["y0"], r["ceil"])], "clear")
    for y in (-5.5, -4.0, -2.5, -1.0, 0.5):
        b.box(13.94, 14.0, y - 0.03, y + 0.03, ZF, r["ceil"], "M_Frame", caps=False)
    room = b.to_obj("Guide_LoggiaRoom", (0, 0, Z0), m, col, parent=floor)

    lights = []
    for name, kind, loc, energy, size in (("RoomCeiling", "AREA", (9.3, -2.8, r["ceil"] - 0.05), 320, (6.0, 5.0)),
                                          ("RoomLamp", "POINT", (12.0, 0.2, ZF + 1.6), 60, None),
                                          ("RoomShelves", "AREA", (8.2, r["y1"] - 0.6, ZF + 2.4), 90, (4.5, 0.6)),
                                          ("LoggiaSoffit", "AREA", (DOOR_X, -8.6, Z1 - 0.05), 160, (5.0, 1.4))):
        ld = bpy.data.lights.new(name, kind)
        ld.energy, ld.color = energy, bt.srgb("#ffc690")[:3]
        if size:
            ld.shape, ld.size, ld.size_y = "RECTANGLE", *size
        lo = bpy.data.objects.new(name, ld)
        lo.location = loc
        col.objects.link(lo)
        lights.append(lo)
    return room, lights


# ---------------------------------------------------------------- stacking animation
def stacking_schedule():
    """Frames at which each piece starts growing; growth = local Z scale 0 -> 1 from the
    piece's base pivot, so a storey always rises out of the one below it."""
    a, _ = FRAMES["S2"]
    sched = {"Podium": (a + 3, 14)}
    if ALT_S2:
        # Compressed: storeys every 3.5 frames from frame 133 (after the S1 overlap), glass
        # 9 frames behind, crown done by frame 239 = local frame 119 of 180.
        for i in range(bt.N_FLOORS):
            start = 133 + round(i * 3.5)
            sched[f"Floor_{i:02d}"] = (start, 7)
            sched[f"Glass_{i:02d}"] = (start + 9, 6)
        sched["Crown"] = (226, 13)
        return sched
    for i in range(bt.N_FLOORS):
        start = a + 15 + i * 5
        sched[f"Floor_{i:02d}"] = (start, 9)
        sched[f"Glass_{i:02d}"] = (start + 14, 8)      # glass trails the frame by ~3 storeys
    sched["Crown"] = (a + 15 + bt.N_FLOORS * 5 + 14, 14)
    return sched


def key_growth(obj, start, length):
    obj.scale = (1, 1, 1e-3)
    obj.keyframe_insert("scale", frame=start)
    obj.scale = (1, 1, 1)
    obj.keyframe_insert("scale", frame=start + length)


def key_visible_from(obj, frame):
    """Hidden (not merely collapsed) until it starts to grow, children included."""
    for o in [obj] + list(obj.children_recursive):
        if o.name.startswith("Glass_") and o is not obj:
            continue
        o.hide_render = True
        o.keyframe_insert("hide_render", frame=1)
        o.hide_render = False if not o.name.startswith("Loggia_14") else True
        o.keyframe_insert("hide_render", frame=frame)


def animate_stack(extra_lights):
    sched = stacking_schedule()
    for name, (start, length) in sched.items():
        obj = bpy.data.objects[name]
        key_growth(obj, start, length)
        key_visible_from(obj, start)
    # Loggia lights come on once their storey is complete.
    for i in range(bt.N_FLOORS):
        lo = bpy.data.objects.get(f"LoggiaLight_{i:02d}")
        if lo is None:
            continue
        if i == LOGGIA_FLOOR:
            bpy.data.objects.remove(lo)
            continue
        done = sum(sched[f"Floor_{i:02d}"])
        e = lo.data.energy
        lo.data.energy = 0
        lo.data.keyframe_insert("energy", frame=done)
        lo.data.energy = e
        lo.data.keyframe_insert("energy", frame=done + 4)
    done = sum(sched[f"Floor_{LOGGIA_FLOOR:02d}"])
    for lo in extra_lights:
        e = lo.data.energy
        lo.data.energy = 0
        lo.data.keyframe_insert("energy", frame=done)
        lo.data.energy = e
        lo.data.keyframe_insert("energy", frame=done + 4)
    return sched


# ---------------------------------------------------------------- the camera
def camera_keys():
    """(frame, position, look-at target) keys. Positions are interpolated with a
    time-based cubic Hermite spline (C1: no velocity jumps anywhere, including the
    cuts); the first and last keys start and end at rest."""
    s1a, s1b = FRAMES["S1"]
    s2a, s2b = FRAMES["S2"]
    s3a, s3b = FRAMES["S3"]
    s4a, s4b = FRAMES["S4"]
    s5a, s5b = FRAMES["S5"]
    s6a, s6b = FRAMES["S6"]
    eye = ROOF_Z + 1.7
    keys = [
        (s1a, roof_local(8.5, 0.8, eye), Vector((0, 0, eye + 1.0))),
        (s1a + 50, roof_local(10.6, 0.7, eye + 0.6), Vector((0, 0, eye))),
        (s1b, roof_local(16.8, 0.3, ROOF_Z + 5.0), Vector((0, 0, 12.0))),
        (s2a + 84, polar(-177.0, 260, 33.0), Vector((0, 0, 30.0))),
        (s2b, polar(-175.5, 185, 38.0), Vector((0, 0, 46.0))),
    ]
    # From here on, points are tower-local and turned into world space with T().
    p4_local = Vector((DOOR_X, bt.SEAM_FRONT - 4.4, EYE))
    p3_local = p4_local + 75.0 * Vector((math.sin(LOGGIA_HEADING), -math.cos(LOGGIA_HEADING), 0))
    p3_local.z = EYE - 0.1
    # Orbit: clockwise from the S2 end (184.5 deg) to the loggia approach line, closing in and rising.
    n = 7
    th0 = 184.5
    th1 = math.degrees(math.atan2(p3_local.y, p3_local.x) + TOWER_YAW)
    r0, r1, z0, z1 = 185.0, p3_local.to_2d().length, 38.0, p3_local.z
    for k in range(1, n + 1):
        u = k / n
        e = u * u * (3 - 2 * u)
        f = s2b + round((s3b - s2b) * u)
        tgt = Vector((0, 0, 46.0)).lerp(T((DOOR_X, -10.4, EYE - 0.4)), e)
        keys.append((f, polar(th0 + (th1 - th0) * u, r0 + (r1 - r0) * e, z0 + (z1 - z0) * e), tgt))
    p3, p4 = keys[-1][1], T(p4_local)
    # Approach: straight line onto the loggia axis, 4.4 m outside the stone face.
    keys.append((s4a + 60, p3.lerp(p4, 0.62), T((DOOR_X, -6.0, EYE - 0.3))))
    keys.append((s4b, p4, T((DOOR_X, -2.0, EYE - 0.25))))
    # Threshold: through the open centre leaves, into the room.
    keys.append((s5a + 60, T((DOOR_X, -8.2, EYE - 0.03)), T((DOOR_X + 0.2, 1.5, EYE - 0.4))))
    keys.append((s5b, T((DOOR_X, -3.7, EYE - 0.08)), T((DOOR_X + 0.4, 1.5, EYE - 0.55))))
    # Drift: slow lateral move left, keeping the shelf wall in view.
    keys.append((s6b, T((DOOR_X - 2.3, -4.0, EYE - 0.1)), T((DOOR_X - 1.4, 1.5, EYE - 0.6))))
    return keys


def hermite(keys, idx):
    """Evaluate the C1 cubic Hermite through keys[i][idx] at every integer frame."""
    ts = [k[0] for k in keys]
    ps = [k[idx] for k in keys]
    tangents = []
    for i in range(len(keys)):
        if i == 0 or i == len(keys) - 1:
            tangents.append(Vector((0, 0, 0)))          # ease in from rest, ease out to rest
        else:
            tangents.append((ps[i + 1] - ps[i - 1]) / (ts[i + 1] - ts[i - 1]))
    out = {}
    for i in range(len(keys) - 1):
        t0, t1 = ts[i], ts[i + 1]
        for f in range(t0, t1 + 1):
            h = t1 - t0
            s = (f - t0) / h
            h00, h10 = 2 * s ** 3 - 3 * s ** 2 + 1, s ** 3 - 2 * s ** 2 + s
            h01, h11 = -2 * s ** 3 + 3 * s ** 2, s ** 3 - s ** 2
            out[f] = ps[i] * h00 + tangents[i] * h * h10 + ps[i + 1] * h01 + tangents[i + 1] * h * h11
    return out


def build_camera(col):
    cam = bpy.data.objects.new("GuideCam", bpy.data.cameras.new("GuideCam"))
    cam.data.lens, cam.data.sensor_width = LENS, 36.0
    cam.data.clip_start, cam.data.clip_end = 0.05, 3000
    col.objects.link(cam)
    bpy.context.scene.camera = cam
    keys = camera_keys()
    pos, tgt = hermite(keys, 1), hermite(keys, 2)
    if ALT_S2:
        # Raise the camera 5 m and aim 14 m lower mid-shot (about 4.7 deg, ~12% of the frame),
        # so the base and hoarding sit higher with more open ground in front. The offset
        # is zero on frames <= 132 and >= 288, so the S1 and S3 overlaps are untouched.
        def w(f):
            def ss(x):
                x = min(1.0, max(0.0, x))
                return x * x * (3 - 2 * x)
            return ss((f - 132) / 44) * (1 - ss((f - 252) / 36))
        for f in pos:
            pos[f] = pos[f] + Vector((0, 0, 5.0 * w(f)))
            tgt[f] = tgt[f] + Vector((0, 0, -14.0 * w(f)))
    cam.rotation_mode = "QUATERNION"
    prev = None
    track = []
    for f in range(1, LAST_FRAME + 1):
        q = (tgt[f] - pos[f]).to_track_quat("-Z", "Y")
        if prev is not None and q.dot(prev) < 0:
            q.negate()
        prev = q
        cam.location = pos[f]
        cam.rotation_quaternion = q
        cam.keyframe_insert("location", frame=f)
        cam.keyframe_insert("rotation_quaternion", frame=f)
        track.append((f, pos[f], tgt[f]))
    return cam, keys, track


# ---------------------------------------------------------------- render + encode
def setup_render():
    scene = bpy.context.scene
    scene.render.fps = FPS
    scene.render.resolution_x, scene.render.resolution_y = RES
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = "PNG"
    scene.eevee.taa_render_samples = 24
    scene.eevee.shadow_pool_size = "1024"
    for o in bpy.data.objects:                 # small fills don't need shadow maps
        if o.type == "LIGHT" and o.name.startswith(("LoggiaLight_", "RoomShelves", "LoggiaSoffit")):
            o.data.use_shadow = False
    scene.frame_start, scene.frame_end = 1, LAST_FRAME


def render_frames(frames):
    scene = bpy.context.scene
    os.makedirs(FRAME_DIR, exist_ok=True)
    for f in frames:
        path = os.path.join(FRAME_DIR, f"{f:04d}.png")
        scene.frame_set(f)
        scene.render.filepath = path
        bpy.ops.render.render(write_still=True)
    print(f"RENDERED {len(frames)} frames")


def shot_range(name):
    a, b = FRAMES[name]
    return a, min(LAST_FRAME, b + OVERLAP)        # each guide runs 12 frames into the next shot


def encode(name, label=None):
    a, b = shot_range(name)
    name = label or name
    out = os.path.join(GUIDE_DIR, f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-start_number", str(a),
                    "-i", os.path.join(FRAME_DIR, "%04d.png"), "-frames:v", str(b - a + 1),
                    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart", out], check=True)
    shutil.copyfile(os.path.join(FRAME_DIR, f"{a:04d}.png"), os.path.join(GUIDE_DIR, f"{name}_first.png"))
    shutil.copyfile(os.path.join(FRAME_DIR, f"{b:04d}.png"), os.path.join(GUIDE_DIR, f"{name}_last.png"))
    print("ENCODED", out)


def write_json(keys, sched, track):
    shots = []
    for name, sec, note in SHOTS:
        a, b = FRAMES[name]
        ra, rb = shot_range(name)
        p_in, p_out = track[ra - 1][1], track[rb - 1][1]
        shots.append({
            "shot": name, "nominal_frames": [a, b], "rendered_frames": [ra, rb],
            "file": f"{name}.mp4", "frames": rb - ra + 1, "duration_s": round((rb - ra + 1) / FPS, 3),
            "nominal_duration_s": sec, "camera": note,
            "camera_start_m": [round(v, 2) for v in p_in], "camera_end_m": [round(v, 2) for v in p_out],
        })
    cuts = [FRAMES[n][0] for n, _, _ in SHOTS[1:]]
    data = {
        "version": VERSION, "fps": FPS, "resolution": list(RES), "lens_mm": LENS, "sensor_mm": 36, "total_frames": LAST_FRAME,
        "total_s": LAST_FRAME / FPS, "overlap_frames": OVERLAP,
        "cuts": [{"frame": c, "time_s": round((c - 1) / FPS, 3),
                  "note": f"{SHOTS[i][0]} -> {SHOTS[i + 1][0]}: same camera; guides share frames {c}-{c + OVERLAP - 1}"}
                 for i, c in enumerate(cuts)],
        "shots": shots,
        "world": {
            "axes": "Blender: Z up, metres; tower at origin, yawed 224.5 deg so its front (travertine band, "
                    "loggias) faces azimuth 134.5 deg (north-west); the band corner faces the S1/S2 camera",
            "tower_yaw_deg": round(math.degrees(TOWER_YAW), 2),
            "site": "76 x 64 m concrete pad with a 2.4 m hoarding (gate on the tower's front) at grade",
            "slabs": [{"centre": [sx, sy], "length_m": ln, "depth_m": dp, "height_m": SLAB_STOREYS * SLAB_STOREY_H,
                       "storeys": SLAB_STOREYS, "long_axis": "y" if ay else "x"} for sx, sy, ln, dp, ay in SLABS],
            "tower": "round-2 ORIZONT tower (blender/build_tower.py): 28x20 m, podium 6 m, 24 storeys x 3.6 m, parapet 96 m",
            "rooftop": {"centre": [round(ROOF_C.x, 1), round(ROOF_C.y, 1)], "terrace_z": ROOF_Z,
                        "distance_to_plot_m": ROOF_R, "eye_height_m": 1.7},
            "loggia": f"Loggia_{LOGGIA_FLOOR:02d} (storey {LOGGIA_FLOOR + 1}), floor at {ZF:.2f} m, camera eye {EYE:.2f} m",
            "sun": {"azimuth_deg": round(math.degrees(math.atan2(bt.SUN_DIR.y, bt.SUN_DIR.x)), 1),
                    "elevation_deg": round(math.degrees(math.asin(bt.SUN_DIR.z)), 1),
                    "reads": "back-right throughout: ~54 deg right of view in S1-S2, almost behind the tower at the S3 end and in S4"},
            "lake": {"centre": list(LAKE_C), "radii_m": list(LAKE_R), "rotation_deg": round(math.degrees(LAKE_ROT), 1)},
        },
        "stacking": {"method": "local Z scale 0->1 from each storey's base pivot (grows out of the one below); "
                               "Glass_XX trails its frame by 14 frames (~3 storeys)",
                     "start_frames": {k: v[0] for k, v in sched.items() if not k.startswith("Glass")},
                     "glass_start_frames": {k: v[0] for k, v in sched.items() if k.startswith("Glass")}},
        "camera_keys": [{"frame": f, "pos": [round(v, 2) for v in p], "target": [round(v, 2) for v in t]}
                        for f, p, t in keys],
    }
    with open(os.path.join(GUIDE_DIR, "guides.json"), "w") as fh:
        json.dump(data, fh, indent=2)


# ---------------------------------------------------------------- main
def main():
    bt.clear_scene()
    bpy.context.preferences.filepaths.save_version = 0
    bt.SUN_DIR = Vector((math.cos(math.radians(-52)), math.sin(math.radians(-52)), 0.09)).normalized()
    mats = bt.build_materials()
    _, loggia_home = bt.build_tower(mats)
    bt.build_city(mats, lot_filter=lot_filter)
    gm = guide_materials()
    gm.update(mats)
    col = bpy.data.collections.new("GUIDE")
    bpy.context.scene.collection.children.link(col)
    build_rooftop(gm, col)
    build_lake(gm, col)
    _, room_lights = open_loggia_and_room(gm, col)
    root = bpy.data.objects["Tower"]
    build_site(gm, col, root)
    build_slabs(gm, col)
    bt.setup_render_world(loggia_home)
    sched = animate_stack(room_lights)
    # Lights that belong to the tower turn with it; then turn the tower.
    for lo in [o for o in bpy.data.objects if o.name.startswith("LoggiaLight_")] + room_lights:
        lo.parent = root
        lo.matrix_parent_inverse = root.matrix_world.inverted()
    root.rotation_euler = (0, 0, TOWER_YAW)
    bpy.context.view_layer.update()
    cam, keys, track = build_camera(col)
    setup_render()
    os.makedirs(GUIDE_DIR, exist_ok=True)
    if ALT_S2:
        a, b = shot_range("S2")
        render_frames(list(range(a, b + 1)))
        encode("S2", label="S2_alt")
        with open(os.path.join(GUIDE_DIR, "S2_alt.json"), "w") as fh:
            json.dump({"file": "S2_alt.mp4", "rendered_frames": [a, b], "frames": b - a + 1, "fps": FPS,
                       "same_as_S2": "camera identical on frames 121-132 and 289-300 (S1/S3 overlaps)",
                       "stacking": "fully glazed with the crown complete at frame 239 (local 119); finished tower after",
                       "camera": "+5 m height and 14 m lower aim mid-shot (blend 132->176, back 252->288): base and "
                                 "hoarding ~12% higher in frame, more open ground in front",
                       "start_frames": {k: v[0] for k, v in sched.items()}}, fh, indent=2)
        return
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(bt.ROOT, "blender", "orizont_guides.blend"), compress=True)
    write_json(keys, sched, track)
    names = ONLY or [n for n, _, _ in SHOTS]
    if STILLS_ONLY:
        frames = sorted({f for n in names for f in shot_range(n)} | set(EXTRA))
        render_frames(frames)
        for n in names:
            a, b = shot_range(n)
            for tag, f in (("first", a), ("last", b)):
                shutil.copyfile(os.path.join(FRAME_DIR, f"{f:04d}.png"), os.path.join(GUIDE_DIR, f"{n}_{tag}.png"))
        return
    frames = sorted({f for n in names for f in range(shot_range(n)[0], shot_range(n)[1] + 1)})
    render_frames(frames)
    for n in names:
        encode(n)


main()
