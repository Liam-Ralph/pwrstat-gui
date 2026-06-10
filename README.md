# PwrStat GUI
### Released July 2025
### Version 1.3.0
### Updated June 2026

<br/>

## Description

A graphical user interface for CyberPower's PowerPanel
Linux software using Python's tkinter library. Runs the
command `sudo pwrstat -status` to gather information from
the UPS. Can also log gathered information in a CSV file.
Not affiliated with CyberPower.

<br/>

## Requirements

x86_64 is the only supported architecture.

This project requires __CyberPower's PowerPanel for Linux__,
which can be found on
[CyberPower's website](https://www.cyberpowersystems.com/products/software/power-panel-personal/).
It also requires the DejaVu Sans font and PolicyKit support.
Both are included with most distros, but are added as a
dependency in packaged applications.

|      Debian     |      Fedora     |       Arch      |
|-----------------|-----------------|-----------------|
|fonts-dejavu-core|dejavu-sans-fonts|    ttf-dejavu   |
|      pkexec     |      polkit     |      polkit     |

Minimum glibc version requirement by package. You can check your distro's
version with `ldd --version`.

|Package   |glibc|
|----------|-----|
|Debian    |2.39 |
|Debian LTS|2.27 |
|Fedora    |2.43 |
|Fedora LTS|2.42 |
|Arch      |2.43 |

If your distro is unsupported, you can try creating your own
package using the developer packages.

### Memory

This application uses approximately 25 MiB of memory.

### Storage

This application uses approximately 20 MiB of storage,
varying based on distro and needed dependencies.

<br/>

## Installation

Packages can be found on this respository's GitHub page.

## Development

I have added some developer packages on
[GitHub](https://github.com/liam-ralph/pwrstat-gui-dev-pkgs). These include the
files used to create packages and some documentation, as well as some scripts
to automate compilation and packaging.

<br/>

## Operating System Support

Support is assumed for all distros based on Debian, Fedora, and Arch. Below is a
list of distros with confirmed support. Italics indicate the distro used to
compile its supported package.

|Distro     |Version|Supports|
|-----------|-------|--------|
</br>
|Debian     |13     |Reg     |
|           |11     |LTS     |
|Ubuntu     |24.04  |*Reg*   |
|           |18.04  |*LTS*   |
|Linux Mint |22.3   |Reg     |
|Pop!_OS    |24.04  |Reg     |
|MX Linux   |25.2   |Reg     |
|antiX      |26     |Reg     |
|Zorin OS   |18.1   |Reg     |
</br>
|Fedora     |44     |*Reg*   |
|           |43     |*LTS*   |
|Nobara     |43     |LTS     |
|Bazzite    |44     |Reg     |
</br>
|Arch       |       |Reg     |
|EndeavourOS|       |Reg     |
|Manjaro    |       |Reg     |
|CachyOS    |       |Reg     |