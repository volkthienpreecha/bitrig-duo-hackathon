# Corgi Crossroads — the single execution prompt

Version 2.0 · September 26, 2026 · Street repair and actual outside-display continuation

**Execution active:** user explicitly requested implementation after the street-plan revision. Start recorded at 11:58 PDT; keep the fixed freeze/cutoff. App display name is Corgi Crossroads; do not rename or regenerate model files.

**Portrait requirement:** run vertically throughout. Upper/lower regions stack along the portrait height; the outside view is portrait too. Use actual region frames and window geometry, not a side-by-side assumption or forced equal halves. Configure portrait for the cover display, and verify the host’s inner portrait pose because its orientation behavior differs.

**Latest scope:** replace the rooftop beam with a city street missing a manhole cover. The user explicitly selected **aim inside, close the phone, then release on the separate outside cover display**. This replaces the lower-inner-only destination, beam geometry and three-rooftop progression. The prior build authorization is recorded; the latest conversation requested this plan revision. Reading or packaging instructions alone does not trigger a build. The old 11:30 automation stays paused.

## 1. Mission and authority

Build one polished native iPhone Duo demo named **Corgi Crossroads** in `/Users/volkthienpreecha/Documents/ChatGPT/Bitrig Duo Hackathon`. Preserve historical FoldAndFetch paths. Codex coordinates three workers; **Bitrig must build/run the same canonical project and host the recorded demo**. Xcode provides tests/diagnostics. Do not run a second master in Bitrig or send its stale unsent v1.0 composer.

Loop: **guide a clamped cover around a blocker → park and fold to aim → lock placement → close Duo → pull Release outside → watch the real landing and coverage → manually cross with Kaprao → next repair or replay**. One city kit, one cover type, two short data-only arrangements. No free-moving maze, traffic, moving hazards, timed release, lives, leaderboard, backend, camera capture or third puzzle.

Authority: latest user → this master → [PRD](PRD.md) → selected character handoff → historical assets/UI/reviews. This is the only executable plan. Old Workshop/Garden/Terrace assemblies and beam UI are historical references. Once execution resumes, implement, delegate, integrate, test, repair and save local commits autonomously; no routine milestone approval. Preserve other chats' work. Do not publish, submit or message people.

Submitted source/tests/scaffolding must be created within **September 26, 11:30–15:30 America/Los_Angeles**. Target **150 minutes**, maximum **180 minutes**, bounded by the event cutoff. Preserve **14:15 feature/art freeze**, **15:15 recording target**, **15:30 coding cutoff**. Rebase intermediate milestones at actual start, reserve the last 40 minutes for verification/recording and report unmet requirements. No guarantee of first-pass compilation or contest outcome.

## 2. Two arrangements and the exact interaction

| Repair | Configuration | Purpose |
| --- | --- | --- |
| Utility Corner | One dogleg rail around a fixed utility blocker; centered road opening | Learn guide, aim, lock, close, release and cross |
| Opposite Curb | Mirrored rail/blocker; road opening, route and goal shifted +0.30 m in depth | Re-aim using the same rules and a different measured fold solution |

Build both with one `PuzzleDefinition` loader. Prove the first before exposing the second. If the second has not independently passed landing, crossing, Retry and display transitions by freeze, hide Next/count UI and report it incomplete. No old rooftop progression.

**Staging:** the upper inner region shows a cover visibly held by a clamp carriage on a short dogleg rail around one static blocker. Drag along contiguous rail segments, stopping at corners until the pointer follows the next segment. Never globally project a pointer jump to a later segment through the blocker. Clearance includes the disk extent. Letting go parks the carriage; no sustained mouse hold. The final short horizontal rail segment provides continuous X placement; the hinge rotates the arm about X and changes the held center's Y/Z. Wrong placement/angle remains possible. The rail and mechanism must not sweep through the road, corgi or rim.

Use a **visible self-leveling holder**: the disk stays horizontal while its center follows the arm. This is a declared held constraint; no orientation correction or leveling force after release. Do not build free tray physics or a tilt maze. In compact inner layout, keep the staging controls reachable; route rail drags separately from dog gestures. A layout change cancels the active drag without changing the parked rail position.

**Lock placement:** available only on the launch segment, parked, with live hinge and settled mechanism. Start with ≤0.5° change over 0.20 s, tune from measured jitter. Do not require exact float equality/new callbacks or correct hole alignment. Capture the actual cover world transform, rail progress, aim angle and generation in an immutable `PlacementLock`; park the same cover there. Show “Placement locked. Close Duo to drop.” Closing cannot change the captured pose. Reopening before release offers `Adjust placement`, which explicitly unlocks and safely reconciles with the current live hinge.

**Outside release:** on the actual outside display, frame suspended cover, hole and corgi. Once active with valid layout, show **Pull Release**: ≥44 pt handle, initial 36 pt downward pull, one command on completed pull; short/canceled pulls spring back. Provide an accessibility action using the same command. Pull/button gestures never move Kaprao. Neither locking nor closing starts the drop.

Release preserves the captured world transform, detaches the same cover to the fixed world root, makes it dynamic once with zero initial velocities, opens the clamp and clears the lock. Remove every nonphysics transform writer. Gravity creates the fall. Later fold/camera/score changes cannot move it. No teleport, recorded fall or fabricated landing.

**Recovery/progression:** native Retry stays available throughout. Retry restores the current repair's pre-hole checkpoint and cover start. Outside Retry says “Open Duo to aim again.” Reopening restores live aiming; never fake a 90° hinge. Replay street starts the first enabled repair. Next repair appears only after the corgi reaches the toy and the next arrangement is verified. Reset/Next increments generation and clears placement, input, contact/dwell, forces, velocities and cosmetic/audio state; exactly one player and cover remain.

**Corgi controls:** retain bounded left/right bursts (initially one body length/0.35 s), grounded-only jump, and one downward dash per airtime. No speed stacking, extra airtime, air-jump spam or automatic walk. Initial swipe classifier: 28 pt, 0.08–0.6 s, axis ratio 1.35, one command per touch. Ignore diagonals/cancels/button/rail/reserved-region touches. Jump/dash practice is optional. Screen +X stays right on both displays. One Mac mouse must complete the sequence without simultaneous fold/drag/swipe.

## 3. Physical street and honest coverage

One unscaled world in metres: X route, Y up, Z depth; hinge axis X. Stable IDs: player, cover, carriage, clamp, named rim sectors, road, recovery and goal. Author a small native street kit during the build: asphalt, curb, zebra paint, barriers, recessed rim, metal cover and toy. Reuse palette/individual props if useful; never import a whole old bridge assembly or its hidden collider beneath the hole.

Starting dimensions: opening diameter **2.30 m**, cover diameter **2.75 m**, thickness **0.14 m**, recess diameter **2.81 m**. Seat top Y=-0.14, seated center Y=-0.07, road/cover top Y=0; nominal radial seam 0.03 m. Use 16 matching visible/convex rim sectors around a real opening and one matching convex disk collider. A convex hull across a ring fills the hole and is prohibited. The road outside the recess must use geometry/colliders with the same opening. Validate flush seam crossing from rest. These are toy-city starting dimensions, not measured real manhole dimensions or proven tuning.

Keep the dog's fixed depth lane legible with visible worksite barriers. Measure the opening's unsupported route chord against maximum jump reach including body extent and adversarial air input. Test rim shelves, tray, clamp, curb and props as bypasses. Tune visible geometry and colliders together if needed. SceneKit CCD is not a general solution for fast boxes/capsules; use tested speeds, step sizes and sufficiently thick colliders. No invisible bypass barrier or score-created floor.

**Coverage is feedback, separate from safety.** While airborne show “Landing…”. Once slowed/settled, estimate **Coverage: ~XX%** from deterministic samples of the opening polygon inside the disk's actual projected footprint. Use world geometry, not camera pixels. Mark it approximate, bound 0–100, and never treat projection overlap while high above the road as safe. This is game feedback, not an engineering safety certification.

`Safe to cross` requires: real upward/load-bearing contacts on separated intended rim sectors; their support polygon surrounds the projected center of mass; complete opening containment with initial 0.03 m margin; road/cover top difference ≤0.03 m; tilt ≤5°; linear speed ≤0.05 m/s and angular speed ≤0.1 rad/s; **0.40 s continuous simulation-time dwell**. Any failed condition resets dwell. Check actual sector geometry. A conservative circular precheck is offset + opening radius + margin ≤ cover radius × cos(tilt), but it never substitutes for contact/height tests. Partial coverage, edge perch, three neighboring contacts, tilted jam, tray rest and brief bounce remain unsafe regardless of percentage.

Only after genuine seating, visible rim clamps may hold **the same cover at the same pose**. No snap, replacement collider or invisible floor. The player must walk across that cover and reach the toy to finish. The cover hitting the toy cannot win. Unsafe openings remain physically open; a corgi fall gets gentle checkpoint recovery without injury. A five-second attempt timeout ends endless rolling/falling; Retry is immediate.

One hint at a time: “Drag around the blocker” → “Fold to aim” → “Hold steady” → “Lock placement” → “Close Duo to drop” → “Pull Release” → “Landing…” → “Coverage: ~XX% · Unsafe / Safe to cross” → “Swipe right to cross” → “Street repaired!” Derive miss direction from actual offset; otherwise say “Cover missed the opening.” Highlight exposed gaps. Do not guess correction direction from an uncalibrated hinge sign.

## 4. Actual outside display and one simulation

The user selected ordinary app continuation **after closing**, not simultaneous content on both displays. Apple's [adaptation guidance](https://developer.apple.com/videos/play/tech-talks/111461/) and [layout guidance](https://developer.apple.com/videos/play/tech-talks/111463/) describe this behavior. This is documented support, not proof in Bitrig. Early gate: actual app opens inside, preserves a placement value on close, shows reachable outside Release, falls there and survives reopening.

No `CameraCaptureAccessory`: documented simultaneous inner/outer camera presentation requires an active capture session. `ExternalNonInteractiveAccessory` is for connected/AirPlay displays, not a verified general Duo-cover output route. No second application window/game session. If ordinary continuation fails in Bitrig, diagnose and report the actual failure; do not silently substitute the lower inner panel and call it outer.

Use SwiftUI `.onHingeChange`, optional `DeviceHingeContext.hinge`, and `DeviceHinge.angle.radians`; UIKit `UIHingeInteraction` is an alternative, not a second feed. Nil is unavailable, never zero; system-controlled callback frequency means unchanged held values remain valid. Use `GeometryProxy.reservedRegions(kind:options:layoutDirectionBehavior:)` division/occlusion with `.includeInactive`; fully open can have an inactive zero-width divider. Frames already include margins. Derive usable panels in one coordinate space, clip to real bounds and convert to drawable pixels once. Avoid `UIScreen.main`, guessed equal halves and angle-only display detection; log actual scene/window geometry, lifecycle and hinge observations to establish inner/outer mapping.

**Closed outside layout is supported gameplay.** Live hinge is required to adjust/lock placement, not to release a valid lock or continue a released cover outside. Scene inactivity, invalid/zero bounds or unsupported geometry pauses physics and clears incomplete gestures; it does not automatically Replay. While paused, update device/layout/camera/HUD without SceneKit advancement. Require explicit Resume after lifecycle interruptions, rebase elapsed time and preserve world/lock. Release remains a separate explicit action. If reconciliation is unsafe, stay paused with a reason rather than move bodies or silently reset.

SwiftUI shell, SceneKit world/physics, explicit `SCNRenderer`/Metal. One persistent **MainActor-owned GameSession**, main-thread driver and monotonic simulation clock. Ordering: drain immutable commands → gameplay pre-step → `update(atTime:)` once per simulation step → post-step contact/coverage/safety → render-only passes → snapshots/events. No independent gameplay/presentation timers, unsafe actor crossings or arbitrary Sendable declarations. Never invoke update-and-render once per camera. Recreating views on display changes must not recreate the session. Count simulation steps separately from renders; replay never moves renderer time backward.

Expanded inner diorama uses calibrated planes and asymmetric projections from one fixed virtual eye, correct clipping/pixel scale, separate or proven-owned color/depth targets. Test seam/scale/occlusion with grid and crossing objects. Compact inner composition may keep staging readable during folding, but is not outside-display acceptance. Outside uses one stable camera on the same world with cover, opening, dog and controls visible. Share immutable framing anchors/bounds; interpolate camera/frustum parameters, never bodies or screenshot crossfades. Keep +X screen-right. Use one eye-facing sprite orientation per frame for both inner passes.

No app-added depth-of-field/motion blur. No verified host blur-disable, blur callback or external-orbit API exists. Compare raw and whole-Bitrig captures; rehearse one host viewing pose. Freeze touch layout/input-map version and cancel across mapping changes, not every hinge update. Native controls: ≥44 pt targets, 16 pt inset, 8 pt gaps, outside active occlusions and crucial objects. Pull/drop occurs only once the outside view is active and readable.

## 5. Selected assets, updates and sound

The latest [KapraoSprite handoff](../../DesignAssets/KapraoSprite/README.md) selects an **illustrated character in the 3D world**, superseding v3/v4 for visuals. [asset-selection.json](asset-selection.json) lists runtime files. Root scale **1**, visible height **0.84 m**, its own feet offset; never apply v3's 0.72/0.007 transforms. This is a pose-card visual, not a rigged mesh or exact reconstruction of unseen views. Read metadata/native validation; validate iOS atlas UVs, facing, feet and alpha/depth sorting against the new rim/barriers. Mirror only visual child, not the physics root. Pose/bob never moves the controller. Add only a visual support shadow. Keep styled orange/cream primitive dog with ears/scarf as an explicit fallback if necessary.

The user can change assets mid-run. **Check handoff docs and hashes at dispatch, every 10–20 minute integration, before copying resources, and before freeze/package.** Coordinator alone adopts a complete handoff and captures immutable bytes/hashes in owned staging. Do not edit/regenerate the other chat's files, mix revisions or hot-reload partial writes. Validate runtime import, scale/pivot/bounds/pose, appearance/performance and relevant gameplay regressions. A visual change cannot silently resize physics, hole or cover. Keep incomplete candidates pending and use last integrated visual. Replacements must finish regression before 14:15; later only required repairs with affected checks rerun.

No street runtime asset exists yet; the new kit is authored native geometry. Old rooftop UI SVG/PNG/JSON are visual references only; current hints/controls come from this master. No full-image game UI or old seated beam. Source archives/previews/rejected models stay outside runtime targets. Bundle files flattened or under `AssetContent`, never a top-level directory literally named `Resources` (known isolated install issue).

Eight existing WAVs: step_soft, jump, land_soft, dash_down, mechanism_release, bridge_land, success, retry. The bridge_land filename now maps to accepted cover impact. Preload, deduplicate events by ID/generation, cooldown impacts, cadence steps, mute and stop stale reset effects. Missing audio is nonfatal. Verify decoding, audible playback and captured recording audio separately. Preserve [audio provenance](../../DesignAssets/Licenses/AudioManifest.md).

## 6. Parallel execution and contracts

Coordinator records dirty status and preserves unrelated work; creates compiling native target, fixed contracts, neutral A/B/C implementations and explicit source/test/resource membership. Record a baseline with an explicit file allowlist; no broad git add. Three managed worker worktrees start at that exact revision with separate build directories, never remote default or missing untracked dependencies. If unavailable, use disjoint paths and coordinator-only Git. Only coordinator operates shared Bitrig/simulator/project/resources.

| Owner | Exclusive paths and responsibility |
| --- | --- |
| Coordinator | FoldAndFetch/App, Contracts, Integration, Resources; project/schemes/Git; Handoffs/Verification.md; builds and runtime evidence |
| A — platform/render | FoldAndFetch/Platform, Rendering; FoldAndFetchTests/Platform; Handoffs/A.md; hinge/layout/lifecycle, input, display continuation, one driver/cameras |
| B — gameplay | FoldAndFetch/Gameplay; FoldAndFetchTests/Gameplay; Handoffs/B.md; world, rail, lock/release, score/safety, controller/reset, two configurations |
| C — presentation | FoldAndFetch/Presentation, AssetStaging; FoldAndFetchTests/Presentation; Handoffs/C.md; selected sprite, native HUD, city dressing and audio |

Freeze actual Swift signatures before dispatch. Value contracts: `DeviceFrame` (timestamp, raw/calibrated angle, source/availability, lifecycle, resolved display/layout/version); `GameCommand` (sequence, generation, time, layoutVersion, action); `PlacementLock` (generation, captured world transform, rail progress, aim angle); `PuzzleDefinition` (ID, rail/blocker, opening/route/goal transforms, shared dimensions/tuning); `GameSnapshot` (step/generation/phase, repair/count, framing bounds, player, parked/settled/locked, coverage/safety/pause reasons); `GameEvent` (ID/generation/sim time/type/intensity). Actions: rail drag begin/update/end, lock/adjust, release, movement/jump/dash, retry/replay/next/resume. Mute is presentation. B owns scene/physical transforms; C attaches through integration on the session owner. A renders completed state.

- [ ] **Task 1 — coordinator/A:** green target/contracts, one SCN/WAV, actual Bitrig launch/refresh and inner→outer session preservation. Recorder permission/audio route in preflight; short saved playback test when audio runs. Dispatch workers after compiling baseline while coordinator diagnoses Bitrig.
- [ ] **Task 2 — A/B:** rail/blocker, hinge-causal held pose, lock and outer pull/physical fall. Pure checks: rail shortcut/cancel, pull threshold/repetition, lock immutability and stale generation. Runtime: actual mouse/hinge/display continuation.
- [ ] **Task 3 — B:** matching hole/rim/disk, coverage/safety, manual crossing, resets and second configuration. Test partial/perched/adjacent contacts/bounce, camera-independent score, bypasses and unchanged disk identity. Three controlled misses/lands each.
- [ ] **Task 4 — C/coordinator:** selected sprite/city/HUD/audio and asset-update transaction. Verify pose/facing/UV/feet/depth, bundle and offline launch. C finishes bounded delivery before final regression, freeing a reviewer slot.
- [ ] **Task 5 — coordinator/fresh reviewer:** exact integrated revision, independent spec/ownership review, fixes/re-review, enabled configurations, ten mixed cycles/ten-minute performance, final Bitrig movie/playback.

Deliver immutable compilable slices every **10–20 minutes**. Worker pauses edits; supplies base/delivery revisions, files, behavior, contract/resource requests, tests/failures and smoke scenario. Coordinator integrates one delivery at a time, builds/smokes combined app, publishes baseline; paused workers refresh. No independent writers to the shared Git index/simulator. Maximum four active agents including coordinator. A/B/complex reviews strongest available; C standard. Focused briefs. Never use author self-review as independent review, or module-only tests as combined acceptance.

## 7. Budget, cut lines and proof

| Actual-start budget | Outcome |
| --- | --- |
| 0–20 min | SDK/Bitrig/recorder; compiling baseline/dispatch; prove actual outside continuation |
| 20–55 min | Rail, live fold, lock, outer pull, one clock and visible physical miss/landing |
| 55–85 min | Safe manual crossing, coverage/reset, second data-only configuration |
| 85–110 min | Selected art/audio; second configuration checks; independent review/fixes |
| Last 40 min, target 110–150 | Combined regression, ten cycles/performance, offline rebuild, recording/playback and delivery |
| Reserve to 180 min | Core repairs only; no feature work after 14:15 or code after 15:30 |

Two failed attempts or ten minutes without new evidence triggers a different diagnostic hypothesis; keep the last working revision. Do not consume final verification time adding content. If outside continuation cannot be proven, record the core failure and seek an explicit scope decision; never silently relabel lower-inner footage.

Record pass/fail/not-run, exact revision/assets/app path, logs/captures in `Handoffs/Verification.md`:

1. Bitrig builds/installs/launches exact canonical saved revision, refreshes external edits, works offline. Developer directory `/Users/volkthienpreecha/Downloads/Xcode.app/Contents/Developer`, Xcode 27.1/Duo. No copied asset-viewer code.
2. One player/held cover, empty opening, correct rail/blocker/goal and no old bridge/static cover. New geometry is not certified by old asset tests.
3. Real hinge calibration; stable pose remains valid; same carriage checkpoint A misses/B lands three each. Both enabled arrangements have distinct measured fold solutions.
4. Rail corners/blocker/fast-pointer shortcut; canceled/repeated pull; four actual mouse swipes and button/rail isolation. One-pointer complete run.
5. **Actual outside display:** guide/aim/lock inside, close, release outside, full fall/coverage/cross visible, reopen same session. Closing at another angle cannot change the lock. No camera session or second simulation.
6. Partial coverage/perch/adjacent contacts/bounce/tilt/tray/floating overlap unsafe; dwell resets. Same disk/pose clamps only after real qualification; crossing flush seams from rest.
7. Approximate coverage bounded/camera-independent; no score-based safety or invisible floor. Jump/dash/props/rim cannot bypass repair.
8. Retry/Replay/Next during drag/lock/fall/settle/cross/win; no duplicate bodies or stale lock/contact/input/audio. Outer Retry asks to reopen for live aiming.
9. Close/reopen, lifecycle pause/resume, nil hinge while aiming versus valid lock outside, zero/changed bounds, touch mapping changes: no catch-up/reset/false win. Explicit Resume after interruption.
10. Same simulation step across 1/2 render passes, 30/60 cadence comparison; connected inner seam/scale/occlusion and clear single outer composition. No screenshot crossfade hiding landing.
11. Selected sprite hashes/scale/pose/UV/depth and all eight WAVs; actual audibility/mute/capture. New visuals do not alter physics silently.
12. Ten mixed play/miss/retry/win/close/reopen cycles and ten-minute frame-time/memory observation, target 60 fps with measured results. Independent review and fixes recorded.
13. Final **60–90-second whole-Bitrig-window movie**, showing host/Duo, obstacle, fold/lock, actual outside transition, deliberate miss, Retry/changed aim, safe physical landing, manual crossing, celebration and Next/Replay as enabled. Save path/duration/resolution/audio result/revision; play it back. Raw app/Device Hub footage is diagnostic only.

Deliver native app running in Bitrig, saved revision/build, verified movie, launch/control/replay steps, asset provenance and explicit unmet requirements. No claim of completion while outside flow, physical landing/safety, manual control or recording remains unproven.
