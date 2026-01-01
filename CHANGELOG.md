## Version 1.2.0 (December 2025)

 - Confirmed support for Fedora-based distros and Pop!_OS 24.04.
 - Added scripts in package files for local Python compilation.
     - This should allow for expanded compatibility.

## Version 1.1.2 (October 2025)

 - Added documentation comments to functions.
 - Confirmed support for Linux Mint 22.2.
 - Updated CHANGELOG formatting (vx.y.z --> Version x.y.z)

## Version 1.1.1 (September 2025)

 - Changed logging time from epoch to HH:MM:SS string.
 - Changed default font.
 - Fixed settings window text width.
 - Improved settings updating, removing need for sampling interval "Update" button.

## Version 1.1.0 (September 2025)

 - Added viewing of README, CHANGELOG, and License in-app.
 - Tweaked code conventions.
 - Confirmed support for more operating systems.
     - Removed pkexec for antiX compatibility.
     - Compiled on Pop!_OS for compatibility with older versions of GLIBC.
 - Changed supported font list and default font.
     - All installed font can be chosen from.
     - Note that some fonts may be too large to work properly.
 - Extended shutdown time to 10 seconds when PowerPanel or sudo permissions are
   missing.

## Version 1.0.3 (August 2025)

 - Confirmed support for more operating systems.

## Version 1.0.2 (August 2025)

 - Changed button background colours for better text visibility.

## Version 1.0.1 (July 2025)

 - Changed graph updater code to prevent flashing images.
 - Reduced graph update frequency, reducing flashing but also reducing
   responsiveness to window size changes.

## Version 1.0.0 (July 2025)

Initial app release.
