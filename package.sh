#!/bin/bash

# Checking for distro group argument
if (( $# != 1 )); then
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
    mkdir -p package-build/debian/pwrstat-gui_${version}_x86_64/

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