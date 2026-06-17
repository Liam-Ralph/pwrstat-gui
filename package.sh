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
        *) echo -e "Usage: ./package.sh -d <distro group (debian/fedora/arch)> [-l]"; exit 1 ;;
    esac
done

# Checking for distro group argument

if [ -z $distro_group ]; then
    echo -e "Missing required distro group argument (debian, fedora, or arch)."
    echo -e "Usage: ./package.sh -d <distro group (debian/fedora/arch)> [-l]"
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
done < pwrstat-gui-clone/README.md

# Creating package structure

case $distro_group in

    debian)

        # Setting build path
        build_path="package-build/pwrstat-gui_${version}_x86_64"
        if [ $lts_flag == true ]; then
            build_path="package-build/pwrstat-gui_${version}_lts_x86_64"
        fi

        mkdir -p $build_path

        # Creating source
        copy_usr_resources $build_path

        # DEBIAN
        mkdir $build_path/DEBIAN
        cp -r resources/debian/* $build_path/DEBIAN/
        sed -i -e "s/VERSION/$version/g" $build_path/DEBIAN/control
        sed -i -e "s/INSTALLED_SIZE/$(du -s $build_path/usr | awk '{print $1}')/g" \
            $build_path/DEBIAN/control

        # Building package
        dpkg -b $build_path
        mv $build_path.deb ${build_path:14}.deb

        ;;

    fedora)

        # Setting build path
        mkdir -p package-build/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
        rpmbuild_path="package-build/rpmbuild"

        # Creating source
        source_dir="pwrstat-gui-$version"
        mkdir $rpmbuild_path/SOURCES/$source_dir
        copy_usr_resources $rpmbuild_path/SOURCES/$source_dir
        cd $rpmbuild_path/SOURCES/
        tar -czf $source_dir.tar.gz $source_dir
        cd ../../../

        # SPECS
        cp resources/fedora/pwrstat-gui.spec $rpmbuild_path/SPECS/pwrstat-gui.spec
        sed -i -e "s/VERSION/$version/g" $rpmbuild_path/SPECS/pwrstat-gui.spec
        sed -i -e \
            "s/CHANGELOG/\"* ${date +"%a %b %d %Y"} Liam Ralph <liamralph42@gmail.com>$version\n" \
            "- Available in app or on GitHub.\"/g" \
            $rpmbuild_path/SPECS/pwrstat-gui.spec

        # Building package
        rpmbuild -bb $rpmbuild_path/SPECS/pwrstat-gui.spec
        if [ $lts_flag == true ]; then
            mv $rpmbuild_path/RPMS/x86_64/pwrstat-gui-*.rpm ./pwrstat-gui_${version}_lts_x86_64.rpm
        else
            mv $rpmbuild_path/RPMS/x86_64/pwrstat-gui-*.rpm ./pwrstat-gui_${version}_x86_64.rpm
        fi

        ;;

    arch)

        # Setting build path
        build_path="package-build"
        mkdir $build_path

        # Creating source
        mkdir $build_path/pwrstat-gui-$version
        copy_usr_resources $build_path/pwrstat-gui-$version
        cd $build_path
        tar -czf pwrstat-gui-$version.tar.gz pwrstat-gui-$version
        rm -rf pwrstat-gui-$version
        cd ..

        # PKGBUILD
        cp resources/arch/PKGBUILD $build_path/PKGBUILD
        sed -i -e "s/VERSION/$version/g" $build_path/PKGBUILD
        sha256sum=$(sha256sum $build_path/pwrstat-gui-$version.tar.gz | awk '{print $1}')
        sed -i -e "s/SHA256SUM/$sha256sum/g" $build_path/PKGBUILD

        # Building package
        cd $build_path
        makepkg
        cd ..
        if [ $lts_flag == true ]; then
            mv $build_path/pwrstat-gui-*.pkg.tar.zst ./pwrstat-gui_${version}_lts_x86_64.pkg.tar.zst
        else
            mv $build_path/pwrstat-gui-*.pkg.tar.zst ./pwrstat-gui_${version}_x86_64.pkg.tar.zst
        fi

        ;;

    *)
        echo -e "\nInvalid distro group argument (must be debian, fedora, or arch).\n"
        exit 1
        ;;

esac