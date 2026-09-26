# Integration into the event app

The easiest tested path is **SwiftUI + SceneKit using the supplied `.scn` files**. No Blender, GLB loader, texture downloader, paid service or backend is needed at app runtime. Blender is only needed to edit/rebuild source assets.

## Add the resources

1. Read the existing event `Master-Prompt.md`; create the submission app during the permitted coding window. The asset-only validation app was isolated under `/private/tmp/FoldFetchAssetCheck` and is not included here as submission code.
2. Add selected files from `Runtime/Workshop`, `Revisions/Kaprao-v3/Runtime/Kaprao`, and the eight WAVs from `Runtime/Audio` to the app target's Copy Bundle Resources. Use an `AssetContent` folder if preserving subfolders. Avoid a top-level folder literally named `Resources` inside the iOS app bundle: that caused bundle recognition/install failure in the isolated test project.
3. For a quick visual check, load `workshop-assembled.scn` and one `kaprao-Idle_Look.scn`. The workshop scene already has placements; do not add standalone copies of the same objects on top of it. For modular assembly instead, use individual pieces and their recorded origins.
4. Keep `.blend`, `.glb`, `.usdc`, source photos, concepts, SVG screen mockups, validation logs and modeling tools outside bundled resources. Ship only the runtime assets actually used. Reference screenshots are not a functioning HUD.
5. Preview through Xcode/Device Hub first. The tested environment is Xcode 27.1 build 27A9269, iOS 27.1 Duo simulator. Set `DEVELOPER_DIR` to the actual Xcode `Contents/Developer` when command-line tools point elsewhere. Bitrig's embedded preview install remained unsuccessful in this session.

## Coordinates and assembly

Meters, Y up, +X route/character forward, +Z toward the front. Source Blender Z-up maps to game `(X,Z,-Y)`; exchange files already apply that conversion. Do not rotate them a second time. See [Workshop README](Source/Workshop/README.md) and [geometry manifest](Validation/workshop-geometry.json) for precise root pivots/anchors.

- Deck tops Y=0. Outer platform gap is 2.20m. The centerline landing pockets make a 2.96m opening for the 2.90m beam, with approximately 30mm end clearance per side.
- Beam core is 2.90×0.22×0.35m in X/Y/Z; landed center `(0,-0.11,0)`. Use the core collider, not all raised decorative geometry. Contact shelves top out at Y=-0.22.
- Chute hinge pivot is `(0,3.00,-1.20)` and rotates about X. Folding changes release depth/elevation, not left-right aim.
- Neutral held-beam center is `(0,1.75,0)`. `ANCHOR_held_beam_center` and the release/gate anchors are supplied.
- Gate is already parented under the chute in the assembled scene. Its local pivot `(0,-1.40,+0.93)` must not be interpreted as another world-space offset.
- The bridge is a separate root. When released, preserve its world transform under the authoritative physics world. One physics owner controls the falling body.
- Rear service deck/backdrop are scenery, not an alternate path around the puzzle. Enforce the intended character lane in runtime collision/movement.

The three storyboard poses are authored hinge offsets (-28°, 0°, +28°) around a design reference. They are **not calibrated absolute Duo angles**. Determine reference angle, sign, clamping and release depth in the real app. The viewer proves live hinge readings, not the final mapping.

## Kaprao and animation

Use a parent gameplay node for movement/collision, with the imported character beneath it. Use [Kaprao v3](Revisions/Kaprao-v3/README.md), not the rejected root-level character. Its full silhouette is approximately 1.45m long, 1.17m high and 0.78m wide. Tune a simple controller collider separately; no detailed fur/ear/sunglasses collision is needed.

| Native file | Intended use |
| --- | --- |
| `kaprao-static.scn` | Static pose/import fallback |
| `kaprao-Idle_Look.scn` | Four-second loop |
| `kaprao-Walk_InPlace.scn` | 0.8-second loop; movement comes from controller |
| `kaprao-Jump_Fall.scn` | 1.2-second source and tested native clip; non-looping; dash may reuse airborne pose |
| `kaprao-Celebrate.scn` | Two-second non-looping celebration |

USD export uses one clip per file to preserve native animation import. GLB holds all four named actions for interchange, but **direct SceneKit GLB loading failed in testing**. Use SCN files, or USD through the tested conversion tool. Do not rename container animation keys and assume that creates a new clip. Enumerate the animation player on the imported hierarchy. Transitioning between clips is runtime work; keep one visible character and one active movement owner.

The v3 rig has 11 joints with normalized smooth skin weights. Fine silhouette fur shares body weights. First-pass foot locking and game animation transitions need review; source sampling found up to 8.4mm of foot-floor penetration. Glasses are separately removable geometry sharing the head joint. The RGB trim uses restrained static color accents; no animated neon shader is required.

## Materials and lighting

Workshop meshes use self-contained PBR constant colors, roughness, metalness and restrained emission; their palette PNGs are references. Kaprao v3 uses embedded 1024px PBR texture maps in each SCN, with original 2048px images packed into the editable Blender source. No runtime external texture lookup is required. Blender lights/cameras are excluded from exports so the app can own its projection and illumination.

Starting native viewer setup: one warm directional key (650 intensity, RGB 1/.84/.65), cool ambient fill (130 intensity, RGB .69/.76/1), HDR camera with exposure offset -1.2, bloom and depth-of-field disabled. This is a visual starting point, not a measured performance budget. Shadow softness, exposure and material appearance differ between Blender and SceneKit. Limit real-time shadow lights; emission on a lamp is not an expensive point light.

Full workshop is about 60k triangles, Kaprao v3 is 46,156 triangles across three meshes and ten materials. The workshop is 19 merged visual meshes with multiple material groups; material groups still imply rendering work. Optional skyline can be removed. Profile actual FPS/frame time and memory after the gameplay cameras and two-display rendering are implemented; simulator screenshots alone do not certify 60fps.

## UI and sound

Follow [UI/README.md](UI/README.md) for native safe-region placement, 44pt touch areas and progressive hints. Preserve editable SVGs as design sources. Build native buttons/text from the spec; do not display the entire concept image as the interactive screen. Control placement must use actual fold/reserved regions at runtime.

All eight supplied WAVs are mono 44.1kHz 16-bit PCM; preload and trigger only on accepted gameplay events. Source/license records are under `Licenses/`. Simulator decode is distinct from audible playback and mix approval. Keep gameplay understandable muted.

## Required next gameplay checks

- One authoritative world and correctly connected folded projections; no second unsynchronized simulation.
- Open/book/closed/rotated layouts and control reachability, narrow/reserved regions and state retention.
- Chute fold mapping, held-to-dynamic transition, two-support contact/stability, genuine miss/retry and reset.
- Kaprao crossing the physical beam without scenery shortcuts, root-motion drift or clipped transitions.
- Audio event cooldowns/mute, real output audition and performance under continuous folding.

The provided collision boxes and nominal clearance checks support this work; they are not proof that a physics engine has solved the puzzle.

## Rebuilding exchange/native files

Use the scripts under `Tools/` with Blender 5.2.2 LTS for model regeneration. Each model README describes its commands. Native conversion is reproducible with Apple's SDK:

```sh
xcrun swiftc Tools/convert_scenekit.swift -framework SceneKit -framework AppKit -o /tmp/foldfetch-convert
/tmp/foldfetch-convert Exports/Workshop Runtime/Workshop
/tmp/foldfetch-convert Revisions/Kaprao-v3/Exports/Kaprao Revisions/Kaprao-v3/Runtime/Kaprao
```

Run from `DesignAssets` with the correct `DEVELOPER_DIR`. Inspect `scenekit-conversion.json` for every record's `roundtrip: pass`; the converter continues after per-file failures so the report, not only shell exit status, is authoritative. Reload in the target simulator after any export change.
