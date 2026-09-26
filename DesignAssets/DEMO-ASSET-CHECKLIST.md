# Demo asset status and optional three-stage plan

September 25, 2026. Asset inventory and scope advice, not another execution prompt. [Master-Prompt.md](../Preparation/FoldAndFetch-Bitrig/Master-Prompt.md) remains the only build entry point.

## What the repository actually requires

[PRD §3](../Preparation/FoldAndFetch-Bitrig/PRD.md#3-scope-and-level-count) and Master §2 require **one polished, replayable bridge level** with three beats: meet Kaprao, fold/aim/release, cross/finish. These are three beats in one level, not three levels. The target is a convincing demo, not a full commercial app. The default four-hour build explicitly excludes a second level or puzzle. Three stages were suggested by the user for consideration; they are not yet the locked execution scope.

Keep the cozy cyberpunk rooftop setting: a warm miniature workshop against a night-city backdrop. Kaprao is fluffy and textured with RGB sunglasses; the world stays smooth and rounded. No new medieval environment is needed.

## Already generated

| Asset | Status / canonical location |
| --- | --- |
| Fluffy Kaprao + RGB glasses and scarf | Selected v3; [editable source, native runtime, GLB, textures, renders and evidence](Revisions/Kaprao-v3/README.md). Do not use the rejected root-level character or original full ZIP. |
| Character turnaround and four clips | Actual-model front/side/three-quarter renders; idle/look, walk in place, jump/fall and celebration. 11-joint smooth skin; root travel belongs to the controller. |
| Workshop world kit | [19 independent modules](Source/Workshop/README.md): two floors, two supports, chute, gate, beam, tray, optional practice curb, exit bell, goal toy, base, frame, rails, bench, planters, lamps, cables and skyline. Editable Blender, GLB/USD and native SCN are present, plus separate collision proxies. |
| World visuals | [Wide workshop view](Previews/Workshop/workshop-main.png), two close-ups, top/side/front layouts and three fold poses. These are design renders, not proof of a working fold puzzle. |
| Palette and materials | Named palette and material sheet; workshop constant PBR materials. Character source maps are 2048px; runtime maps are embedded at 1024px. No mandatory additional texture pack. |
| UI | [Gameplay, pause and completion](UI/README.md), transparent overlays, 14 icons, swipe hints, Release, Restart/Replay and sound controls. Editable local SVG/PNG designs are complete. |
| Audio | Eight supplied WAV effects and source/license records. Music is not required. |
| Handoff | Native import reports, character animation probes, Duo asset-viewer screenshots, scale/pivot notes, source and conversion tools. These prove asset compatibility, not complete gameplay. |

## Remaining for a polished one-level demo

- [ ] **Combined visual pass:** put current Kaprao v3 into the existing workshop for a hero composition and gameplay-distance review. Tune scale, warm lighting, glasses readability, fur visibility and the route's contrast together. Existing character and workshop renders were reviewed separately.
- [ ] **Refresh final presentation images that show the old character:** update any chosen HUD mockup, Figma concept or pitch image with v3. No new mandatory screen designs are needed.
- [ ] **Integration-driven asset fixes, only if exposed:** check paws on decks/beam, character collider versus the narrow bridge, camera framing, material cost and animation transitions. The first-pass rig has sampled foot penetration up to 8.4mm; close-up foot locking is not final. Do not change bridge or route dimensions without updating colliders and physical puzzle checks together.
- [ ] **Optional Figma completion:** compose native Controls/Screens pages. Foundations exist, but the earlier account quota stopped composition. Local SVG/PNG designs already supply the demo UI, so this is not a demo blocker.

**No required base world model remains ungenerated.** Most remaining work is assembly, visual polish and game implementation. Additional plants, signs or background clutter are optional, and should not obscure the fold mechanic.

## If we choose three short stages

Recommendation: retain one guaranteed complete level; make two variations stretch content. Reuse the same mechanics, character, animations, sounds and workshop kit. Avoid three separate environments or a new puzzle system.

| Proposed stage | Visual treatment | Puzzle variation |
| --- | --- | --- |
| 1 — Workshop | Existing warm repair rooftop | Broad visible catch channel; establish fold, release, miss/retry and manual crossing. |
| 2 — Rooftop garden | Rearrange existing planters, lamps, rails and bench | Shift the route/catch assembly in depth to change the useful fold angle. Move decks, supports, goal and character lane together; keep a continuous walkable lane. |
| 3 — Skyline terrace | More open skyline composition; restrained cyan accents and warm lamps | A modestly narrower catch channel or another calibrated depth offset. Keep generous feasible geometry and the same settle-then-release interaction; no timed folding while moving. |

Extra asset checklist for those two variations, **not generated yet**:

- [ ] Two assembled level scenes using existing modules, with separate editable sources and tested native exports.
- [ ] Two annotated top/side layout sets: start, route, gap, supports, chute/release, tray, hinge, goal and collider/anchor locations.
- [ ] Two three-pose fold storyboard sets showing intended hits and misses; authored angles must be calibrated against the real Duo input during implementation.
- [ ] Two simple dressing/lighting variants and a review render of each. New bespoke meshes are optional.
- [ ] Compact stage progress and a Next/Continue completion variant using the existing UI style. A full level-selection screen is unnecessary.
- [ ] Per-stage geometry and native resource checks; then real physics, crossing, miss/retry, reset and progression checks in the event app.

Do not commit to all three until stage 1 reliably demonstrates the real physical transfer and fold-connected presentation. Respect the master's 14:15 feature/art freeze. To adopt three required stages, update the existing Master, PRD and workshop checklist together rather than creating a competing prompt.

## Demo implementation still required

During the permitted event coding window: implement connected Duo projections and hinge calibration; real held-to-dynamic release, named-support contact and stability; a genuine miss/retry; manual Kaprao movement and physical crossing; native controls, reset/replay and audio; performance and posture tests. Bitrig's embedded preview previously failed installation; Xcode/Device Hub is the verified asset-viewing path. A working viewer or attractive screenshot alone is not the playable demo.
