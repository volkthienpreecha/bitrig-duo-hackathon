# Corgi Crossroads

Native portrait iPhone Duo demo. Tilt a manhole cover through the upper puzzle, stop at the target, close Duo, then watch the cover drop into the street and help Kaprao cross.

- [Current master v2.1](Preparation/FoldAndFetch-Bitrig/Master-Prompt.md) and [Bitrig build instructions](Preparation/FoldAndFetch-Bitrig/Bitrig-Build-Instructions.md)
- [iPad motion sender, Mac receiver and setup](MotionBridge/README.md)
- [Verification and remaining gates](Handoffs/Verification.md)
- [Selected character handoff](DesignAssets/KapraoSprite/README.md)
- [Isolated tilt prototype evidence](Experiments/TiltLab/README.md)

Open `CorgiCrossroads.xcodeproj` in Xcode 27.1, select the iPhone Duo simulator, and run the `CorgiCrossroads` scheme. Use Device Hub to open and close Duo while playing. The current demo is built and tested directly from this native project; Bitrig is not required for the build or simulator run.

The simulator reads live tilt from the separate iPad sender through the local Mac receiver. Physical main-app builds use native Core Motion. Manual input is explicitly diagnostic. The main Duo project requires iOS 27.1; the separate sender supports iPadOS/iOS 16+.

Models and historical filenames remain unchanged. Old beam/rooftop plans and ZIPs are superseded; [historical preparation overview](Preparation/FoldAndFetch-Bitrig/Review/README-historical.md) is retained only as reference.
