# Current Kaprao visual handoff — September 26

The user approved **image-based Kaprao inside the existing 3D world**, replacing the earlier mesh-first visual direction. Start with [DesignAssets/KapraoSprite/README.md](DesignAssets/KapraoSprite/README.md).

Runtime files are in `DesignAssets/KapraoSprite/Runtime/`:

- `kaprao-idle.png`: transparent high-resolution corgi with RGB glasses and teal scarf.
- `kaprao-sprite.scn`: native single-plane idle visual with embedded image and a floor-aligned pivot; root scale 1, visible height 0.84 m.
- `kaprao-poses.png`: transparent 3×2 atlas containing idle, two walk poses, jump, fall and celebration.
- `kaprao-sprite.json`: exact pixel rectangles, tested SceneKit UV transforms, common scale/pivot and suggested state mapping.

Use these as **visuals only** under the existing player/controller. Keep the 3D stage, bridge and physical collision rules. Do not use the old v3 0.72 visual scale on the already-sized sprite. Both Duo panels must share one world-space sprite orientation. Read the handoff's alpha/depth, mirroring, shadow and fold-test cautions before integrating.

The native idle asset and six atlas cells were reloaded/rendered with macOS SceneKit. Duo hinge/seam behavior and game physics still need testing in the canonical app. The two walk cards are a limited pose animation, not a polished skeletal walk cycle. No app source was added as part of this asset handoff, and this document is not another app-build prompt.
