# PwrStat Developer Packages
### Released June 2026
### Version 2.0.0
### Updated June 2026

</br>

## Description

Files and documentation to aid any who want to
add changes to [PwrStat GUI](https://github.com/liam-ralph/pwrstat-gui),
or create new packages.
Includes packages for distros based on Debian,
Fedora, and Arch. Not affiliated with CyberPower.

</br>

## Requirements

Packages required to compile and package PwrStat GUI
can be installed using `install-dependencies.sh`.
`install-dependencies.sh` has one flag:
 - -d \[Required\] Distro group (debian, fedora, or arch).

<br/>

## Compilation

You can compile the Python code using `compile.sh`,
which uses PyInstaller inside a virtual environment.
`compile.sh` has two flags:
 - -b \[Optional\] The branch of pwrstat-gui to use (uses default if
   unspecified).

<br/>

## Packaging

You can package the project using `package.sh`, which will also
run `compile.sh` if you haven't already.
`package.sh` has two flags:
 - -d \[Required\] Distro group (debian, fedora, or arch) to target.
 - -l \[Optional\] No arguments. If flag is present, the package's name
   will be changed to signify an LTS version.