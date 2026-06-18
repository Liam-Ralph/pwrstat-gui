Name: pwrstat-gui
Version: VERSION
Release: %{?dist}
Packager: Liam Ralph <liamralph42@gmail.com>
Summary: A GUI for CyperPower PowerPanel on Linux.

License: GPLv3+
URL: https://github.com/Liam-Ralph/pwrstat-gui
Requires: powerpanel dejavu-sans-fonts polkit
Source0: %{name}-%{version}.tar.gz

%description
A GUI for CyperPower PowerPanel on Linux.

%global debug_package %{nil}

%prep
%autosetup

%install
cp -a * $RPM_BUILD_ROOT/

%clean
rm -rf $RPM_BUILD_ROOT

%files
/usr/bin/pwrstat-gui
/usr/share/applications/pwrstat-gui.desktop
/usr/share/doc/pwrstat-gui/CHANGELOG.md
/usr/share/doc/pwrstat-gui/copyright
/usr/share/doc/pwrstat-gui/README.md
/usr/share/icons/hicolor/512x512/apps/pwrstat-gui.png
/usr/share/icons/hicolor/scalable/pwrstat-gui.svg
/usr/share/licenses/pwrstat-gui/LICENSE
/usr/share/pwrstat-gui/data/info.txt
%config(noreplace) /usr/share/pwrstat-gui/data/settings.txt
/usr/share/pwrstat-gui/images/info.png
/usr/share/pwrstat-gui/images/logo.png
/usr/share/pwrstat-gui/images/settings.png

%changelog
%autochangelog
