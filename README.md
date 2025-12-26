# PwrStat GUI
### Released July 2025
### Version 1.2.0
### Updated December 2025

<br/>

## Description
A graphical user interface for CyberPower's PowerPanel
Linux software using Python's tkinter library. Runs the
command `sudo pwrstat -status` to gather information from
the UPS. Can also log gathered information in a CSV file.

<br/>

## Requirements
This project requires __CyberPower's PowerPanel for Linux__,
which can be found on
[CyberPower's website](https://www.cyberpowersystems.com/products/software/power-panel-personal/).

### Memory
This application uses approximately 128 KiB of memory.

### Storage
This application uses approximately 15 MiB of storage.

<br/>

## Installation

1. Download the .deb file [here](liam-ralph.github.io/projects/pwrstat-gui).
2. Navigate the folder you downloaded to.
3. Install the file using `apt install ./<file_name>.deb`, replacing
`<file_name>` with the actual .deb file's name.

I have also added a developer package to my website, which includes
a number of other files used to create the .deb package, as well as
some documentation. This is not required to run the project, but may
be useful for those looking to edit it.

<br/>

## Operating System Support

Support is assumed for all debian-based, fedora-based, and arch-based distros.
Some distros may require the Python program to be compiled locally. One example
of this is Pop!_OS, due to its older version of GLIBC. Below is a list of all
distros for which support has been confirmed.

### Debian Based

 - Ubuntu 24.04.3
 - Ubuntu 25.04
 - Linux Mint 22.2
 - Debian 13
 - Pop!_OS 22.04 (v1.1.0+)
 - antiX 23.2 (v1.1.0+, must be started from terminal)
 - MX Linux 23.6

### Fedora Based (all v1.2.0+)

 - Fedora 43 KDE
 - Nobara 42

### Arch Based (all v1.2.0+)

 - EndeavourOS Ganymede
 - Manjaro 25.0.7 KDE
 - CachyOS Desktop 250713