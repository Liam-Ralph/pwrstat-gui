# PwrStat GUI
### Released March 2025 (planned)
### Version 0.0

<br/>

## Description
A graphical user interface for CyberPower's PowerPanel
Linux software using Python's tkinter library. Runs the
command `sudo pwrstat -status` to gather information from
the UPS. Can also log gathered information in a csv file.

<br/>

## Requirements
This project requires __CyberPower's PowerPanel for Linux__,
which can be found on
[CyberPower's website](https://www.cyberpowersystems.com/products/software/power-panel-personal/).

### Memory
As per testing, the executable program uses approximately
128KiB of memory, though results may vary.
Running the Python program uses more memory, and memory usage
can increase to an unknown limit by change settings repeatedly.
Memory usage starts at around 16MiB and typically stays below 20MiB,
but can be increased to 50MiB through purposeful effort.

### Storage
This application uses approximately 16MiB of storage.

<br/>

## Operating System Support

### Legend
 - Confirmed - Support for unedited versions of this
   operating system have been confirmed by the developer
 - Assummed - Support for this operating system is assumed,
   but has not been confirmed

|Ubuntu 24.04 |Ubuntu 18.04 |Linux Mint 22|Linux Mint 21|Debian 12    |Other Debian |
|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|
|Confirmed    |Confirmed    |Confirmed    |Confirmed    |Confirmed    |Assumed      |