#!/bin/bash

# Funtions

copy_usr_resources() {

    # Copy resources
    cp -r resources/common/* $1
    mkdir -p $1/usr/{bin/,share/pwrstat-gui/} # Empty dirs won't exist in repo

    # /usr/bin
    cp pwrstat-gui $1/usr/bin/

    # /usr/share/applications
    sed -i -e "s/VERSION/$version/g" $1/usr/share/applications/pwrstat-gui.desktop

    # /usr/share/doc/pwrstat-gui
    cp pwrstat-gui-clone/README.md $1/usr/share/doc/pwrstat-gui/README.md
    cp pwrstat-gui-clone/CHANGELOG.md $1/usr/share/doc/pwrstat-gui/CHANGELOG.md

    # /usr/share/pwrstat-gui
    cp -r pwrstat-gui-clone/data $1/usr/share/pwrstat-gui/
    cp -r pwrstat-gui-clone/images $1/usr/share/pwrstat-gui/

}


# Parsing Flags

distro_group=""
lts_flag=false

while getopts "d:l" flag; do
    case $flag in
        d) distro_group=$OPTARG ;;
        l) lts_flag=true ;;
        *) echo -e "\nUsage: ./package.sh -d <distro group (debian/fedora/arch)> [-l]\n"; exit 1 ;;
    esac
done

# Checking for distro group argument

if [ -z $distro_group ]; then
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

case $distro_group in

    debian)

        # Setting build path
        build_path="package-build/debian/pwrstat-gui_${version}_x86_64"
        if [ $lts_flag == true ]; then
            build_path="package-build/debian/pwrstat-gui_lts_${version}_x86_64"
        fi

        mkdir -p $build_path

        # DEBIAN
        cp -r resources/debian/* $build_path/DEBIAN/
        sed -i -e "s/VERSION/$version/g" $build_path/DEBIAN/control

        # Creating source
        copy_usr_resources $build_path

        # Building package
        dpkg -b $build_path
        mv $build_path.deb ${build_path:21}.deb

        ;;

    fedora)

        # Setting build path
        mkdir -p package-build/fedora/
        cd package-build/fedora/
        rpmdev-setuptree
        cd ../../
        rpmbuild_path="package-build/fedora/rpmbuild"

        # SPECS
        cp resources/fedora/pwrstat-gui.spec $rpmbuild_path/SPECS/pwrstat-gui.spec
        sed -i -e "s/VERSION/$version/g" $rpmbuild_path/SPECS/pwrstat-gui.spec

        # Creating source
        source_dir="pwrstat-gui-$version"
        mkdir $rpmbuild_path/SOURCES/$source_dir
        copy_usr_resources $rpmbuild_path/SOURCES/$source_dir
        cd $rpmbuild_path/SOURCES/
        tar -czf $source_dir.tar.gz $source_dir
        cd ../../../

        # Building package
        rpmbuild -bb $rpmbuild_path/SPECS/pwrstat-gui
        mv $rpmbuild_path/RPMS/x86_64/pwrstat-gui-*.rpm package-build/fedora/

        ;;

    arch)

        mkdir -p package-build/arch/
    
        ;;

    *)
        echo -e "\nInvalid distro group argument (must be debian, fedora, or arch).\n"
        exit 1
        ;;

esac