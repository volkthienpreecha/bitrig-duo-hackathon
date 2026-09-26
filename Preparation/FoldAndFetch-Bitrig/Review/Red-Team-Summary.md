# Fold & Fetch — adversarial review outcome

September 25, 2026. Three independent reviewers examined gameplay, rendering/physics/APIs, and multi-agent coordination, then reviewed the consolidated master again. Superpowers parallel-review, systematic-debugging and verification guidance informed the work. This is a design/preflight audit, not a passing application test.

## Verdict

The idea is buildable enough to attempt, but **the connected folded perspective and readability remain the decisive unproven dependency**. The strongest outcome is one intentionally small physical puzzle that looks distinct and replays reliably. Adding levels, tilt, tracking, accounts or a second machinery system reduces time available to prove it.

One prompt now carries the task from primitive test room to finished demo. It contains automatic evidence gates, exact agent ownership and contracts, integration every 10–20 minutes, a feature freeze, and fallback decisions. It cannot guarantee a one-pass model output or a hackathon win; it can make iteration happen inside one authorized run.

## High-impact failures caught and addressed in the prompt

| Failure | Required design/test correction |
| --- | --- |
| Folding about X cannot aim left/right along X | Beam spans X; folding aims its release depth Z into a visible receiver channel. Demonstrate three misses at one angle and three successes at another from the same checkpoint. |
| Two cameras do not create a coherent folded illusion | One virtual eye; calibrated planes and asymmetric projections; primitive seam/scale/occlusion tests before art. No claim of arbitrary-view holography. |
| Two render views can double physics or events | One serial runtime owner and clock; update once per step, render both from the same state, then publish events. |
| A released beam can inherit its moving parent | Preserve world pose and detach to the fixed root before enabling dynamics; no competing transform writer. |
| A “landed bridge” can actually be an impassable curb | Recess seats by beam thickness, align decks and fixed Z lane, keep clamps/rails out of the corridor; cross from rest without jumping. |
| One-mouse simulator cannot comfortably fold and swipe simultaneously | Park, fold, settle, release, observe, cross. No compulsory midair folding. |
| Swipes can bypass the bridge or restore jump on a wall | Bounded movement; real grounded test; measured worst reach, gap margin and alternate-path checks. |
| Brief/irrelevant collisions can falsely mark success | Named supports, valid load-bearing geometry and overlap, velocity/orientation bounds, continuous dwell; visible clamp only after genuine seating. |
| Physics drop/dash can tunnel through thin supports | Verify speeds, thickness and step policy; do not assume box/capsule CCD works. |
| Held hinge can be misclassified as stale; Release can stay disabled forever | Explicit availability, finite settling tolerance/window; no dependency on exact equality or another callback. |
| Miss/reset/pause can strand the player or retain old events | Bounded miss outcome, always-available Retry, generation-guarded reset, current hinge pose, explicit inactive/background pause, no clock catch-up. |
| Three agents can deliver three incompatible apps | One compiling scaffold/contracts baseline; disjoint module folders; coordinator-only project/resources/integration and all demo-simulator operations. |
| Worker tests can overwrite the running demo | Separate derived build folders are insufficient; coordinator schedules simulator tests or allocates a distinct simulator. |
| Bitrig prompt may imply nonexistent subagent capabilities | Codex coordinates real workers; Bitrig-only runs serial roles and discloses limitations. One active coordinator. |
| Missing models/audio can derail the demo | Recognizable primitive corgi mandatory; 15-minute failed-import cap; eight local WAVs, packaging evidence and separate output-volume check. |

These are mitigations specified in documents, not implemented fixes. Runtime acceptance remains pending.

## What was actually inspected

- The installed Xcode 27.1 SDK exposes the required hinge and explicit SceneKit update/render APIs. API availability is not proof of a working integration.
- Device Hub boots the Duo simulator. Settings was sharp when open; immediately after Book one region blurred, then became sharp in the same held pose. The observed effect was transient; duration, cause, continuous-fold behavior and custom game rendering are unmeasured. No blur opt-out was found or promised.
- Device Hub’s inspected Sound value was 0 and output System. No preference was changed. An eventual silent game must check the output route before blaming sound assets.
- Bitrig successfully opened and read the actual hackathon folder. It reports No Project File. Project creation/build, two-way edit refresh and app resource loading remain unverified.
- Eight licensed WAVs are present and their encoding/non-silent content was checked. No corgi/workshop runtime kit is present.

Full direct observations are in verified-preflight.md. No app code was created or executed; the coding window starts September 26 at 11:30 Pacific.

## What still decides success tomorrow

The first integrated primitive scene must prove live hinge, readable connected 3D, four usable swipes, physical miss/land/cross, and reset. If projection/ordinary-fold readability fails, art expansion stops while the core is repaired. A conventional-view physics prototype is useful but must be called a reduced result. After the full loop works, prioritize corgi readability, satisfying effects and repeated clean runs.

The Master-Prompt.md schedule is authoritative. Individual first-pass reports preserve their original proposed timings for audit context; do not combine those into competing deadlines.

## Second-pass findings

Rendering review found the need to explicitly pause on inactive/background scenes. Coordination review found host-routing ambiguity and simulator CLI/test ownership races. Gameplay review found deck-height/corridor geometry, bounded miss termination, and finite settling tolerance omissions. All were incorporated into the master and related requirements. Reviewers found no other P0/P1 issues in that pass; this is not a proof that no defects remain.
