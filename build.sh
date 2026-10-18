#!/bin/bash
# Builds OXAQ-Server-1.0.iso. Run on Debian/Ubuntu (real PC, VM or WSL2) with internet. Takes ~20-40 min.
set -e
[ "$(id -u)" = 0 ] || exec sudo "$0" "$@"
apt-get update && apt-get install -y live-build debootstrap squashfs-tools xorriso
HERE=$(cd "$(dirname "$0")" && pwd)
rm -rf "$HERE/work" && mkdir "$HERE/work" && cd "$HERE/work"
lb config --distribution bookworm --architectures amd64 --binary-images iso-hybrid \
  --debian-installer none --archive-areas "main contrib non-free-firmware" \
  --iso-application "OXAQ Server" --iso-volume "OXAQ_SERVER_1_0" \
  --bootappend-live "quiet loglevel=0 vt.global_cursor_default=0 locales=pl_PL.UTF-8 keyboard-layouts=pl timezone=Europe/Warsaw"
mkdir -p config/includes.chroot config/package-lists config/hooks/live
cp -a "$HERE/overlay/." config/includes.chroot/
cp "$HERE/packages.list" config/package-lists/oxaq.list.chroot
cp "$HERE/0100-oxaq.hook.chroot" config/hooks/live/
lb build
mv ./*.iso "$HERE/OXAQ-Server-1.0.iso"
echo "DONE: $HERE/OXAQ-Server-1.0.iso"
