# Fold & Fetch — audio starter kit

Eight downloaded and converted sound effects, ready to add as native app resources. Prepared September 25, 2026. This folder contains assets and documentation only; it does not implement playback or establish that Bitrig has imported them.

## Files and intended use

All playable files are **44,100 Hz, mono, 16-bit PCM WAV**. Total WAV size: approximately 206 KiB. Source names describe the creator's original sounds; their gameplay assignments below are our proposed use.

| Delivered file | Trigger | Duration | Original file | Pack | Suggested starting volume |
|---|---|---:|---|---|---:|
| `step_soft.wav` | Corgi foot contact, only while grounded and moving | 0.145 s | `Audio/footstep_carpet_000.ogg` | Impact Sounds | 0.15 |
| `jump.wav` | Successful jump, not every swipe | 0.186 s | `Audio/maximize_007.ogg` | Interface Sounds | 0.35 |
| `land_soft.wav` | Airborne corgi contacts ground | 0.118 s | `Audio/impactSoft_medium_000.ogg` | Impact Sounds | 0.30 |
| `dash_down.wav` | Accepted downward dash | 0.186 s | `Audio/minimize_007.ogg` | Interface Sounds | 0.35 |
| `mechanism_release.wav` | Chute latch opens and releases the piece | 0.618 s | `Audio/switch_001.ogg` | Interface Sounds | 0.40 |
| `bridge_land.wav` | Bridge piece makes a meaningful collision | 0.779 s | `Audio/impactPlank_medium_000.ogg` | Impact Sounds | 0.45 |
| `success.wav` | Corgi reaches the goal after solving the puzzle | 0.290 s | `Audio/confirmation_001.ogg` | Interface Sounds | 0.55 |
| `retry.wav` | Player intentionally resets the puzzle | 0.064 s | `Audio/back_001.ogg` | Interface Sounds | 0.25 |

Volumes are proposed linear playback gains, not an already implemented mix. Jump and dash are short interface-style movement cues, not realistic animal sounds. Success is a brief confirmation rather than a musical fanfare. There is no background music in this kit.

## Creator, sources, and license

**Creator/distributor for every file: Kenney (www.kenney.nl).** Both packs identify their license as **Creative Commons Zero (CC0 1.0)**. Attribution is not required by the included licenses; a courteous credit is `Sound effects by Kenney — kenney.nl (CC0)`.

- [Impact Sounds official asset page](https://kenney.nl/assets/impact-sounds)
- [Impact Sounds exact downloaded archive](https://kenney.nl/media/pages/assets/impact-sounds/87b4ddecda-1677589768/kenney_impact-sounds.zip)
- [Interface Sounds official asset page](https://kenney.nl/assets/interface-sounds)
- [Interface Sounds exact downloaded archive](https://kenney.nl/media/pages/assets/interface-sounds/fa43c1dd4d-1677589452/kenney_interface-sounds.zip)
- [CC0 1.0 dedication](https://creativecommons.org/publicdomain/zero/1.0/)

The `Sources/` folder preserves the eight original OGG files and the **unaltered license text distributed inside each archive**:

- `Kenney-impact-License.txt`
- `Kenney-interface-License.txt`

The source archives were downloaded directly from the official creator website. No paid account, external upload, or third-party mirror was used.

## Modifications and verification

Each source was decoded from Ogg Vorbis, mixed to mono by averaging channels, and exported to PCM WAV at its original 44.1 kHz sample rate. Gain was reduced so each file peaks at approximately -3 dBFS. No trimming, pitch shift, rearrangement, or extra sound generation was performed.

`Sources/Verification.json` records original filenames, duration, sample rate, exact applied gain, output peak, byte size, and SHA-256 checksums. Every WAV was decoded and checked to contain non-silent PCM samples; all have one channel and a 16-bit sample width. This verifies the files, not their subjective fit or playback inside the future game. **Audition the mix in Bitrig/Xcode before the demo.**

## Integration handoff for Bitrig

When implementation is permitted, add only the eight root-level WAV files to the app target's bundled resources. Keep `Sources/` and this manifest in project documentation; they do not need to ship in the app. Load assets by exact filename and preload the short effects so the first jump or impact does not stall.

Sound follows accepted gameplay events. A rejected swipe should not play a jump. A piece settling across many physics frames should not repeatedly retrigger the bridge sound. Use an impact-strength threshold and a short cooldown, then tune by listening. Keep corgi steps much quieter than the main bridge impact. Avoid adding a constant hinge sound: continuous angle updates should not create hundreds of audio events.

Gameplay must remain understandable with sound muted. Provide one simple sound toggle; confirm mute, reset, and background/resume do not leave a sound running or unexpectedly replay a victory cue. Verify playback through the actual demo output route when that route is available.
