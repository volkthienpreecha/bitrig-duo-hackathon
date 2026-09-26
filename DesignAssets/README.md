# Fold & Fetch — design asset pack

> **Current character: [Kaprao v3](Revisions/Kaprao-v3/README.md)** — a fluffy reconstructed model with fitted RGB glasses, rig, four clips, embedded-texture native SCN exports and Duo simulator evidence. Selected by the user for the repository. v1 and v2 remain rejected. The original ZIP and root-level Kaprao folders are historical v1 assets; use the v3 paths below for every character resource. The workshop and UI are unchanged. [Exact character target](Concepts/kaprao-authoritative-furred-reference.png).

**Locked direction:** cozy cyberpunk rooftop workshop, smooth rounded 3D diorama, restrained warm lighting, and Kaprao with a teal scarf and removable RGB sunglasses. This is an asset handoff for one spatial bridge puzzle. It is not a completed game.

Start with [INTEGRATION.md](INTEGRATION.md), then [the remaining-assets checklist](DEMO-ASSET-CHECKLIST.md). Character files live under `Revisions/Kaprao-v3/`; workshop and audio remain under the root asset folders. Read the [v3 character tests](Revisions/Kaprao-v3/Validation/README.md) and [workshop test record](Validation/README.md). Use native SCN for the tested Apple SceneKit path, Blender for editing, and GLB/USD for exchange. Do not bundle this entire design folder into the app.

## Delivered checklist

| Asset | Files |
| --- | --- |
| Kaprao character sheet | [Fur reference](Concepts/kaprao-authoritative-furred-reference.png), [actual model turnaround](Revisions/Kaprao-v3/Previews/kaprao-turnaround.png), [RGB sunglasses hero](Revisions/Kaprao-v3/Previews/kaprao-hero.png) |
| World concept + close-ups | [Wide concept](Concepts/workshop-world-concept.png), [modeled workshop](Previews/Workshop/workshop-main.png), [bridge detail](Previews/Workshop/workshop-detail-bridge.png), [rooftop detail](Previews/Workshop/workshop-detail-rooftop.png) |
| Level layout | [Top](Previews/Workshop/layout-top.png), [side](Previews/Workshop/layout-side.png), [front](Previews/Workshop/layout-front.png), [named anchor coordinates](Validation/workshop-geometry.json) |
| Fold storyboard | [Open reference](Previews/Workshop/fold-01-open.png), [play reference](Previews/Workshop/fold-02-play.png), [more folded](Previews/Workshop/fold-03-more-folded.png) |
| Palette/materials | [Material sheet](Palette/material-sheet.png), [editable SVG](Palette/material-sheet.svg), [palette JSON](Palette/palette.json), [art direction](ART-DIRECTION.md) |
| Kaprao editable model + rig | [Blender source](Revisions/Kaprao-v3/Source/Kaprao/kaprao.blend), [model contract](Revisions/Kaprao-v3/README.md), [GLB](Revisions/Kaprao-v3/Exports/Kaprao/kaprao.glb), `Revisions/Kaprao-v3/Runtime/Kaprao/` native SCN |
| Four animations | [Idle/look](Revisions/Kaprao-v3/Previews/kaprao-idle-look.gif), [walk in place](Revisions/Kaprao-v3/Previews/kaprao-walk-in-place.gif), [jump/fall](Revisions/Kaprao-v3/Previews/kaprao-jump-fall.gif), [celebrate](Revisions/Kaprao-v3/Previews/kaprao-celebrate.gif); separate native SCN and USDC clips |
| Modular workshop kit | [Blender source](Source/Workshop/fold-and-fetch-workshop.blend), [piece inventory/pivots](Source/Workshop/README.md), `Runtime/Workshop/` and `Exports/Workshop/` |
| Textures/materials | Kaprao v3: packed 2048px source textures, 1024px runtime textures embedded in SCN. Workshop: self-contained constant PBR materials; palette swatches are references. |
| UI states/controls/hints | [Three-state preview](UI/ui-contact-sheet.png), [editable SVGs + overlays](UI/README.md), 14 icons, four swipe directions and contextual hints |
| Handoff/provenance | [Setup](INTEGRATION.md), [sources/licenses](Licenses/README.md), native import reports, geometry checks, runtime hashes and Duo evidence |
| Existing audio | Eight original provided WAVs copied to `Runtime/Audio/`, [manifest](Licenses/AudioManifest.md), original CC0 license texts |

Every requested workshop object is independent: two floors, two supports, upper chute, separate gate, one bridge beam, recovery tray, jump curb, exit bell, wall/frame and rails. Extra reusable modules include a goal toy, repair bench, plants, lamps, cables, base and optional skyline. Collision proposals are separate from visible geometry.

Kaprao v3 has an 11-joint smoothly weighted rig, textured coat, fine silhouette fur and removable RGB sunglasses. Its four motions have no gameplay root translation. Close-up foot locking and animation transitions still need a game-context review.

## What the checks establish

Native SceneKit conversion and resource loading are tested, and the assets render in an isolated iPhone Duo simulator viewer with live hinge callbacks. These checks do **not** establish fold-dependent spatial projection, beam physics, character collision, complete native HUD behavior, sustained frame rate or physical-device performance. Those are event implementation gates.

[Figma foundations](https://www.figma.com/design/5RQpJ3a4FGxOEzKya5mAeI) contains the palette, text styles, notes and concepts. The account's MCP quota blocked native screen composition; the three complete local SVG/PNG screen designs are included, with a resume script. See [UI status](UI/README.md).

Bitrig opened the isolated test folder, but its built-in preview reported “The app couldn't be installed,” including after relaunch. Xcode/Device Hub is the verified preview path. No unverified Bitrig success is implied.

The handoff archive excludes Kaprao's original personal photo, intermediate draft renders, Blender backup files and raw animation frames. It includes the finished designs, editable sources, runtime assets, GIF previews, tools and test evidence. The original input ZIP remains unchanged.

The repository versions the unpacked v3 source, exchange, runtime, previews and evidence. `Tools/package_kaprao_v3.py` rebuilds the separate replacement ZIP locally; generated ZIPs and intermediate frames are excluded from Git.
