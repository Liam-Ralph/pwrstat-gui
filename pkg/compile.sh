#!/bin/bash

# Parsing Flags

clean=0

while getopts "c" flag; do
    case $flag in
        c) (( clean++ )) ;;
        *)
            echo -e "Usage: ./compile.sh\n" \
                "    [-c] <remove PyInstaller files before compilation>\n" \
                "    [-cc] <remove compile-venv before compilation"
            exit 1 ;;
    esac
done

if [ -d "compile-venv" ]; then
    if (( clean == 1 )); then
        echo "Remove pyinstaller files"
        rm -rf compile-venv/{pyinstaller-files,pwrstat-gui.spec}
        ls compile-venv
    elif (( clean == 2 )); then
        rm -rf compile-venv
    fi
fi

# Setting up virtual environment if necessary

if [ ! -d "compile-venv" ]; then
    echo -e "\nCreating virtual environment...\n"
    python3 -m venv compile-venv
    compile-venv/bin/python3 -m pip install --upgrade \
        pyinstaller pillow setproctitle tkinterweb markdown
fi

if [ ! -d "compile-venv/pyinstaller-files" ]; then
    mkdir compile-venv/pyinstaller-files
fi

# Compiling using PyInstaller

echo -e "\nCompiling...\n"
cp ../src/main.py compile-venv/pyinstaller-files/pwrstat-gui.py
cd compile-venv
bin/python3 -m PyInstaller \
    --onefile --optimize=2 --strip \
    --distpath=pyinstaller-files/dist --workpath=pyinstaller-files/build \
    --hidden-import=PIL --hidden-import=PIL._tkinter_finder --hidden-import=tkinter \
    pyinstaller-files/pwrstat-gui.py
cd ..
mv compile-venv/pyinstaller-files/dist/pwrstat-gui pwrstat-gui

echo -e "\nComplete, compile-venv can be removed or reused.\n"