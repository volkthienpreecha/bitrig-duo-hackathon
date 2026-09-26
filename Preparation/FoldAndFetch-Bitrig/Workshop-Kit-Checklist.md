# Workshop kit — exact handoff checklist

> **Asset update, September 25, 2026:** The locked style is a cozy cyberpunk rooftop 3D diorama with smooth rounded shapes, restrained warm lighting, and Kaprao wearing removable RGB sunglasses and a teal scarf. The selected character is [fluffy Kaprao v3](../../DesignAssets/Revisions/Kaprao-v3/README.md); root-level Kaprao assets and the old full ZIP contain rejected v1. Read [the remaining-assets status](../../DesignAssets/DEMO-ASSET-CHECKLIST.md) and [the current asset pack](../../DesignAssets/README.md) and [art direction](../../DesignAssets/ART-DIRECTION.md) before older asset guidance below. The pack supplies editable models, native SceneKit assets, animations, UI, and measured validation; this does not certify the future game physics or connected Duo projection.

The immediate target is one workshop level. Please send one ZIP containing references, original editable models, textures, animations, and license/source information. Use the folders below as a guide; incomplete items can be identified explicitly rather than disguised as finished.

## Minimum useful handoff

1. A wide workshop reference image showing the intended look.
2. A top view or annotated sketch locating the corgi route, gap, upper chute, beam, and exit.
3. A usable corgi model, or clearly state that only a character reference is available.
4. Separate 3D meshes for the static workshop and moving mechanism, or clearly state that these still need modeling.
5. Source and license information for every downloaded asset.

References can arrive first; they let us finalize the level without waiting for a complete kit. A PNG of a workshop or corgi does not become a rotating, colliding 3D asset automatically.

## Requested files and formats

| Asset | What to supply | Preferred format |
| --- | --- | --- |
| Overall workshop look | One main view plus two useful close-ups; approximately 1920 px or larger | PNG or JPG |
| Level layout | Top view and side view; annotate gap, supports, chute, release point, corgi start, exit, and hinge axis | PNG or PDF; SVG optional |
| Fold behavior reference | Brief clip or three stills showing open, intended play angle, and more-folded pose; distinguish concept from working footage | MP4 H.264 or PNG sequence |
| Corgi design | Front, side, and three-quarter views; orange/cream body, teal scarf | PNG, transparent background if practical |
| Corgi editable source | Mesh, materials, rig, and animation actions; pack external resources | Blender .blend preferred; other editable source acceptable |
| Corgi runtime export | Skinned mesh and named clips, with a format tested in the selected renderer | For proposed SceneKit: .dae through Xcode or .scn; include original source |
| Workshop source | Walls/floor/rails separated from moving parts | .blend plus exchange export |
| Static props fallback | Geometry, materials, and referenced textures together | .obj + .mtl + PNG textures, requiring import/conversion validation |
| Exchange copy | Convenient handoff for modeling tools; not assumed directly loadable in SceneKit | .glb optional in addition to source |
| Textures | Base color; roughness/metalness and normal maps only if needed | PNG, usually 1024 px, up to 2048 px for the hero asset |
| Icons | Release marker, restart, sound/mute, gesture hints only if custom icons improve clarity | SVG source or vector PDF; PNG export |
| Palette | Named colors or a small swatch image | TXT/MD with hex values, or PNG |
| Fonts | Only if a custom font is necessary; include redistribution license | OTF/TTF plus license; otherwise use system type |
| Audio | Eight downloaded WAVs are present in Assets/Audio | Short PCM WAV files plus manifest/licenses |
| Rights | Author, source URL, license text/file, required attribution, and modifications | MD/TXT/PDF |

Do not supply only Unity prefabs, Unreal assets, or a paid marketplace preview. We need the underlying geometry/textures and a license permitting our use. FBX can be useful source material but must be converted and checked; it is not the default native SceneKit delivery format. Do not spend time producing USDZ-only assets unless the selected renderer/import path has been tested.

Apple documents the SceneKit .dae/.scn workflow here: https://developer.apple.com/documentation/scenekit/scnscenesource/

## Required workshop pieces

- Static lower floor and a pair of gap supports.
- Upper chute with a separate release gate.
- One recognizable beam long enough to span the gap.
- A recovery tray under a missed drop.
- Optional safe practice pad for jump/dash; no required curb/timing obstacle.
- Clearly visible toy/ball goal.
- Minimal background wall/frame that makes the upper region feel recessed.

Do not prepare a second puzzle or environment for the default four-hour demo.

## Geometry and animation handoff rules

- Use separate objects for anything that moves. Do not merge the chute, gate, and beam into one mesh.
- Put a pivot on each gate/lever's actual rotation axis. Annotate hinge positions in the layout sketch.
- Use one stated scale, preferably meters. State axis conventions; the game world uses Y up, X along the corgi route and hinge, and Z for depth. The long beam spans X; folding aims its drop depth Z into both supports. Supply a front-direction marker for the corgi rather than silently assuming an orientation.
- Apply accidental non-uniform scales and keep transforms understandable. Keep animation rigs intact when exporting.
- Use descriptive names such as corgi, chute, release_gate, bridge_beam, support_left, support_right, recovery_tray, and goal_toy.
- Keep visual meshes separate from simple collision proxies. Boxes/capsules are sufficient for most initial colliders.
- Bake any essential procedural materials into ordinary textures, or include a simple material fallback. Do not depend on a Blender-only shader or render engine.
- Initial art budgets: about 10–20k triangles for the corgi and roughly 50k for the visible workshop; these are conservative planning targets, not measured device limits. Prefer a few materials and small textures over many unique surfaces.

Essential character clips: idle/look, walk, jump/fall pose, and celebrate. Dash can reuse the jump pose. Optional clips: brace, land, sniff, and disappointment. Name clips clearly, state whether each loops, and avoid baked root motion for walking; the game controls position. A static corgi with simple transform animation is an acceptable first demo fallback.

## Suggested ZIP contents

```text
WorkshopKit/
  README.md
  References/
    workshop-main.png
    level-top.png
    level-side.png
    fold-reference.mp4
    corgi-turnaround.png
  Source/
    workshop.blend
    corgi.blend
  Exports/
    workshop.dae
    corgi.dae
  Textures/
    ...png
  Licenses/
    sources-and-rights.md
```

Filenames above illustrate the desired contents; they are not claims that these files already exist. Put incoming files in Assets/Models/IncomingWorkshopKit or References as appropriate. Test one mesh, one material, and one animation before converting the full pack.

## Decisions recommended now

- One workshop environment and one required level.
- Warm ivory, teal, copper, and orange; no competing art styles.
- Corgi is the playable character and uses swipes.
- Main fold interaction is the falling bridge beam; no second machinery puzzle in this demo.
- Start with a fixed, rehearsed simulator viewing pose; no head tracking requirement.
- Prioritize readable silhouettes and tactile sounds over effects that soften the image.
