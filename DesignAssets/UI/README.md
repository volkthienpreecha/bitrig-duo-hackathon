# Fold & Fetch UI assets

The package contains three shared editable UI concepts refreshed over the actual workshop/Kaprao v3 render, transparent overlays, fourteen original rounded vector icons, and contextual hint copy. These are design assets, not a running game or a device-size guarantee.

- `States/gameplay-concept.svg` and `.png`: active play, contextual fold hint, Release, pause, and sound.
- `States/pause-concept.svg` and `.png`: Resume, Restart, and sound.
- `States/completion-concept.svg` and `.png`: bell celebration, Replay, and sound.
- `States/*-overlay.svg` and `.png`: the corresponding transparent UI only.
- `Icons/*.svg`: 24-unit icons with a 1.8-unit rounded stroke. Four swipe directions, pause, resume, restart, replay, audio on/off, release, fold, bell, and check.
- `hint-library.svg` and `.png`: six contextual hints, shown one at a time.
- `ui-contact-sheet.png`: all three states at a glance.
- `ui-spec.json`: element hierarchy, editable text, coordinates, palette, and icon paths.
- `safe-regions.json`: semantic placement rules and reference-image exclusion bounds.

## Three-stage extension

[UI/Stages](Stages/README.md) adds progress identity for all three rooftops, Next-rooftop completion for stages 1–2 and Replay-demo completion for stage 3. Local editable files are complete. The connected Figma Starter quota still blocks live composition.

## Native integration

Use native labels and controls at runtime. Reference SVG text remains editable; it is not baked into the concept background. Nunito is the verified Figma design typeface. Rounded system typography is the intended native match. The local renderer uses the listed font fallback if Nunito is unavailable; PNG typography can therefore differ slightly from Figma.

The 1080×720 canvas describes composition only. Place controls in native safe areas using current fold geometry and projected scene bounds. Keep active UI outside Kaprao, the chute, falling beam, bridge, bell, and hinge regions. Keep at least 16pt inset within the usable safe region and at least 8pt between adjacent hit areas. Use at least 44×44pt touch areas; Release is 144×52 reference units. Increase hit areas independently from icon size.

Top-left: game and level identity. Top-right: mute and pause. Lower-left: one short contextual hint. Lower-right: Release. When either bottom corner conflicts with a scene object or fold, relocate that control to another free safe region. Do not overlay the center as a fixed fallback. Pause and completion panels should center within one uninterrupted usable region, not across a physical hinge.

Hints are progressive: left/right movement, jump, airborne dash, fold to aim, and Release. Dismiss each after a successful action. Down is only described as dash while airborne. Release drops the beam; it does not jump or move Kaprao. Repeated failure may bring the same hint back. Do not stack hint strips.

Sound is a toggle: `audio-on.svg` means sound is currently on; its accessible action name is “Mute sound”. `audio-off.svg` means sound is currently off; its action name is “Unmute sound”. Pause, Resume, Restart, Replay, and Release all need spoken labels. The sound row in paused/completed concepts has a 44pt reference hit height.

Use deep teal with cream labels for the primary action. Focus uses a visible ink outline. Press feedback may darken or lower opacity briefly. Disable Release only when the game cannot accept a release, with a contextual reason. Avoid an artificial loading state for these synchronous local actions.

Transitions are 150–200ms ease-out opacity or short translation. Honor reduced motion. No blur, glow, bounce, or perpetual pulsing is required for the UI.

## Figma status

[Fold & Fetch · Rooftop UI](https://www.figma.com/design/5RQpJ3a4FGxOEzKya5mAeI)

The live file contains the Foundations palette/material sheet, placement notes, 30 variables, four text styles, and the approved world and character concepts. Foundations was screenshot-verified after a font correction. The Controls and Screens pages exist but their contents could not be completed: the Figma MCP Starter call quota rejected the composition call. A normal browser import was also attempted; the only enabled browser is a guest Figma session and has no edit access.

All three local SVG/PNG states are complete. `../Tools/ui_figma_resume.js` can create the native editable screen layouts in the existing Screens page when MCP access is available again. It includes the exact target file/page IDs and uses the already uploaded world fill. Run through `use_figma` with the required Figma skills; this file is a resume artifact, not evidence it has executed. The SVGs can also be imported manually into the file, though Figma's import may convert text to outlines depending on import behavior. The resume script retains native TEXT nodes.

## Rebuild

Run `../Tools/ui_assets.py`, then `../Tools/ui_render.cjs` with the bundled Python and Node paths declared in the tool headers/environment. The first builds editable assets and schematic previews; the second replaces concept previews with the approved world image and creates PNGs. Neither script touches game source.
