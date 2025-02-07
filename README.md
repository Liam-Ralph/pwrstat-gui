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
as well as __python3__, __python3-pil__,
__python3-setproctitle__, and __python3-tk__. PowerPanel
can be found on
[CyberPower's website](https://www.cyberpowersystems.com/products/software/power-panel-personal/)
and Python dependencies can be installed using
`sudo apt update` and `sudo apt install <dependency>`,
assuming they are not installed already.

### Memory
As per testing, this program uses approximately xxxMiB of memory,
though results may vary.

### Storage
Installing this application requires approximately xxMiB of storage.
