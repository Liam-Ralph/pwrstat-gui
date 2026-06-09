# Parsing Flags

distro_group=""
python_version=""

while getopts "d:p:" flag; do
    case $flag in
        d) distro_group=$OPTARG ;;
        p) python_version=$OPTARG ;;
        *) echo -e "\nUsage: ./package.sh -d <distro group (debian/fedora/arch)> [-p <python version>]\n"; exit 1 ;;
    esac
done

# Checking for distro group argument

if [ -z $distro_group ]; then
    echo -e "\nMissing required distro group argument (debian, fedora, or arch).\n"
    echo -e "\nUsage: ./package.sh -d <distro group (debian/fedora/arch)> [-p <python version>]\n"
    exit 1
fi

# Installing dependencies by distro group

case $distro_group in

    debian)
        sudo apt update
        sudo apt install git python3-venv python3-tk -y
        if [ ! -z $python_version ]; then
            sudo apt-add-repository ppa:deadsnakes/ppa -y
            sudo apt update
            sudo apt install python$python_version -y
        fi
        ;;

    fedora)
        sudo dnf install git rpmdevtools -y
        ;;

    arch)
        sudo pacman -S git base-devel --noconfirm
        ;;

    *)
        echo -e "\nInvalid distro group argument (must be debian, fedora, or arch).\n"
        exit 1
        ;;

esac