# PwrStat GUI
### Released July 2025
### Version 1.2.0
### Updated January 2026

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
It also requires the DejaVu Sans font family. This is
included by default with most distros, and will be
installed when missing.

### Memory
This application uses approximately 128 KiB of memory.

### Storage
This application uses approximately 19 MiB of storage. Slightly more storage
will be used during installation. Debian-based distros also require
`fonts-dejavu-core`, which is usually installed by default, and takes about 2
MiB. Fedora-based distros also require `dejavu-sans-fonts`, which takes about
6 MiB.

<br/>

## Installation

1. Download the appropriate file
   [here](liam-ralph.github.io/projects/pwrstat-gui).
2. Navigate the folder you downloaded to.
3. Install the package file, either from the terminal or your distro's GUI.

I have also added two developer packages to my website, which include
a number of other files used to create the .deb and .rpm packages, as
well as some documentation. These are not required to install the package,
but may be useful for those looking to edit it.

<br/>

## Operating System Support

Support is assumed for all Debian- and Fedora-based distros. Below is a list of
all distros for which support has been confirmed.

### Debian Based

 - Ubuntu 24.04.3
 - Ubuntu 25.04
 - Linux Mint 22.2
 - Debian 13
 - MX Linux 23.6
 - Pop!_OS 24.04

Pop!_OS 22.04 is no longer supported as of version 1.2.0, but you can compile
the executable yourself (for instructions, see the developer package). antiX is
not supported, as the required dependency powerpanel will not install.

### Fedora Based

Version 1.2.0+
 - Fedora 43
 - Nobara 43