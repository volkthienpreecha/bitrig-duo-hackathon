# Corgi Crossroads — Duo API audit

Inspected September 26, 2026 against installed Xcode 27.1 build 27A9269. This is preparation evidence, not a claim that game implementation or runtime acceptance has passed. Master v1.4 is the only execution entry point. Build is on hold until the user's new explicit signal.

| Capability | Selected API / decision | Evidence and limits |
| --- | --- | --- |
| Live fold input | SwiftUI `.onHingeChange`, `DeviceHingeContext.hinge`, `DeviceHinge.angle.radians` | Present in SwiftUICore's installed arm64 simulator interface. Angle is SwiftUI `Angle`; hinge is optional. Feed one immutable device-input path. |
| UIKit alternative | `UIHingeInteraction`, `UIHinge` | Present in UIKit headers. Angle is already radians. Status additionally includes `unknown`; handler receives initial state, later updates and unavailable/nil state on hierarchy changes. Do not run competing SwiftUI/UIKit input feeds. |
| Hinge update policy | System-controlled rate and granularity | Stated in `UIHinge.h`. Do not require a particular callback frequency, infer unavailability from a held unchanged value, or turn nil into zero. |
| Reserved regions | `GeometryProxy.reservedRegions(kind:options:layoutDirectionBehavior:)` | Division/occlusion kinds, frame, margins, isActive and includeInactive query exist. UIKit's documented frame already includes margins. Do not double-inflate or mistake it for calibrated physical display geometry. |
| Adaptive arrangements | `ArrangementView`, split/overlay; UIKit arrangement controllers | Available, but not chosen to own the game's explicit render surfaces. |
| Fold handoff | App-owned camera/composition effect driven by calibrated fold input | Approved lower inner panel, not outer cover display. Actual panel bounds come from layout/region APIs. Expanded connected views transition to the complete action below without changing the world. Initial 10–40° closure interval is tuning input, not a discovered blur threshold. |
| Physics/render timing | `SCNRenderer.update(atTime:)`, then render-only `render(withViewport:commandBuffer:passDescriptor:)` | Installed `SCNRenderer.h` explicitly says render-only does not advance animations/physics/particles. One MainActor session advances once; both views draw completed state. |
| Multiple app scenes | Not used | Keep one persistent game session. Multiple render views do not mean multiple app scenes or physics worlds. |
| Outer-display accessory | Not used | Apple's documented simultaneous camera accessory requires full-screen inner UI and an active camera session. Not needed for the approved lower-inner-panel design. |
| Motion / viewer tracking | Not used | No tilt, camera session or viewer tracking requirement. |

No connected-world projection API, Bitrig blur-disable API, blur-state callback or simulator external-orbit-camera API was established. We implement connected projections and the handoff ourselves. The earlier Settings test blurred one region transiently and then cleared; its cause was not identified. The handoff must pass real Bitrig recording/readability checks.

## Inspected local SDK sources

Under `/Users/volkthienpreecha/Downloads/Xcode.app/Contents/Developer/Platforms/iPhoneSimulator.platform/Developer/SDKs/iPhoneSimulator.sdk/System/Library/Frameworks/`:

- `SwiftUICore.framework/Modules/SwiftUICore.swiftmodule/arm64-apple-ios-simulator.swiftinterface`: `ReservedRegion`, `GeometryProxy.reservedRegions`, `ArrangementView`, `DeviceHinge`, `DeviceHingeContext`, `.onHingeChange`.
- `UIKit.framework/Headers/UIHinge.h`, `UIHingeInteraction.h`, `UIViewReservedRegion.h`, `UIArrangementViewController.h`, `UISplitArrangement.h`, `UIOverlayArrangement.h`.
- `SceneKit.framework/Headers/SCNRenderer.h`: separate scene update and render-only Metal pass.

## Primary documentation and acceptance boundary

[Apple's hinge and display guidance](https://developer.apple.com/videos/play/tech-talks/111464/) distinguishes hinge-driven interactions/effects from layout-region APIs and documents camera-accessory availability. [Apple's adaptive-layout guidance](https://developer.apple.com/videos/play/tech-talks/111463/) covers layout adaptation. [Bitrig's Duo release](https://bitrig.com/blog/bitrig-builds-iphone-duo-apps) documents live folding in its built-in simulator.

The isolated asset viewer previously received live hinge values in one ordinary viewport. It is not submission code and will not be copied into the game. No submitted game source or Xcode project exists at finalization. Bitrig launch, connected projection, lower-panel handoff, physical landing/crossing, controls, audio and reset remain separate build-time gates. The simulator service and installed SDK were checked successfully; this does not establish those gates.
