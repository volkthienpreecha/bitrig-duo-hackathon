# Kaprao v2 — rejected character draft

The user rejected both the first model and this v2 as unlike the supplied reference. This folder is a separate rebuilt character candidate, not an approved replacement or an update to the original ZIP.

The target remains `../../Concepts/kaprao-character-sheet.png` and the user's Kaprao photograph. The workshop is outside this revision.

## Changes

- Continuous remeshed torso/haunches and face; removed the isolated shoulder tufts.
- Rounded ear bowls with a continuous gold rim and recessed pink interior.
- Carved mouth opening, smaller inset eyes with a thin upper lid, softened eyebrows.
- Wider contoured sunglasses with short RGB accents and a fabric-band scarf.
- Two baked 2048px base-color textures for smooth cheek, blaze and chest markings.

[Actual Blender render](Previews/Kaprao/kaprao-hero.png) · [Without glasses](Previews/Kaprao/kaprao-unadorned.png) · [Editable source](Source/Kaprao/kaprao.blend)

## Technical status

GLB buffer, normalized weight, clip endpoint and root-translation checks pass. All five native SCN exports reload, and all four animations show actual native bone movement. Reports are under `Validation/` and `Runtime/Kaprao/scenekit-conversion.json`.

53,500 triangles total, compared with 19,900 in v1. This increase was deliberate to preserve smoother sculpt surfaces, and is not a device-performance certification. GLB embeds the textures; keep the `Exports/Kaprao/textures/` folder with USD files. The Blender source packs its images. Native texture verification is recorded separately.

This revision has not been installed on Duo or substituted into the old pack. Its material/visual quality needs review against the concept, beyond file-format checks. The existing rigid-island rig and separate action structure are retained.

Rebuild with `../../Tools/kaprao_build_v2.py`; export clips with `../../Tools/kaprao_export_clips_v2.py`; validate GLB with `../../Tools/kaprao_validate_v2.py`. Paths resolve from the main DesignAssets tools directory automatically.
