#!/bin/zsh
set -e
R=${0:A:h:h:h}
I=$R/public/img
O=$R/assets-src/video/ph
mkdir -p $O
FPS=24
seg() { # name src prefilter frames z0 z1 fx0 fx1 fy0 fy1
  local n=$1 src=$2 pre=$3 N=$4 z0=$5 z1=$6 fx0=$7 fx1=$8 fy0=$9 fy1=${10}
  local t="(on/(${N}-1))"; local e="(0.5-0.5*cos(PI*$t))"
  ffmpeg -loglevel error -y -loop 1 -i $src -vf "${pre}scale=5120:2880:flags=lanczos,zoompan=z='$z0+($z1-$z0)*$e':x='($fx0+($fx1-$fx0)*$e)*iw-iw/zoom/2':y='($fy0+($fy1-$fy0)*$e)*ih-ih/zoom/2':d=${N}:s=1280x720:fps=${FPS},format=yuv420p" -frames:v ${N} -c:v libx264 -crf 16 -preset medium -an $O/$n.mp4
}
seg S1 $I/hero-rooftop.webp ""                   132 1.04 1.22 0.5 0.52 0.62 0.44
seg S2 $I/skyline-dusk.webp ""                   180 1.00 1.32 0.5 0.5  0.5  0.56
seg S3 $I/location.webp "crop=1600:900:0:330,"   180 1.02 1.16 0.52 0.62 0.5 0.46
seg S4 $I/loggia.webp ""                         132 1.00 1.70 0.5 0.5  0.5  0.54
seg S5 $I/interior-living.webp ""                132 1.00 1.18 0.5 0.46 0.5 0.55
seg S6 $I/interior-living.webp ""                120 1.18 1.18 0.46 0.56 0.55 0.55
# crossfades of 12 frames (0.5 s); offsets = cumulative length - 0.5*k
ffmpeg -loglevel error -y -i $O/S1.mp4 -i $O/S2.mp4 -i $O/S3.mp4 -i $O/S4.mp4 -i $O/S5.mp4 -i $O/S6.mp4 -filter_complex "\
[0][1]xfade=transition=fade:duration=0.5:offset=5.0[a];\
[a][2]xfade=transition=fade:duration=0.5:offset=12.0[b];\
[b][3]xfade=transition=fade:duration=0.5:offset=19.0[c];\
[c][4]xfade=transition=fade:duration=0.5:offset=24.0[d];\
[d][5]xfade=transition=fade:duration=0.5:offset=29.0,format=yuv420p[v]" -map "[v]" -an -r 24 -c:v libx264 -profile:v high -crf 27 -g 6 -bf 0 -pix_fmt yuv420p -movflags +faststart $R/assets-src/video/placeholder.mp4
ffprobe -v error -select_streams v -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames,duration -of compact $R/assets-src/video/placeholder.mp4
ls -l $R/assets-src/video/placeholder.mp4
