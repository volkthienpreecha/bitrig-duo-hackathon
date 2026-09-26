# Fold & Fetch UI Design

## Scene and theme

A player operates the folding-phone simulator at a demo table and follows a warm, lamp-lit miniature rooftop against a quiet ink-blue night. Small opaque cream controls maintain legibility without lighting up the whole screen.

## Color strategy

Restrained interface: warm tinted neutrals, deep teal for the one primary action, copper for material details, small cyan and peach cues only. World palette may occupy more area than UI accents.

## Typography

Nunito (Regular/SemiBold/Bold) in Figma and local assets. Native .rounded system text is the intended implementation match. SF Pro Rounded was listed by Figma but failed screenshot rendering, so Nunito is the verified editable design substitute. Local SVG has editable text and the same family fallback stack. 12 metadata, 14 hint, 16 action, 28 state title. Scale up for accessibility, wrap hints or reduce secondary copy before shrinking labels.

## Components

Rounded 44×44 icon targets, a 144×52 Release action, contextual hint strip, pause panel with Resume and Replay rooftop, and completion panel with Replay. Solid fill, 1px optional outline, no blur. Hover/focus/pressed/disabled belong in design controls; loading/error are not runtime states for local synchronous actions.

## Layout

Reference canvas 1080×720 only. Reserve the top-left for level label and top-right for secondary controls. Bottom-left hint and bottom-right Release must remain outside projected character/bridge/fold bounds. Move controls as safe areas and fold geometry change. Center pause/completion panels within one uninterrupted safe region.

## Motion

150–200ms opacity/translation only, ease out. No bounce, pulse, or blur. Reduced motion uses immediate state changes. Hints disappear after successful action and never stack.

## September 26 runtime contract

The master v1.2 is authoritative. Release and a labeled Retry share a free lower-right safe region with at least 8pt separation; relocate both outside scene objects and hinge regions. Retry remains accessible during flight, settling, crossing and failure. Pause offers Resume and Replay rooftop. The toy is the goal, with “Toy reached!” completion; the bell is dressing. Gameplay reference backgrounds show a held beam and an empty gap. They still do not establish runtime physics or projected safe regions.

Workshop-only is the default: use the shared single-stage UI, hide “1 of 3” and Next. Three-stage variants apply only after the master’s optional progression gate. Native runtime hints come from the master’s state table, including front/behind miss feedback when measured. The existing Figma file/resume script is historical; no live sync is claimed.
