#!/bin/zsh
# Frame-step QA: tiles the guide (top row) against an edited clip (bottom row) at the same frame numbers.
# usage: compare.sh guide.mp4 edit.mp4 out.jpg [step]
set -e
g=$1 e=$2 out=$3 step=${4:-30}
ffmpeg -loglevel error -y -i $g -i $e -filter_complex "\
[0]fps=24,scale=320:180,select='not(mod(n\,${step}))',tile=6x1[a];\
[1]fps=24,scale=320:180:force_original_aspect_ratio=increase,crop=320:180,select='not(mod(n\,${step}))',tile=6x1[b];\
[a][b]vstack" -frames:v 1 $out
