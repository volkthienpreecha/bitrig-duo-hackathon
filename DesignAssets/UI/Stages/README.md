# Three-stage UI asset variants

Six editable overlays and matching actual-world concepts: gameplay for each rooftop, Next-rooftop completion for stages 1–2, and final Replay-demo completion for stage 3. [Contact sheet](contact-sheet.png). Every concept background shows the actual scene with Kaprao v3; it is an art preview, not a playable screenshot.

`stage-ui-spec.json` contains editable hierarchy, copy, coordinates, stage identities and transition intent. SVGs retain editable text; transparent overlay PNGs are available for preview. Existing pause/Resume, mute, Release, swipe and retry assets remain in `../States` and `../Icons`. Use native labels and controls in the event app, not a screenshot as an interactive HUD.

- Progress reads `ROOFTOP 1 OF 3`, `2 OF 3`, or `3 OF 3`; it does not open a level-selection screen.
- Stage 1–2 completion: **Next rooftop** primary, **Replay rooftop** secondary.
- Stage 3 completion: **Replay demo** primary, **Replay rooftop** secondary.
- Show completion only when the player reaches the goal after a genuine bridge landing. Reset all per-stage physics and hint state when advancing.
- 44pt minimum native hit target, 16pt safe inset and 8pt control gap. Final positions depend on actual Duo usable/reserved regions. Center modal panels within one uninterrupted usable region; the 1080×720 concept is not a pixel-accurate Duo layout.

Figma MCP remains quota-blocked on the connected Starter plan; no upgrade or new login was attempted. The complete local editable assets are ready to import. The existing `Tools/ui_figma_resume.js` describes older screens; use this folder's current spec/SVGs for the three-stage version. The live Figma file has not been updated to these variants.

## September 26 runtime contract

The master v1.2 is authoritative. Release and a labeled Retry share a free lower-right safe region with at least 8pt separation; relocate both outside scene objects and hinge regions. Retry remains accessible during flight, settling, crossing and failure. Pause offers Resume and Replay rooftop. The toy is the goal, with “Toy reached!” completion; the bell is dressing. Gameplay reference backgrounds show a held beam and an empty gap. They still do not establish runtime physics or projected safe regions.

Workshop-only is the default: use the shared single-stage UI, hide “1 of 3” and Next. Three-stage variants apply only after the master’s optional progression gate. Native runtime hints come from the master’s state table, including front/behind miss feedback when measured. The existing Figma file/resume script is historical; no live sync is claimed.
