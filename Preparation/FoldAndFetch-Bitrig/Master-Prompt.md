# Corgi Crossroads — executable master v2.1

Updated September 26, 12:17 PDT. Execution authorized by latest user: implement full revised tilt game, including live iPad motion input for Mac simulator testing. Validate each subsystem as it is integrated. No routine approval pauses. This replaces the drag rail/hinge aiming v2.0, preserved in Review/Master-v2.0-historical.md only for implementation reference.

## Experience

Portrait iPhone Duo. Inner upper panel is a 2D top-down marble-run board. A manhole cover starts upper-left. Tilt steers it around static barriers toward the target aligned with the missing cover in the street below. Momentum and collisions are real; the player must slow and hold within the target for a short dwell. Lower inner panel shows the waiting corgi and street at a fixed readable 3D angle. Use native reserved division/occlusion regions for layout.

When the disk reaches the target and is still, capture the actual position. Prompt the player to close Duo. Once ordinary scene continuation has reached a valid, active outside cover display, show the actual cover falling into the street opening. Start the drop only when outside is visible, not during the blurred transition. The latest close-to-drop request supersedes the old mandatory Pull Release. Preserve one session and an immutable placement through the transition. No simultaneous-display camera workaround. A repeat close cannot release twice.

Use the real board position to derive landing alignment, real gravity/contact physics for the street drop, and approximate coverage separately from safe support. No snap-to-hole, hidden floor, fabricated success or score-created collider. Once safe, the user crosses with the corgi. Keep Retry and simple movement/jump/dash controls. One polished puzzle first; add a second data variant only after the first complete flow passes. No new model generation or renaming: app name Corgi Crossroads, selected KapraoSprite handoff at scale 1.

## Motion input — required

Physical main app uses native Core Motion. Simulator uses timestamped readings streamed from a real iPad over local Wi-Fi through a Mac receiver. Provide a separate installable SwiftUI iPad sender, dependency-free Mac receiver, reusable main-app client, local-network/motion permission strings, connection/stale/disconnected states, and exact run/sign/install instructions. Native sender exposes actual accelerometer x/y/z including gravity and device-motion gravity separately. Use gravity for stable tilt; do not silently call raw acceleration gravity.

Use session IDs, monotonically increasing sequence values and timestamps, finite bounded samples, bounded request sizes, and receiver monotonic freshness. The receiver requires a pairing token; no internet service or third-party telemetry. Simulator polls the Mac on localhost. Sender uses Mac LAN IP and token. No pretending simulator controls are actual accelerometer data. An explicitly labeled manual tilt pad remains available as a diagnostic mode.

If readings stop, pause board physics and show connection state; never integrate stale acceleration indefinitely. Reconnection must recover without a physics time jump. Board retains position. Stop motion/network work on inactive lifecycle. Input is portrait, x right and y up after explicit mapping; calibrate neutral while steady and show source. Physical native motion, actual iPhone bridge, and synthetic protocol testing are separate evidence gates.

## Architecture and ownership

Canonical CorgiCrossroads.xcodeproj remains the Bitrig product. MainActor persistent game/session state survives view/layout changes. SpriteKit owns upper-board simulation; SceneKit owns the lower-world simulation. These are sequential gameplay phases, not competing simulations of a released cover: freeze upper placement before transfer; exactly one active clock per subsystem. Fixed camera replaces the old unnecessary dual asymmetric projection renderer. Keep normal native SwiftUI HUD and system layout/hinge APIs.

Coordinator owns canonical project, App, integration, resources, plan, Git and final Bitrig recording. The user-authorized Check Duo asset requirements task owns Experiments/TiltLab and temporarily leases shared simulator/Bitrig to prove its isolated board; it must return the lease before canonical testing. Platform worker owns MotionBridge and its client/sender/receiver/docs. Gameplay worker owns FoldAndFetch/TiltStreet and physical street continuation. Preserve old rail commits as historical; do not cherry-pick incompatible rail modules. Do not overwrite another owner's paths.

Existing C presentation can supply unchanged sprite/audio code after review, but rail HUD is obsolete. Recheck asset handoffs/hashes at each integration boundary; stage only complete immutable batches. Keep unrelated dirty design work. No bulk git add, publishing or submission. Old scheduled start remains paused.

## Execution and proof

1. Update this plan and repository instructions, freeze motion/board/street interfaces, preserve old worker commits. Provide Bitrig with the updated plan plus iPad motion requirement; never submit its stale v1.0 composer.
2. In parallel: prove top-board tilt/collision/stopping prototype; build sender/receiver/client with protocol and disconnect tests; build real street drop/support/crossing.
3. Integrate a vertical canonical game with source status/settings, upper puzzle, lower corgi, settled placement, outside detection, single release, retry/reopen. Build on simulator and physical SDK. Run actual Bitrig UI tests after returning simulator lease.
4. Test protocol auth/invalid/out-of-order/stale/session reconnect, board bounds/barriers/target dwell, lock preservation, drop miss/success/support, dog crossing, reset and disconnect/lifecycle. Record exact results; compile-only does not prove motion or gameplay.
5. Rehearse and save a whole-Bitrig demo capture, verify playback and audio separately. Target short 60–90 second story. Report unverified physical iPad sensor/installation if no device is connected; still ship complete install instructions and tested bridge software.

Submitted source window September 26 11:30–15:30 America/Los_Angeles; feature/art freeze 14:15, recording target 15:15. Check real clock. Cut optional second puzzle and decoration before compromising core testability. App display name only; preserve asset filenames. No guaranteed hackathon outcome or unverified ready claims.
