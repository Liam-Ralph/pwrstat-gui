#!/bin/bash

# Removing old executable if it exists

rm -f pwrstat-gui

# Cloning repo if necessary

if [ ! -d "pwrstat-gui-clone" ]; then
    echo -e "\nCloning PwrStat GUI repository from GitHub...\n"
    git clone https://github.com/liam-ralph/pwrstat-gui pwrstat-gui-clone
fi

# Setting up virtual environment if necessary

if [ ! -d "compile-venv" ]; then
    echo -e "\nCreating virtual environment...\n"
    python3 -m venv compile-venv
    compile-venv/bin/python3 -m pip install --upgrade pyinstaller pillow setproctitle
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