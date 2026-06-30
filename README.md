# PwrStat GUI
### Released July 2025
### Version 1.4.0
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

x86_64 is the only supported architecture. CyberPower's PowerPanel Personal
requires systemd.

This project requires __CyberPower's PowerPanel for Linux__,
which can be found on
[CyberPower's website](https://www.cyberpowersystems.com/products/software/power-panel-personal/).
It also requires the DejaVu Sans font and PolicyKit support.
Both are included with most distros, but are added as a
dependency in packaged applications.

|      Debian     |      Fedora     |       Arch      |
|-----------------|-----------------|-----------------|
|fonts-dejavu-core|dejavu-sans-fonts|    ttf-dejavu   |
|      polkit     |      polkit     |      polkit     |

The operating system used to compile each package, as well as that OS's glibc
and Python versions. A target system may not have an older version of glibc
than the one used for packaging, but it may have an older Python version.

|Package|Operating System|glibc|Python |
|-------|----------------|-----|-------|
|Debian |Ubuntu 22.04    |2.35 |3.10.12|
|Fedora |Fedora 43       |2.42 |3.14.5 |
|Arch   |Arch            |2.43 |3.14.5 |

If your distro is unsupported, you can try creating your own
package using the scripts under pkg.

### Memory

This application uses approximately 25 MiB of memory.

### Storage

This application uses approximately 20 MiB of storage,
varying based on distro.

<br/>

## Installation

Packages can be found on this respository's GitHub page under releases.

## Packaging

You can use the scripts under pkg to create a complete Linux package.

Packages required to compile and package PwrStat GUI
can be installed using `install-dependencies.sh`.
`install-dependencies.sh` has one flag:
 - -d \[Required\] Distro group (debian, fedora, or arch).

You can compile the Python code using `compile.sh`,
which uses PyInstaller inside a virtual environment.
`compile.sh` has one flag:
 - -c \[Optional\] No arguments. If the flag is present, PyInstaller files will
   be removed prior to compilation. with -cc, compile-venv will be removed.

You can package the project using `package.sh`, which will also
run `compile.sh` if you haven't already.
`package.sh` has two flags:
 - -d \[Required\] Distro group (debian, fedora, or arch) to target.
 - -l \[Optional\] No arguments. If flag is present, the package's name
   will be changed to signify an LTS version.


<br/>

## Operating System Support

Support is assumed for all distros based on Debian, Fedora, and Arch, except
Bazzite and antiX. Below is a list of distros with confirmed support.

|Distro             |Version|
|-------------------|-------|
|Debian             |13     |
|                   |12     |
|Ubuntu             |24.04  |
|                   |22.04  |
|Fedora             |44     |
|                   |43     |
|Arch               |       |

</br>

Bazzite is not supported. It may run, but you cannot change any settings. A fix
is expected in the next release.
antiX is not supported, due to PowerPanel Personal requiring systemd.