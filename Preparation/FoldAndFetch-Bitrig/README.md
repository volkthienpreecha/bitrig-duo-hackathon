# Fold & Fetch — one-prompt hackathon kit

**Start with [Master-Prompt.md](Master-Prompt.md).** It is the only executable prompt. Paste it once during the event into the coordinating host. It continues from a tiny prototype to the polished demo without another prompt.

Recommended: Codex coordinates three agents; Bitrig edits/previews the same canonical project. Bitrig has opened the existing repository through File → Open Folder and read its README. Stage work in that folder’s New Conversation. Agent orchestration inside Bitrig is unverified; without agent tools, the master explicitly runs the same roles sequentially. Do not run two coordinators.

This kit contains preparation, not a running app. No submission code has been created. Event coding window: September 26, 2026, 11:30–15:30 Pacific. The verified event is simulator-based; a polished demo is sufficient. [Official event](https://events.ycombinator.com/bitrig-hacks-september2026).

## Files

- **Master-Prompt.md:** self-contained mission, controls, physical design, APIs, agent ownership/contracts, integration schedule, scope cuts and evidence gates.
- **PRD.md:** full product requirements, aligned with the master.
- **Review/Red-Team-Summary.md:** prioritized failures, fixes and remaining uncertainty.
- **Review/verified-preflight.md:** direct Bitrig/Device Hub observations; not app-test results.
- **Review/gameplay-review.md**, **rendering-review.md**, **coordination-review.md:** independent adversarial reviews. Their earlier proposed deadlines are superseded by the master’s unified schedule.
- **Workshop-Kit-Checklist.md:** requested source/reference/model formats, pivots, scale and licensing.
- **Assets/Audio:** eight verified WAV effects, original sources, licenses and mapping manifest. Runtime integration is pending.
- **References:** earlier visual concept; visual style only, historical controls superseded.
- **Assets/Models/IncomingWorkshopKit**, **Assets/Textures**, **Assets/UI:** incoming asset staging locations. The completed [design asset pack](../../DesignAssets/README.md) supplies editable sources, native SceneKit files, GLB/USD exchange files, UI designs and validation. These older directories remain staging locations.

The older Prototype and Demo prompt filenames are pointers only. Do not paste them as separate build steps.

## Scope and workflow

One level, one meaningful physical bridge puzzle, corgi mascot, four swipe controls, one-mouse park–fold–release–cross sequence. No extra puzzle, mandatory tilt, head tracking or backend. The beam spans the route along X; folding changes its release depth Z. It must visibly miss or genuinely seat on two supports, then carry the corgi.

Canonical repository: `/Users/volkthienpreecha/Documents/ChatGPT/Bitrig Duo Hackathon`. Repository kit copy: `Preparation/FoldAndFetch-Bitrig/`. Preparation is not automatically live-synchronized through GitHub or an attached ZIP. Coordinator records the exact revision and verifies small combined builds throughout the event.

One coordinator owns project configuration, shared declarations, runtime resource copying and simulator UI. A owns platform/rendering; B gameplay/physics; C corgi/HUD/audio. Their detailed contracts and immutable handoff protocol are in the master.

## Verification boundary

Confirmed: Duo simulator boots; Bitrig opens and reads the actual folder; eight WAVs decode and have recorded CC0 provenance. No game app project existed at preflight. A later isolated asset viewer outside the repository loaded the workshop and Kaprao on Duo and received live hinge callbacks; see [asset validation](../../DesignAssets/Validation/README.md). This does not validate game physics, connected projection, shared editing or the final audio mix.

Device Hub Settings briefly showed a blurred region after Book, then the same held pose became sharp. Cause, duration and continuous folding remain unmeasured; no blur-disable switch was established. Last observed Sound was 0/Output System. Tomorrow’s first technical gates test actual app rendering, input, audio and physics rather than assuming this preflight proves them.
