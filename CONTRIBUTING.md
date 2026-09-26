# Working together on Fold & Fetch

This repository is the source of truth for the prompt and resources. Both teammates can clone, pull, edit and push using their own GitHub accounts once repository access is accepted. Windows contributors can edit docs, assets and source; native Xcode/Duo build verification happens on the Mac.

## One master prompt

Edit `Preparation/FoldAndFetch-Bitrig/Master-Prompt.md` in place. Keep `PRD.md`, asset directions and acceptance criteria consistent. Put rationale or evidence in `Preparation/FoldAndFetch-Bitrig/Review/`; do not make a second runnable master. The image-generation prompts under `DesignAssets/Concepts/` document art creation and are not alternative app-build prompts.

During the event run the master through one coordinator. The master defines three worker ownership areas, shared interfaces and integration checkpoints. Do not start independent coordinators in Codex and Bitrig against the same files.

## Small changes with clear ownership

1. Pull the latest `main` before starting. Use a short feature branch for changes that overlap another teammate's work.
2. Agree which files each person or agent owns. Only the coordinator changes shared app configuration and integration contracts during the build.
3. Change a small, reviewable unit. Explain what changed, why, and what was actually checked in the commit or pull request.
4. Open a pull request for overlapping changes and merge after review. Avoid force-pushing shared history. Independent small preparation edits can also be committed directly if teammates agree.
5. Pull merged changes before the next edit. GitHub does not synchronize live keystrokes or refresh an old attached ZIP.

## Asset handling

Keep editable `.blend` sources, exchange formats, native runtime conversions and preview images in their existing separate folders. Preserve licenses/provenance for downloaded sounds and any future third-party art. The private source photo is a design reference, not a runtime resource. Do not bundle entire preparation or source directories into the app.

When an asset changes, refresh its relevant exports, previews and validation together. Record tests that were not run. Native import evidence does not prove full gameplay, optical continuity or real-device performance.

## Event boundary

Submitted game source, tests and scaffolding start during the September 26, 2026 coding window, 11:30–15:30 Pacific. Existing preparation contains design assets, specifications and asset-generation/conversion tools. It does not contain a completed game. Follow the master’s simulator acceptance gates before claiming the demo works.
