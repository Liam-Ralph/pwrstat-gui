#!/bin/bash

# Parsing Flags

while getopts "c" flag; do
    case $flag in
        c) rm -rf compile-venv ;;
        *) 
            echo -e "Usage: ./compile.sh [-c] <remove PyInstaller files before compilation>\n"
            exit 1 ;;
    esac
done

# Setting up virtual environment if necessary

if [ ! -d "compile-venv" ]; then
    echo -e "\nCreating virtual environment...\n"
    python3 -m venv compile-venv
    compile-venv/bin/python3 -m pip install --upgrade \
        pyinstaller pillow setproctitle tkinterweb markdown
    mkdir compile-venv/pyinstaller-files
fi

# Compiling using PyInstaller

echo -e "\nCompiling...\n"
cp ../src/main.py compile-venv/pyinstaller-files/pwrstat-gui.py
cd compile-venv
bin/python3 -m PyInstaller \
    --onefile \
    --distpath=pyinstaller-files/dist --workpath=pyinstaller-files/build \
    --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=tkinter \
    pyinstaller-files/pwrstat-gui.py
cd ..
mv compile-venv/pyinstaller-files/dist/pwrstat-gui pwrstat-gui

echo -e "\nComplete, compile-venv can be removed or reused.\n"