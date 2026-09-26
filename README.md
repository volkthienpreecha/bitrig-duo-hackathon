# Bitrig Duo Hackathon

Preparation repository for Bitrig Hacks: iPhone Duo Edition, September 26, 2026.

**Preparation only: app code must be written during the hackathon.** The organizer's full reminder email specifies this rule. Ideas and assets can be prepared ahead of time.

## Environment checked September 25

| Dependency | Status |
| --- | --- |
| macOS 26.6 or newer | Installed: 26.6.2 |
| Xcode 27.1 | Installed: build 27A9269, currently in `~/Downloads/Xcode.app` |
| iOS 27.1 SDK | Installed, including simulator SDK |
| iOS 27.1 simulator runtime | Download in progress in Xcode Settings > Components; not yet installed at inspection |
| Git | Installed; this folder is a Git repository |
| GitHub | Connector and CLI authenticated as `volkthienpreecha` |
| Active command-line developer directory | Still standalone Command Line Tools; see below |

An SDK compiles the app; a simulator runtime is separately required to run it.

## Finish machine setup

1. Let the iOS 27.1 beta components download finish in Xcode Settings > Components.
2. Prefer moving Xcode from Downloads to Applications before selecting its final developer path.
3. In Xcode Settings > Locations, select Xcode 27.1 for Command Line Tools. Alternatively use `sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer` after moving it.
4. Open Device Hub and confirm an iPhone Duo simulator is available.
5. During hacking, create an iOS App using Swift and SwiftUI inside this repository, using the existing Git repository. Open that `.xcodeproj` in Xcode and this same folder in Codex.

Until Xcode is moved/selected, a terminal session can explicitly use its current installation:

```sh
export DEVELOPER_DIR="$HOME/Downloads/Xcode.app/Contents/Developer"
xcodebuild -version
xcrun simctl list runtimes
```

## Dependencies for the app

Start with Apple frameworks included in Xcode: Swift, SwiftUI, and the iOS 27.1 SDK. Use Swift Package Manager only when the chosen idea needs another library. A basic simulator demo needs no backend, CocoaPods, Node.js, or paid developer membership.

- RevenueCat: required only if competing for the RevenueCat prize / implementing purchases.
- Supabase: optional for authentication, shared data, or storage.
- Sentry: optional for error reporting.
- OpenAI: optional for an AI feature; keep service credentials on a backend.
- Bitrig: optional alternate development tool and Duo preview workflow.
- Metal toolchain: add if the project needs Metal compilation.
- XcodeBuildMCP: optional build/simulator automation. The installed iOS debugger skill expects it, but its MCP tools are not exposed in this session. Xcode UI and `xcodebuild` remain available.

## Collaboration

GitHub stores the shared history; Xcode and Codex operate on the same local files. Xcode does not need a special GitHub plugin to recognize a project in a Git checkout. Push/pull through Git or Xcode source control. Add a teammate once their GitHub username is known.

## Skills

Already available in Codex's build-ios-apps plugin: `swiftui-ui-patterns`, `swiftui-view-refactor`, `swiftui-liquid-glass`, `swiftui-performance-audit`, `ios-debugger-agent`, and `ios-app-intents`.

- Apple's **App Resizability** skill in Xcode 27.1 supports SwiftUI and iPhone Duo. [Apple introduction](https://developer.apple.com/videos/play/tech-talks/111461/).
- [SwiftUI Expert](https://www.skills.sh/avdlee/swiftui-agent-skill/swiftui-expert-skill), by Antoine van der Lee: about 32.8K installs and 3.6K repository stars at inspection. A strong general SwiftUI addition; not a substitute for current Duo API documentation.
- [iPhone Duo skills](https://github.com/mirzaaghazadeh/iphone-duo-skills), a community pack: readiness, adaptive layout, vertical bars, hinge/scenes, camera, and design review. The adaptive-layout skill had 140 installs and the repository 78 stars at inspection. New and less established; review against Apple's SDK/docs before relying on it. No additional skills were installed during preparation.

Optional installation commands, when Node/npm are available:

```sh
npx skills add https://github.com/AvdLee/SwiftUI-Agent-Skill --skill swiftui-expert-skill
npx skills add mirzaaghazadeh/iphone-duo-skills --skill iphone-duo-adaptive-layout
```

## Duo API reading and demo checks

- [Apple Duo developer hub](https://developer.apple.com/iphone-duo/)
- [Prepare your app](https://developer.apple.com/videos/play/tech-talks/111461/)
- [Adaptive layouts](https://developer.apple.com/videos/play/tech-talks/111463/): arrangement and reserved-region APIs for fold-aware layout.
- [Hinge and multiple scenes](https://developer.apple.com/videos/play/tech-talks/111464/): hinge input for interactions; scene accessories for supported multi-display experiences.
- [Bitrig guide](https://bitrig.com/blog/iphone-duo-app-development)

Test folded, unfolded, partially folded, rotated, and narrow multitasking configurations. Preserve navigation, editing, and sheet state across transitions. Use native navigation and toolbars, respect asymmetric safe areas, and keep controls away from reserved regions. Verify all new API signatures against the installed SDK.

## Event

- Check-in: 10:30 AM; opening: 11:00 AM.
- Hacking: 11:30 AM–3:30 PM; demos: 3:30–5:00 PM.
- Aim for one polished interaction that depends on the Duo's capabilities.
- One submission per team; maximum five people (full organizer email).
- Bring laptop and charger. Transport/parking and dietary instructions remain in the invitation.
