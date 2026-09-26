# Fold & Fetch — gameplay red-team review

> Historical review / September 25 observations. Current master v1.2, stage/v3 handoffs and the September 26 preparation-readiness report supersede old asset-availability, scope, path and draft-composer statements. This report is not fresh build or gameplay evidence.

Prepared September 25, 2026. This is a design review only; no submitted app code was created or changed. Reviewed `PRD.md`, `Workshop-Kit-Checklist.md`, `Bitrig-Prototype-Prompt.md`, `Bitrig-Demo-Prompt.md`, and the asset inventory.

## Verdict

The idea can support a strong short demonstration. The current brief still permits an implementation that has four recognized gestures, a falling beam, and attractive screenshots, yet is frustrating to operate and does not show why folding matters. The highest priority is a repeatable causal sequence: the player parks the corgi, changes the upper geometry with a real simulator fold, releases the same beam, sees why it lands or misses, then manually crosses it.

Lock one level and one physical transfer. All four user-selected swipe controls stay. Make jump and downward dash optional play on a safe platform; do not make a timed jump a prerequisite to seeing the fold mechanic. Do not replace movement with autoplay.

The official event asks for creative, thoughtful use of Duo APIs that enables a meaningfully new or more compelling experience, accepts a polished demo, and may put top entries on a live stage. It does not publish numerical scoring weights or a demo duration. These are reasons to prioritize visible fold causality and live reliability, not evidence that this concept will win. [Official event page](https://events.ycombinator.com/bitrig-hacks-september2026)

## Ranked findings

| Rank | Severity | Concrete failure | Required correction |
| --- | --- | --- | --- |
| 1 | P0 | One mouse must drag the simulator fold, drag the corgi controls, and click a foreshortened release target. A puzzle that requires simultaneous folding and steering is practically unplayable on the demo machine. | Author the sequence as park → set fold while beam is held → release → watch → cross. No simultaneous controls, time limit, or midair fold correction. Test the actual Mac input route. |
| 2 | P0 | The beam lands at nearly every angle because the cradles are broad, or success is secretly an angle threshold. Folding then looks like a decorative trigger for a bridge animation. | Prove one reset-matched live angle misses and another succeeds, changing only hinge pose. Show the held beam/chute moving continuously between them. Keep success geometry forgiving locally but not invariant across the whole supported fold range. |
| 3 | P0 | Air swipes restart horizontal bursts without a total displacement limit; jump buffering or grounded-contact bugs replenish flight. The corgi bypasses the bridge. | Bound horizontal speed and airborne displacement; swipes cannot restart airtime, gravity, vertical velocity, or air-control allowance. Test maximum reach with input spam. Include collider extents and a safety margin when sizing the gap. |
| 4 | P0 | A beam touches one support for one frame, turns green, then tips away; a crossing corgi knocks a valid beam loose; a downward dash tunnels through it. | Require both supports, continuous low-motion dwell, and usable top-face orientation. After valid settlement, visible clamps may lock that same beam in place. Use conservative movement collision sweeps and capped dash speed. Never spawn a replacement invisible bridge. |
| 5 | P0 | The character is a capsule until the final hour because the expected corgi model never arrives or its rig, materials, axes, and clips fail to import. | The inventory contains no corgi or workshop runtime model. Make a recognizable primitive corgi the guaranteed deliverable, with body, muzzle, four short legs, upright ears, orange/cream blocks, and teal scarf. Imported art gets one short import budget and is optional polish. |
| 6 | P1 | A horizontal swipe lasts 0.35 seconds; a novice must finish an up-swipe before it expires to jump a compulsory curb. On a mouse, the tutorial becomes a timing test unrelated to folding. | Remove the compulsory curb. Put the jump/dash hint on a wide safe start pad. Let users demonstrate up then down without lateral steering. Tune burst duration only after actual mouse trials. The user selected directions, not the provisional 0.35-second timing. |
| 7 | P1 | A missed beam rolls forever in the tray, or retry sends the corgi back through the entire tutorial. Conversely, an invisible offscreen fall traps the player. | Bound the landing attempt with a timeout and a visible recovery tray. A single Retry returns the loaded beam and corgi to the pre-gap checkpoint. Replay returns to the start. Keep Retry and Replay semantically distinct even if they share reset internals. |
| 8 | P1 | Reset restores a nominal 90-degree mechanism while the real simulator is still folded differently. The next hinge event snaps the chute and appears to teleport the beam. | Reset gameplay state while preserving the current live hinge pose. Reload the beam into the chute at that pose. Clear gesture, physics, sound, and delayed callback state; do not claim to reset the external simulator control. |
| 9 | P1 | The bridge lands but the viewer thinks that is the win; “Fetch” contains nothing to fetch; the corgi crosses without an obvious destination. | Put a simple toy at the far goal, visible from the start. Say “Bring the corgi to the toy” or equally concrete wording. Win only when the corgi reaches the goal after bridge readiness. The toy can be a primitive ball; no second journey or inventory. |
| 10 | P1 | One successful drop takes ten seconds, so developers add walking distance, repeated swipes, or an extra lift to reach the 60–90-second target. | Treat 60–90 seconds as a presenter’s budget, not mandatory game length. Keep an unassisted success short. Use the available presentation time to show one understandable miss, correction, physical landing, and manually controlled crossing. |
| 11 | P1 | The fixed camera makes the bridge seem aligned even though its collision path is elsewhere; changing simulator orbit destroys the illusion or hides the release hit target. | Author all critical controls and movement in the supported view; validate camera/viewing pose before art. Keep character travel in one explicit X–Y plane. Render collision proxies in diagnostics to prove the visible bridge and path coincide. Do not imply arbitrary-view optical fidelity. |
| 12 | P1 | The 19-row acceptance matrix becomes a checklist somebody marks “tested” after a single happy-path video. Parallel agents each believe another owns the actual simulator checks. | Assign one integration owner, one evidence record, and concrete release-blocking tests below. Record actual outcomes and unresolved failures. A simulator pass cannot be inferred from a unit test or injected angle. |

P0 means the intended live demo is invalid or unreliable until resolved. P1 means substantial learnability, clarity, or schedule risk. These are engineering priorities, not organizer judging scores.

## Additional failure paths worth testing

- **Underside shortcut:** the recovery tray becomes a walkable lower route and the corgi jumps out near the goal. Keep it outside the character route, with visible containment. A lower recovery volume should respawn the corgi, not create a second route.
- **Edge forgiveness becomes free flight:** coyote-time logic refreshes every frame while touching a wall, beam side, or sloped rail. Grounding must require valid support below the character, not any contact.
- **Gesture starvation:** the proposed 0.08–0.6-second duration window rejects a very fast drag or a careful slow drag. The 28-point threshold is measured in app points, not screen-capture pixels. Start generously, test real input, and record recognition failure instead of assuming these constants are correct.
- **Fold changes gesture coordinates:** a drag begins in one layout and ends after its region has resized. A coordinate jump is misread as movement. Cancel an active touch when its region mapping/topology changes; do not classify movement from a remapped coordinate system.
- **Release cannot be hit:** a tiny upper 3D button becomes narrow at the chosen fold. Keep a clearly associated, large hit area whose accessibility survives the supported range. A decorative release mesh alone is not an adequate hit target.
- **Multiple releases:** double click or a repeated command spawns two beams. The loaded-to-released transition must be atomic and idempotent.
- **Stale reset events:** an old settlement callback announces success after Retry, or an old respawn moves the newly restarted corgi. Invalidate pending work with the reset generation/session identity.
- **Fold after release:** moving upper kinematic colliders through the free beam injects excessive impulses. Choose a geometry in which the released beam has cleared the mechanism; test live post-release folding. Do not silently freeze the real hinge-driven geometry to conceal this.
- **Beam–character collisions:** the dog can stand under the drop, be launched, or accidentally catch the beam. Place the safe waiting platform outside the fall corridor. Restrict game collision interactions deliberately and visibly; the puzzle does not need injury simulation.
- **Goal event spam:** character overlap emits victory on every frame, or the beam reaches the goal trigger. Filter by character identity and require one active-to-won transition.

## Locked scope and cut lines

Required: one workshop, one authored character route, a corgi recognizable at demo scale, four swipe commands, live hinge input, one held/released physical beam, one miss/retry path, one supported bridge, one visible goal, one celebration, Replay, offline resources, and a repeatable demo pose.

The corgi moves in a 2.5D lane inside the 3D scene. Depth movement, camera orbit controls, extra levels, a lift/counterweight, tilt, consumables, accounts, network services, a level selector, and a return trip with the toy are excluded from the four-hour build. RevenueCat is a separate optional prize branch only if selected by the user; it must not delay the required loop.

Imported rigs, custom fonts, skeletal animation, fancy materials, particles, complex shadows, and all eight sounds are lower priority than the playable loop. Keep a primitive corgi and simple transform animations available even if a supplied asset imports. A static external asset with broken animation is not an excuse to miss the corgi deliverable.

Suggested schedule gates, in San Francisco time on September 26:

| Gate | Evidence required | Cut if missing |
| --- | --- | --- |
| 12:00 | Native launch, live hinge evidence, one mouse swipe accepted, readable supported view | No art integration yet. Reduce presentation complexity immediately; unresolved live hinge is a core feasibility blocker, not permission to substitute a hidden slider. |
| 12:45 | Complete primitive route: miss → retry → successful support → manual crossing → win → replay | Drop mandatory tutorial obstacle, air steering complexity, advanced effects, and imported animation work. Keep all four commands. |
| 1:30 | The core loop survives repeated input, early release attempts, and post-reset play | Freeze mechanics and geometry except fixes. No second puzzle under any “stretch” interpretation. |
| 2:00 | Recognizable corgi; readable single workshop; first unfamiliar player can operate the mouse controls | End all external asset conversion attempts. Use primitives/simple local materials for any missing asset. |
| 2:15 | Integrated build with pass/fail evidence and a selected presentation pose | Freeze feature scope. Spend the remaining time on demonstrated failures, rebuild, rehearsal, and an actual-play backup recording. |

Allow at most about 15 minutes for a candidate corgi runtime import, including orientation, scale, textures, and one animation. This is a recommended schedule budget, not a measured tool limit. Do not begin a custom modeling or retargeting pipeline during the event. Assets and documents can be prepared before the event; submitted app code must start within the permitted window.

## Release-blocking acceptance checks

These complement the rendering agent’s tests. They replace vague gameplay “works” claims with observable evidence.

| ID | Procedure | Pass condition |
| --- | --- | --- |
| G1 — Mouse control | In the chosen simulator pose, perform five deliberate mouse drags in each direction. Attempt upper-release and reset clicks; cancel one drag; change layout mid-drag. | All intended legal commands are recognized once. Up when airborne and down when grounded are rejected. Button clicks never move the corgi. Canceled/remapped drags never execute later. Record any failed recognition and retune before acceptance. |
| G2 — Sequential operation | One person with one mouse walks to the safe pad, sets a fold, releases, and crosses. | No simultaneous fold/character input, developer command, debug slider, or precision-timed gesture chain is required. |
| G3 — Fold counterfactual | Reset the same physical level. Release at live pose A, then reset and release at live pose B. Repeat each at least three times. Record actual hinge values. | A visibly misses; B visibly lands. The same beam is simulated each time. Only the fold changes between attempts. Success comes from physical support, not an angle comparison. If outcomes are unstable, fix capture geometry before widening the target until every angle works. |
| G4 — Bridge necessity | From the closest legal edge, try maximum-speed repeated horizontal swipes, repeated up-swipes, up/right alternation, dash near the far side, wall contacts, and a fall toward the tray. | No route reaches the goal without the bridge. Report the maximum observed reach. Gap clearance includes the character’s extent and a safety margin, not only center-to-center distance. |
| G5 — Support correctness | Land the beam on one support, briefly touch both while bouncing, land at a steep angle, and then land stably on both. Traverse and down-dash onto a valid bridge. | Only sustained, usable dual support becomes ready. The valid bridge remains traversable; no floor tunneling, invisible replacement collider, or character-induced collapse. Visible post-settlement clamps are permitted. |
| G6 — Recovery/reset | Retry while the beam is falling, settling, and missed; replay after victory. Repeat while the simulator remains at a non-default hinge angle. | One corgi and one beam exist; no stale sound/win/respawn callbacks fire. Retry restores the pre-gap checkpoint. Replay restores the start. The mechanism matches the current real hinge pose. |
| G7 — Pause | Interrupt during a swipe and during a falling beam; return at a changed fold pose and explicitly resume. | No catch-up explosion, queued movement, duplicate release, or false win. Rendering and collision geometry agree after resume. |
| G8 — Reliability | Run ten complete mixed miss/retry/success/replay cycles on the demo Mac, including audio muted for at least one. | Zero crash, stuck state, duplicate beam, input lock, or incorrect win. Keep an honest record of failures and rerun the affected check after fixes. |
| G9 — Cold player | Give three unfamiliar people the mouse, the app’s own hints, and one sentence stating the objective. Do not explain the solution. | Each can identify the goal, move intentionally, find Release/Retry, and describe what to change after a miss. Record time to first meaningful fold and time to success; do not claim the 60–90-second target was met without timing it. |
| G10 — Saved demo | Quit and reopen the saved build, start offline, restore the rehearsed simulator pose, then complete the live sequence. | Demo works without development-only state, remote files, or a previous successful session. A backup video shows actual interaction and is described honestly as a recording. |

Recommended stable-support starting criteria: both receiver regions are supported continuously for roughly 0.4 seconds, bridge top-face alignment is within a tuned usable tolerance, and linear/angular speeds are low relative to level scale. The implementer must state the final numbers and demonstrate the negative cases. These starting criteria are not a physics guarantee.

## Exact additions for the master implementation prompt

> Preserve the user’s controls: left/right swipes move the corgi, up jumps when grounded, and down dashes downward once per airtime. Keep the corgi player-controlled. Use a short bounded horizontal burst as an initial implementation choice, then tune with mouse-drag tests; the proposed one-body-length/0.35-second values are not fixed user requirements. Keep all movement in an authored X–Y lane with Z fixed. Do not require a timed horizontal-swipe-plus-jump combination to reach the fold puzzle.

> Build one complete level with this sequence: optional safe movement/jump/dash practice, a safe waiting area beside an uncrossable gap, fold adjustment while the beam is held, deliberate release, a visible physical miss or dual-support landing, manual crossing, and reaching a clearly visible toy/goal. A successful bridge landing unlocks crossing; reaching the goal triggers the celebration. Do not add another puzzle, route, return journey, or mandatory tutorial obstacle.

> Author the entire required loop for one mouse. Folding, release, and movement must work sequentially. Use generous release/reset hit areas that stay usable in the supported folded view. Validate app-point gesture coordinates in that view. A button tap, canceled touch, or gesture whose region mapping changes must never produce a movement command. Do not enforce the initial gesture timing thresholds without actual mouse trials.

> Make folding demonstrably causal. Live hinge input must continuously change upper mechanism geometry. From identical reset state, one live fold pose must visibly miss and another must reliably land. Keep success determined by the simulated beam’s sustained support on both receivers and usable orientation; never compare hinge angle to a success threshold. A visible clamp may lock the same beam after valid settlement so crossing is reliable. No invisible replacement bridge or prerecorded success trajectory.

> Bound character speed, flight time, and air-control displacement. Air swipes cannot replenish jump time, upward velocity, or movement allowance. A side contact is not ground. Measure and adversarially test the largest reachable gap, including repeated gestures, dash, edge forgiveness, and character bounds, before fixing level dimensions. Keep the recovery tray from becoming a lower bypass route. Prevent downward-dash tunneling with an appropriately bounded/swept controller.

> Implement separate Retry and Replay outcomes. Retry restores the beam and corgi to the pre-gap checkpoint; Replay returns to the start. Both clear physical velocities, contacts, transient commands, pending callbacks, settlement dwell, timers, and sound events. Preserve the actual current hinge pose while resetting gameplay. Release must be accepted only once per loaded beam. Victory must be accepted only once for the corgi reaching the goal after the bridge is ready.

> The repository currently has eight audio assets but no runtime corgi/workshop model. A recognizable primitive corgi is the guaranteed art fallback, not an unresolved dependency. Keep its visual model separate from its simple gameplay collider. Imported art has a short capped attempt budget; fall back immediately if import, scale, orientation, materials, or one animation cannot be verified. Simple leg motion, jump pose, and celebration transforms are sufficient. No custom rigging pipeline during the event.

> The 60–90-second figure is a presentation target, not an organizer rule or required game length. Do not pad it with swipes or additional content. Rehearse a short introduction, visible fold adjustment, release, landing, manual crossing, and replay. A single intentional miss can demonstrate causality if reliable, but a live miss is not mandatory in every presentation.

> One gameplay owner controls commands, character state, physical beam state, support detection, goal state, and reset. Renderers consume the same authoritative simulation and must not independently advance it. Art/audio agents consume named events and must not invent success/reset behavior. Agree interfaces before parallel edits, keep file ownership exclusive, and have one integration owner run G1–G10 on the real simulator. Report pass/fail evidence; do not label an injected-input test as live hinge verification.

## What this review does not establish

No prototype exists in this handoff, so physics stability, gesture feel, fold causality, asset import, simulator frame rate, and timing are unverified. The review proposes testable design constraints; it is not evidence that any of them already pass. The fixed-camera visual illusion and API/runtime feasibility remain the rendering/platform reviewer’s responsibility and can independently block this concept.
