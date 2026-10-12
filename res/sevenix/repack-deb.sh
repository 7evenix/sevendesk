#!/bin/sh
# Repack build.py's rustdesk deb as "sevendesk". The Rust code names the
# binary, systemd unit, tray processes and desktop files after APP_NAME in
# lowercase (src/platform/linux.rs), so they must all be "sevendesk".
# Usage: repack-deb.sh rustdesk-<ver>.deb sevendesk-<ver>-<arch>.deb
set -eu
src=$1
dst=$2
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
dpkg-deb -R "$src" "$work/p"
cd "$work/p"

mv usr/share/rustdesk usr/share/sevendesk
mv usr/share/sevendesk/rustdesk usr/share/sevendesk/sevendesk
mv usr/share/sevendesk/files/systemd/rustdesk.service usr/share/sevendesk/files/systemd/sevendesk.service
sed -i -e 's/rustdesk/sevendesk/g' -e 's/^Description=RustDesk$/Description=SevenDesk/' \
    usr/share/sevendesk/files/systemd/sevendesk.service
for f in rustdesk rustdesk-link; do
    n=$(echo "$f" | sed 's/rustdesk/sevendesk/')
    mv "usr/share/applications/$f.desktop" "usr/share/applications/$n.desktop"
    sed -i 's/rustdesk/sevendesk/g' "usr/share/applications/$n.desktop"
done
mv usr/share/icons/hicolor/256x256/apps/rustdesk.png usr/share/icons/hicolor/256x256/apps/sevendesk.png
mv usr/share/icons/hicolor/scalable/apps/rustdesk.svg usr/share/icons/hicolor/scalable/apps/sevendesk.svg

for s in preinst postinst prerm postrm; do
    [ -f "DEBIAN/$s" ] && sed -i 's/rustdesk/sevendesk/g' "DEBIAN/$s"
done
sed -i 's/^Package: rustdesk$/Package: sevendesk/' DEBIAN/control
# Lists the old paths; regenerated below.
rm -f DEBIAN/md5sums
grep -q '^Package: sevendesk$' DEBIAN/control

if grep -rIl 'rustdesk' usr/share/applications DEBIAN usr/share/sevendesk/files; then
    echo "repack-deb: leftover 'rustdesk' references above" >&2
    exit 1
fi

find . -path ./DEBIAN -prune -o -type f -printf '%P\0' | xargs -0 md5sum > DEBIAN/md5sums
cd - >/dev/null
dpkg-deb --root-owner-group -b "$work/p" "$dst"
