# Fold & Fetch — rooftop workshop

> **Original reusable kit.** For the approved three-stage handoff use [Stages](../../Stages/README.md), whose beam and matching collider are wider for Kaprao v3. The original 0.35 m beam dimensions below do not describe the current stage exports.

Original modular 3D workshop art, authored for this project with reproducible Blender geometry. The warm enamel, sea glass machinery, copper bridge, little plants, lamps, and distant skyline are actual meshes. The rendered PNGs are **design previews, not simulator captures or evidence of working physics**.

Open `fold-and-fetch-workshop.blend` in Blender 5.2 or later. Rebuild from `../../Tools/workshop_build.py` with Blender's background Python runner; add `-- --all-renders` to generate all views, or `-- --no-render` for exports only. `../../Tools/workshop_render.py -- --all-renders` renders the existing source without changing exchange files. Metal rendering is used when available. That path is relative to this folder only as a reading aid; the tool script itself resolves the DesignAssets root automatically.

## Files and modular pieces

`Exports/Workshop/workshop-assembled.glb` and `.usdc` contain the neutral assembled visual scene. Each of the 19 modules also has its own GLB and USDC file, with its root pivot at file origin. The separate `workshop-collision-proxies` pair contains only proposed collision geometry and module roots.

| Piece | Purpose |
| --- | --- |
| `floor_left`, `floor_right` | Separate route decks with a 2.20 m gap |
| `support_left`, `support_right` | Broad load-bearing cradle shelves and depth-channel walls |
| `upper_chute` | Open-bottom carrier; pivot at the real X hinge axis |
| `release_gate` | Separate pivoted copper gate, under the carrier in the assembled hierarchy |
| `bridge_beam` | Independent root; 2.90 m copper bridge core |
| `recovery_tray` | Low padded basin underneath the gap |
| `practice_curb` | Optional tiny practice step, offset from the main lane |
| `exit_bell`, `goal_toy` | Brass bell arch and distinct teal ball |
| `rooftop_base`, `workshop_frame`, `roof_rails` | Static diorama structure |
| `repair_bench`, `planters`, `workshop_lamps`, `service_cables` | Separate decorative groups |
| `distant_city` | Optional low-contrast skyline geometry |

The Blender source retains editable component meshes; exchange files consolidate each visual module to one mesh with multiple material groups. Cameras, lights, preview ground, and typography overlays are excluded from exports. No runtime animations are included for the environment.

## Scale, axes, and pivots

- All dimensions are meters. Root and mesh scales are 1,1,1.
- Blender source: X is the route, Z is up, negative Y is the front.
- GLB and USD: X is the route, Y is up, positive Z is the front.
- Conversion is **game (X,Y,Z) = Blender (X,Z,-Y)**, a rigid rotation with no reflection.
- Left deck covers X -4.00 to -1.10; right deck covers X +1.10 to +4.00. Core deck top is game Y=0. The 2.20 m figure is the gap between platform extents. Shallow landing pockets expand the opening along the exact route centerline to 2.96 m; the 2.90 m beam leaves 30 mm end clearance on each side. These small deck joints require controller testing. Pocket bottoms lie at Y=-0.25, 30 mm below the landed beam core, preventing an initial beam/floor penetration.
- Bridge core is 2.90 m along X, 0.22 m high, 0.35 m deep. Its origin is its core center. Small grip, edge, and cap details expand its visual bound slightly; use the supplied simple core box for initial collision testing.
- Cradle shelf top is Y=-0.22. The neutral beam core center is (0,-0.11,0), so its top is flush with the decks.
- Hinge pivot is game **(0,3.00,-1.20)**, axis X.
- Intended held beam center at the neutral design pose is **(0,1.75,0)**.
- Gate pivot is game **(0,1.60,-0.27)**. Its local position under `upper_chute` is **(0,-1.40,+0.93)**; do not apply its world origin a second time if keeping the assembled hierarchy.
- Standalone module placement origins are recorded in `Validation/workshop-geometry.json` in both conventions. The assembled exchange files already contain those placements.

`ANCHOR_corgi_start`, `ANCHOR_route_forward`, `ANCHOR_gap_center`, `ANCHOR_world_origin`, `ANCHOR_hinge_axis`, `ANCHOR_held_beam_center`, `ANCHOR_release_point`, `ANCHOR_release_gate_pivot`, both contact anchors, beam endpoints, recovery center, and exit goal are named empties in source and exchange files. Character route forward is +X.

## Motion and collision contract

The beam is deliberately **not a child of the moving chute** in the assembled file. The game may compute its held pose from the named carrier anchor. On release, preserve the authoritative world pose under the fixed simulation root and let one physics owner control it. There is no landing animation masquerading as physical success.

The three storyboard images use exactly the same carrier and beam geometry at hinge offsets -28°, 0°, and +28°. They show held design poses. Zero is an authored reference, **not a calibrated device angle**. Rotation about X changes the release's elevation and depth; it does not aim the bridge left or right. Gate opening, the held-to-dynamic transition, velocity policy, success qualification, reset, and supported device range still need runtime implementation and tests.

Twenty-three simple boxes live in `90_COLLISION_PROXIES_NONRENDER`. They are hidden for source rendering and exported separately. They propose floors split around the landing pockets, cradle shelves/walls, beam core, tray and long lips, curb, chute guides, gate, and toy bounds. A measured nominal-pose check verifies no positive-volume overlap between the landed beam proxy and any floor proxy; ray queries also verify that the visual deck pockets were cut. This is a geometry-fit check, not a physics stability result. The decorative service deck and backdrop are not intended alternate walkable routes. Collider masks, thickness/speeds/timestep, moving carrier strategy, contacts, and two-support stability have not been physics-tested.

## Materials and rendering

Nineteen simple Principled/PBR materials use constant color, roughness, metalness, and restrained emission. The palette PNG and named hex JSON are provided in `Textures/Workshop`; they are reference swatches, not required texture dependencies. No Blender-only procedural shader, missing image, external font, HDRI, or downloaded mesh is required. The palette reference is packed into the source blend.

Design renders are 2160×1440 with warm soft key lighting, a cool fill and roof rim, contact shadows, no depth of field, and no motion blur. Neutral source pose is the landed bridge; the fold references show the held bridge. Lighting is for art review and has not been ported or performance-tested in the game renderer.

## Counts and validation

- Full visible workshop: **59,956 triangles**, including the optional skyline.
- Without `distant_city`: **55,092 triangles**.
- Runtime visual scene: **19 meshes, 53 nodes, 94 material primitives**.
- Collision proposals: **23 boxes, 276 triangles** in a separate file.
- All **21 GLBs** passed fresh Blender reimport, finite-coordinate, unit-scale, resource-containment, camera-exclusion, and animation-exclusion checks.
- Every standalone visual GLB reimported as one mesh. Full workshop reimported as 19 meshes.

See `Validation/workshop-import-validation.json` for measured bounds and per-file results. SceneKit/RealityKit behavior, device performance, actual hinge mapping, collision stability, and simulator sharpness are outside this asset validation. Use the project-level validation record for any later native import checks.

## Source and rights

All geometry, materials, placement, and procedural modeling scripts in this workshop folder were created for this project. No marketplace or downloaded 3D models or textures were incorporated. Labels are converted geometry generated from Blender's built-in font; no font file needs redistribution. The palette is an original arrangement of plain colors. This kit has no third-party asset attribution requirement. The project's concept references remain reference images; their pixels are not used as runtime textures.
