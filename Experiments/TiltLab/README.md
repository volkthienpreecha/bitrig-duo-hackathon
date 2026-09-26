# TiltLab — top-board feasibility prototype

This isolated experiment implements the user's September 26 request to prove the tilt board before graphics or the outside-screen drop. It is not a competing app-build prompt. Canonical integration remains coordinator-owned through Preparation/FoldAndFetch-Bitrig/Master-Prompt.md.

## What runs

SwiftUI + SpriteKit, portrait 480×360 logical board: cover starts upper-left, two static barriers require a right/down/left/down/right route, and the target requires the cover center within 20 points at less than 8 points/sec for 0.6 continuous seconds. Motion changes gravity, not position. The cover has physical collision, damping and counter-tilt braking; there is no target magnet or success teleport. Hinge angle is observed independently. No graphics polish, corgi street, closing/drop transition or 3D landing is implemented here.

Sources/TiltLab.swift contains the entire isolated prototype. TiltBoard.diskPosition and target expose board coordinates. sampleOverride: (() -> CGVector?)? is the external motion seam: normalized gravity components, portrait +x right / +y up, nil means unavailable and freezes physics. Clamp upstream values to ±0.6. Canonical integration should replace TiltInput with the coordinated MotionBridge adapter, preserving source and freshness reporting. The separate MotionBridge worker owns networking; this experiment does not duplicate it.

## Inputs

- **Device motion:** CMMotionManager processed gravity, 60 Hz requested, sample freshness checked against local monotonic uptime. Calibrate subtracts the held neutral x/y gravity. Missing/stale samples freeze physics and invalidate the park dwell.
- **Manual tilt:** drag pad, or sustained X/Y sliders; Level returns gravity to zero while velocity decays naturally. Clearly labeled simulated input, never claimed as sensor readings.
- **Scripted test:** launch with `--tilt-smoke`. Initially pushes straight down into the first rail, checks it blocks the disk, then drives gravity with a feedback controller through five waypoints and the stationary target. No route teleport or position writer. Writes Documents/tilt-smoke.json. Do not include this test controller in the game.

## Actual evidence

- Native iOS 27.1 simulator build: PASS, `/tmp/TiltLab-build/Build/Products/Debug-iphonesimulator/TiltLab.app`.
- Standard Duo simulator 14D82C7C-A4A4-45E6-B3A1-DB7F304F8738: launch PASS; Device Hub UI displays the board.
- Core Motion availability observed in-app: **deviceMotion=false, accelerometer=false**. This is measured on this simulator, not inferred solely from older simulator documentation.
- Live hinge: observed 0° closed → 180° open, independently of motion input. Portrait achieved using Device Hub Rotate Right.
- Actual SpriteKit physics smoke PASS: direct-down blocked at y=268.7943; all five route waypoints reached; stationary target reached at (410.6827,55.1841), speed 5.5699 pt/s and dwell ≥0.6 s. See Evidence/tilt-smoke.json and .log. UI subsequently showed stationary (417,55), speed 0.
- Manual mouse/slider interaction: UI exists, but CUA interactions did not yield reliable state changes; **manual playthrough not verified**.
- Real iPhone motion, Wi-Fi bridge, stale disconnection during physical play, reset/lifecycle regression, outside-screen drop and Bitrig-owned build: **not yet verified**.
- Bitrig preview continued to show the canonical game while Device Hub showed TiltLab, so do not equate this standard simulator launch with a Bitrig build. Coordinator must explicitly test its target.

The final small safety edit explicitly clears parked when input becomes unavailable or lifecycle suspends; it compiled successfully. The physics smoke predates that safety-only edit, which does not change normal valid-input physics. A final interactive launch uses the new binary without scripted automation.

## Build

Use the installed Xcode developer directory per command; no global Xcode switch:

```sh
DEVELOPER_DIR=/Users/volkthienpreecha/Downloads/Xcode.app/Contents/Developer xcodebuild -project Experiments/TiltLab/TiltLab.xcodeproj -scheme TiltLab -configuration Debug -sdk iphonesimulator -derivedDataPath /tmp/TiltLab-build CODE_SIGNING_ALLOWED=NO build
```

Bundle ID: `com.corgicrossroads.tiltlab`. This project currently targets iOS 27.1 for the Duo region/hinge APIs. The phone motion sender is a separate project owned by MotionBridge and can support the user's ordinary iPhone OS.

## Real-phone connection

No physical phone was listed by devicectl at inspection. Connect and unlock an iPhone via USB for initial installation, accept Trust on the phone, and enable Developer Mode if requested by Xcode. The coordinator's sender project needs the user's signing team and device provisioning. Then keep phone and Mac on the same Wi-Fi, run the local receiver, enter its LAN address/token in the sender, and allow the requested local-network/motion access. The simulator consumes the receiver through localhost. Remote timestamps must not be compared directly to Mac uptime: freshness uses the receiver's local receipt age.

This transport is not built into Core Motion or magically provided by connecting a cable. Full setup and token/permission instructions belong to MotionBridge's handoff. A regular iPhone can supply gravity; Duo's simulator supplies hinge input separately.

References: [Apple CMMotionManager](https://developer.apple.com/documentation/coremotion/cmmotionmanager), [processed device motion](https://developer.apple.com/documentation/coremotion/getting-processed-device-motion-data).

Capture limitation: the two saved `inactive-display-*.png` CLI captures are black inactive-display outputs, **not visual success evidence**. The visible board/parked state was verified through Device Hub accessibility and its live CUA screenshots in this chat.
