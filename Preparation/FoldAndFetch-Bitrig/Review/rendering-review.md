# Fold & Fetch: rendering, physics, and API red-team review

> Historical review / September 25 observations. Current master v1.2, stage/v3 handoffs and the September 26 preparation-readiness report supersede old asset-availability, scope, path and draft-composer statements. This report is not fresh build or gameplay evidence.

September 25, 2026. Scope: the PRD and prototype prompt, inspected Apple documentation, and installed Xcode 27.1 SDK. No app code was written, compiled, or run. No UI was operated by this reviewer. Therefore API presence is verified; runtime feasibility is not.

## Decision

**The proposal is plausible, but not yet a demonstrated four-hour implementation. Its largest risk is the projection and simulator presentation, followed by an unspecified character controller and bridge qualification.** SceneKit deprecation is a known tradeoff, not the immediate blocker. The explicit update/render split exists in the installed SDK. An engine switch does not automatically solve display projection or simulator blur.

The first event milestone must demonstrate a sharp, continuous two-region primitive scene with real hinge input, one falling box, one simulation clock, and one reliable reset. A single conventional camera is useful diagnosis but cannot count as completion of the requested folded 3D scene.

Evidence labels below: **Verified** = SDK/API or primary-source fact; **Observed by root** = a supplied observation, not reproduced by this reviewer; **Risk** = a concrete failure hypothesis; **Unverified** = needs runtime evidence.

## Ranked findings

### P0 — Two ordinary cameras do not establish a continuous world across angled planes

**Verified:** SceneKit exposes a custom `SCNCamera.projectionTransform`. A custom matrix replaces the projection synthesized from camera properties; `zNear`, `zFar`, and `fieldOfView` no longer describe that custom projection. [Apple: projectionTransform](https://developer.apple.com/documentation/scenekit/scncamera/projectiontransform)

**Risk:** Giving the upper and lower regions independent centered perspective cameras, even with matching FOV, produces different centers of projection, mismatched scale, or a discontinuity when the beam crosses their boundary. Rotating the camera, world root, mechanism, and screen-plane model together can also apply hinge motion twice or cancel it entirely.

**Required design:** Declare one virtual eye in the fixed lower-world frame. Define a calibrated geometric model of both screen planes: hinge axis/pivot, plane corners, units-to-screen scale, and angle reference/sign. Derive each plane's asymmetric view/projection from that same eye and its plane corners. This is a mathematical rendering design, not an Apple-provided Duo projection API. Verify seam rays, scale, occlusion, handedness, clipping, and SceneKit/Metal depth convention with labeled primitives before art. The installed renderer defaults to reverse Z; do not paste an unrelated OpenGL matrix and assume compatibility.

**Limits:** The inspected hinge API supplies angle/status, not the Device Hub external camera. No API connecting that external viewing pose to the app was established. A single virtual eye can support a rehearsed viewing position; it cannot promise a perfect illusion from arbitrary simulator orbits. Reject or pause geometrically singular views where the eye is effectively on/behind a modeled screen plane.

**Fallback trigger:** If the primitive seam and moving-box test fails by approximately 12:10, stop asset integration and diagnose projection. A single view or two intentionally separate viewpoints is a scope reduction, not a passing version of the user's continuous-world requirement. Report that honestly instead of calling it a solved renderer.

### P0 — Simulator blur is an unresolved presentation dependency

**Observed by root:** Opening Settings on the tall inner display and choosing Book produced a frame with the upper half broadly blurred while the lower half remained crisp. A later screenshot at the same pose, with no intervening pose/input changes, was fully sharp. This establishes a transient effect in that test. Exact duration, cause, angle, and whether the raw simulator output shares the blur remain unknown. Continuous arbitrary-angle folding was not tested.

**Unverified:** Whether this is Device Hub visualization/postprocessing, an OS effect, or Settings' own adaptation. This evidence does not prove the effect occurs only during preset transitions, does not establish its behavior during continuous folding, and cannot certify the game's later custom renderer. The Book label is not a measured angle.

**Required protocol:** Capture both the whole Device Hub window and the raw simulator/app image at the same stable pose; record actual hinge values once event code exists. Repeat ordinary partial folding, a held pose, and full closing/opening separately. Include the previous good frame, immediate changed frame, and held-pose frames. A raw screenshot can exclude host rendering but cannot show its final presentation quality; a host screenshot alone cannot locate the cause. Settings is a control, not proof of the game's behavior.

**Required behavior:** No app-added depth-of-field, motion blur, full-screen blur, material blur, or blur transition. Pausing protects simulation state and does not disable postprocessing. No invented opt-out, blur callback, or guarantee that scene lifecycle captures all blur.

**Fallback trigger:** If ordinary supported folding keeps important game objects unreadable in the actual judge presentation, the live interaction fails acceptance even if raw app pixels are sharp. Try a verified alternate simulator viewing pose or presentation mode; narrower measured fold range only counts if folding remains meaningful. Position-then-release is an experiment, not an established blur cure.

### P1 — Hinge rotation may not move the beam toward the target as imagined

**Geometric fact:** If the supported pose puts the hinge axis parallel to the route's X axis, rotation about it changes Y and Z, not X. For a release point `p = H + Rx(theta) r`, its X coordinate stays constant. Folding cannot directly aim that chute left/right along the route.

**Recommended concrete level:** Keep the beam's long axis along X so it can span the X-separated supports. Make folding continuously change the release depth Z and elevation Y. Put a visible, forgiving depth channel across both supports; the player aligns the beam with that channel before release. Show enough depth perspective for misses in front/behind to be understandable. An alternative would require a visible mechanism converting rotation to X translation; do not add that complexity accidentally.

**Acceptance:** At least two distinct release configurations produce visibly distinct physical paths/outcomes. The success range emerges from geometry and support, never from an angle predicate. Keep the initial release point clear of its chute collider.

### P1 — The released beam must leave the moving upper hierarchy

**Risk:** A dynamic beam left under a hinge-transformed parent may inherit later folding and teleport, rotate twice, or move with the chute after landing. Parenting a simulated body under arbitrary scaled art can introduce a similar mismatch.

**Required contract:** Use one unscaled simulation root in meters; world X is route, Y is up, Z is depth; gravity remains world downward. The held beam follows the upper mechanism. At release, sample the current authoritative world pose, detach to the fixed simulation root preserving that pose, and activate its dynamic body once. Stop all nonphysics writers to its transform. Use current post-physics presentation state when inspecting simulated transforms, not stale model transform values. Read presentation nodes; do not mutate them. [Apple: presentation](https://developer.apple.com/documentation/scenekit/scnnode/presentation)

Specify release velocity deliberately. For the tiny prototype, require the mechanism to be settled and release with zero initial velocity; expose a brief settling cue if needed. Do not derive a throw from noisy callback-to-callback angle velocity. If moving-release momentum is later added, calculate and clamp it in the world frame and test it separately.

Moving upper colliders must use an intentional kinematic strategy. A rapid fold can sweep a collider through a dynamic body and inject large impulses. Keep the chute's swept volume away from the landing area and test fastest supported folds; do not simply teleport a static mesh collider every hinge callback.

### P1 — The simulation clock and renderer need one runtime owner, even with two work owners

**Verified:** Installed `SCNRenderer.h` declares `update(atTime:)` and `render(withViewport:commandBuffer:passDescriptor:)`. Its viewport-only method explicitly does not advance animations, physics, or particles. `render(atTime:viewport:commandBuffer:passDescriptor:)` does update and render. [Apple: SCNRenderer](https://developer.apple.com/documentation/scenekit/scnrenderer)

**Risks:** Two SCNViews, two independent drawable callbacks, or calling the update-and-render overload twice can double-step state. Audio/game logic in per-render callbacks can fire twice even if physics is correct. A first panel can show state N while the other shows N+1. Multiple owners mutating SCNNodes from SwiftUI callbacks and renderer callbacks can race.

**Required implementation contract:** One serial coordinator owns all scene mutation, time, and render submission. It consumes queued input; runs the physics owner's pre-step logic; calls SceneKit update; lets the physics owner evaluate post-step state; then renders both regions from that same completed step. Hinge values, projection values, mechanism transforms, and region layout must belong to one coherent frame snapshot. Panel render calls do not perform game actions. UI gets value snapshots/events, not permission to mutate nodes.

Choose and log the clock policy. A controlled accumulator with bounded catch-up is reasonable, but SceneKit stepping behavior must be observed at different rendering cadences. `sceneTime` alone is not a general physics rewind/reset control. Never feed a long wall-clock pause as one simulation delta. Never reset the update timestamp backwards on Replay; reset world state while maintaining a monotonic simulation time or reconstruct the coordinator intentionally. [Apple: timeStep](https://developer.apple.com/documentation/scenekit/scnphysicsworld/timestep), [Apple: sceneTime](https://developer.apple.com/documentation/scenekit/scnscenerenderer/scenetime)

Metal details must be tested: point-space region rectangles versus drawable pixels; consistent scale; zero-size resize; separate color/depth target ownership; second render clearing the first render's attachment; and out-of-region background/postprocess drawing. Viewport alone is not proof of safe compositing. Two region targets rendered sequentially and composited into the actual regions are an option if direct shared-target passes clobber one another. This remains one scene/world, not two simulations.

### P1 — A kinematic character is not automatically collision-constrained

**Verified:** SceneKit kinematic bodies are directly moved and affect dynamic bodies; forces and collisions do not stop the kinematic body itself. [Apple: SCNPhysicsBody](https://developer.apple.com/documentation/scenekit/scnphysicsbody)

**Risk:** Implementing left/right with a kinematic node action and assuming the physics engine will block walls violates the controls requirement. A dynamic body plus node actions can also make two systems fight for transform ownership.

**Recommended first choice:** A simple dynamic primitive controller, fixed to the route's depth lane with rotation constrained, controlled through bounded velocities/impulses rather than position actions. Art animates as a child and does not alter the collision body. If a kinematic controller is chosen instead, its owner must implement swept movement, collision response, support querying, and moving-surface handling explicitly; budget it as real controller work.

Ground support requires contacts/queries below the foot with an upward-facing normal, correct body-normal orientation, and sensible separation/relative vertical motion. A wall hit, side-of-beam contact, near-ground ray during takeoff, or contact from the previous frame must not restore jump. One jump consumes eligibility immediately; down-dash consumes its own once-per-airtime flag. Recheck after physics.

Horizontal swipes set or reverse a bounded burst; they must not add unbounded impulses. Cap air speed, burst duration, and relevant input accumulation. Measure maximum horizontal reach under repeated/reversed swipes, edge takeoff, jump spam, and down-dash at differing render cadences. Design the gap from those measurements plus margin.

### P1 — CCD is not a blanket solution for the beam or downward dash

**Verified:** Apple's `continuousCollisionDetectionThreshold` documentation states that continuous detection works only for spherical physics shapes. It defaults to disabled. A box beam or capsule cannot be assumed safe merely because a developer sets this property. [Apple: continuousCollisionDetectionThreshold](https://developer.apple.com/documentation/scenekit/scnphysicsbody/continuouscollisiondetectionthreshold)

**Required mitigation:** Use chunky visible supports and colliders; cap fall/dash speeds; select a verified timestep; use suitable swept tests if needed. Keep per-step travel comfortably below the smallest relevant support thickness as an initial engineering heuristic, then test. An angularly fast long beam also needs rotational stress testing. Never solve the box's tunneling by substituting a sphere collider that can no longer physically span the gap.

**Fallback:** Reduce drop height/dash speed, thicken supports, or increase the measured simulation rate within performance budget. Do not replace the physical drop with a landing animation.

### P1 — Stable bridge means two load-bearing supports, not two arbitrary contacts

**Risk:** One cradle plus a wall can produce two contacts; one long beam can briefly brush both cradles while flipping; an asleep beam may be asleep in the recovery tray. None proves a traversable bridge. Collision contacts default to no notifications unless masks are configured in the inspected SDK.

**Required qualification:** Test the intended left and right support identities, load-bearing contact direction/regions, beam orientation, endpoint overlap and continuous route surface, low linear/angular speed, and a minimum dwell measured in simulation time. Reset dwell when any predicate fails. Evaluate after physics. Keep qualification revocable if the beam later tips or leaves support; `bridgeReady` is not permission to ignore the current body. The corgi collides with/queries the actual beam shape, not an invisible gap-filling platform switched on by a flag.

**Crossing risk:** A dynamic corgi may knock the beam out of place. Solve with broad visible cradles, low restitution, stable mass/friction tuning, and small controller impulses. A visible latch after genuine seating is a possible later design choice, but must preserve pose and identity and should not be smuggled in as a teleport or hidden replacement floor.

### P1 — Reset and pause are physical operations, not only UI-state changes

**Verified:** `resetTransform()` synchronizes a changed static/dynamic body's physics pose to its model node; `clearAllForces()` does not mean velocity is zero. [Apple: resetTransform](https://developer.apple.com/documentation/scenekit/scnphysicsbody/resettransform()), installed `SCNPhysicsBody.h`.

**Required reset transaction:** On the serial owner, increment a run/generation ID, discard old commands/events/contact records, cancel held gestures and timers, remove/reload or fully restore the single beam and character, restore parents/types/transforms/masks, clear linear and angular velocities and forces, set appropriate resting state, reset support dwell and jump/dash/burst state, restore mechanism from current hinge input, and stop old effects. Verify exactly one beam and one character. Reconstructing the tiny level is acceptable if stale callbacks are generation-guarded.

On pause, stop simulation advancement and invalidate in-flight gestures; retain the level. On explicit Resume, use the current hinge/layout snapshot and rebase elapsed-time handling. If folding while paused would sweep machinery into the preserved beam, reconcile visibly and safely before resuming; do not resume with intersecting colliders. Treat that as a supported-range/layout decision, not an OS blur detector.

### P2 — Layout regions are not a calibrated physical screen model

**Verified:** UIKit's reserved-region frame is local to the queried view and includes interactive margins. Apple's fold division region is inactive at flat, with zero width; querying inactive regions is possible. System arrangement containers can reposition, hide, or overlay their two views. [Apple: adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/), installed `UIViewReservedRegion.h`.

**Required separation:** Use actual division/occlusion data and view bounds for placement, availability, and touch routing. Do not treat a margin-inflated reserved rectangle as a measured hinge gap or take half the app bounds as a physical calibration. Do not let ArrangementView silently collapse the second camera when the aspect ratio changes. Restrict the initial gameplay to one verified pose/region orientation and pause clearly for unsupported layouts; do not rely on an orientation lock to prevent inner-display changes. [Apple: prepare your app](https://developer.apple.com/videos/play/tech-talks/111461/)

Map upper Release hit testing through its own current region and camera, not whichever point of view the shared renderer last used. A conventional 2D button anchored to the visible upper target avoids an unnecessary 3D-picking dependency. Controls stay outside active reserved areas. Keep gameplay target geometry readable near the fold, whose curved region may inherently obscure it.

### P2 — Hinge callbacks are not a metronome or a velocity sensor

**Verified:** `UIHinge.angle` is radians. Apple states update rate and precision are system policy. `UIHingeInteraction` delivers nil after leaving a supporting hierarchy; disabled interactions do not queue lost changes, and reenable receives current state if available. SwiftUI provides `onHingeChange` and a nullable `DeviceHingeContext.hinge`. [Apple: hinge interaction talk](https://developer.apple.com/videos/play/tech-talks/111464/), installed `UIHinge.h`, `UIHingeInteraction.h`, and SwiftUICore interface.

**Required adapter:** Timestamp arrival with a monotonic app clock; retain latest angle/status/source and availability; calibrate sign and flat reference from real simulator observation rather than assumed numeric endpoints. Use one documented smoothing/slew policy for the mechanism and corresponding visual model. Do not integrate gravity from hinge callbacks. Do not call unchanged data stale solely because no callback arrives while the device is held still. Debug injection remains conspicuously labeled and cannot pass live integration.

## Safe event test protocol and gates

1. **11:30–11:45: build/API gate.** Create submission code only after start. Record Xcode build, deployment target, simulator runtime, actual hinge callback/status/radians, actual region bounds, and available drawable dimensions. Verify callbacks from real folds, not only injection. Primitive geometry only.
2. **11:45–12:10: presentation gate.** Grid, numbered seam markers, outlined box straddling the fold, foreground occluder, one virtual eye. Hold several logged partial angles and sweep slowly/quickly. Compare raw output with whole-window capture; inspect blur, scale, seam, clipping, and camera flips. Count simulation updates separately from render submissions. A falling box must take the same time with one or two region renders.
3. **12:10–12:30: physical loop gate.** Release from several angles; miss and recover; land on one support only; settle correctly on both; fold while beam is falling/landed; reset during each state. Display beam ID, run ID, support IDs, dwell, speed, grounded state, and simulation time in diagnostics.
4. **Controller gate before art.** All four swipes; diagonals/cancellations; button arbitration; wall hit; jump near ledge; airborne dash; spam and reversals; maximum-gap attempt; crossing with the beam still dynamic. Repeat at 30/60 rendering cadence and with a deliberate interruption. Physics tolerance is acceptable; bypasses or tunnel-through are not.
5. **Interruption gate.** Pause midair, during a swipe, while the beam falls, and during settling. Change fold while paused. Resume explicitly without a large time jump, stale input, phantom contact, or overlapping geometry. Test changed/zero bounds.
6. **Reliability gate.** Ten complete play/miss/retry/win/reset cycles and a short repeated render/performance run. Record actual result and revision. If the physical primitive demo is not reliable around 12:30, drop cosmetic complexity and extra systems before weakening the mechanics.

These are proposed stop/go times for a four-hour build, not organizer requirements. The exact hour may move, but unresolved P0/P1 issues must stay ahead of art and optional work.

## Parallel ownership boundary for the unified master prompt

| Owner | Owns | Must not own |
| --- | --- | --- |
| Coordinator/integrator | Shared types, serial execution policy, persistent session lifetime, Xcode project/build configuration, command queue, master update/render order, merge/build gates | Concurrent unscheduled changes to either owner's scene nodes |
| Device/render owner | Hinge and region adapter; availability/layout snapshots; virtual-eye and screen-plane calibration; cameras/projections; Metal targets/compositing; gesture surface routing; diagnostics for render/input; raw versus host capture evidence | Beam/corgi transforms, velocities, contacts, support predicates, state transitions, duplicate physics clock |
| Physics/gameplay owner | Level graph/collision root; hinge-to-mechanism transform function in agreed coordinates; beam lifecycle; controller; colliders/masks; support checks; reset and pause reconciliation; gameplay events | Drawable loop, camera transforms, screen layout, direct UIKit/SwiftUI mutation, independent timers for gameplay |

Both owners can work against injected value snapshots initially, but only the real adapter's event build passes T02. The renderer and physics portions are not independently mergeable until the coordinate convention and shared data contract are fixed.

Minimal agreed contract before parallel work: `FrameInput` equivalent with generation, simulation time, current hinge radians/status/source/availability, accepted layout version and commands; `GameSnapshot` equivalent with authoritative state and diagnostic values; immutable `RenderLayout` equivalent with region rectangles and calibrated plane/camera description; named `GameEvent` values for audio/UI. These are requirements for later implementation, not pre-event source files. Avoid scattering SceneKit objects across actors or treating them as freely sendable data.

One runtime coordinator executes: accept input → physics pre-step → SceneKit update → physics post-step/contact qualification → both camera renders → publish UI/events. Mutations from asynchronous contact callbacks are queued or reconciled within the same serial policy. Specify how callbacks are drained and guard them by generation.

## Exact requirements to add to the master prompt

- Prove the real SDK hinge callback and region layout in the event-created app; report actual radians, status, source, bounds, build, and runtime. API presence alone is not a run result.
- Freeze one lower-world coordinate frame and supported pose. Publish hinge axis/pivot, angle offset/sign, world scale, and the X/Y/Z meaning before parallel implementation.
- Use an X-length beam over an X route gap; folding aligns release depth Z through a visible catch channel unless another mechanically valid mapping is explicitly chosen.
- Implement one scene, one serial mutation owner, one monotonic simulation clock, update once per simulation step, and two render-only region submissions from the same completed state.
- Use one declared virtual eye and per-plane projections; prove seam/scale/occlusion with primitive tests. Do not count arbitrary two-camera views or a stretched screenshot as this requirement.
- Do not infer optical plane dimensions from reserved-region margins. Handle inactive division regions, changing layouts, drawable scale, clipping, and zero bounds.
- Detach the released beam to the fixed simulation root preserving its actual world pose; make it dynamic once and remove competing transform writers. Use a settled zero-velocity release initially.
- Implement collision-constrained movement deliberately. A kinematic body moved by a node action is insufficient. Bound horizontal bursts/air control; consume jump/dash eligibility immediately; measure maximum gap reach.
- Do not claim a box/capsule is protected by SceneKit CCD. Verify thick supports, bounded speeds, timestep, and any sweeps against tunneling and rapid folding.
- Qualify the bridge through both intended supports, stable pose and velocity over simulation time, and a real traversable surface. The character uses the actual landed beam, and support loss invalidates readiness.
- Reset physical bodies, hierarchy, velocities, forces, contacts, run IDs, timers, controls, and effects atomically. Pause/resume uses current hinge/layout and bounded elapsed time.
- Keep app imagery sharp and test raw simulator output against whole Device Hub captures. Report uncertain blur causes; never invent a disable API or claim pause fixes blur.
- Do not integrate polished art until the primitive rendering/physics/gesture loop passes. Treat failure of connected folded rendering or ordinary-fold readability as a reported scope blocker, not silent success.

## Source and inspection record

Installed Xcode version file reports 27.1, product build 27A9269. Inspected SDK root:

`/Users/volkthienpreecha/Downloads/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks/`

Inspected primary SDK files: UIKit `UIHinge.h`, `UIHingeInteraction.h`, `UIViewReservedRegion.h`, `UIView.h`; SwiftUICore `Modules/SwiftUICore.swiftmodule/arm64-apple-ios-simulator.swiftinterface`; SceneKit `SCNRenderer.h`, `SCNSceneRenderer.h`, `SCNCamera.h`, `SCNPhysicsWorld.h`, `SCNPhysicsBody.h`, `SCNNode.h`.

SceneKit's deprecated status is explicitly documented by [Apple's SceneKit overview](https://developer.apple.com/documentation/scenekit/). The API choice remains reasonable only if the event build proves the specific pipeline. RealityKit was not runtime-tested here and is not a guaranteed fallback. No private simulator controls, external-camera API, or blur opt-out was verified.
