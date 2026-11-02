#!/bin/sh
# 現行サイトのスタッフ動画を、どのブラウザでも再生できる H.264/AAC の MP4 に変換し、サムネイルも作る
# 使い方: sh tools/convert_videos.sh <元動画フォルダ> <出力フォルダ>
src="$1"; dst="$2"
for f in "$src"/*; do
  name=$(basename "${f%.*}")
  case "$name" in kagawa_video202309) name=kagawa;; fujimoto-h_video202311) name=fujimoto-h;; esac
  ffmpeg -v error -y -i "$f" -vf "scale='if(gt(iw,ih),min(960,iw),-2)':'if(gt(iw,ih),-2,min(960,ih))'" \
    -c:v libx264 -preset slow -crf 27 -pix_fmt yuv420p -c:a aac -b:a 96k -movflags +faststart "$dst/$name.mp4"
  ffmpeg -v error -y -ss 1 -i "$dst/$name.mp4" -frames:v 1 -c:v libwebp -quality 75 "$dst/$name.webp"
done
