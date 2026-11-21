#!/bin/zsh
# Same-scale geometry check: guide (left) vs edit (right) at the given frames, both scaled to 960×540,
# with horizontal grid lines every 5 % of frame height (left = guide, right = edit; rows top→bottom = the frames given) to read base/top rows.
# usage: measure.sh guide.mp4 edit.mp4 out.jpg [frames...]   (default frames: 36 90 144 179)
set -e
g=$1 e=$2 out=$3; shift 3
fr=($@); (( ${#fr} )) || fr=(36 90 144 179)
grid="drawgrid=w=iw:h=ih/20:t=1:c=cyan@0.45"
rows=()
for f in $fr; do
  rows+=("[0]select='eq(n\,${f})',scale=960:540,${grid}[g${f}];[1]fps=24,select='eq(n\,${f})',scale=960:540,${grid}[e${f}];[g${f}][e${f}]hstack[r${f}]")
done
fc="${(j:;:)rows};$(for f in $fr; do printf "[r$f]"; done)vstack=inputs=${#fr}"
ffmpeg -loglevel error -y -i $g -i $e -filter_complex "$fc" -frames:v 1 $out
