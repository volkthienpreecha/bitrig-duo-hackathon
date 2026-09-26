# Neon map expansion — six puzzle layouts

Current requested world-art update: cozy cyberpunk dioramas with more cyan/pink neon, warm lanterns, and Japanese shop signs. Smooth rounded meshes and the existing warm lighting remain. This folder supplies six complete world arrangements, expanding the previous three. These are six alignment variations of the same fold-and-drop bridge mechanic, not six new mechanics or proven playable levels.

## Integration handoff

- Use `<stage>/Runtime/<stage>-assembled.scn` with its **same-folder** `<stage>-colliders.scn`. Do not mix colliders across stage folders or use the old narrow beam.
- Each visual scene has 20 module meshes, including a separately removable `neon_signage` root. Each collider scene has 23 proposed box colliders. Decorative neon has no collision.
- Keep `upper_chute` and its child `release_gate` together. `bridge_beam` remains a separate root; it must genuinely fall and become the crossing surface.
- Runtime units: meters, Y-up, +X along the route. Beam dimensions: **2.90 × 0.22 × 0.54 m**.
- Each scene contains named anchors. Read `Validation/geometry.json` for spawn, hinge/release anchors and an analytical fold alignment reference. Fold offsets are relative to the authored pose, **not calibrated Duo sensor angles**.
- Load Kaprao separately from `../KapraoSprite/Runtime/kaprao-sprite.scn` at scale 1, following its README. World previews deliberately omit the character; no rejected dog mesh is embedded.
- Japanese lettering is converted to mesh geometry: no runtime font installation or network dependency. Cyan/pink emissive PBR materials provide the neon layer; no extra runtime light sources or bloom requirement. Retain the warm scene lighting in the app.
- Bundle only required `.scn` resources and the separate character/audio assets. Source `.blend`, exchange files, previews and validation reports are preparation materials.
- This is an asset handoff, not another build prompt. The existing `Preparation/FoldAndFetch-Bitrig/Master-Prompt.md` remains the sole app-build entry point. One complete workshop is still the first acceptance gate; extra arrangements are optional content after it passes.

## Six arrangements

| ID | Layout | Route depth (m) | Puzzle variation |
|---|---|---:|---|
| 01 | Rooftop Repair Club | 0.00 | Neutral alignment introduction |
| 02 | Moonleaf Garden | +0.32 | Larger negative fold offset |
| 03 | Starlight Terrace | −0.28 | Opposite-direction alignment |
| 04 | Midnight Repair Market | +0.16 | Smaller negative adjustment |
| 05 | Lantern Garden | −0.14 | Smaller positive adjustment |
| 06 | Stargazer Tea Deck | +0.46 | Furthest positive-depth target |

All use the existing start, jump curb, gap, supports, recovery tray, chute, release gate and exit. The six target depths are distinct. No additional interactions, counterweights or invisible bridges were introduced. Difficulty labels are design intentions until playtested.

## Signs

- 修理工房 — repair workshop
- 修理 — repair
- 屋上庭園 — rooftop garden
- 喫茶 — tea / café
- 出口 — exit
- 夜市 — night market
- 星見 — stargazing

Signs use macOS Hiragino rounded glyph outlines converted to meshes by the generator; no font file is distributed. Geometric scenery and sign meshes are generated locally; no new paid generation or external asset download was used.

## Verification boundary

`validation-summary.json`: fresh GLB imports, finite geometry, unit scales, self-contained resources, gate/beam hierarchy, source reopen, Japanese meshes, analytical alignment and matching floor clearance.

`native-validation.json`: SceneKit reload, mesh counts, hierarchy and all 90 authored anchor positions across six scenes. Per-stage `Runtime/scenekit-conversion.json` records USD-to-SCN round trips.

These checks are **asset import and geometry evidence**, not physical landing, successful crossing, hinge projection, frame-rate or Bitrig/Duo gameplay evidence. All six layouts need live validation before being called playable.

Regeneration tools: `../Tools/neon_stages_build.py`, `neon_stages_validate.py`, `neon_stages_native_validate.swift`, and the existing `convert_scenekit.swift`. The build tool depends on the original workshop source and helper definitions. `--draft` produces quick hero renders.
