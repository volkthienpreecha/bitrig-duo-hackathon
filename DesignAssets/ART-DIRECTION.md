# Fold & Fetch: locked art direction

Approved September 25, 2026 in the design conversation. This file supersedes the older generic workshop art descriptions in the preparation kit. It does not change the one-level puzzle, swipe controls, physics requirements, or event coding boundary.

## World and character

A cozy cyberpunk rooftop repair workshop in a gentle night city, presented as a compact 3D diorama. Smooth rounded silhouettes, matte cream enamel, muted teal machinery, copper, dark ink recesses, warm window light, and restrained cyan/peach illuminated details. Plants and everyday repair objects make it welcoming. Avoid visible low-poly faceting, gritty dystopia, harsh neon and busy screens. The rounded-world direction does not require a plastic or hairless character.

Kaprao is the mascot, based on the user's supplied latest photo: round golden-orange body, cream chest and cheeks, short legs, white forehead blaze, upright ears, broad smile. Textured teal fabric scarf and properly fitted angular wraparound RGB sunglasses. Preserve recognizable dog anatomy. Source photo is a private reference and is not a runtime app asset.

## Lighting and rendering

Use a warm main light, gentle cooler fill, clear contact shadows, and restrained highlights. The atmosphere comes from materials and composition rather than effects. No depth-of-field blur, motion blur, full-screen blur, or required bloom. Blender preview lighting is an art reference, not automatically the game renderer's lighting. Actual SceneKit material appearance and illumination must be checked in the app.

## Geometry contract

One level, X left/right route, Y up, Z depth, meters, hinge axis X. Fold changes upper machinery elevation and depth, not left/right aim. Beam runs along X and remains a distinct object. Gate and chute are independently addressable. After release game code must detach the beam preserving its world pose. Collision proxies are separate from art; never create collision from the entire decorative diorama. The rear service deck and backdrop are not alternate walking routes. Make this visually evident through a restrained boundary or props outside the walking corridor and continuous route edge markings. Keep Kaprao, the goal toy and both receiver edges prominent in actual-window framing; reduce optional skyline framing before shrinking the gameplay. The toy is the goal; the bell is celebration dressing. The character's depth lane is constrained by the game controller.

All exported dimensions are starting art dimensions. The gap must exceed measured controller jump reach; stable bridge support and walking clearances need gameplay tests. One eye and two calibrated projections are still needed for the connected folded-world illusion; these assets do not implement that renderer.

## Authoritative references

- Concepts/kaprao-authoritative-furred-reference.png: authoritative character target explicitly supplied by the user after rejecting both models. Preserve its soft detailed fur, natural eye sockets and muzzle, full cheek ruff, fluffy chest, short legs, smile, textured scarf and angular sunglasses.
- Concepts/kaprao-character-sheet.png: earlier smooth concept; superseded as the character modeling target.
- Concepts/workshop-world-concept.png: world art target. Mechanism geometry is illustrative.
- Source/Workshop/README.md and validation manifests: actual model geometry and transforms.
- Palette/palette.json and Palette/README.md: UI color roles and material guidance.
- UI/README.md: editable interface assets, state designs, and safe-region guidance.

The original preparation mockup is historical and does not override this direction.

## Character correction after user review

Both v1 and v2 Blender models are visually rejected. Their file-format and animation tests remain valid technical observations, not character-design acceptance. Kaprao should have appealing stylized realism with soft visible fur and convincing dog anatomy. Do not use smooth plastic skin, button eyes, plate-like eyebrows, detached geometric fur pieces, or a flat triangular scarf to stand in for the reference.

A new character must first match the authoritative reference in an actual neutral-lit model render. A generated beauty image does not establish that a rigged 3D asset matches it. Choose the modeling/texture workflow on visual fidelity, then optimize and retest native exports. The workshop direction is unchanged.

## Three rooftop variations

Rooftop Repair Club uses the original warm cream/teal workshop. Moonleaf Garden adds sage enamel, denser planting and a copper trellis. Starlight Terrace opens the rear wall toward the skyline with muted blue enamel and a tea detail. All retain the same cozy cyberpunk miniature setting, Kaprao v3, restrained lighting and bridge mechanic. These are actual 3D asset arrangements, not generated background images.
