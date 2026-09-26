# Kaprao — editable character asset

An original smooth, stylized corgi based on the user's orange/cream corgi photo and the approved character concept. The asset uses solid PBR materials and actual sculpted geometry. No downloaded meshes, texture packs, hair system, simulation, or Blender-only procedural shader is required.

## Files

- `kaprao.blend`: editable source, organized model/accessory/collision/studio collections, one armature, four actions, and the rendering setup.
- `../../Exports/Kaprao/kaprao.glb`: one GLB with two skinned mesh nodes and all four named animation clips.
- `../../Exports/Kaprao/kaprao-static.usdc`: static rest-pose USD exchange copy with materials and skeleton.
- `../../Exports/Kaprao/kaprao-Idle_Look.usdc`, `kaprao-Walk_InPlace.usdc`, `kaprao-Jump_Fall.usdc`, `kaprao-Celebrate.usdc`: one animated USD file per clip, for import paths that do not expose glTF animations.
- `../../Previews/Kaprao/`: actual Blender renders, both with and without glasses, and four orthographic views. These are renders of the supplied model, not concept images.
- `../../Textures/Kaprao/kaprao-palette.png`: reference palette only; none of the meshes requires an external texture.
- `../../Validation/kaprao-manifest.json`: measured geometry, material colors, skeleton and source details.
- `../../Validation/kaprao-validation.json`: GLB buffer/skin/animation validation.

## Coordinates and dimensions

Units are meters. The Blender source is **Z up, +X facing forward**. Both GLB and USDC are **Y up, +X facing forward**; conversion is `(X,Y,Z) Blender → (X,Z,-Y) exchange`. The origin is on the floor, with paw bottoms at zero. The torso is approximately 0.91 m long; the full silhouette including head, nose and tail is approximately 1.51 m long and 1.17 m high. Character width is approximately 0.73 m including the ears.

`COL_corgi` is a hidden wire collision guide in the source only. It is deliberately excluded from every exchange file. The geometry has no baked gameplay collision or controller. `FORWARD_+X` is also a source-only guide.

## Meshes and materials

The final runtime target is **19,900 triangles total**: 18,000 for the character and 1,900 for removable glasses. See the measured JSON for exact final counts, bounds, and material list. Smooth normals are included. The 15 material definitions produce 16 material primitives across two mesh nodes. These are intentionally simple base-color, roughness and emissive materials; the RGB edge emission is subtle and does not require bloom.

`Kaprao_RGB_Sunglasses_REMOVABLE` is a separate mesh node. Hide or remove that node for the plain face. Its weights refer to the same head bone as the face. The shades sit below the eyes so expression and identity stay visible. Dark lenses are opaque for consistent rendering across importers; the RGB rims use ordinary emissive PBR values.

The white forehead stripe is part of the head mesh's material layout. Cream face and chest lobes are geometrically fused and smoothed. Small independent muzzle/eye/paw/scarf details remain editable mesh islands, selectable by linked geometry or bone group.

## Rig and clips

This is a real exported skin with ten joints, using **rigid 1.0 weights on smooth geometric islands**. It is deliberately a compact first-demo rig; limbs rotate as rigid pieces and it is not a fully deforming production quadruped rig. The large ruff hides the shoulder joints. There is no cloth, fur, facial blend-shape or physics simulation.

| Clip | Frames at 30 fps | Duration | Loop | Use |
| --- | --- | --- | --- | --- |
| `Idle_Look` | 1–121 | 4.0 s | Yes | Small breath, head look and ear/tail motion |
| `Walk_InPlace` | 1–25 | 0.8 s | Yes | Alternating leg cycle; no route translation |
| `Jump_Fall` | 1–37 | 1.2 s | No | Crouch, airborne tuck and return to neutral |
| `Celebrate` | 1–61 | 2.0 s | No | Small art hops, head tilt and tail wag |

No clip translates the root. The gameplay controller must move the character through the world and own the actual jump/fall trajectory. The small body offsets are visual animation only. Dash can reuse the airborne portion of `Jump_Fall`. Looped clips repeat endpoint values to numerical tolerance.

The Blender source opens in the neutral pose. In the Action Editor select one action on `Kaprao_Rig`. Muted NLA tracks retain all clips for export; do not unmute several tracks simultaneously. Set the timeline to that clip's listed range.

## Reproduction and validation

Run these from the repository root with Blender 5.2.2 LTS:

```sh
/Applications/Blender.app/Contents/MacOS/Blender -b -t 6 --python DesignAssets/Tools/kaprao_build.py
/Applications/Blender.app/Contents/MacOS/Blender -b -t 6 --python DesignAssets/Tools/kaprao_export_clips.py
python3 DesignAssets/Tools/kaprao_validate.py
```

On this Mac, Blender requires permission beyond the filesystem sandbox to initialize its graphics stack. The asset generator is tooling only and contains no game implementation.

The validation checks actual exported indices, finite positions/normals/weights, unit normal lengths, weight sums, joint indices, zero-area triangles, triangle count, collision/studio exclusion, named clips, root translation, and loop endpoints. Preview rendering uses no depth of field or motion blur. Native SceneKit and simulator evidence is maintained separately by the coordinator; this file does not claim a Duo runtime pass.

## Source and rights

The mesh geometry, rig, animation, materials, scripts, palette and rendered previews were created for this project. No third-party art was downloaded or incorporated. The user supplied the photographic character reference; it is not embedded in the runtime files. The project's image-generated character sheet is a separate visual reference, not a mesh source. No third-party asset attribution is required by this character pack.
