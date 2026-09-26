# Corgi Crossroads verification

Start 11:58 PDT September26. Portrait required. All runtime gates NOT RUN until evidence recorded. Assets captured in AssetSnapshot.json; character handoff now KapraoSprite. User requested only app naming; no model rename/regeneration.

## Baseline 82c6668 — 12:07 PDT

- Native simulator build PASS: /tmp/corgi-baseline-build.log, /tmp/CorgiCrossroads-baseline/Build/Products/Debug-iphonesimulator/CorgiCrossroads.app. Initial sandbox macro execution failure resolved by approved unsandboxed Xcode invocation.
- Actual Bitrig embedded Duo closed outside display launched Corgi Crossroads and showed its title. This proves baseline project discovery/build/install/resource bootstrap, not gameplay. Inner portrait and lock preservation still NOT RUN on implemented modules.
- 12 selected resource files rehashed; no source changes since snapshot. No model files modified.
- Recorder CLI is available; audio input capture exists, system/app-audio capture still unverified.

## Revised tilt integration — 12:28 PDT

- User authorized revised full tilt game + iPad motion bridge, superseding rail. A physical iPad is connected; installation/signing and live sensor streaming remain separate verification gates.
- Integrated immutable worker revisions: 2803ff5 (street), 1b5eca2 (motion), 495626d5 (audio); root counterparts 4e0a6bf/5f680ca/12b937f.
- Canonical combined simulator Xcode build PASS: /tmp/corgi-tilt-build.log, app /tmp/CorgiCrossroads-tilt/Build/Products/Debug-iphonesimulator/CorgiCrossroads.app. One audio mute-binding compile error was repaired before successful build.
- Built Info.plist inspected: correct display name, motion/local-network usage descriptions, local-only ATS permission, portrait iPhone/iPad orientation keys. No global ATS disable.
- Coordinator flow+dwell executable checks PASS17: immutable placement, no early/inactive/unmounted/double release, reset, continuous fresh stationary dwell.
- Coordinator receiver test rerun PASS11, using temporary localhost sockets after approved sandbox escalation. Initial socket-blocked run was not passing.
- Coordinator actual SceneKit render/physics suite PASS: center+4 corners seated, manual crossing to won, genuine56.8% miss, reset, open-hole recovery, pause. Initial sandbox GPU execution failed; approved unsandboxed run passed, log /tmp/corgi-street-integrated.log.
- Isolated TiltLab actual SpriteKit route+barrier+dwell PASS with scripted gravity, not real sensor input: Experiments/TiltLab/Evidence/tilt-smoke.json. Adapted canonical board still needs integrated runtime proof.
- Twelve runtime source asset hashes unchanged. No model file changes.
- Bitrig preview was stale after source integration. Project window closed/reopened; preview currently Starting. No canonical visual/outer transition/recording proof claimed yet.

## Portrait/runtime follow-up — 12:42 PDT

- 21 coordinator checks PASS, including a wide window with horizontal division remaining inside and an unsupported active division never releasing outside.
- Portrait-only base and iPhone-specific orientation declarations; single app scene confirmed in built plist.
- Added explicit flexible height for both render surfaces. Integrated b79c6fa fixes road triangle winding and pins horizontal camera extent without changing physical geometry. Worker native renders show selected Kaprao sprite and toy at compact inner and tall outside sizes; worker physics60/120Hz pass.
- Rehashed all12 source and staged resources: unchanged. No model regeneration.
- Bitrig canonical process launch confirmed; console initial layout at12:41:36: size867x635, divisionnil, activefalse, closedfalse. Preview remains visually stale and game interaction not yet verified. Investigating rendering callbacks.
- Actual hinge, outside visible release, controls/crossing/reset and recording still NOT VERIFIED. The Bitrig draft was updated to v2.1 and iPad bridge language; no competing AI rewrite sent.

## Live renderer repair — 12:45 PDT

- Process sample `/tmp/corgi-current-sample.txt` proves deadlock: main thread inside `setOutsidePresentation` → `C3DTransactionCommit` waits for scene lock while SceneKit callback waits on `DispatchQueue.main.sync`.
- Replaced synchronous delegate hops with one coalesced asynchronous main-thread controller update from SceneKit's post-physics callback. SCNView remains the sole simulation clock. Canonical Xcode build PASS.
- Bitrig relaunch PID42502 now visibly renders Kaprao, the actual road opening and goal toy. Rotate Right yields upright vertical Duo with horizontal physical fold. Live SDK observations: angle1.567rad; view669x835; horizontal division `(0,373.5,669,40)` active; flowinside. This proves actual hinge + portrait region handling, not yet a full playthrough.

## Current verified state — 12:49 PDT

- Simulator and physical iOS device builds PASS after render-ready change: `/tmp/corgi-tilt-build.log`, `/tmp/corgi-device-build.log`. Device build is unsigned compilation, not a hardware run.
- Post-frame controller-order native physics regression PASS: `/tmp/corgi-postframe-physics.log`; actual centered/corner drops seat, crossing wins, deliberately offset cover fails at58.5% projected coverage, and reset/open-hole recovery/pause pass.
- Renderer readiness now means first completed `didRenderScene` frame in the mounted view, not mere window attachment. One bounded asynchronous controller update avoids the proven main/SceneKit deadlock.
- Actual Bitrig close/open logs from PID42502: closed status arrives while inner division still active; only after resize382x644 and divisioninactive does modeoutside occur. Reopening transitionsunknown theninside at669x835 with horizontal region. This verifies topology classification with real simulator transitions.
- Motion settings opened successfully. Repeated macOS `noWindowsAvailable` errors still intermittently block coordinate controls even after user makes Bitrig visible. Complete interactive target-to-outside-release/crossing playthrough and final recording remain NOT VERIFIED. No successful physical iPad stream is claimed in this thread.
