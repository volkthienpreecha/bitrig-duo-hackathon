# Direct preflight observations — September 25, 2026

> Historical review / September 25 observations. Current master v1.2, stage/v3 handoffs and the September 26 preparation-readiness report supersede old asset-availability, scope, path and draft-composer statements. This report is not fresh build or gameplay evidence.

These observations were made through the actual Mac applications during the red-team review. They are not results from a game prototype; no game exists yet.

## Bitrig

- The prior New Project draft contained the older stop-after-prototype prompt and the handoff ZIP.
- File menu exposes Open Project and Open Folder, as well as GitHub import/export options.
- File → Open Folder successfully opened `/Users/volkthienpreecha/Documents/ChatGPT/Bitrig Duo Hackathon`.
- The resulting window is named Bitrig Duo Hackathon. Its Source Files view displays the matching repository README.
- The built-in preview says: No Project File — this project does not contain a project file to build.
- The project shows pull-request/branch status unavailable. Local folder opening does not depend on proving Bitrig's GitHub integration.
- Opening and reading the folder are verified. After an external README edit, Bitrig displayed the new execution-kit section. That proves this document refreshed; bidirectional app-source editing/build and packaged resource loading remain unverified.
- No Bitrig subagent-spawning interface was established. Codex's parallel-agent tools are available and were used for this review. Do not assume a prompt alone creates parallel agents in another host.

## Device Hub

- The iPhone Duo simulator is booted on iOS 27.1. Built-in Settings launches and displays readable text.
- In a tall inner-display orientation, the Open pose showed both Settings regions sharp.
- Immediately after choosing Book, a screenshot showed the upper region strongly blurred while the lower region stayed readable.
- A later screenshot, without another pose change, showed that same Book pose sharp. Thus the observed effect was transient in this case. Exact duration, rendering layer, behavior during continuous interactive folding, and behavior of a custom game are unmeasured.
- An earlier wide-orientation test likewise captured one blurred Settings pane after Book. Neither observation proves an app-wide permanent blur policy.
- The Controls menu includes ordinary device actions, rotation, screenshots, and recording. No blur opt-out was established there.
- The inspector exposes Reduce Motion (off), Reduce Transparency (off), and a Sound slider currently at 0 with Output set to System. No preference was changed. The effect of Reduce Motion on this transition is untested. A silent audio test must check simulator volume/output before blaming the assets.

## Repository and assets

- The existing checkout is on main tracking origin/main, with Preparation/ untracked. No Swift source or Xcode project was found during this preflight.
- Runtime installation/download is complete; the older root README's download-in-progress statement is stale and will be corrected as part of this handoff.
- Eight real WAV effects and their creator licenses are present. File decoding/format checks passed earlier; in-game loading, event timing, and subjective mix remain untested.
- No user-supplied workshop or corgi runtime model is present. A recognizable primitive corgi must be the build's fallback.

## Evidence still required tomorrow

Actual app build/run; continuous live hinge callbacks; gesture delivery inside a folded preview; one-mouse operation; world/physics/projection alignment; fold-causes-miss-versus-land comparison; stable bridge support; blur during continuous folding and settling; audio through the demo output; complete reset/replay; clean saved-build launch. None can be marked passing from this preflight alone.

## Final handoff UI state

- The entire 26,457-character Master-Prompt.md was placed in the existing Bitrig Duo Hackathon folder’s New Conversation composer. Its complete text was matched against the saved file through the accessibility state, and remained intact after switching away and back.
- Send was not pressed. There is no generated app or claimed game test.
- The older New Project prototype draft and its stale attachment were removed; that composer is empty and Send disabled.
- The root repository README now states the runtime is installed and links to the unified master. Its externally edited contents were observed in Bitrig’s Source Files view.
- Recommended execution host remains Codex for genuine parallel agents. The staged Bitrig draft is an alternative entry point; execute only one copy. Bitrig agent tools remain unverified.
