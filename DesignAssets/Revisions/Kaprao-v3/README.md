# Kaprao v3 — fluffy stylized-realism rebuild

Status: v3 generated, refined, rigged and checked in the native Duo simulator. The user selected this version for the repository on September 25, 2026; it is the current character asset. v1/v2 remain rejected. The workshop is unchanged.

## Open and use

- Preview: `Previews/kaprao-hero.png`; `Previews/kaprao-turnaround.png`; four motion GIFs.
- Editable source: `Source/Kaprao/kaprao.blend` with packed 2048px textures, source mesh, removable RGB glasses, fine silhouette fur and 11-joint rig.
- Apple runtime: `Runtime/Kaprao/kaprao-Idle_Look.scn`, `kaprao-Walk_InPlace.scn`, `kaprao-Jump_Fall.scn`, `kaprao-Celebrate.scn`, or `kaprao-static.scn`.
- Exchange: `Exports/Kaprao/kaprao.glb` contains all four named clips. Native SceneKit should load SCN, not this GLB.
- All SCN textures are embedded; no runtime Weave, Blender, texture downloading, custom fur shader or account connection is required.
- Use these **instead of** the rejected Kaprao files in the original pack. Keep the existing workshop and UI. Copy the selected SCN files into the app target's bundle resources and retain their filenames.
- Units are metres; native/GLB Y up, +X forward, origin on the floor. Approximate overall bounds: 1.45m long × 1.17m high × 0.78m wide. Put the model under the gameplay movement node; do not add another axis conversion.
- Idle/look: 4.0s loop; walk: 0.8s loop; jump/fall: 1.2s one-shot; celebration: 2.0s one-shot. Game code owns travel, jumping trajectory, collision and animation transitions. All clips have zero root translation.
- Hide the `Kaprao_RGB_Sunglasses_REMOVABLE` mesh to remove the glasses. They share the head joint. RGB accents are ordinary static emissive materials, not animated lights.

Measured geometry: 46,156 triangles across three visual meshes and ten materials; 11 joints. Fine fur is 2,300 tapered ribbons with body-matched skin weights. Source includes a rendered studio; runtime exports exclude its camera and lights. Runtime texture maps are reduced to 1024px; the original and editable source retain 2048px maps.

## Verification and limits

`Validation/kaprao-validation.json` checks geometry buffers, normalized weights, clip names/durations, loop endpoints, root drift and floor origin. `Runtime/Kaprao/scenekit-conversion.json` records all five native conversions/reloads. `Validation/native-animation.txt` confirms actual changes in native presentation-bone transforms for all four clips. `Validation/duo-asset-audit.txt` records native simulator loads and durations. Screenshots show the new model in open, book and closed postures.

The test viewer is isolated from the submission app. These checks do not certify final game physics, connected fold projection, locomotion blending or physical-device frame rate. The first-pass skin is smoothly weighted, but close-up production animation and foot locking may need further refinement. The coat combines textured relief and small silhouette ribbons; it is not a strand-fur simulation. Existing Bitrig embedded-preview installation remained unresolved in the earlier test; the confirmed native route is Xcode plus Device Hub.

## Visual target

Use the user's exact `../../Concepts/kaprao-authoritative-furred-reference.png`: believable short-legged corgi anatomy, full cream cheek ruff and chest, honey-orange coat, natural inset eyes, soft furry ears, a proper smiling muzzle, a textured teal scarf, and fitted angular RGB sunglasses. The coat must have a soft silhouette and visible directional fur detail. Do not substitute a plastic or clay finish.

## Workflow

1. Prepare a clean, single-character, full-body image with neutral lighting for image-to-3D reconstruction. The input is a reference illustration, not a completed model. Generate the base without sunglasses so the eyes and underlying face can be reconstructed; fit separate glasses afterward.
2. Reconstruct a textured mesh using a dedicated image-to-3D model, then inspect front, side and three-quarter views in Blender against the reference. Reject uncanny anatomy before adding animations or packaging.
3. Refine the face, mouth, paws, scarf, silhouette and accessory fit. Decide how much silhouette fur should be geometry and how much should be texture after inspecting the generated mesh. Do not assume painted strands alone satisfy the silhouette target.
4. Produce portable materials, a suitable rig and four in-place clips. Preserve the existing meters/Y-up/+X-forward integration contract.
5. Recheck texture containment, native import, deformation, Duo rendering and performance. No prior validation result certifies this new asset.

## Generation record

The Figma account is linked to Weave. MCP uploads require a paid Weave plan, but the ordinary website supports Rodin V2 on this account's Free plan. The reference was uploaded through the website and connected to a single Rodin node.

- Workflow: [Kaprao v3 — fluffy corgi + RGB glasses](https://app.weavy.ai/flow/Xmzwuez9adzJ3kmozE92aP).
- Input: `Reference/kaprao-base-three-quarter.png` (1536 × 1024).
- Model: Rodin 3D V2; PBR materials; 50K Quad; T/A pose off; original alpha off; preview render off; random seed on.
- One run explicitly approved by the user for 36 credits. The website completed the task and the balance changed from 150 to 114 credits.
- No subscription or additional credits purchased. Another generation requires another exact-cost approval.
- The base was deliberately generated without glasses to preserve the underlying face. Separate frames, smoked lenses and restrained RGB accents were fitted in Blender and included in all runtime files.

## Rebuild

The project tools `DesignAssets/Tools/kaprao_refine_v3.py`, `kaprao_preview_clips_v3.py` and `kaprao_validate_v3.py` target this revision folder. The original downloaded reconstruction is preserved at `Source/Incoming/kaprao-rodin-original.glb`. Refinement is deterministic; regeneration through Weave is unnecessary. Convert the exported USDs with `DesignAssets/Tools/convert_scenekit.swift` and check every conversion report entry. Read `SOURCES.md` for provenance.

Official workflow references: [Weave 3D model comparison](https://help.weavy.ai/en/articles/12344357-3d-models-comparison), [Meshy image-to-3D](https://docs.meshy.ai/en/webapp/image-to-3d).
