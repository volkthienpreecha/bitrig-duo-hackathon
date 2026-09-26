# Three rooftop stage assets

The approved cozy cyberpunk diorama set: **Rooftop Repair Club**, **Moonleaf Garden**, and **Starlight Terrace**. Same smooth rounded scenery, restrained warm lighting, physical bridge idea and fluffy Kaprao v3 with RGB glasses. The worlds are reusable 3D assets; previews are not gameplay footage.

## Open the work

- [All three scenes](three-stages.png)
- [Stage 1 source](01-workshop/Source/01-workshop.blend), [preview](01-workshop/Previews/hero.png), [fold storyboard](01-workshop/Previews/fold-storyboard.png)
- [Stage 2 source](02-garden/Source/02-garden.blend), [preview](02-garden/Previews/hero.png), [fold storyboard](02-garden/Previews/fold-storyboard.png)
- [Stage 3 source](03-terrace/Source/03-terrace.blend), [preview](03-terrace/Previews/hero.png), [fold storyboard](03-terrace/Previews/fold-storyboard.png)
- Each `Previews` folder includes a Kaprao close-up, annotated editable SVG/PNG top/side plans, orthographic renders and three separate fold frames.
- [Six UI variants and progress/Next designs](../UI/Stages/README.md)

## Easy native setup

Choose one stage's `Runtime/*-assembled.scn` and, when configuring physics, its separate `Runtime/*-colliders.scn`. Bundle those with the selected shared [Kaprao v3 SCN clips](../Revisions/Kaprao-v3/Runtime/Kaprao) and existing `../Runtime/Audio` WAVs. Do not bundle Blender sources, GLBs, previews or the whole preparation folder. Do not add the old root-level workshop assembly on top of a stage assembly.

Runtime exports contain 19 independently named visual module roots, one consolidated multi-material mesh each, and named anchors. There are 23 simple collider proposals in the separate collider file. Cameras, lights and the preview-only dog are excluded from stage exports. Native code owns lighting/cameras and instantiates the shared character once. The `.blend` review source includes Kaprao with packed original textures for easy editing.

Use the supplied `ANCHOR_corgi_start` world position. Place a gameplay parent there, with the visual character scaled to **0.72** and lifted **0.007 m** relative to the deck. Model files themselves retain their original units and proportions. The lift compensates for the small source-pose foot penetration; animation contact and controller collision still require testing.

## Changed geometry: use the stage beam

The original workshop beam was too narrow for Kaprao's paws at scene scale. All new stage beams and their collision proxies are **2.90 × 0.22 × 0.54 m** in runtime X/Y/Z. Endcaps and grip details widened with the core. Deck pockets remain 0.64 m deep; the support channel is 0.63 m deep, so the approximately 0.555 m endcaps fit. The 2.96 m pocket opening still leaves 30 mm along X at each end. Shelf height and core thickness remain unchanged, keeping the seated beam flush with the decks.

Do not mix the original 0.35 m beam collider with these stage visuals. The supplied stage collider scenes match their visuals. A new source/import check measures nominal paw width, beam/floor clearance and hierarchy; it is not a physics proof.

## Three arrangements, one mechanic

| Stage | Route depth Z | Art variation |
| --- | --- | --- |
| 01-workshop | 0.00 m | Warm repair club, cream and teal enamel, copper bridge. |
| 02-garden | +0.32 m | Sage surfaces, fuller planting, copper trellis; lower route moves together. |
| 03-terrace | -0.28 m | Open rear frame, distant skyline, muted blue enamel, tea detail; lower route moves together. |

Coordinates: metres; native Y up and +X route/forward. Blender `(X,Y,Z)` maps to native `(X,Z,-Y)`. Hinge stays native `(0,3,-1.2)` with X axis. The gate follows `upper_chute`; `bridge_beam` is an independent world root. `Validation/geometry.json` records anchors, held poses and the solved design reference angle for each stage. The before/after fold frames miss the route depth on opposite sides; these are held-pose references, not simulated falling results. Never substitute the design angle for a physical landing test.

## Lighting and performance

Sources use a broad warm key, modest cool fill and restrained practical accents. No depth of field or motion blur. Colors/material changes define the variations without a new texture dependency. SceneKit lighting must be matched by eye in the actual game; Blender render appearance and native screenshots are separate evidence. Nominal source/import checks and simulator loading do not establish sustained frame rate, contact stability, optical continuity or physical-device performance.

## Rebuild and rights

Run `Tools/stages_build.py` through Blender from the project root, then `Tools/stages_validate.py`. Convert each `Exports` folder with `Tools/convert_scenekit.swift`. Run `Tools/stages_design.py` followed by `Tools/stages_render_design.cjs` and `Tools/ui_render.cjs` to rebuild annotated plans and UI previews. Source scripts resolve paths relative to themselves; the Node renderer uses the already-installed Sharp runtime. No new account, service subscription or paid generation is needed.

World geometry/materials derive from the project's original workshop kit; the added trellis, tea cup and placement variants are authored here. Kaprao provenance remains [the v3 record](../Revisions/Kaprao-v3/SOURCES.md). No new third-party model or texture was downloaded.
