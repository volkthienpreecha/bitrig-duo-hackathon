# Local iPad Motion Bridge

The iPad sender captures Core Motion at 30 Hz and sends timestamped x/y/z raw accelerometer readings and processed gravity separately to a small Mac HTTP receiver. The simulator client polls the receiver through an interchangeable motion-input provider; the same client uses native Core Motion when the main app runs on a physical iOS device. No packages or Bonjour setup are required.

## 1. Run the Mac receiver

From the repository root:

```sh
python3 MotionBridge/Receiver/receiver.py
```

Keep the terminal running. It listens on port **8765** and prints a new random pairing token every start. Find the Mac's Wi-Fi IPv4 in **System Settings → Wi-Fi → Details → TCP/IP**. Allow incoming connections for Python if macOS asks. The iPad and Mac must be on the same local Wi-Fi; a guest network with device isolation may block the connection.

The token authorizes both write and read routes. It is never stored by the sender or written in receiver request logs. This is a local HTTP development bridge, with no Internet service or TLS. Stop the receiver with Control-C when finished; restarting rotates the token and clears all samples.

## 2. Install Motion Sender on an iPad

1. Open `MotionBridge/MotionSender.xcodeproj` in Xcode. The universal sender supports **iPadOS/iOS 16 or later** and is independent of the Duo project/SDK deployment target.
2. In **MotionSender target → Signing & Capabilities**, choose your Apple development team (a Personal Team works), keep automatic signing enabled, and change `com.example.MotionSender` to a unique bundle identifier if Xcode requires it.
3. Connect the iPad to the Mac with a data-capable USB cable for initial installation, unlock it, tap **Trust**, and select the iPad as Xcode's run destination. Enable **Settings → Privacy & Security → Developer Mode** on the iPad if requested. Run the **MotionSender** scheme. After the app is installed, the cable is optional; keep both devices on the same Wi-Fi.
4. In the app enter the **Mac's Wi-Fi IPv4**, without `http://` or `:8765`, and the printed token. Tap **Start sending**. Allow Local Network access and motion access if prompted. If permission prompting interrupts the first connection, tap Stop then Start again.
5. Keep the sender active in the foreground. Raw acceleration and gravity are visible separately, in **g**. The accepted-sample count rises after successful HTTP responses. Leaving the active state stops capture/transmission; tap Start after returning to create a new session.

No simultaneous touch/fold input is needed. The iPad is solely a motion source for the Mac simulator. The sender intentionally refuses capture when run in a simulator.

Troubleshooting: "token rejected" means use the token from the currently running receiver. "Mac unreachable" means check the IPv4, same Wi-Fi, firewall and iPad **Settings → Privacy & Security → Local Network → Motion Sender**. Confirm the Mac can accept incoming connections and that the Wi-Fi does not isolate clients. HTTP 409 after unusually many restarts means restart the receiver and use its new token. Editing address/token while running takes effect after Stop/Start.

## 3. Integrate the reusable client

Add **both** files to the main app target:

- `MotionBridge/Client/MotionTypes.swift`
- `MotionBridge/Client/MotionInputClient.swift`

```swift
@StateObject private var motion = MotionInputClient()

// Simulator uses localhost; a physical iOS device uses native Core Motion.
motion.start(host: "127.0.0.1", token: pairingToken)

// Only use gravity while input is fresh. Preserve the board state while paused.
if motion.isFresh, let gravity = motion.sample?.gravity {
    // gravity.x / gravity.y / gravity.z, all Double and measured in g
} else {
    // Pause motion-driven gameplay and show motion.status.
}

// Stop on lifecycle inactivity or when switching to another input mode.
motion.stop()
```

The client is `@MainActor` and `ObservableObject`. Published read-only fields are `sample: MotionSample?` and `status: String`; `isFresh: Bool` checks the published state and the exact current monotonic deadline on every read. The watchdog updates presentation after expiry, while gameplay pauses immediately at its next input read. `stop()` cancels timers, capture, requests and polling, and clears usable input. Starting again is safe. Native samples must be no older than 0.5 seconds in the local monotonic clock; delayed native callbacks do not revive input. Remote freshness is derived from the receiver's monotonic sample age, conservatively reduced by the entire HTTP request duration, plus a local expiration watchdog. No iPad/Mac clock synchronization is assumed. Consumers must also require non-nil gravity for stable tilt.

Add these keys to the main app's Info.plist (already included in the standalone sender):

```xml
<key>NSMotionUsageDescription</key>
<string>Read accelerometer and gravity to control the tilt prototype.</string>
<key>NSLocalNetworkUsageDescription</key>
<string>Read live motion from the paired iPad through a local Mac relay.</string>
<key>NSAppTransportSecurity</key>
<dict><key>NSAllowsLocalNetworking</key><true/></dict>
```

Apple documents that [`NSAllowsLocalNetworking`](https://developer.apple.com/documentation/bundleresources/information-property-list/nsapptransportsecurity/nsallowslocalnetworking) covers local hostnames and IPv4/IPv6 addresses. No global ATS disable is used. The actual permission/transport path on the user's physical iPad must still be checked after installation.

## Protocol v1

Both routes require `Authorization: Bearer <pairing token>`. HTTP requests use port 8765.

`POST /sample`, Content-Type `application/json`, maximum body 4096 bytes:

```json
{"version":1,"sessionID":"11111111-1111-4111-8111-111111111111","seq":1,"timestamp":123.456,"accelerometer":{"x":0.1,"y":-0.2,"z":-1.0},"gravity":{"x":0.0,"y":0.0,"z":-1.0}}
```

`timestamp` is the iPad sensor's monotonic timestamp in seconds. `seq` is a nonnegative integer ≤ 2^53−1. Both must strictly increase within a session; skipped sequence numbers are normal. Start generates a new UUID. Old sessions cannot take over after reconnect. Receiver memory holds at most 128 retired sessions; reaching the limit rejects new sessions until receiver restart, rather than forgetting replay history.

Raw acceleration includes gravity. The independent `gravity` vector comes from `CMDeviceMotion.gravity` and may be **explicit null** until ready. The sender uses a gravity sample only within 0.2 seconds of the raw acceleration timestamp. Coordinates are device axes, unaffected by app orientation; consumers choose their own axis mapping and calibration. Raw components must be finite within ±32 g; gravity components within ±1.5 g. Timestamps are finite and nonnegative. Extra fields, duplicate JSON keys, nonfinite/unbounded values and invalid UUIDs are rejected.

`GET /latest` returns:

```json
{"version":1,"available":true,"fresh":true,"ageSeconds":0.02,"sample":{"version":1,"sessionID":"11111111-1111-4111-8111-111111111111","seq":1,"timestamp":123.456,"accelerometer":{"x":0.1,"y":-0.2,"z":-1.0},"gravity":{"x":0,"y":0,"z":-1}}}
```

Before a sample arrives, `available`/`fresh` are false and `ageSeconds`/`sample` are null. Freshness expires after 0.5 seconds using **receiver monotonic time**. Stale samples remain in the relay for diagnostics; the client clears them from usable input. Responses disable caching. Status codes: 200 accepted/read, 400 malformed, 401 token mismatch, 404 route missing, 409 replay/session ordering, 413 oversized/empty body, 415 content type, 408 body timeout.

The sender maintains **one network request at a time**. It drops intermediate readings and transmits the newest next reading; it never queues an ever-growing backlog. The receiver serializes small bounded requests. The client also polls with only one in-flight request.

## Connection and disconnection behavior

The iPad sender shows **Capturing**, **Sending live motion**, **token rejected**, or **Mac unreachable**. The simulator settings show the provider's current status. Samples expire after 0.5 seconds; on Wi-Fi loss, sender backgrounding, receiver shutdown, or stale data, the provider clears its usable sample and the board pauses in place. It does not substitute zero gravity or continue on an old reading. Restart the receiver if needed, enter its new token on both sides, reconnect, and recalibrate neutral.

## Verification commands

Use the installed full Xcode toolchain (set `DEVELOPER_DIR` if it is not selected):

```sh
python3 -m unittest discover -s MotionBridge/Tests -v
xcrun swiftc MotionBridge/Client/MotionTypes.swift MotionBridge/Tests/check_types.swift -o /tmp/motion-type-checks
/tmp/motion-type-checks
python3 MotionBridge/Tests/run_client_live.py
xcodebuild -project MotionBridge/MotionSender.xcodeproj -scheme MotionSender -sdk iphoneos -configuration Debug CODE_SIGNING_ALLOWED=NO build
xcodebuild -project MotionBridge/MotionSender.xcodeproj -scheme MotionSender -sdk iphonesimulator -configuration Debug CODE_SIGNING_ALLOWED=NO build
```

The live client check temporarily binds `127.0.0.1:8765` and cleans it up; stop the normal receiver before running that check. It compiles the same HTTP client branch for macOS and tests actual URLSession traffic against the real Python receiver. Native device/simulator builds compile both sensor and HTTP paths without controlling a simulator or installing on an iPad.

The checked-in Xcode project is ready to open. If source membership changes, regenerate it with `python3 MotionBridge/Tools/generate_sender_project.py` (this resets target signing customizations; do not regenerate during normal installation).
