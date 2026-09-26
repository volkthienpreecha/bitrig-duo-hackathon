# Kaprao image-based character — current user-approved approach

On September 26, the user chose an illustrated character inside the existing 3D diorama instead of further image-to-mesh reconstruction. This handoff supersedes earlier instructions to use Kaprao v3 **for the character visual only**. The existing world, bridge, collision rules and Duo projection requirements remain in force. This is an asset handoff, not authorization to begin the submitted app build.

## Quick integration

Bundle `Runtime/kaprao-idle.png` and, if using SceneKit, `Runtime/kaprao-sprite.scn`. The native file embeds its image: load it with `SCNScene(url:options:)`, detach `KapraoSpriteRoot`, and attach it under the existing physics/player node at the feet. Use root scale 1; the visible illustration is already 0.84 m high. Do **not** reuse the v3 visual scale of 0.72.

`KapraoSpriteVisual` is one vertical XY plane with its front along local +Z. Its local offset compensates for the transparent margins. The root is centered under the visible silhouette at ground level. `Validation/native-validation.json` gives measured image bounds, plane dimensions and offset. This plane has no physics body, no baked camera constraint and no animation track. It is portable visual content; movement and physics stay with the gameplay controller.

Keep the constant/unlit material to preserve the illustration's colors and baked lighting. The RGB glasses are painted into every frame, not separate geometry or real lights. Transparent blending and depth reads are enabled; depth writes are disabled. Test sorting against rails and the bridge. Do not disable depth testing globally or render this character as a HUD overlay.

## Duo and facing

Use one orientation computed from the agreed shared virtual eye, then reuse that world transform for both panel render passes. Do not attach independent camera-facing constraints for the two panels: they can disagree at the seam. Keep the feet anchored as the device folds and the composition changes. Preserve real world-space position, occlusion and the existing collision proxy.

The artwork is a three-quarter view facing screen right, not a freely rotatable 3D model. Mirror the **visual child only** horizontally when screen-space travel reverses; never scale the physics root negatively. Mirroring also mirrors the scarf knot and RGB accents. Do not add a 180-degree turn that shows the flat plane edge. Camera yaw changes, steep pitches and the compact fold transition require visual testing. Maintain a stable rehearsed view if the illusion breaks.

## Motion and shadow

Use the included pose metadata for illustrated pose changes. These are pose cards, not a skeletal rig or a polished many-frame walk cycle. Idle may have subtle visual breathing; walking may alternate the two walk cards with a small bob; jump/fall follow the actual controller state; celebration is triggered only by a real goal event. Keep displacement on the gameplay root and cosmetic motion on the visual child. Reset cosmetic state on Retry/Replay.

Add a soft translucent ellipse on the actual supporting surface, separately from the upright character. Fade/shrink it with airborne height. Do not let a shadow or sprite plane create support or alter physical bridge seating. Reuse the controller's collision proxy; measure visual/physical fit before finalizing jump reach.

## Evidence and limits

`Validation/native-cream.png` and `native-night.png` are actual macOS SceneKit render probes of the reloaded native file, not AI concepts. The PNG has genuine alpha and the SCN contains its image data. This verifies image decoding, embedding and native material rendering. It does **not** establish Duo seam continuity, hinge transitions, iOS installation, physical-device performance or gameplay correctness. The host agent must exercise those gates in the canonical app.

The illustration is an imagegen-derived cutout of the user's supplied art; it is visually close, not pixel-identical to the original. The single cutout retains detail better than the attempted generated meshes. Do not claim that it reconstructs unseen angles.

## Sources and rebuild

`Reference/character-sheet.png` is the supplied authoritative reference. The runtime illustrations were derived using the built-in imagegen tool; no further Weave credits were used. v3/v4 mesh experiments remain separate historical alternatives and are not dependencies of this sprite asset.

Run `DesignAssets/Tools/kaprao_sprite_native.swift` with this folder as its sole argument using the configured Xcode Swift runtime to rebuild the native idle asset and its render probes. The tool writes preparation assets only.
