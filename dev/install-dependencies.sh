# Parsing Flags

distro_group=""
python_version=""

while getopts "d:p:" flag; do
    case $flag in
        d) distro_group=$OPTARG ;;
        p) python_version=$OPTARG ;;
        *) echo -e "Usage: ./package.sh -d <distro group (debian/fedora/arch)> " \
            "[-p <python version>]"; exit 1 ;;
    esac
done

# Checking for distro group argument

if [ -z $distro_group ]; then
    echo -e "Missing required distro group argument (debian, fedora, or arch)."
    echo -e "Usage: ./package.sh -d <distro group (debian/fedora/arch)> [-p <python version>]"
    exit 1
fi

# Installing dependencies by distro group

case $distro_group in

    debian)
        sudo apt update
        sudo apt install git python3-venv python3-tk binutils -y
        ;;

    fedora)
        sudo dnf install git rpmdevtools python3-tkinter binutils -y
        ;;

    arch)
        sudo pacman -S git base-devel tk ttf-dejavu binutils --noconfirm
        ;;

    *)
        echo -e "\nInvalid distro group argument (must be debian, fedora, or arch).\n"
        exit 1
        ;;

esac