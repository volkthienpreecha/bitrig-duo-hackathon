# Workshop art handoff review

Reviewed September 25, 2026. Scope: authored Blender art, GLB exchange reimports, nominal geometry fit, and design preview images. No game implementation or physics simulation was created by this work.

## Deliverables

- Editable `Source/Workshop/fold-and-fetch-workshop.blend`, packed palette, and detailed source README.
- Nineteen separate visual module GLBs and USDCs, plus full assembly and separate collider files: 21 files in each exchange format.
- Nine 2160×1440 PNG design previews: wide workshop, bridge close-up, rooftop close-up, top plan, right profile, front elevation, and three fold poses.
- Reproducible build, render-only, reimport-validation, and source-finalization Python tools.
- Named palette swatch PNG and hex JSON. Runtime materials have no external texture dependency.

## Visual review

The wide view and both details show smooth enamel edges, rounded rails, capped mechanism tubes, warm practical lamps, restrained copper and cyan accents, a distinct bridge, small plants, a brass exit bell, and a low-contrast night skyline. The static hinge brackets visibly attach to the rear frame. The final pocket surfaces were re-normalized after their boolean cuts to remove diagonal shading artifacts.

The layouts show the X route, start, exit, both cradles, hinge axis/height, held beam anchor, optional practice curb, recovery tray, and dimensions. Captions have dark backing for contrast. Top plan hides the upper carrier and states that explicitly. Right profile frames the full mechanism without cropping the hinge.

All three fold images use the same meshes and camera. The carrier and held beam rotate about X while the deck remains fixed. Their labels state the authored offsets (-28°, 0°, +28°), that they are held poses, and that no physics is shown. All previews are labeled **DESIGN PREVIEW / NOT A SIMULATOR CAPTURE**. Source cameras have depth of field disabled; scene motion blur is disabled.

## Measured checks

- 59,956 visible triangles including the optional skyline; 55,092 without it.
- Assembled GLB: 19 meshes, 53 nodes, 94 material primitives.
- Separate collider GLB: 23 simple boxes, 276 triangles.
- All 21 final GLBs reimported successfully into a fresh Blender scene with finite coordinates and unit node scales; no cameras, animations, or external resource paths were present.
- The assembled beam is an independent root. Gate parent is the upper chute; pivot and world coordinates match the stated Y-up convention.
- The final `.blend` reopened successfully in the neutral landed pose with the palette packed and collision collection hidden from render.
- AABB checks on the actual source proxies show no positive-volume overlap between the nominal landed beam and any floor proxy. End and bottom separation are approximately 30 mm.
- Ray tests on both cut visual floor bodies hit the pocket floors at source Z=-0.25 m, confirming that the recesses exist in the visual geometry as well as in the collider decomposition.

Machine-readable evidence: `workshop-geometry.json`, `workshop-import-validation.json`, `workshop-source-validation.json`, and `workshop-fold-poses.json`.

## Integration limits

The **2.20 m platform extent gap** differs from the **2.96 m opening along the pocketed route centerline**. The 2.90 m beam leaves 30 mm deck joints at its ends. Character crossing, friction, mass, timestep, gate timing, fast-fold sweeps, support qualification, and reset behavior still require runtime tests. The geometry fit test is not a claim of stable physics. The static decorative service deck is not supplied as an alternate walkable route.

The 0° play pose is an art reference, not a device hinge calibration. Rendering these views does not verify the continuous folded-screen projection or simulator blur behavior. Device frame time and the cost of 94 material primitives remain unmeasured; the skyline and decorative modules can be omitted independently.
