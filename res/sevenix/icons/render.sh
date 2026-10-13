#!/bin/sh
set -eu
F=$1; O=$2; R=$3   # font, svg dir, repo root
python3 -I /tool/gen.py "$F" "$O"
r() { rsvg-convert -w "$2" -h "$2" "$O/$1.svg" -o "$3"; }
cd "$R"
for f in flutter/assets/icon.svg res/logo.svg res/scalable.svg; do cp "$O/square.svg" "$f"; done
r square 1024 res/icon.png; r mac 1024 res/mac-icon.png
r square 32 res/32x32.png; r square 64 res/64x64.png; r square 128 res/128x128.png; r square 256 res/128x128@2x.png
r black 60 res/mac-tray-dark-x2.png; r black 48 res/mac-tray-light-x2.png
t=$(mktemp -d)
for s in 16 24 32 48 64 128 256; do r square $s $t/$s.png; done
magick $t/16.png $t/32.png $t/48.png $t/64.png $t/128.png $t/256.png res/icon.ico
magick $t/16.png $t/24.png $t/32.png $t/48.png $t/64.png $t/128.png $t/256.png flutter/windows/runner/resources/app_icon.ico
magick $t/16.png $t/24.png $t/32.png res/tray-icon.ico
for s in 16 32 48 128 256 512 1024; do r mac $s $t/m$s.png; done
png2icns flutter/macos/Runner/AppIcon.icns $t/m16.png $t/m32.png $t/m48.png $t/m128.png $t/m256.png $t/m512.png $t/m1024.png >/dev/null
A=flutter/android/app/src/main/res
for d in mdpi:1 hdpi:1.5 xhdpi:2 xxhdpi:3 xxxhdpi:4; do
  n=${d%%:*}; k=${d#*:}
  px() { python3 -c "print(round($1*$k))"; }
  r square $(px 48) $A/mipmap-$n/ic_launcher.png
  r round $(px 48) $A/mipmap-$n/ic_launcher_round.png
  r foreground $(px 108) $A/mipmap-$n/ic_launcher_foreground.png
  r white $(px 24) $A/mipmap-$n/ic_stat_logo.png
done
r square 512 fastlane/metadata/android/en-US/images/icon.png
