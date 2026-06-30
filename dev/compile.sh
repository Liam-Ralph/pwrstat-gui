#!/bin/bash

# Removing old executable if it exists

rm -f pwrstat-gui

# Setting up virtual environment if necessary

if [ ! -d "compile-venv" ]; then
    echo -e "\nCreating virtual environment...\n"
    python3 -m venv compile-venv
    compile-venv/bin/python3 -m pip install --upgrade \
        pyinstaller pillow setproctitle tkinterweb markdown
    mkdir compile-venv/pyinstaller-files
    cp ../src/main.py compile-venv/pyinstaller-files/pwrstat-gui.py
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