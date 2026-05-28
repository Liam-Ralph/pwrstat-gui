# PwrStat GUI
### Released July 2025
### Version 1.3.0
### Updated May 2026

<br/>

## Description
A graphical user interface for CyberPower's PowerPanel
Linux software using Python's tkinter library. Runs the
command `sudo pwrstat -status` to gather information from
the UPS. Can also log gathered information in a CSV file.
Not affiliated with CyberPower.

<br/>

## Requirements

This project requires __CyberPower's PowerPanel for Linux__,
which can be found on
[CyberPower's website](https://www.cyberpowersystems.com/products/software/power-panel-personal/).
It also requires the DejaVu Sans font family. This is
included by default with most distros, and will be
installed when missing.

### Memory
This application uses approximately 256 KiB of memory.

### Storage

Debian-based
19 MiB
Dependencies: fonts-dejavu-core (2 MiB)

Fedora-based
22 MiB
Dependencies: fonts-dejavu-core (6 MiB)

Arch-based
XX MiB
Dependencies: fonts-dejavu-core (X MiB)

<br/>

## Installation

Packages can be found either on this respository's GitHub page under released,
or in the AUR for Arch-based distros.

## Development

I have added some developer packages on
[GitHub](https://github.com/liam-ralph/pwrstat-gui-dev-pkg). These include the
files used to create packages and some documentation.

<br/>

## Operating System Support

Support is assumed for all distros based on Debian, Fedora, and Arch. Below is a
list of distros with confirmed support.

### Debian Based

 - Ubuntu 24.04.3
 - Ubuntu 25.04
 - Linux Mint 22.3
 - Debian 13
 - MX Linux 23.6
 - Pop!_OS 24.04

### Fedora Based

Version 1.2.0+
 - Fedora 43
 - Nobara 43