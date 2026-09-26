# Kaprao v3 verification — September 25, 2026

The v3 character was generated from the prepared fluffy reference, refined in Blender and rendered natively on the iOS 27.1 iPhone Duo simulator. The workshop and submission game code were not changed.

| Check | Result |
| --- | --- |
| Editable source reopens | Pass; three packed 2048 × 2048 images — `source-deformation.json` |
| Mesh buffers, normals, weights, joint indices, degenerate triangles | Pass — `kaprao-validation.json` |
| Geometry | 46,156 triangles, three visual meshes, ten materials, shared 11-joint rig |
| Four named clips, durations, loop endpoints, root translation | Pass; 4.0 / 0.8 / 1.2 / 2.0 seconds; zero root translation |
| Sampled mesh deformation | Finite, bounded geometry; no exploding vertices. Worst sampled floor excursion about 8.4mm below zero; this first-pass rig does not implement foot locking. |
| Runtime textures | Three 1024 × 1024 PBR maps; source remains 2048 × 2048 |
| USD to SCN and reload | All five files pass with embedded textures — `../Runtime/Kaprao/scenekit-conversion.json` |
| Native bone motion | All four clips pass at 0 vs 0.23 seconds — `native-animation.txt` |
| Duo build / installation / resource load | Pass, isolated `local.foldfetch.assetcheck` viewer — `asset-viewer-build.log`, `duo-asset-audit.txt` |
| Final optimized texture rendering | Captured at Open 180°, Book approximately 127°, Closed 0° — `duo-open-idle.png`, `duo-book-idle.png`, `duo-closed-idle.png` |

The SCN files together occupy about 45.4 MiB before ZIP compression. Each clip is self-contained and repeats the geometry/textures; bundle only the clips required by the app. The GLB contains all four clips but is an exchange file, not the supported direct SceneKit input.

The source's high-resolution studio previews and final native screenshots use the same mesh and accessory design. Native lighting differs from the Blender studio. Fur is a combination of texture relief and 2,300 fine tapered mesh ribbons, with no Blender-only shader at runtime.

This is an asset compatibility check, not game or physical-device certification. The temporary viewer displays hinge callbacks using a single ordinary viewport; it does not implement the connected folded projection, controller collision, beam physics or final animation transitions. Physical-device memory/frame-time measurements are still needed. Bitrig's earlier embedded-preview install failure is not represented as a pass; Device Hub and Xcode are the verified route.

The image `duo-book-walk.png` records the earlier 2048px runtime draft; the three final idle screenshots record the optimized 1024px runtime files. The viewer loops one-shot actions for inspection; the game should play jump/fall and celebration once.
