# HANDOFF: Team 3D

## Round 2 + Guides (21 Nov 2026, SPEC §8 Amendment 2)

The hero is now a Higgsfield-edited video. Team 3D supplies the **motion guides**: one scene, one continuous camera. The guides are never published on the site.

**v2 (current) vs v1.** v1 is kept in `blender/guides/v1/`. v2 follows the judge's VIDEO-pilot notes:
- **Tower yaw:** the tower is turned 224.5° about its axis, so the travertine band corner faces the S1/S2 camera at about 50°, with the east face visible. The band reads at 3/4 for the whole rise.
- **Ground:** a 76 × 64 m concrete site pad and a 2.4 m hoarding ground the base at grade.
- **Orbit:** to keep S4's dolly into the loggia, S3 now orbits about 60° clockwise and ends 20° off the loggia axis. With the band facing the S1/S2 camera, a longer orbit would have to end oblique to the loggia.
- **Sun:** now at azimuth −52°, so it reads back-right in every exterior shot.
- **Lake:** moved to sit behind the tower at the S3 end.
- **Height yardsticks:** three 1970s Bucharest prefab slabs (10 storeys × 2.8 m = 28 m, 12 m deep, banded windows, a few lit) stand within 115–190 m of the plot: front-left of the site, behind-right and behind-left. They give the video model a scale reference against the 96 m tower. Like the rest of the world, they appear in every shot.
- **Unchanged:** frame counts, cut frames and the 12-frame overlaps are identical to v1. All six shots were re-rendered, because the S3 end (and so S4's start) moved.

**Contingency `S2_alt.mp4`** (plus `S2_alt_first/last.png` and `S2_alt.json`; render with `-- --alt-s2`):
- **Range:** the same frames as S2 (121–300).
- **Faster stack:** the tower is fully glazed with the crown complete at frame 239 (local 119); the last ~60 frames show the finished tower.
- **Camera:** mid-shot it rises 5 m and aims 14 m lower, blended over frames 132→176 and back over 252→288. This puts the base and hoarding about 12% higher in frame, with open ground in front. Frames 121–132 and 289–300 have exactly the S2 camera, so the S1/S3 overlaps hold.

**Files** (`blender/guides/`, all 1280×720, 24 fps, H.264 yuv420p, EEVEE):
| shot | file | frames (nominal → rendered incl. 12-frame overlap) | length | camera |
|---|---|---|---|---|
| S1 RISE | `S1.mp4` | 1–120 → 1–132 | 5.5 s | eye height (1.7 m) on a 24 m terrace 340 m west of the plot; rises over the travertine parapet between olive planters and tilts down to the empty plot |
| S2 STACK | `S2.mp4` | 121–288 → 121–300 | 7.5 s | drone push from 340 m to 185 m on a gentle arc while the tower stacks on its site pad: podium, then 24 storeys each growing up out of the one below, glass trailing the frame by ~3 storeys, crown last. The band faces the camera at about 50° (3/4) |
| S3 ORBIT | `S3.mp4` | 289–456 → 289–468 | 7.5 s | ~60° clockwise round the finished tower, closing from 185 m to 87 m and rising from 38 m to loggia height (58.5 m), lake behind; ends 20° off the loggia axis, framed on the travertine band |
| S4 APPROACH | `S4.mp4` | 457–576 → 457–588 | 5.5 s | straight dolly onto the loggia axis toward `Loggia_14` (storey 15) until the loggia fills the frame (4.4 m out from the stone) |
| S5 THRESHOLD | `S5.mp4` | 577–696 → 577–708 | 5.5 s | over the balustrade, through the open centre of the sliding glass (2.6 m clear) into the living room |
| S6 DRIFT | `S6.mp4` | 697–816 | 5.0 s | slow lateral drift left (2.3 m) across the living room: smoked-oak shelf wall, low sofa, coffee table, floor lamp, window right |

- **Stills:** `S#_first.png` / `S#_last.png` are each guide's first and last rendered frames.
- **`guides.json`:** frame ranges, cut frames (121, 289, 457, 577, 697), camera keys, the stacking schedule, the sun and the world layout.
- **Total:** 816 frames = 34.0 s.

**Physical plausibility**
- **Scale:** storeys 3.6 m; eye height 1.7 m on the rooftop and 1.6 m in the loggia/room. The rooftop is 340 m from the plot at 24 m.
- **Camera:** one 28 mm lens, no zooms. The path is a time-based C1 cubic Hermite spline through keys: velocity is continuous everywhere, including the cuts, and the camera starts and ends at rest. There are no teleports, and the camera clears every object (parapet, balustrade cap, door leaves).
- **Stacking:** each storey scales 0 → 1 in Z from its base pivot, so it rises out of the one below. It is hidden, not collapsed, until it starts, so nothing floats in mid-air.
- **Sun:** fixed in the world at azimuth −52°, elevation 5°. It reads back-right in every exterior shot: about 54° right of view in S1–S2, and nearly behind the tower at the S3 end and in S4.
- **Interior:** the living room sits inside `Floor_14`, behind the open sliding doors. Its tall window is the tower's own east facade; those panels are removed in the guide only. It grows with the storey during S2. Furniture scale follows `interior-living.webp`; the loggia (lounge chairs, round table, planters, glass balustrade) follows `loggia.webp`.

**Reproduce**
```
/Applications/Blender.app/Contents/MacOS/Blender -b -P blender/build_guides.py                  # all six (~20 min)
... -P blender/build_guides.py -- --shots S1,S2     # subset
... -P blender/build_guides.py -- --stills --frames 200,380   # first/last stills + spot frames
```
Frames render to `$TMPDIR/orizont_guide_frames_v2` and are then encoded with ffmpeg. The script imports `build_tower.py`, so the guide tower is the round-2 tower. It also saves `blender/orizont_guides.blend`.

**GLBs moved:** `build_tower.py` now exports to `blender/export/tower.glb` and `blender/export/city.glb` (production files) and still copies them to `public/models/` until RELEASE drops those from the build. Their content is unchanged (same sha256).

**Bridge:** the Higgsfield Blender bridge reported `blr: false` at every check, including at the start of the guides work. Everything ran headless in Blender 5.2.1. Headless renders log harmless tracebacks from the installed Higgsfield add-on, whose background account lookup times out; they don't affect the output. Add `--factory-startup` to silence them.

**Status (end of guides work):** all seven v2 guides are rendered in one consistent world: S1, S2, S2_alt, S3, S4, S5 and S6. They were checked frame by frame from contact sheets for scale, continuity at the overlaps and the stacking read. VIDEO now builds S4 from S3's real last frame and has S5/S6 already, so the v2 S4–S6 guides are for the record.

## Round 2 (21 Nov 2026): judge fixes, matched to the canonical `tower-exterior.webp`

**Unchanged for HERO.**
- **Contract:** every node name, parent, pivot and material name is identical to Round 1. There are still 101 nodes:
  - `Floor_XX` pivots stay at `(0, 6 + 3.6·i, 0)`.
  - `Loggia_XX` pivots stay at `(10.3, base, 8.8)`.
  - The loggia offset `(0, 0.55, +1.8)` still holds.
- **Loading:** `tower.glb` is still uncompressed and still loads with a plain `GLTFLoader`.

**What changed**
1. **Lit windows by occupancy.**
   - **Occupancy:** each storey has 2 homes (1 on the two penthouse storeys). About half are "home" at dusk (seeded; 31 of the 46 homes in this build). An occupied home lights 2–3 rooms of 2–4 adjacent panels. An empty home sometimes leaves one dim lamp on. The result is **16.9% of façade panels lit** (241/1429), down from 30%.
   - **Room atlas:** `M_WindowGlow` now carries `room_atlas.jpg`, a 256×512 emissive texture of 21 KB with 8 room cards:
     - colour temperatures from 2700 to 3300 K, intensity 0.25–1.0
     - a bright ceiling/cove band and a dark sill
     - two cards with sheer curtains, others with sofa and lamp, shelving or table silhouettes
     - a soft flat card for the crown lantern and a dim "away" card
   - **UV mapping:** each lit panel's UVs point at a slice of one card, so all panels of a room share one interior across their width. `emissiveFactor` is white, and `KHR_materials_emissive_strength` is 2.0. This is plain glTF, with no custom shader.
   - **Loggias follow occupancy:** 15 of 24 are lit, each with a different card for each half of the back wall and a cove strip. The other 9 show the dim "away" card, so there is no uniform ladder.
2. **The seam, rebuilt to the canonical silhouette.**
   - **Width:** it is now a narrow travertine corner band, about 8.4 m wide at the top and 9.8 m at the base, made of a 5.4 m loggia opening, a leading pier and a corner pier. The loggia stack fills it.
   - **The step:** the leading edge steps in by 1.4 m at mid-height, on a diagonal facet across storeys 11–12, as in the photo.
   - **Corner:** the corner pier returns only 2 m onto the right facade, which is otherwise all glass, as in the photo.
   - **Stone surface:** it now has vertical panel joints (6 cm facing panels with 3 cm shadow gaps) as well as the 5 cm storey joints. Each panel samples the texture at its own offset, which gives a slight tone variation, and the texture repeat is now 1.5 m. No flat stone area wider than about 2 m remains.
   - **Base and top:** the seam lands as piers framing a double-height glazed entrance. At the top it ends in a jointed stone cap level with the parapet, at **96.0 m**.
3. **Minor fixes.**
   - **Balustrades:** frameless glass, drawn as the slim bronze cap and base shoe. The pane itself is omitted, because an opaque `M_Glass` pane read as a black bar.
   - **Crown lantern:** one continuous soft band (every panel on the flat card) behind the fin screen.
   - **Bare storeys:** each `Floor_XX` now holds a core block and 12 slim columns (`M_Frame`), hidden behind the opaque glass until `Glass_XX` is hidden. Then the construction look reads as structure (`construction.png`).
4. **Renders.**
   - **World:** a dusk sky with a dark ground, a warm horizon, a sun glow and the pink "belt of Venus" opposite the sun.
   - **Glass coat:** `M_Glass` got a glossy coat, exported as `KHR_materials_clearcoat`; base #2a2118, metal 0.6 and rough 0.15 are unchanged. The glass now reads as reflective bronze rather than matte black.
   - **Light:** the sun is back-right, and there is a render-only light in each occupied loggia.
   - **New stills:** the ch1 and ch2 camera positions, plus a construction-look still.
5. **Heights.** The marketing "ÎNĂLȚIME 96 m" is the **parapet / seam-cap height, 96.0 m**: the crown fin screen and the stone cap both top out there. The roof slab of `Floor_23` is at 92.4 m. The Round 1 blade (99 m) and crown screen (97.8 m) are gone.

**For HERO**
- Because of the clearcoat, `GLTFLoader` now creates a `MeshPhysicalMaterial` for `M_Glass`. It still needs a PMREM environment, ideally a dusk gradient with a warm side.
- With the room atlas, `M_WindowGlow` has an `emissiveMap`, so it looks right at `emissiveIntensity` 2.0 (the value from the file). Lower it if bloom is strong.
- One storey has no lit panels (`Glass_16`), so its only material is `M_Glass`. Code that looks up a `Glass_XX` child by material name must tolerate that.

### Round 2 renders (`blender/renders/`, EEVEE, AgX)
| file | view |
|---|---|
| `tower_34.png` (1600×2000) | full tower, 3/4 from front-right |
| `seam_closeup.png` (1600×2000) | the seam band, step and loggia stack |
| `loggia_closeup.png` (1600×1000) | loggias: stone returns, room cards, balustrade caps |
| `ch1_skyline.png` (1600×1000) | ch1 position: about 250 m out, from mid-height (45 m), tower centred |
| `ch2_seam.png` (1600×1000) | ch2 position: close 3/4 on the seam from +Z/+X |
| `construction.png` (1600×1000) | top 3 storeys with `Glass_21–23` and `Crown` hidden: core and columns visible |

## Current state

**`public/models/tower.glb`:** 1.80 MB uncompressed (budget 3 MB), **24,774 triangles**, two embedded JPEGs (travertine 512², room atlas 256×512). Extensions used: `KHR_materials_clearcoat` and `KHR_materials_emissive_strength`, none required. Metres, Y-up, origin at the base centre. The footprint is 28 × 20 m: a 6 m podium, 24 storeys of 3.6 m (roof 92.4 m), and a parapet and seam cap at 96.0 m.

Node tree (pivots in three.js coordinates):
```
Tower (empty, 0,0,0)
├─ Podium            (0, 0, 0)        lobby glass, bronze columns, transfer slab, canopy, stone plinth
│  └─ Seam_Podium    (0, 0, 0)        piers to the ground framing the glazed entrance, head band
├─ Floor_00 … Floor_23  (0, 6 + 3.6·i, 0)   slab edge, fins, core + columns, lid: the bare frame
│  ├─ Glass_XX       (same pivot)     glass panels (M_Glass + M_WindowGlow room cards)
│  ├─ Seam_XX        (same pivot)     that storey's stone: band (loggia floor) + jointed piers
│  └─ Loggia_XX      (10.3, base, 8.8) stone returns, glazed back wall (card per half), frames, cove, balustrade cap
└─ Crown             (0, 92.4, 0)     roof slab edge, lantern band, bronze fin screen to 96.0
   └─ Seam_Crown     (0, 92.4, 0)     jointed travertine cap to 96.0
```
Animate each `Floor_XX` from its pivot: its seam, glass and loggia follow, so the seam never hangs over missing floors. `Podium` comes first and `Crown` last. For the §7.1 construction look, hide `Glass_XX` on the top 2–3 rising storeys. A loggia's floor level and outer face are its `Loggia_XX` pivot + `(0, 0.55, +1.8)`.

**Materials**
| name | values |
|---|---|
| `M_Glass` | base #2a2118, metal 0.6, rough 0.15, clearcoat 1.0 / 0.03, opaque |
| `M_Stone` | travertine JPEG (mean ≈ #cdbfa6), rough 0.8, world-space triplanar UVs at 1.5 m per repeat, per-panel UV offsets |
| `M_WindowGlow` | emissive texture = room atlas, emissiveFactor 1, strength 2.0, base #3a2a1c |
| `M_Frame` | #33271c, metal 0.85, rough 0.35 |

**`public/models/city.glb`:** 0.10 MB, 1,454 triangles, same frame, unchanged from Round 1. It holds `Ground` (a 1400 m square) and `City_Blocks` (110 blocks, 7–75 m tall), with a 70 m clear plot and a low-rise front approach. Material: `M_City`.

## How to re-run
```
cd /Volumes/Development/imobiliare_landing_page
/Applications/Blender.app/Contents/MacOS/Blender -b -P blender/build_tower.py              # build + export + 6 renders (~25 s)
/Applications/Blender.app/Contents/MacOS/Blender -b -P blender/build_tower.py -- --no-render
/Applications/Blender.app/Contents/MacOS/Blender -b -P blender/verify_glb.py                # re-import + report
python3 -I docs/reviews/tools/glb_inspect.py public/models/tower.glb                         # judge's inspector
```
The script is seeded. **The exported GLBs and textures (`tower.glb`, `city.glb`, `travertine.jpg`, `room_atlas.jpg`) are byte-identical between runs** (sha256 checked). The renders differ only by EEVEE noise and the `.blend` only by save metadata. All dimensions are named constants at the top of `blender/build_tower.py`, and the build prints an `OCCUPANCY` line with the lit share.

Blender path: the Higgsfield bridge reported `blr: false` at the start and end of Round 1 and again at the start of Round 2. Everything ran in **headless Blender 5.2.1**, with no `bl_execute` run or `bl_screenshot`. The script falls back to `ORIZONT_ROOT` when `__file__` is missing, so it can run through `bl_execute` later.

## Verification (Round 2; Blender re-import via `blender/verify_glb.py`, storeys 01–22 elided, all present)
```
=== public/models/tower.glb  1.80 MB
nodes (101):
  Crown        parent=Tower     origin(x,y,z)=(  0.00, 92.40, -0.00)  tris=  1966 mats=M_Frame,M_WindowGlow
  Floor_00     parent=Tower     origin(x,y,z)=(  0.00,  6.00, -0.00)  tris=   620 mats=M_Frame
  Floor_23     parent=Tower     origin(x,y,z)=(  0.00, 88.80, -0.00)  tris=   628 mats=M_Frame
  Glass_00     parent=Floor_00  origin(x,y,z)=(  0.00,  6.00, -0.00)  tris=   118 mats=M_Glass,M_WindowGlow
  Glass_23     parent=Floor_23  origin(x,y,z)=(  0.00, 88.80, -0.00)  tris=   120 mats=M_Glass,M_WindowGlow
  Loggia_00    parent=Floor_00  origin(x,y,z)=( 10.30,  6.00,  8.80)  tris=   102 mats=M_Frame,M_Stone,M_WindowGlow
  Loggia_23    parent=Floor_23  origin(x,y,z)=( 10.30, 88.80,  8.80)  tris=   102 mats=M_Frame,M_Stone,M_WindowGlow
  Podium       parent=Tower     origin(x,y,z)=(  0.00,  0.00, -0.00)  tris=   598 mats=M_Frame,M_Glass,M_Stone,M_WindowGlow
  Seam_00      parent=Floor_00  origin(x,y,z)=(  0.00,  6.00, -0.00)  tris=    84 mats=M_Stone
  Seam_23      parent=Floor_23  origin(x,y,z)=(  0.00, 88.80, -0.00)  tris=    60 mats=M_Stone
  Seam_Crown   parent=Crown     origin(x,y,z)=(  0.00, 92.40, -0.00)  tris=   108 mats=M_Stone
  Seam_Podium  parent=Podium    origin(x,y,z)=(  0.00,  0.00, -0.00)  tris=    84 mats=M_Stone
  Tower        parent=-         origin(x,y,z)=(  0.00,  0.00, -0.00)  EMPTY
materials: ['M_Frame', 'M_Glass', 'M_Stone', 'M_WindowGlow']
images: [('room_atlas', (256, 512)), ('travertine', (512, 512))]
triangles: 24774
bbox x -18.00..19.00  height -0.05..96.00  depth -14.00..15.00  -> 37.0 x 96.1 x 29.0 m (w x h x d)
lights/cameras: none
```
`glb_inspect.py`: 1,804,160 B, `missing contract nodes: none`, `Seam_XX not parented to Floor_XX: none | single Seam node present: False`, `missing contract materials: none`, TOTAL tris 24774.

## Known gaps
- The bridge Blender was never connected, so there is no `bl_execute` run or `bl_screenshot`.
- The glass is opaque, so lit rooms are flat room cards (no parallax). They read well at chapter 1–2 distances and are flat in extreme close-up.
- The balustrade panes are omitted: the cap and shoe stand in for frameless glass.
- The city is massing only, meant to sit under fog.

## Round 1 (21 Nov 2026), summary
This round built the node contract, the per-storey seam (Amendment 1 §7.3) and the separate `Glass_XX` node, with a reproducible script. The judge passed it with fixes, craft 6/10: the window pattern read as a barcode, the seam was a blank stone wedge, and the renders were matte. Round 2 addresses all of these.
