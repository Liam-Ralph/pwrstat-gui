#!/bin/bash

# Checking for distro group argument
if (( $# == 0 )); then
    echo -e "\nMissing required distro group argument (debian, fedora, or arch).\n"
    exit 1
fi

# Removing old build if necessary
rm -rf package-build

# Checking for executable
if [ ! -e "pwrstat-gui" ]; then
    echo -e "\nExecutable not found, running compile.sh...\n"
    ./compile.sh
fi

# Cloning repo if necessary
if [ ! -d "pwrstat-gui-clone" ]; then
    echo -e "\nCloning PwrStat GUI repository from GitHub...\n"
    git clone https://github.com/liam-ralph/pwrstat-gui pwrstat-gui-clone
fi

# Getting version from repo README
while read p; do
    if [[ $p == "### Version "* ]]; then
        version=${p:12}
        break
    fi
done <pwrstat-gui-clone/README.md

# Creating package structure

# Debian
if [ $1 == "debian" ]; then
    build_path="package-build/debian/pwrstat-gui_${version}_x86_64"
    if [[ $* == *"--lts"]]; then
        build_path="package-build/debian/pwrstat-gui_${version}-lts_x86_64"
    fi
    mkdir -p $build_path
    cp -r resources/debian/* $build_path
    mkdir -p $build_path/usr/{bin/,share/pwrstat-gui/}
    cp pwrstat-gui $build_path/usr/bin/
    sed -i -e "s/VERSION/$version/g" $build_path/DEBIAN/control
    sed -i -e "s/VERSION/$version/g" $build_path/usr/share/applications/pwrstat-gui.desktop
    cp pwrstat-gui-clone/README.md $build_path/usr/share/doc/pwrstat-gui/README.md
    cp pwrstat-gui-clone/CHANGELOG.md $build_path/usr/share/doc/pwrstat-gui/CHANGELOG.md
    cp -r pwrstat-gui-clone/data $build_path/usr/share/pwrstat-gui/
    cp -r pwrstat-gui-clone/images $build_path/usr/share/pwrstat-gui/
    dpkg -b $build_path
    mv $build_path.deb pwrstat-gui_${version}_x86_64.deb

# Fedora
elif [ $1 == "fedora" ]; then
    mkdir -p package-build/fedora/

# Arch
elif [ $1 == "arch" ]; then
    mkdir -p package-build/arch/

# Invalid
else
    echo -e "\nInvalid distro group argument (must be debian, fedora, or arch).\n"
    exit 1
fi