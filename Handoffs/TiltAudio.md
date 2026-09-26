# Tilt audio handoff

Status: **DONE**. Standalone source: `FoldAndFetch/TiltAudio/CrossroadsAudio.swift`.

`CrossroadsAudio` is a main-actor `ObservableObject` with `@Published private(set) var muted`, `toggleMute()`, `play(_ name: String)`, and `stopAll()`. It preloads the eight existing flat-bundled WAV names with `AVAudioPlayer`; unknown or missing names do nothing. Per-name monotonic cooldowns prevent repeated step/impact/retry effects. `stopAll()` stops and rewinds every player and clears cooldowns, so Retry can immediately play a fresh effect. It owns no timer, scene, gameplay state, or old GameSession/HUD hook.

Verification: standalone `swiftc -typecheck` passed for arm64 iOS Simulator 27.1. Python's WAV decoder opened all eight unchanged files (mono, 44.1 kHz, nonzero frames). No simulator UI or audio-device playback was used.

Coordinator integration: add this new file to the canonical app target and call `play` only on accepted release, real cover impact/safe contact, success and Retry state changes as appropriate. Call `stopAll()` on reset or scene teardown. Bundle files are already present with their historical names; no resource copies are requested. Audible playback and capture remain a Bitrig/device gate.
