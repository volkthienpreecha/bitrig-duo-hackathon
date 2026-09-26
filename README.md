# Bitrig Duo Hackathon

## Shared project workspace

This private repository is the shared home for Fold & Fetch: the master build prompt, product requirements, Kaprao character and rooftop workshop assets, UI designs, sounds, and validation records. Edit these files here and use Git commits to keep their history.

**Start with the [single master prompt](Preparation/FoldAndFetch-Bitrig/Master-Prompt.md).** It is the only app-build entry point; update it in place instead of creating competing prompt versions. The prototype/demo prompt filenames are redirects.

| Resource | Location |
| --- | --- |
| Master execution prompt | [Master-Prompt.md](Preparation/FoldAndFetch-Bitrig/Master-Prompt.md) |
| Full product requirements | [PRD.md](Preparation/FoldAndFetch-Bitrig/PRD.md) |
| Current art direction | [DesignAssets/ART-DIRECTION.md](DesignAssets/ART-DIRECTION.md) |
| Current Kaprao v3: source, runtime, clips and previews | [Kaprao v3](DesignAssets/Revisions/Kaprao-v3/README.md) |
| Remaining assets and proposed three-stage scope | [Demo asset checklist](DesignAssets/DEMO-ASSET-CHECKLIST.md) |
| Editable workshop model | [DesignAssets/Source/Workshop](DesignAssets/Source/Workshop) |
| Native SceneKit assets | [Current character](DesignAssets/Revisions/Kaprao-v3/Runtime/Kaprao), [workshop](DesignAssets/Runtime/Workshop), [audio](DesignAssets/Runtime/Audio) |
| Exchange models and animation exports | [Current character](DesignAssets/Revisions/Kaprao-v3/Exports/Kaprao), [workshop](DesignAssets/Exports/Workshop) |
| UI layouts, icons and Figma status | [DesignAssets/UI](DesignAssets/UI) |
| Concepts and rendered previews | [DesignAssets/Concepts](DesignAssets/Concepts), [DesignAssets/Previews](DesignAssets/Previews) |
| Eight sound effects and licenses | [Assets/Audio](Preparation/FoldAndFetch-Bitrig/Assets/Audio) |
| Red-team findings and technical gates | [Review](Preparation/FoldAndFetch-Bitrig/Review) |
| Asset validation and limitations | [DesignAssets/Validation](DesignAssets/Validation) |
| Collaboration workflow | [CONTRIBUTING.md](CONTRIBUTING.md) |

The newer DesignAssets art direction takes precedence over historical visual mockups. Asset/tool validation does not establish a running game or passing Duo physics/perspective tests. Preparation scripts reproduce art and conversion; they are not submitted game implementation.

Preparation repository for Bitrig Hacks: iPhone Duo Edition, September 26, 2026.

**Preparation only: app code must be written during the hackathon.** The organizer's full reminder email specifies this rule. Ideas and assets can be prepared ahead of time.

## Environment checked September 25

| Dependency | Status |
| --- | --- |
| macOS 26.6 or newer | Installed: 26.6.2 |
| Xcode 27.1 | Installed: build 27A9269, currently in `~/Downloads/Xcode.app` |
| iOS 27.1 SDK | Installed, including simulator SDK |
| iOS 27.1 simulator runtime | Installed; iPhone Duo booted in Device Hub and Settings tested September 25 |
| Git | Installed; this folder is a Git repository |
| GitHub | Connector and CLI authenticated as `volkthienpreecha` |
| Active command-line developer directory | Still standalone Command Line Tools; see below |

An SDK compiles the app; a simulator runtime is separately required to run it.

## Finish machine setup

1. Duo simulator startup is verified. Recheck the runtime/destination at event start.
2. Use the current Xcode installation with an explicit developer directory for builds; moving Xcode or changing global settings is not a demo prerequisite.
3. During the coding window, follow the unified master to create one native app in this repository and verify it in Xcode/Device Hub.
4. Bitrig has opened this exact folder and displayed its files; app build and two-way external-edit refresh remain unverified.

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

## Fold & Fetch execution kit

[Master-Prompt.md](Preparation/FoldAndFetch-Bitrig/Master-Prompt.md) is the single event execution prompt. It includes the four swipe controls, one bridge level, three-worker ownership, frequent integration gates, and evidence-based simulator tests. [Read the adversarial review](Preparation/FoldAndFetch-Bitrig/Review/Red-Team-Summary.md).

Use one coordinator: Codex supports the requested real subagents; Bitrig-only execution without those tools runs the same roles sequentially. Do not launch the master in both hosts. The existing Bitrig folder conversation is ready for preparation, with no app project yet. All submitted code starts in the September 26, 11:30–15:30 Pacific window.

## Generated design assets

The [complete asset checklist and files](DesignAssets/README.md) cover the cozy cyberpunk rooftop workshop and Kaprao, including editable Blender sources, animations, native SceneKit exports, UI and palette. Start with [integration notes](DesignAssets/INTEGRATION.md) and [actual validation results](DesignAssets/Validation/README.md). A temporary asset-only viewer outside this repository verified native imports and live Duo hinge callbacks; it is not submission/game code or proof of puzzle physics.
