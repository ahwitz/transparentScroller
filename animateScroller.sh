#!/bin/bash
join()
{
local IFS="$1"; shift; echo "$*";
}

usage()
{
cat << EOF
usage: $0 options

This script creates an animated scrolling Prores 4444 movie with transparent backgroud from an input PDF or series of PNGs.

OPTIONS
   -h       Show this message
   -s(opt)  FPS for FFMPEG, defaults to 30 fps
   -o(req)  Output filename WITHOUT EXTENSION. This will add .mov automatically
   -i(req)  Input files, either one PDF or a bunch of pngs, filenames separated by spaces
EOF
}

SPEED=30
OUTPUT=""

while getopts “hs:o:i:” OPT; do
  case $OPT in
    h) 
      usage
      exit 1;;
    s) 
      SPEED=$OPTARG;;
    o)
      OUTPUT=$OPTARG
  esac
done
shift $(( OPTIND - 2 ))

filesArr=()
for file in "$@"; do
  filesArr+=($file)
done

filenames=$(printf " %s" "${filesArr[@]}")
filenames=${filenames:1}

echo "Running python script on $filenames"
source /Users/vp2/VideoProd_Assets/TransparentScrollerScript/scrollerEnv/bin/activate
python /Users/vp2/VideoProd_Assets/TransparentScrollerScript/scroller.py -t $OUTPUT $filenames
if [ $? == 1 ]
  then
    echo "Error in python - aborting."
    exit 1
fi

OUTPUT_FILE=$OUTPUT".mov"

echo "Running ffmpeg on contents of imgout"
ffmpeg -framerate $SPEED -i /Users/vp2/VideoProd_Assets/TransparentScrollerScript/$OUTPUT/frame%05d.png -vcodec prores_ks -pix_fmt yuva444p10le $OUTPUT_FILE

if [ $? == 1 ]
  then
    echo "Error in ffmpeg - aborting."
    exit 1
fi

echo "Cleaning up…"
deactivate
#rm -rf /Users/vp2/VideoProd_Assets/TransparentScrollerScript/$OUTPUT
exit 0
