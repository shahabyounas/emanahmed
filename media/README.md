# media/

Video used on the landing page. It is the **background of the "What I work on"
section**, not a standalone figure -- see `.sec--reel` in `css/styles.css` for the
panel, the scrim and the palette override that keep the text on top of it
readable.

## `automation-loop.mp4` + `automation-poster.jpg`

A five-shot montage, 20.04 s, **1280x720** (the full source frame), 25 fps, no
audio, H.264, 1.12 MB.

- **Why the full frame, not a wide crop:** `object-fit: cover` has to fill a
  section roughly 1425x1580 at a 1440px viewport, and height is always the
  binding dimension, so the clip is magnified by (section height / clip height).
  An earlier 1280x534 cut meant 2.96x, which looked over-blown in the gutters
  either side of the panel. Keeping all 720 rows brings it to 2.20x for 30% more
  bytes. Mixkit does not serve 1080p for these ids (403), so 720 is the ceiling
  and 2.20x is the floor for a single element covering the whole section.
  Nothing important should sit near the frame edges: at this aspect only the
  middle ~51% of the width is ever on screen.

| # | shot | Mixkit source |
|---|------|---------------|
| 1 | circuit-assembly machine (opens and closes the loop) | [machine-placing-components-on-a-circuit-board-46965](https://mixkit.co/free-stock-video/machine-placing-components-on-a-circuit-board-46965/) |
| 2 | robotic gripper closing on a part | [robotic-arm-in-a-factory-20970](https://mixkit.co/free-stock-video/robotic-arm-in-a-factory-20970/) |
| 3 | pick-and-place gantry over boards | [automated-machine-places-parts-on-circuit-boards-47266](https://mixkit.co/free-stock-video/automated-machine-places-parts-on-circuit-boards-47266/) |
| 4 | data-centre aisle | [bluish-data-center-hallway-23282](https://mixkit.co/free-stock-video/bluish-data-center-hallway-23282/) |
| 5 | drifting field of connected points | [scrambled-dots-and-lines-within-a-sphere-of-dots-31771](https://mixkit.co/free-stock-video/scrambled-dots-and-lines-within-a-sphere-of-dots-31771/) |

- **Licence:** all five are under the [Mixkit Free Stock Video
  licence](https://mixkit.co/license/#videoFree) -- free for commercial and
  non-commercial use on a website, no attribution required, may not be
  redistributed as stock footage.

- **How it loops:** shot 1 is split in half and put at both ends, so the last
  frame and the first frame are consecutive frames of the same continuous take.
  The wrap is therefore a normal one-frame step, not a cut and not a dissolve --
  measured at 27 dB PSNR between them, which is a motion step, where an
  unrelated cut would be 10-15 dB. The four internal transitions are 0.6 s
  dissolves.

- **Grading:** each shot is cropped 1280x534 from the centre of the 720p source
  and pushed cool and slightly desaturated, per-shot, so five different
  cameras read as one piece against the site's palette. Shot 3 is the brightest
  source and is pulled down hardest.

- **Weight:** a five-scene montage costs far more bits than a single shallow-focus
  shot, so this is encoded at crf 39 with a light `hqdn3d` denoise ahead of the
  encoder -- visually indistinguishable from crf 30 on this material at this
  size, and a third of the bytes. Do not raise the quality without checking what
  it does to the page weight.

- **Legibility:** the content sits on `.reel__panel`, a translucent dark surface
  with a backdrop blur, rather than directly on the footage. That is deliberate:
  text laid straight onto a moving clip has contrast that changes shot by shot,
  which reads as wrong even where it technically passes. The panel holds it
  constant, and because it does, the video underneath can stay sharp and close
  to full brightness instead of being dimmed into mud.

  Measured across six points in the loop with the panel's contents hidden, the
  surface under the text stays between 0.011 and 0.027 relative luminance --
  worst case 12.2:1 for `--ink`, 8.0:1 for `--ink-2`, 6.3:1 for `--ink-3`. The
  section forces the dark palette whatever the page theme, since the backdrop is
  dark video either way, and `--ink-3` is set lighter here than the page default.

  If the panel is ever made more transparent, or the scrim lightened, re-measure.
  An earlier version put the text straight on the footage: it passed AA at
  5.2:1, but the small mono type fell to 3.98:1 as soon as the video brightness
  went up 10%, and it looked unsettled the whole way through the loop.

- **Provenance:** stock footage, none of it Eman's instrument, none of it the
  source of any result on this site. The line at the foot of the section says
  so. Keep it if the clip changes.

Rebuild: `/tmp/mont/final.sh` in the session that made it; the same command is
reproduced below. Sources are the `-720.mp4` renditions from `assets.mixkit.co`.

```sh
C="crop=1280:534:0:93,setpts=PTS-STARTPTS,fps=25"
ffmpeg -y \
 -ss 5.90 -t 2.9 -i 46965.mp4 \
 -ss 0.25 -t 4.3 -i 20970.mp4 \
 -ss 3.20 -t 4.3 -i 47266.mp4 \
 -ss 2.40 -t 4.3 -i 23282.mp4 \
 -ss 3.60 -t 4.3 -i 31771.mp4 \
 -ss 3.00 -t 2.9 -i 46965.mp4 \
 -filter_complex "\
[0:v]$C,eq=brightness=0.01:contrast=1.03:saturation=0.92,colorbalance=bs=0.03[v0];\
[1:v]$C,eq=brightness=0.02:contrast=1.04:saturation=0.90,colorbalance=bs=0.04[v1];\
[2:v]$C,eq=brightness=-0.04:contrast=1.05:saturation=0.85,colorbalance=bs=0.06[v2];\
[3:v]$C,eq=brightness=-0.01:contrast=1.02:saturation=0.90,colorbalance=bs=0.02[v3];\
[4:v]$C,eq=brightness=0.02:contrast=1.04:saturation=0.90,colorbalance=bs=0.03[v4];\
[5:v]$C,eq=brightness=0.01:contrast=1.03:saturation=0.92,colorbalance=bs=0.03[v5];\
[v0][v1]xfade=transition=fade:duration=0.6:offset=2.3[x1];\
[x1][v2]xfade=transition=fade:duration=0.6:offset=6.0[x2];\
[x2][v3]xfade=transition=fade:duration=0.6:offset=9.7[x3];\
[x3][v4]xfade=transition=fade:duration=0.6:offset=13.4[x4];\
[x4][v5]xfade=transition=fade:duration=0.6:offset=17.1,hqdn3d=2:1.5:6:6,format=yuv420p[v]" \
 -map "[v]" -an -c:v libx264 -profile:v high -crf 39 -preset veryslow \
 -pix_fmt yuv420p -movflags +faststart automation-loop.mp4
```
