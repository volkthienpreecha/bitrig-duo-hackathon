# UI verification

Completed 2026-09-25/26 in the project workspace.

## Local assets

- Three gameplay/pause/completion concept SVGs and PNGs exist, with three corresponding transparent overlays.
- All 22 SVG files parse as valid XML and have viewBoxes. All three UI state SVGs retain editable `<text>` elements. Results are in `ui-svg-validation.json`.
- Fourteen 24-unit rounded icons exist, including all four swipe directions, Release, pause, resume, replay/restart, and both sound states.
- The reference gameplay overlay leaves Kaprao, the beam/chute, bridge gap, and bell visible. Pause and completion intentionally dim the inactive scene.
- UI contact sheet and full-size gameplay, pause, and completion exports were visually inspected. No clipped labels, overlapping controls, blurred surfaces, or baked-in interface text were found.
- Reference touch targets are 44×44 or larger. Native layout and touch testing still require integration; these assets do not prove behavior on Duo hardware.
- The four approved text color pairs exceed the 4.5:1 normal-text threshold. Exact calculated ratios and method are in `ui-contrast.json`.
- Native safe area and fold placement constraints are documented in `UI/safe-regions.json`. They are semantic implementation rules, not tested native behavior.

## Figma

File: https://www.figma.com/design/5RQpJ3a4FGxOEzKya5mAeI

Created and verified: 30 variables (12 palette and 18 semantic/size tokens), four text styles, Foundations palette/material sheet, native placement notes, imported world concept and character sheet. Foundation frame ID `4:2` was screenshot-reviewed after repair. The saved screenshot is `UI/figma-foundations-qa.png`.

The initial SF Pro Rounded label nodes had zero width despite the font being listed. A screenshot exposed the missing labels. Nunito rendered correctly; all foundation labels and four text styles were changed to Nunito and a new screenshot passed. The native implementation may use system rounded type. A line in the existing Figma placement note still names SF Pro Rounded; the local DESIGN.md records the corrected distinction.

The Starter plan allowed three pages, so the file uses Foundations, Controls, and Screens. Further screen/component composition was then rejected with: “You've reached the Figma MCP tool call limit on the Starter plan. Upgrade your plan for more tool calls.” Controls and Screens remain empty. No upgraded plan or paid action was attempted.

Browser fallback: only Codex In-app Browser was enabled. The file opened in guest view with “Sign up to comment, edit, inspect and more.” Continue with Google did not establish a session. There was no authenticated editing surface available for importing the local SVGs.

Therefore the three local UI states are finished, while the editable Figma screen requirement remains blocked. `Tools/ui_figma_resume.js` preserves the intended native text/auto-layout composition for a later authorized run; it has not executed. No screen screenshot from Figma is claimed.
