# Three-stage asset validation

September 25, 2026. Actual generated source and native files were checked, not only concept images.

| Check | Result |
| --- | --- |
| Editable source reopens, packed original character textures | Three scenes pass |
| Fresh GLB imports | Six pass: three visual scenes at 19 meshes each, three collider scenes at 23 boxes each |
| Geometry/resource checks | Finite coordinates, unit-scale export nodes, no external GLB resources, no exported camera/light/animation dependency |
| Nominal beam/floor overlap | No positive-volume overlap with the supplied floor boxes |
| Paw/beam fit | 0.4282 m nominal low-paw envelope at 0.72 character scale; fits 0.54 m beam depth |
| Endcap/channel fit | Approximately 0.5554 m endcap depth within 0.63 m support channel and 0.64 m deck pocket |
| Fold design references | Intended pose aligns release depth; adjacent reference poses straddle the route depth. This is kinematics, not a falling-object simulation. |
| USD to SCN and reload | All six stage files pass |
| Native hierarchy/anchors | All 45 world positions checked within 0.1 mm; held-beam anchor and gate follow chute, beam remains independent |
| Isolated Duo viewer | Build succeeds; all six scene resources pass runtime loading; all three visible worlds render with Kaprao v3 |
| Shared clips/audio | Four native clip imports/durations and eight WAV decode checks pass |
| UI | Six local editable state variants, PNG overlays/concepts, compact progress/Next controls and refreshed existing mockups |

The native viewer uses one ordinary scene and reads the live hinge; it does not implement the game's fold-connected projection. Screenshots show the fully open 180° state, not proof across all game postures. Earlier v3 character checks include separate open/book/closed asset-viewer evidence.

Measured visual world triangle counts: workshop 59,956; garden 71,052; terrace 57,968. Shared Kaprao adds 46,156. These are measured counts, not mobile performance certification. Consider reducing optional skyline and material groups if the actual two-display renderer needs it.

Two issues found and corrected: the old 0.35 m beam was too narrow for the selected visual character scale, and hidden reference empties were omitted from USD. The new beam and collider widened together to 0.54 m; export temporarily includes the selected reference empties, then restores source visibility. `stages_native_validate.swift` guards the anchor contract.

Evidence: `validation-summary.json`, `native-validation.json`, `duo-asset-audit.txt`, each stage's `Validation/geometry.json`, `import-and-fit.json`, `duo-stage.png`, and native `Runtime/scenekit-conversion.json`.

## Not established

Actual beam release/contact/stability, physical crossing or dynamic foot locking; controller collision and animation transitions; connected dual-display perspective; native HUD/safe-region behavior; audible mix; sustained FPS/memory/thermal behavior; physical-device performance; Bitrig embedded-preview installation. Those require event-window game implementation. No submission application code was added to the repository.

Figma's connected Starter MCP quota still blocks live composition. Local assets are complete; the live Figma file has not been synchronized. No paid generation or subscription was used for this stage work.
