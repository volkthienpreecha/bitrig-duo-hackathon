# Bitrig build instructions — current

Build and run the canonical `CorgiCrossroads.xcodeproj` in this repository. Follow `Master-Prompt.md` v2.1. Codex is integrating the source; do not run a competing rewrite or the obsolete v1.0 draft.

The game is **Corgi Crossroads**, portrait Duo: upper inner screen is a 2D tilt/marble-run board; lower inner screen shows corgi and street; after the cover settles at its target and Duo closes, the actual outside screen shows the physical cover drop and crossing.

**Required iPad input:** Provide an iPad Core Motion sender streaming timestamped x/y/z acceleration and processed gravity over local Wi-Fi to the Mac receiver. The simulator game consumes the receiver's live readings through its interchangeable motion provider. Use native Core Motion when the main game runs on a physical device. Include source/connection status, stale/disconnection pause and recovery, motion/local-network permissions, and exact receiver/sender run and installation instructions. The receiver and client live in `MotionBridge`; consult its README. Manual tilt is explicitly labeled diagnostic input, never claimed to be real accelerometer data.

Record and demonstrate the integrated app in Bitrig itself. Build, synthetic network checks, actual iPad streaming, hinge/outer continuation, collisions/landing, controls/reset and recorded audio are separate verification gates.

## Demo controls

Use Bitrig's Rotate Right control until the hinge runs horizontally and the game text is upright: puzzle above, road below. The native reserved division, rather than an assumed half-screen, determines the panel boundary. Use Fully Open while aiming if perspective makes the board hard to read, then close only after PLACEMENT HELD appears.

The antenna button opens motion setup. Connect the iPad relay or enable the explicitly labeled Manual tilt pad for diagnostics. Drag the pad to tilt, release to level, and counter-tilt to brake. Route: right past the first barrier, down, left past the second barrier, down, then right to the yellow target. Stay still for0.6seconds. Closing before parking shows an instruction to reopen and never releases a cover.

After the outside display appears, the held cover drops automatically once. Swipe or use the visible arrows to move left/right, jump, and dash down. Coverage is approximate and separate from the physical safety check. Retry rebuilds the puzzle and physical street. Reopen Duo for another aim.

Do not call the demo ready until the complete interactive sequence and final Bitrig recording pass the gates in Handoffs/Verification.md.
