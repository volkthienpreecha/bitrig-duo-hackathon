# Asset validation — September 25, 2026

> **Character version notice:** character results in this folder describe historical v1. Current character evidence is in [Kaprao v3 validation](../Revisions/Kaprao-v3/Validation/README.md). Workshop results below remain applicable.

**Result:** editable art and runtime assets are supplied. Native SceneKit imports and bone motion pass; the workshop and Kaprao render on the iPhone Duo simulator with live hinge callbacks. This is asset compatibility evidence, not a completed puzzle/game certification.

## Recorded checks

| Check | Result / evidence |
| --- | --- |
| Workshop source reopens; neutral pose/pivots and packed palette | Pass — `workshop-source-validation.json` |
| Workshop GLB fresh reimport | All 21 files pass — `workshop-import-validation.json` |
| Nominal landed bridge/floor clearance | No positive-volume overlap with floor proxies; about 30mm end/bottom clearance — `workshop-source-validation.json` |
| Native USD → SCN → reload | All 21 workshop + 5 Kaprao files preserve mesh, skin and animation counts — `../Runtime/*/scenekit-conversion.json` |
| Actual native animation motion | All four clips show nonzero changes in sampled presentation-bone matrices at 0 vs 0.23 seconds — `native-animation-motion.txt`; repeatable utility in `Tools/probe_scenekit_animation.swift` |
| Kaprao geometry, named actions, scale/root motion | Blender/export checks — `kaprao-validation.json`, `kaprao-manifest.json`, `kaprao-usd-clips.json` |
| iOS simulator app build | Xcode build succeeded — `asset-viewer-build.log` |
| Duo asset load and WAV decode | Isolated native viewer; machine log in `duo-asset-audit.txt` |
| Duo live hinge | Observed Book 127.8° / partiallyOpen, Open 180.0° / fullyOpen, Closed 0.0° / closed; rendered view remained present |
| UI files | 22 SVG XML checks; intended color pair contrast checks — `ui-svg-validation.json`, `ui-contrast.json`, `ui-qa.md` |
| Figma | Foundations/concepts uploaded; full screen composition blocked by account MCP quota — `ui-figma-status.json` |
| Bitrig embedded preview | Failed to install isolated test viewer, including after Relaunch Previews; screenshot `bitrig-preview-install-error.png`. Device Hub install succeeded. Root cause of Bitrig-specific failure not established. |

## Scope and environment

Blender 5.2.2 LTS; macOS 26.6.2; Xcode 27.1 build 27A9269; iOS 27.1 simulator; iPhone Duo device ID `14D82C7C-A4A4-45E6-B3A1-DB7F304F8738`. Runtime test bundle `local.foldfetch.assetcheck`. The test project is separate under `/private/tmp/FoldFetchAssetCheck`, not in the submission repository/archive. Native frameworks and CLI tooling were used because XcodeBuildMCP was unavailable.

The test viewer loads the supplied SCN files, supplies a basic camera and two lights, lets the user select four clips, decodes supplied WAVs and reports the installed SDK's `onHingeChange` values. It uses a single ordinary scene viewport. The hinge value is displayed; it does not drive a connected spatial projection. The test viewer loops every selected clip for inspection; the game must treat jump/celebrate as non-looping.

The native motion probe loads each exported SCN using Apple's SceneKit, assigns scene-time animation, updates a Metal-backed renderer at two times and compares 240 sampled bone-matrix components. All four clips moved. Native durations are 4.0s idle, 0.8s walk, approximately 1.067s jump and 2.0s celebration; the source jump action spans 1.2s, with the native importer retaining the shorter animated interval. This establishes that animation survived export/conversion, not that blending, foot contacts or character gameplay have been implemented.

Full workshop geometry: **59,956 triangles**, 19 visual meshes, 94 material primitives; **55,092 triangles** excluding skyline. Collision proposal: 23 boxes / 276 triangles, separate file. Kaprao: **19,900 triangles**, two mesh objects, ten-joint rig; full GLB has four actions. These are measured asset counts, not a GPU performance certification.

## Evidence interpretation

`Previews/` images and GIFs are Blender design renders. `Concepts/` images are generated concept illustrations. Files here beginning `duo-` are actual simulator captures/logs. Neither a pretty render nor a successful file load proves game physics.

The simulator's sound output was set to zero. WAV decoding/preparation is checked; audible playback, event timing and final mix remain unverified. Do not report a listening test.

The final workshop model includes pocket clearance corrections. Earlier `duo-loaded.png` and `duo-initial.png` were intermediate startup checks and are excluded from the handoff archive; final captures use the refreshed package. The closed-state screenshot taken before final reload demonstrates lifecycle/hinge behavior, not the pocket revision.

No physical-device performance measurements, sustained FPS benchmark, physics simulation stability, fold-projection calibration, narrow multitasking HUD test, accessibility runtime audit or submission app integration was performed. These remain concrete event implementation checks in `INTEGRATION.md`.

Apple API context was cross-checked with the installed SDK and [Apple's hinge and scene presentation](https://developer.apple.com/videos/play/tech-talks/111464/). All claims of success above come from local tests, not from assuming a documentation example proves this app works.
