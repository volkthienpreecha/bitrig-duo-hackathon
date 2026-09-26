# Tilt Street gameplay handoff

Status: DONE_WITH_CONCERNS. Revised standalone tilt-street slice, 2026-09-26 approximately 12:24 Pacific. Real native physics tests pass; actual Duo display/hinge/gesture/recording checks remain coordinator-owned and unverified here.

## Owned delivery

- `FoldAndFetch/TiltStreet/TiltStreetWorld.swift`
- `FoldAndFetch/TiltStreet/Verification/PhysicsCheck.swift` (macOS-only executable verification; excluded by conditional compilation on iOS)
- `Handoffs/TiltStreet.md`

No shared contracts, project, assets, simulator, Bitrig, or TiltLab edits. Earlier rail work remains separately uncommitted in Gameplay and FoldAndFetchTests; do not integrate it for this revised flow.

## Exact API / integration

`@MainActor final class TiltStreetWorld: NSObject, ObservableObject`

- `@Published private(set) phase: TiltStreetWorld.Phase` with `waiting`, `dropping`, `safe`, `failed`, `won`.
- `@Published private(set) coverage: Double` in 0...1; UI must label it approximate. Airborne projection can be 100% and is never safety by itself.
- `@Published private(set) hint: String`.
- `@Published private(set) rendererReady: Bool`. True only after the active SCNView's `didMoveToWindow` confirms a window; false on attachment start, detachment and dismantle.
- Persistent `scene`, `player`, `playerVisualRoot`, and public `camera`.
- `reset()`, `drop(offset: CGPoint)`, `moveRight()`, `moveLeft()`, `jump()`, `dash()`.
- `TiltStreetView(world: TiltStreetWorld)` is a UIViewRepresentable. Keep one world across lower-inner/outside mounts.

Root owns closed-hinge, active portrait, absent-divider, 300ms stable outer layout and renderer-ready gating. `drop` intentionally knows nothing about device layout. Only call it when those conditions pass. It is one-shot while phase is `waiting`.

Offset maps actual X/Z position at **0.018 metres per normalized unit**, starting Y=2.7m. Thus a lawful board target edge +/-1 becomes +/-0.018m, with no snap or alignment correction. Values beyond +/-1 remain real physical error for diagnostics (street bound clamps world X/Z to +/-2m); `(60,0)` produces a 1.08m genuine miss. Production board provides `(position-target)/20`.

SCNView alone advances physics at its 60Hz render cadence, with SceneKit timeStep 1/120. `beforePhysics`/`afterPhysics` are for its delegate and isolated tests; **never also call a session renderer.update on this scene**. Old view's scene and delegate are removed when a new view attaches. Dismantle is identity-guarded. The world honors `scene.isPaused` and never overwrites it. Camera angle stays fixed; viewport aspect only changes orthographic scale to keep both ends of the street visible.

## Physics / visual behavior

- Opening vertex diameter 2.30m; 16 separate visible/physical rim sectors, never a hull across the opening. Recess has 2.81m flat-to-flat clearance. Road and rim use exact static triangle meshes because SceneKit convex-hull padding caused an experimentally reproduced high perch.
- Same 2.75m-diameter, 0.14m-thick native cylinder falls from the supplied pose. No post-release transform writers, safety floor, replacement disk, or scoring-created geometry.
- Rim top is -0.14m; actual seat center measured about -0.0698m and disk top approximately 0.0002m.
- Safety separately requires actual upward rim contacts whose support polygon surrounds COM, full opening containment with 0.03m margin, entire disk top within 0.03m, tilt <=5 degrees, actual measured translation <=0.05m/s, angular motion <=0.1rad/s and 0.40s continuous dwell.
- Motion is measured from actual presentation transforms; cached body velocity getters in offscreen tests were insufficient evidence.
- Rounded native 0.25m sphere body under the sprite avoids box/capsule seam snagging and padding; angular motion disabled, fixed Z lane. Manual bounded bursts use physical horizontal impulses; jumps and one-per-airtime downward dash use impulses and retain gravity.
- Same player and visual root survive reset. One cover is rebuilt; generation increments, motion/contact/dwell/input state clears. Checkpoint recovery follows a real fall through the opening.
- Preferred visual is bundled `kaprao-sprite.scn` / `KapraoSpriteRoot`, unchanged at scale 1. Existing `kaprao-idle.png` is the fallback; no asset changes.

## Verification evidence

Native iOS simulator-target Swift typecheck PASS. Standalone iOS simulator Mach-O library compiled/linked; linker emitted a sysroot-version warning (Mach-O platform checked as IOSSIMULATOR). Canonical full app build remains coordinator-owned.

Actual macOS SceneKit/Bullet offscreen renders at both 120Hz and the live 60Hz callback cadence PASS:

- Center zero-offset gravity fall seats on 16 rim sectors, dwell >0.40s, coverage 1.0.
- Manual right bursts cross the actual disk and reach toy; phase `won`, player X approximately 3.11m, Y=0.25m.
- All four lawful board corners (+/-1,+/-1) physically seat, without snapping.
- Offset `(60,0)` physically rests off-center and remains failed, about 56.8% coverage.
- Duplicate drop ignored; reset retains player/visual identity and children and leaves exactly one cover.
- Three neighboring supports rejected; conservative jump envelope 1.72m < opening minimum chord 2.26m.
- Uncovered opening physically drops the dog into checkpoint recovery.
- Coordinator-controlled pause freezes physical pose.

Run (from worktree):

```sh
DEVELOPER_DIR=/Users/volkthienpreecha/Downloads/Xcode.app/Contents/Developer xcrun swiftc FoldAndFetch/TiltStreet/TiltStreetWorld.swift FoldAndFetch/TiltStreet/Verification/PhysicsCheck.swift -o /tmp/tilt-street-verification
/tmp/tilt-street-verification
```

For 60Hz, replace the harness's `1.0/120` time increment with `1.0/60` in a temporary copy, compile it with the same world and run. Tests use actual `renderer.snapshot` renders: `SCNRenderer.update(atTime:)` alone did not initialize native collisions on macOS and contact queries crashed inside SceneKit. This was diagnosed, not counted as passing.

## Remaining smoke / concerns

1. Build canonical target including the standalone source. Keep old GameSession out of this scene's clock.
2. In real Duo, stage board on upper inner, street below; navigate and dwell target; verify closed/outer/layout-ready gate before drop.
3. Outside: observe suspended pose, gravity fall, approximately flush seat, safe hint, then repeated right swipes across same disk to toy. Confirm actual outside display, no simultaneous-display workaround.
4. Retry during fall, safe, failed, and won; verify one player/cover and reopened board staging. Confirm portrait camera framing and selected SCN visual at scale 1 on both view sizes.
5. Verify jump is grounded-only, one air dash, left/right bursts, no button gestures moving Kaprao, and pause/resume behavior on actual host.
6. Bitrig canonical build/run and final recording are unverified here. No claim of hinge/display transition, mouse gesture, or recording proof from headless tests.
