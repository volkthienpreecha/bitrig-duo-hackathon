# Kaprao v4 — sculpted reference match (in progress)

The user requested a rebuild on September 26, 2026 to match `Reference/authoritative-character-sheet.png`. This new reference supersedes the v3 realistic-fur direction for this revision. The world assets are unchanged.

## Visual target

- Rounded orange body, short cream paws, large upright pink-lined ears.
- Broad cream cheeks and layered sculpted chest tufts; subtle velvety surface rather than long strand fur.
- Large warm eyes, cream forehead blaze and eyebrow markings, rounded dark nose, open smiling mouth and pink tongue.
- Teal triangular scarf, side knot/tails and cream paw emblem.
- Separate angular dark sunglasses, low enough to see the eyes, with cyan lower corners and small violet/yellow/orange accents along the upper frame and temples.
- Compare front, side and three-quarter renders to the supplied sheet before adopting the model. A single illustrated sheet cannot establish a mathematically exact 3D reconstruction; hidden surfaces must be inferred.

## Current progress

- Original user sheet preserved without changes.
- Single-character reconstruction image prepared at `Reference/kaprao-base-three-quarter.png`. Only this preparatory image omits glasses to expose the underlying face; glasses remain required on the final model.
- Separate existing-account Weave workflow prepared: https://app.weavy.ai/flow/mSOfCpR2i9q9GBHfepUFhr
- Uploaded reference is image 2 of 2 in Single mode and connected to Rodin V2. The first image and any pre-existing 3D result are copied v3 history, **not a v4 result**.
- Settings: PBR, 50K Quad, one run, random seed, T/A pose off, preview render off, original alpha off.
- UI quote: 36 credits; balance before run: 114 credits. Explicitly approved by the user; one run started. The website now shows 78 credits remaining (36 spent).
- Connector upload requires a paid Weave plan; ordinary website upload succeeded without an upgrade.

## Remaining

1. On exact-cost approval, run once and download the actual generated mesh.
2. Inspect the generated anatomy and material maps in Blender against the authoritative sheet. Fit separate RGB sunglasses and correct proportion/accessory issues where practical.
3. Preserve meters, floor origin, native Y-up/+X-forward and named in-place clips. Measure the new paw width at runtime scale against the current 0.54 m bridge.
4. Render front/side/three-quarter views, validate source/export/animation/native imports, and check Duo viewer appearance.
5. Only then update current-character handoffs and packaging. v3 remains the usable integration baseline until v4 passes; no v4 runtime model exists yet.
