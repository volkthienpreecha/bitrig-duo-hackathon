# Fold & Fetch — the single execution prompt

> **Asset update, September 25, 2026:** The locked style is a cozy cyberpunk rooftop 3D diorama with smooth rounded shapes, restrained warm lighting, and Kaprao wearing removable RGB sunglasses and a teal scarf. The selected character is [fluffy Kaprao v3](../../DesignAssets/Revisions/Kaprao-v3/README.md); root-level Kaprao assets and the old full ZIP contain rejected v1. Read [the remaining-assets status](../../DesignAssets/DEMO-ASSET-CHECKLIST.md) and [the current asset pack](../../DesignAssets/README.md) and [art direction](../../DesignAssets/ART-DIRECTION.md) before older asset guidance below. The pack supplies editable models, native SceneKit assets, animations, UI, and measured validation; this does not certify the future game physics or connected Duo projection.

Version 1.1 · prepared September 25, 2026 · paste this entire document once during the hackathon.

## Mission and authority

Build and finish **one polished, playable native iPhone Duo simulator demo** called **Fold & Fetch**. A corgi crosses a gap after the player folds the device to aim a chute, releases a real falling beam, and seats it as a bridge. The fold must change the physical outcome; the player must be able to miss, understand why, retry, and succeed. The visual ambition is a miniature 3D workshop apparently continuing across the two angled inner-display regions.

You are the coordinator. This is authorization to implement, delegate, integrate, test, fix, save local commits, and prepare the demo through completion. Report evidence at milestones and continue; do not stop after the tiny prototype or ask for another routine design/build approval. Preserve unrelated work. Do not publish, submit, or message other people without existing explicit authorization. This document supersedes older build prompts and automatic-walking concepts. The accompanying PRD explains the product; `Review/` contains failure analysis, not additional mandatory scope.

**Time boundary:** submitted app source, tests, and scaffolding must be created during the September 26, 2026 coding window, **11:30–15:30 America/Los_Angeles**. If this prompt arrives earlier, inspect tools/docs/assets and prepare only; do not generate reusable submission code. Recheck the organizer's schedule if changed. The official event is simulator-based, using Xcode 27.1 beta; a polished demo suffices. No physical Duo is required by the verified event page. One submission per team, at most five people. RevenueCat SDK is required only for its prize and is excluded from this default build.

## 1. Establish the real workspace and execution host

Canonical repository: `/Users/volkthienpreecha/Documents/ChatGPT/Bitrig Duo Hackathon`. Kit: `Preparation/FoldAndFetch-Bitrig/`. If running elsewhere, locate the supplied kit and declare one authoritative native project path before editing. Inspect existing files and repository instructions; reuse an existing app if one has since been created.

Known preparation state: Xcode 27.1 build 27A9269 is in `/Users/volkthienpreecha/Downloads/Xcode.app`; the iOS 27.1 Duo simulator boots in Device Hub. Bitrig has successfully opened the exact repository with **File → Open Folder** and displayed its README. Its preview says **No Project File** because no app existed at preflight. Local folder reading is proven; app creation/build, two-way edit refresh, and resource loading are not. Bitrig branch/PR status was unavailable. GitHub is history, not live synchronization.

If executing in Bitrig, use the already-open folder’s **New Conversation**, not an unrelated New Project draft. If executing in Codex, remain in Codex and operate the canonical repository; use Bitrig only for bounded editing/preview actions. Do not submit another copy of this master elsewhere. Within eight minutes of event start, verify the actual developer directory, SDK/runtime, Duo destination, available build tools, and project path. Use a per-command developer-directory selection if needed; do not move Xcode or change global settings just to start the demo. When code exists, prove one small edit in each direction at the same path before relying on Bitrig/Codex shared editing. If unavailable, Codex/Xcode own the canonical app and Bitrig is an optional preview/import consumer of a recorded revision. Never maintain two concurrently edited authoritative apps.

**Agent capability:** prefer Codex as coordinator, with three actual subagents. Bitrig is an editor/preview tool, not a verified subagent orchestrator. If the host has no agent tools, execute the identical role packets sequentially and report that limitation. Do not invent delegation tools or pretend independent workers exist. Only one coordinator may run this prompt. Do not launch it simultaneously in Codex and Bitrig.

## 2. Locked product scope and controls

One required level, one physical bridge puzzle, Retry and Replay. The technical test room grows into that same level. Aim for a 60–90-second presentation including a miss and recovery; do not add filler to force that duration. No second level/puzzle, tilt requirement, head tracking, camera scanning, accounts, backend, monetization, or multiplayer. No joystick or automatic walking.

Player sequence: **move to safe staging area → park → fold to aim → let the mechanism settle → tap Release → watch the drop → manually cross → reach a clearly visible toy → celebrate**. This works with one Mac mouse; no simultaneous fold drag and character gesture, timed fold during flight, or midair catch is required. Jump and dash remain available, with an optional safe practice pad; a mandatory curb/timing obstacle must not delay the core reveal.

Lower region swipes: left/right sets or reverses a short bounded movement burst, initially one body length over 0.35 seconds; up jumps only when genuinely grounded; down dashes downward only while airborne, once per airtime. Start classification near 28 points, duration 0.08–0.6 seconds, dominant axis ratio 1.35; tune from actual mouse play. One command per touch. Ambiguous diagonals, canceled gestures, touches starting on buttons/upper controls/reserved areas do not move the corgi. Flush pending gestures on pause/reset/layout changes. Burst inputs cannot stack speed, reset gravity, extend airtime, or allow air-jump spam. Screen-left/right maps consistently to the route.

Release is an obvious 2D button anchored by the upper chute, enabled only when loaded, active, in supported layout, and mechanically settled. Determine settlement with a finite angular/mechanism tolerance over a short monotonic-time window, not exact floating-point equality or a required new callback. A held valid pose enables Release promptly despite normal simulator jitter. A held unchanged hinge value remains valid; absence of new callbacks alone is not unavailability. Retry restores the pre-gap checkpoint; Replay returns to the beginning. Both use the **current live hinge pose**, not a fabricated 90° reset. Falling recovers promptly without health or punishment systems. A missed beam reaches an explicit failure via the visible tray, bounds, or a short attempt timeout; no endless falling/rolling. Retry stays accessible throughout an attempt and restores the saved pre-gap checkpoint. Win requires the corgi reaching the toy after the bridge is ready; the beam hitting the goal cannot win.

## 3. Physical design: fix the geometry before art

One unscaled world in meters: **X = left/right route, Y = up, Z = depth; hinge axis = X** in the selected presentation pose. Coordinator and platform/gameplay owners document origin, pivot, scale, API angle offset/sign, and virtual eye before parallel implementation. API hinge values are radians; calibrate actual open/flat reference and sign on the simulator. Unknown/nil input is explicit, never silently zero. Use actual region/reserved-area data for layout and touches; margin-inflated reserved regions are not physical screen measurements.

The beam is long along X and spans two supports separated along X. Rotating about X changes **Y/Z, not X**: folding aims the beam's **depth Z** into a visible catch channel across both supports. Show front/behind misses clearly. Use generous visible cradles and low bounce, not an angle-conditioned success animation. Keep chute motion away from the corgi, landed beam, and recovery area. Recess support seats by beam thickness so the seated beam’s top aligns with both platform decks within tested controller tolerance. All three surfaces share the character’s fixed Z lane. Keep cradles, rails and clamps outside the walking corridor. The unbridged gap has no static support or trigger shortcut. Verify walking across from rest without jumping.

While held, the beam follows the upper mechanism. On release, preserve its authoritative world pose, detach it to the fixed world root, make it dynamic once, and remove every nonphysics transform writer. Initial release is settled with zero velocity; no noisy inferred throwing momentum. Later folding must not drag the released/landed beam around. Moving chute colliders need an intentional kinematic policy, not teleported static mesh collisions.

Bridge qualification, evaluated after physics: both **named intended supports**, load-bearing contact direction/regions, endpoint overlap, usable orientation, low linear/angular speed, and about 0.4 seconds of continuous simulation-time stability. Any failed predicate resets the dwell. One support plus a wall, a transient bounce, or resting in the tray fails. After genuine seating, visible clamps may lock **the same beam at the same pose**, making the crossing reliable. Before latching, support loss revokes readiness. Do not spawn an invisible floor, teleport to a success position, or replace the beam collider.

Use a simple collision-constrained controller: preferably a dynamic primitive with route-depth and rotation constraints, bounded velocity/impulses, and visual animation beneath it. Kinematic node movement does not automatically stop at walls; choosing it requires actual sweep/response logic. Grounding needs valid support beneath the feet, upward normals, and correct takeoff/contact handling. Consume jump permission immediately. Visual root motion never moves the physical player.

Measure worst-case reachable jump including body extent and adversarial repeated/reversed air swipes. Make the gap wider with margin; prevent jumping via chute, tray, or decor. Test fast drops/dashes and beam rotation against tunneling. SceneKit CCD is documented for spherical shapes: a threshold on a box/capsule is not a fix. Use tested speeds, timestep, chunky colliders, and sweeps where necessary; keep real physical transfer.

## 4. Rendering, time, and blur

Initial stack: SwiftUI shell, SceneKit scene/physics, explicit SCNRenderer/Metal rendering as required. SceneKit deprecation is a conscious demo tradeoff. Verify real installed API signatures and compile a minimal pipeline before expanding. No speculative engine rewrite or custom engine project.

**One scene, one serial runtime owner, one monotonic simulation clock.** The platform frame driver implements the coordinator's ordering: drain immutable input → gameplay pre-step → advance physics once per simulation step → gameplay post-step/contact qualification → draw both regions from that completed state → publish value snapshots/events. Substeps, if used, are explicit and independent of number of views. Queue/reconcile contact callbacks on the same owner; no unsynchronized node mutation or arbitrary Sendable declarations. Gameplay/presentation have no separate simulation timers. SwiftUI recreation must not recreate the session.

The installed SCNRenderer separates `update(atTime:)` from `render(withViewport:commandBuffer:passDescriptor:)`; the latter does not step physics. Do not use an update-and-render overload twice. Show identical step/generation IDs in both views during diagnosis. Bound catch-up; pause drops elapsed wall time. Replay resets the world without moving the renderer's clock backward.

For connected perspective, define **one fixed virtual eye** and calibrated corners of the two display planes. Derive per-plane asymmetric projections from that eye, with correct handedness/depth conventions, clipping, drawable pixel scale, and safe bounds. Two centered cameras are not sufficient. Test grid/seam markers, equal-scale objects, an occluder, and a box crossing the boundary. Viewport alone may not prevent clears/overdraw from destroying the other view; prove color/depth ownership, or render to separate targets then composite. Handle zero/resized bounds and unsupported orientation clearly. No verified API supplies Device Hub's external orbit camera; rehearse one viewing pose and a measured fold range. This is a rendered illusion, not free-space pixels or arbitrary-view holography.

No app-added depth-of-field, motion blur, full-scene/material blur, or blurred transition. Preflight Settings showed one region blurred immediately after Book, then sharp at the same pose later. Duration/cause and continuous-fold behavior are unknown. No blur opt-out or callback was verified. Compare raw app/simulator captures with **whole Device Hub window** captures at the same pose: ordinary partial folding, held poses, and full close/open separately. Record real hinge values once app exists. Pausing does not disable system/host blur. Position-then-release avoids requiring precision during movement but must still pass readability testing. Persistent unreadability during normal meaningful folding is a core blocker; do not disguise it as a pass. A single-view fallback can preserve a useful physics prototype, but must be labeled a reduced result with the spatial requirement unmet.

## 5. Reset and interruption transaction

Retry/Replay increments generation; clears queued commands, gestures, stale contact callbacks, dwell, burst/jump/dash flags, timers, and effects; restores exactly one player and beam, parents/types/transforms/masks, velocities/angular velocities/forces, and mechanism pose from current hinge. Rebuilding the tiny level is acceptable if all callbacks are generation-guarded. Use framework physics-transform synchronization when needed; clearing forces does not clear velocity.

Pause whenever the scene becomes inactive/backgrounded, hinge input is explicitly unavailable, layout is unsupported/invalid, or rendering cannot safely proceed. Preserve the level, stop simulation advancement, invalidate in-flight input, and require explicit Resume after active/supported state returns. On Resume reconcile current hinge/layout and any potential overlapping geometry before restarting; rebase elapsed time without a large jump. Pause midair, mid-swipe, falling beam, settling, then fold while paused and resume. Do not infer blur state from lifecycle events.

## 6. Visual and audio delivery

Warm ivory platforms, dark ink recesses, teal machinery/scarf, copper structure, selective orange interactables. Use depth, occlusion, contact shadows, restrained impact feedback. One hint at a time: move, fold to align, release, cross. Keep the beam/supports/corgi clear of overlays and the fold's obscured region.

Required fallback corgi: recognizable orange/cream body, short legs, muzzle, upright ears, teal scarf; simple idle/walk/airborne/celebrate poses. A generic capsule alone is not the final mascot. The imported workshop/corgi kit is supplied in `DesignAssets/Runtime`, with editable sources and exchange files alongside it. Read `DesignAssets/INTEGRATION.md` and the validation record first. Native `.scn` files passed import; direct GLB loading by SceneKit is not the tested path. Test one mesh/material/animation first, at most 15 minutes of failed import attempts, then use styled primitives. Art attaches to agreed anchors without changing collision geometry. No root-motion translation.

Eight supplied CC0 runtime files in `Assets/Audio/`: `step_soft.wav`, `jump.wav`, `land_soft.wav`, `dash_down.wav`, `mechanism_release.wav`, `bridge_land.wav`, `success.wav`, `retry.wav`. All are 44.1 kHz mono 16-bit PCM. Preserve exact basenames; use `AudioManifest.md` for event mapping, modifications, sources, and licenses. Only the runtime WAVs go in the bundle; retain OGG originals/license/provenance and source models outside it. Preload; trigger from accepted game events, not touches or each camera draw. Deduplicate by event ID/generation; threshold/cooldown impacts and cadence footsteps; stop stale effects on reset. Missing audio is nonfatal. Check Device Hub output/mute: last observed **Sound 0, Output System**. Verify actual audibility and mix separately from successful file loading. No music dependency.

## 7. Parallel work that integrates into one app

Before dispatch, create one compiling native target, entry, minimal shared declarations, integration composition, harmless neutral A/B/C implementations, and source/test/resource membership. Timebox baseline to 15 minutes after path preflight. Do not build a framework. Record one baseline revision including the needed preparation (previously untracked); worktrees omit untracked files. Freeze concrete native type/member signatures, the named serial executor/actor and UI-to-frame queue, and the coordinate contract before workers start. Main-actor device callbacks enqueue immutable input; they do not mutate the renderer’s scene from another context.

| Owner | Exclusive paths and job |
| --- | --- |
| Coordinator | `FoldAndFetch/App/`, `Contracts/`, `Integration/`, `Resources/`, project/workspace/schemes/build configuration, integration records. Own dependency wiring, shared contracts, membership, Git integration, final builds, simulator UI, evidence, deadline/scope. Paths in this row are under `FoldAndFetch/` except project/configuration records. |
| A — platform/render | `FoldAndFetch/Platform/`, `FoldAndFetch/Rendering/`, `FoldAndFetchTests/Platform/`, `Handoffs/A.md`. Live hinge/layout/lifecycle, gesture routing/classification, single frame driver, cameras/targets/compositing, diagnostics. No gameplay policy or independent world. |
| B — gameplay | `FoldAndFetch/Gameplay/`, `FoldAndFetchTests/Gameplay/`, `Handoffs/B.md`. One scene/world, colliders, controller, hinge-to-mechanism transform, release/support/latch, states, reset/pause reconciliation. No display loop or independent timer. |
| C — presentation | `FoldAndFetch/Presentation/`, `AssetStaging/`, `FoldAndFetchTests/Presentation/`, `Handoffs/C.md`. Primitive corgi, visual factories/materials, HUD, event-driven audio, validated asset manifest. No game-state decisions, physical transform writers, collider replacement, or project edits. |

Coordinator alone edits shared project/configuration and copies approved runtime assets into the source Resources folder. In the built iOS bundle, flatten approved files or preserve subfolders beneath AssetContent; do not create a top-level bundle directory literally named Resources, which broke install in the isolated asset test. Use one assembled workshop or the modular pieces, never both overlapping. Bitrig’s isolated preview install failed while Xcode/Device Hub worked; keep the verified latter route available. Workers request new file membership explicitly. Prove one file from each folder compiles and one WAV is bundled; do not assume recursive imports or synchronized-folder behavior. Source docs/models/archives stay outside runtime targets.

Frozen interface semantics: DeviceFrame has monotonic timestamp, raw/calibrated radians, live/injected source, explicit availability, active/supported status, real region bounds, layout version. Commands have sequence/time and left/right/jump/dash/release/retry/replay/resume; mute belongs to presentation. B owns stable IDs for player/beam/chute/supports/tray/goal and exposes the same scene to A. C's visual factories are attached through integration on the serial owner. FrameInput and GameSnapshot carry step/generation, state, character status, support status, pause reason and diagnostics. GameEvents carry unique ID, generation, time, accepted action/contact/goal, optional intensity. C consumes/deduplicates them without altering physics. Reset coordinates all modules, including driver elapsed-time reference. No mutable scene objects cross concurrency boundaries unsafely.

If available, use three isolated worker worktrees from the exact baseline, separate derived build directories, coordinator's canonical checkout as integration. Otherwise use disjoint same-folder ownership and coordinator-only Git operations. Never share a Git index between independent writers. Coordinator exclusively owns the demo simulator through every interface, including UI, CLI and build/test tools. Workers may compile independently; simulator tests require coordinator scheduling or a separately allocated simulator. Separate build directories do not isolate simulator state. Only coordinator controls shared Bitrig UI; workers request scenarios and inspect returned evidence.

Give each worker the full contracts, exact owned paths, baseline, first small deliverable, deadline, and forbidden overlaps. First deliveries: A real-input/primitive-render slice; B movement/world/reset slice; C primitive corgi/HUD/silent feedback. Deliver compilable slices every **10–20 minutes**. Worker pauses edits and provides base/delivery revision, exact files, behavior, contract/resource requests, test evidence, known failures, and one integration smoke scenario. Coordinator reviews owned-path diffs, integrates **one immutable delivery at a time**, builds the combined app, runs the smoke scenario, then publishes the new integration revision. Workers refresh their own checkout only while paused. Contract changes get a short coordinated synchronization; never blind-resolve project conflicts. Separate module test success is not combined-app success.

## 8. Automatic milestones and cut lines

Use current time at each integration. If starting late, compress art; preserve final verification time. Report pass/fail/not-run with evidence, then proceed autonomously. A failed core gate gets a bounded repair; after two failed attempts or ten minutes without new evidence, change the hypothesis/implementation and state the blocker. No repeated blind fixes. Keep the last working revision/build.

| Pacific, September 26 | Outcome / decision |
| --- | --- |
| 11:30–11:38 | Tool/path preflight; choose one authoritative project/host. Stop fighting optional Bitrig synchronization after eight minutes. |
| 11:38–11:55 | Compiling scaffold/contracts/membership and primitive launch; dispatch real workers. |
| 11:55–12:20 | Integrated live hinge, actual mouse swipes, one clock, folded grid and perspective/readability proof. If optical continuity fails, prioritize it over asset expansion; ordinary camera views remain a diagnostic fallback only. |
| 12:20–12:50 | Full primitive loop: release, visible miss, Retry, stable bridge, manual cross, win, Replay. Demonstrate fold causality and gap necessity. |
| 12:50–13:40 | Styled corgi/workshop and sound; one validated asset batch at a time. No extra mechanics. |
| 13:40–14:15 | Acceptance sweep, unfamiliar-player observation if available; all workers switch to assigned defects. |
| 14:15 | Feature/art freeze. Only required fixes, readability, reliability and rehearsal thereafter. |
| 14:45–15:15 | Saved-revision rebuild/launch, resource/offline verification, whole-window backup recording and presentation rehearsal. |
| 15:15–15:30 | Retain ready-to-launch app, exact revision/evidence/demo steps/remaining limitations. Finish coding by 15:30. |

## 9. Required acceptance evidence

Record in one coordinator-owned verification report, linking logs/captures and exact revision. Evidence unavailable means **not run**, not pass. Do not spend the deadline building an elaborate test harness.

1. Native build and launch: actual developer directory/SDK, scheme, Duo destination, successful log, built app path, saved revision and dirty-tree accounting.
2. Real hinge: actual API values/source and continuous mechanism movement while manipulating simulator. Injected replay is separately labeled. Hold a static pose without false stale-input pause.
3. All four gestures using the actual Mac mouse in the folded preview. Buttons, diagonals/canceled touches, wall contact, ground-dash and air-jump rejection. Complete the sequence with one pointer.
4. Physical counterfactual: same checkpoint/environment, angle A visibly misses and angle B lands, repeat three each. Qualification uses actual support; no scripted snap. Fold again after release/landing and confirm beam independence.
5. Gap necessity: worst jump/air-spam/edge takeoff/dash/alternate-surface attempts cannot bypass it. Real beam carries the corgi; walk across flush aligned decks from rest without jumping or hitting clamps.
6. Negative support cases: one cradle, cradle+wall, brief two-support bounce, tipped beam, tray rest do not qualify; dwell resets. Show latch only after genuine stable seating, preserving beam identity/pose.
7. Reset during hold/fall/settle/cross/win at a nondefault live angle; exactly one beam/player, correct checkpoint versus Replay, no stale sound/contact/command.
8. Pause/resume during swipe/jump/drop, fold while paused, unavailable hinge, changed/zero bounds: no catch-up jump, invisible collision, or false victory.
9. Shared-clock/cadence: count updates separately from two renders; same step IDs; compare controlled inputs at 30/60 render cadence within measured physics tolerance. No doubled speed.
10. Projection/readability: seam/scale/occlusion/grid/outlined crossing-object tests at logged supported angles/virtual eye. Whole-window and raw captures; ordinary folding versus complete display switching separately. Report transient blur facts without an invented cure.
11. Resource/audio: inspect built bundle for eight WAVs, successful loads and actual audible event timing; collision chatter/mute/missing-file handling. No runtime dependency on source archives or internet.
12. Reliability: ten complete play/miss/retry/win/reset cycles, ten-minute frame-time/memory observation, target stable 60 fps on demo Mac. Report measurements, not the target as a result.
13. Fresh launch from saved combined build with required assets offline. Seek up to three unfamiliar players if present; record actual count/confusion and fix unclear cues. Their absence is not fabricated or a build blocker.

Automate meaningful pure gesture/state/reset invariants where useful; run actual simulator tests for API wiring, physics, presentation, blur and controls. Visual mockups and unit tests do not prove those pass.

Finish with one ready simulator build, saved revision, concise operating/replay steps, whole-window recording of real play, updated verification report, asset provenance, and explicit unmet requirements. Prioritize **meaningful fold, enjoyable control, readable physical consequence, memorable corgi, reliable replay**. Do not call the demo complete if live input, physical transfer, manual controls, connected presentation, or reset remains unproven.

## Primary references

- Event/rules: https://events.ycombinator.com/bitrig-hacks-september2026
- Apple simulator/preparation: https://developer.apple.com/videos/play/tech-talks/111461/
- Apple adaptive regions: https://developer.apple.com/videos/play/tech-talks/111463/
- Apple hinge input: https://developer.apple.com/videos/play/tech-talks/111464/
- Bitrig Duo support: https://bitrig.com/blog/bitrig-builds-iphone-duo-apps
- Rendering: https://developer.apple.com/documentation/scenekit/scnrenderer
- Projection: https://developer.apple.com/documentation/scenekit/scncamera/projectiontransform
- CCD limits: https://developer.apple.com/documentation/scenekit/scnphysicsbody/continuouscollisiondetectionthreshold
