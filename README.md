# PwrStat GUI
### Released July 2025
### Version 1.1.2
### Updated October 2025

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

This project is confirmed to be compatible with:
 - Ubuntu 24.04.3
 - Ubuntu 25.04
 - Linux Mint 22.1
 - Linux Mint 22.2
 - Debian 13
 - Pop!_OS 22.04 (v1.1.0+)
 - antiX 23.2 (v1.1.0+, must be started from terminal)
 - MX Linux 23.6

Compatibility is assumed for all debian-based distros. Older distros may require
the Python program to be compiled on locally for older versions of GLIBC.