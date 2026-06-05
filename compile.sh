#!/bin/bash

# Parsing Flags

git_branch=""
python_version="3"

while getopts "g:p:" flag; do
    case $flag in
        g) git_branch=$OPTARG ;;
        p) python_version=$OPTARG ;;
        *) echo -e "\nUsage: ./compile.sh -g <git branch> -p <python version>\n"; exit 1 ;;
    esac
done

# Removing old executable if it exists

rm -f pwrstat-gui

# Cloning repo if necessary

if [ ! -d "pwrstat-gui-clone" ]; then
    echo -e "\nCloning PwrStat GUI repository from GitHub...\n"
    git clone https://github.com/liam-ralph/pwrstat-gui pwrstat-gui-clone
    if [ ! -z $git_branch ]; then
        cd pwrstat-gui-clone
        git checkout $git_branch
        cd ..
    fi
fi

# Setting up virtual environment if necessary

if [ ! -d "compile-venv" ]; then
    echo -e "\nCreating virtual environment...\n"
    python${python_version} -m venv compile-venv
    compile-venv/bin/python$python_version -m pip install --upgrade pyinstaller pillow setproctitle
    mkdir compile-venv/pyinstaller-files
    cp pwrstat-gui-clone/main.py compile-venv/pyinstaller-files/pwrstat-gui.py
fi

# Compiling using PyInstaller

echo -e "\nCompiling...\n"
cd compile-venv
bin/python3 -m PyInstaller \
    --onefile \
    --distpath=pyinstaller-files/dist --workpath=pyinstaller-files/build \
    --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=tkinter \
    pyinstaller-files/pwrstat-gui.py
cd ..
mv compile-venv/pyinstaller-files/dist/pwrstat-gui pwrstat-gui

echo -e "\nComplete, compile-venv can be removed or reused.\n"