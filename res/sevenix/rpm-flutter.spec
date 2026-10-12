# SevenDesk RPM, adapted from res/rpm-flutter.spec. Everything is named "sevendesk": the Rust
# code derives binary, systemd unit, tray processes and desktop files from the lowercase
# APP_NAME (src/platform/linux.rs). Build after `build.py --flutter`:
#   HBB=`pwd` rpmbuild res/sevenix/rpm-flutter.spec -bb --define "sevendesk_version 1.5.1"
Name:       sevendesk
Version:    %{sevendesk_version}
Release:    0
Summary:    SevenDesk, assistenza remota Sevenix
License:    AGPL-3.0-only
URL:        https://sevenix.it
Vendor:     Sevenix <info@sevenix.it>
Requires:   gtk3 libxcb libXfixes alsa-lib libva gstreamer1-plugins-base
Recommends: libayatana-appindicator-gtk3 libxdo
Provides:   libdesktop_drop_plugin.so()(64bit), libdesktop_multi_window_plugin.so()(64bit), libfile_selector_linux_plugin.so()(64bit), libflutter_custom_cursor_plugin.so()(64bit), libflutter_linux_gtk.so()(64bit), libscreen_retriever_plugin.so()(64bit), libtray_manager_plugin.so()(64bit), liburl_launcher_linux_plugin.so()(64bit), libwindow_manager_plugin.so()(64bit), libwindow_size_plugin.so()(64bit), libtexture_rgba_renderer_plugin.so()(64bit)

# https://docs.fedoraproject.org/en-US/packaging-guidelines/Scriptlets/

%description
SevenDesk, assistenza remota Sevenix. Based on RustDesk (https://github.com/rustdesk/rustdesk).

%prep
# we have no source, so nothing here

%build
# we have no source, so nothing here

%install

mkdir -p "%{buildroot}/usr/share/sevendesk" && cp -r ${HBB}/flutter/build/linux/x64/release/bundle/* -t "%{buildroot}/usr/share/sevendesk"
mv "%{buildroot}/usr/share/sevendesk/rustdesk" "%{buildroot}/usr/share/sevendesk/sevendesk"
mkdir -p "%{buildroot}/usr/bin" "%{buildroot}/usr/share/sevendesk/files"
sed -e 's/rustdesk/sevendesk/g' -e 's/^Description=RustDesk$/Description=SevenDesk/' $HBB/res/rustdesk.service > "%{buildroot}/usr/share/sevendesk/files/sevendesk.service"
sed 's/rustdesk/sevendesk/g' $HBB/res/rustdesk.desktop > "%{buildroot}/usr/share/sevendesk/files/sevendesk.desktop"
sed 's/rustdesk/sevendesk/g' $HBB/res/rustdesk-link.desktop > "%{buildroot}/usr/share/sevendesk/files/sevendesk-link.desktop"
install -Dm 644 $HBB/res/128x128@2x.png "%{buildroot}/usr/share/icons/hicolor/256x256/apps/sevendesk.png"
install -Dm 644 $HBB/res/scalable.svg "%{buildroot}/usr/share/icons/hicolor/scalable/apps/sevendesk.svg"

%files
/usr/share/sevendesk/*
/usr/share/sevendesk/files/sevendesk.service
/usr/share/icons/hicolor/256x256/apps/sevendesk.png
/usr/share/icons/hicolor/scalable/apps/sevendesk.svg
/usr/share/sevendesk/files/sevendesk.desktop
/usr/share/sevendesk/files/sevendesk-link.desktop

%changelog
# let's skip this for now

%pre
case "$1" in
  1)
    # for install
  ;;
  2)
    # for upgrade
    systemctl stop sevendesk || true
  ;;
esac

%post
cp /usr/share/sevendesk/files/sevendesk.service /etc/systemd/system/sevendesk.service
cp /usr/share/sevendesk/files/sevendesk.desktop /usr/share/applications/
cp /usr/share/sevendesk/files/sevendesk-link.desktop /usr/share/applications/
ln -sf /usr/share/sevendesk/sevendesk /usr/bin/sevendesk
systemctl daemon-reload
systemctl enable sevendesk
systemctl start sevendesk
update-desktop-database

%preun
case "$1" in
  0)
    # for uninstall
    systemctl stop sevendesk || true
    systemctl disable sevendesk || true
    rm /etc/systemd/system/sevendesk.service || true
  ;;
  1)
    # for upgrade
  ;;
esac

%postun
case "$1" in
  0)
    # for uninstall
    rm /usr/bin/sevendesk || true
    rmdir /usr/share/sevendesk || true
    rm /usr/share/applications/sevendesk.desktop || true
    rm /usr/share/applications/sevendesk-link.desktop || true
    update-desktop-database
  ;;
  1)
    # for upgrade
  ;;
esac
