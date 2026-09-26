# Motion bridge delivery

Status: **DONE_WITH_CONCERNS** — implementation and automated loopback/native compilation pass. Physical iPhone installation, permission prompts and real Wi-Fi sensor transport still require the user's device.

Scope: only `MotionBridge/**` and this handoff. The earlier A renderer commit remains preserved and is **not part of this requested integration**. No simulator/Bitrig control, main project edits or `Experiments/TiltLab` edits occurred.

## Integrate

Cherry-pick only the new motion-bridge commit reported in the coordinator message. Add both of these source files to the canonical main app target:

- `MotionBridge/Client/MotionInputClient.swift`
- `MotionBridge/Client/MotionTypes.swift`

`@MainActor MotionInputClient: ObservableObject` has `start(host: String = "127.0.0.1", token: String = "")`, `stop()`, published `sample: MotionSample?` and `status: String`, and read-only **computed** `isFresh: Bool`. `isFresh` checks the exact monotonic deadline on every read, so the game cannot use motion beyond 0.5 seconds merely because a watchdog has not ticked. Require `isFresh && sample?.gravity != nil` before applying tilt. Stop on lifecycle inactivity/manual-mode switches. On physical iOS, start reads native Core Motion and ignores bridge settings; simulator/macOS uses the receiver.

The receiver entry is **`python3 MotionBridge/Receiver/receiver.py`**. It prints its random token and listens on `0.0.0.0:8765`. Full install/signing/network/troubleshooting/protocol instructions are in `MotionBridge/README.md`. The independent `MotionBridge/MotionSender.xcodeproj` supports iOS16+, automatic signing and an intentionally editable example bundle identifier. The user must select their team and unique ID to install.

Main app Info.plist needs `NSMotionUsageDescription`, `NSLocalNetworkUsageDescription` and `NSAppTransportSecurity → NSAllowsLocalNetworking = YES`. The sender already includes these. Current Apple documentation lists IP literals under NSAllowsLocalNetworking; actual physical transport acceptance remains a device check. Do not add a global ATS exception on speculation.

## Frozen protocol

Both `POST /sample` and `GET /latest` require `Authorization: Bearer <startup token>`. POST v1 fields are `version`, UUID `sessionID`, safe-integer `seq`, sender-monotonic `timestamp`, `accelerometer:{x,y,z}`, and `gravity:{x,y,z}` or explicit null. Units are g; raw acceleration includes gravity. The separate gravity field is Core Motion's processed gravity estimate, matched within 0.2 seconds of the raw timestamp. Sequence/time must strictly increase within a session. New sessions replace the current session, and retired sessions are rejected. Replay history is capped at 128 retired sessions; new sessions then require relay restart rather than forgetting history.

GET returns `version`, `available`, `fresh`, `ageSeconds`, `sample`. Receiver freshness uses its monotonic arrival clock, not phone/Mac timestamp comparison. HTTP request duration is conservatively subtracted by the client, which also maintains a local expiration deadline. Native capture validates sensor timestamp age directly; delayed callbacks cannot revive old input. Payload/body/value bounds, strict keys, finite values, UUIDs and JSON duplicates are validated.

Sender capture is 30 Hz, with at most one HTTP request in flight; intermediate readings are dropped rather than queued. Client polling also has one request at a time. Backgrounding the sender stops capture/transmission. Tokens stay in memory and do not appear in request logs; the receiver prints its pairing token only at startup as requested.

## Verification

Tests were written before receiver/type validation, observed failing, then made green. Review found a watchdog-only expiration gap; the final computed freshness gate removes it.

- **PASS**: 11 Python unittest cases, including actual HTTP loopback auth on both routes, malformed/duplicate/oversize/nonfinite payloads, timestamps/sequences, fresh/stale state, reconnect, retired-session replay, and bounded history.
- **PASS**: host Swift production-type checks for JSON decoding, explicit `gravity:null` encoding, finite bounds, bad timestamps, native age and envelope freshness.
- **PASS**: real Swift URLSession client against the real Python receiver:401, empty state, actual gravity, expiry between watchdog ticks, stale sample clearing, new-session reconnect, stop. This runs the same HTTP branch compiled for macOS. Test listener was stopped and port 8765 released afterward.
- **PASS**: final unsigned iPhoneOS Debug build of MotionSender and the native Core Motion branch, 2026-09-26 12:23 Pacific.
- **PASS**: final unsigned iOS Simulator Debug build of MotionSender and polling client, arm64/x86_64, 2026-09-26 12:23 Pacific.
- Build warning only: AppIntents metadata skipped because no AppIntents dependency.
- No physical-iPhone installation/signing, real sensor capture, Local Network permission prompt or phone-to-Mac Wi-Fi test is claimed. No main-game runtime behavior is claimed by this worker.

Reproduce checks using the commands in `MotionBridge/README.md`. The live client check temporarily binds loopback 8765; stop the normal receiver first.

## Coordinator/user smoke

Start the receiver; install sender with the user's signing team; enter Mac Wi-Fi IPv4/token; accept permission; verify raw/gravity live values and accepted count. In the simulator select live iPhone input and enter the same token with host 127.0.0.1. Tilt the real phone and observe the board respond. Stop/background sender: board must pause after at most 0.5 s of sample age without resetting the board. Restart sender: new session reconnects. On a physical main-app device, confirm the native Core Motion route works without the relay.
