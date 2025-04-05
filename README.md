# PwrStat GUI
### Released March 2025 (planned)
### Version 0.0

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
As per testing, the executable program uses approximately
128 KiB of memory, though results may vary.
Running the Python program uses more memory, and memory usage
can increase to an unknown limit by changing settings repeatedly.
Memory usage starts at around 16 MiB and typically stays below 20 MiB,
but can be increased to 50 MiB through purposeful effort.

### Storage
This application uses approximately 16 MiB of storage.

<br/>

## Installation

### 1. Python
1. Download this project using either `git clone` or by manually
downloading files (only main.py, images, and data are required)
2. Run main.py in your favourite console or IDE

### 2. Debian
1. Download the .deb file [here](liam-ralph.github.io/projects/)
2. Navigate the folder you downloaded to
3. Install the file using `dpkg -i <file_name>.deb`, replacing
`<file_name>` with the actual .deb file's name

<br/>

## Operating System Support

### Legend
 - Confirmed - Support for unedited versions of this
   operating system have been confirmed by the developer
 - Assummed - Support for this operating system is assumed,
   but has not been confirmed

|Ubuntu 24.04 |Ubuntu 18.04 |Linux Mint 22|Linux Mint 21|Debian 12    |Other Debian |
|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|:-----------:|
|Confirmed    |Assumed      |Assumed      |Assumed      |Assumed      |Assumed      |