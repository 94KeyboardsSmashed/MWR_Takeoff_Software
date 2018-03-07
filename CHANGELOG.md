# Changelog
This changelog will document all notable changes to this file as per NASA 
request to keep detailed documentation for our Flight Readiness Review (FRR).

## [Beta v0.2.2] - 2018-03-05
### Changed
- Made .txt readout at startup
### Added
- Added buzzer component code to gnd.py
- Added buzzer channel control code in setup.py

## [Beta v0.2.1] - 2018-03-04
### Changed
- Reduced second file startup file amount from 2000 bytes to 1000 bytes
- Increased takeoff threashold from 5 to 7 gs
- Made circular data buffer respond to changes in measurement units

## [Alpha Release v0.2.0] - 2018-03-02
### Added
- Added Gershwin backronym explainer in README
- Added Other MWR repos section
- Added authors seections
### Changed
- Made the readings default measure in gs
- Circular buffer now in acceptable to gforce input
- Made Readme cleaner and added pictures
### Other
- Hardware assembled for first prototype launch on 2018-03-03

## [Alpha Release Candidate v0.1.1] - 2018-02-05
### Added
- Added easy X, Y, Z calibration values in settings.py.
### Changed
- install.sh overhauled to install dependancies to python3.
- Updated readme to do list.

## [Alpha Release Candidate v0.1.0] - 2018-02-04
### Added
- Added second trigger to unwind circular buffer when other accelerometers are unwound.
### Removed
- Removed file startup.py
- Removed all references to neopixels in vdd.py and gnd.py.
- Removed neopixel constant values from settings.py.
### Changed
- Restructured changelog format
- run_experiment.sh now prints "Working..." instead of executing startup.py.
- Max memory limit that stops gnd.py based on the size of loggnd.txt shortened from 5 MB to 2 MB (around 6:40 min).
- Max memory limit that stops vdd.py based on the size of logvdd.txt shortened from 5 MB to 2 MB (around 6:40 min).
- Takeoff Threshold constant in settings.py increased from 3gs to 5gs.
- Renamed accelerometer with address (0x53) from INDUS to YANGTZE.
- Range of accelerometers increased from +-8g to +-16gs.

## [Alpha v0.0.4] - 2018-02-03
### Added
- libbluetooth-dev added in install.sh as dependency.
- Added code to bluez\_client to find and connect with pis running bluez_server [WIP].
- Added additional examples in readme.
- Added CHANGELOG.md to document changes.
### Changed
- Max memory limit that stops vdd.py based on the size of logvdd.txt enlarged from 1 MB to 5 MB.
- Max memory limit that stops gnd.py based on the size of loggnd.txt enlarged from 1 MB to 5 MB.
- Updated module intro strings to contain more accurate information about the wiring of sparkfun accelerometers.
- Updated neopixel wiring specifications on module intro strings.

## [Alpha v0.0.3] - 2018-02-01
### Added
- Added a max memory limit that stops vdd.py when logvdd.txt file exceeds 1 MB.
- Added a max memory limit that stops gnd.py when loggnd.txt file exceeds 1 MB.
- Added code snippets in readme file
### Changed
- LANDING_THRESHOLD contant in settings.py set to 0 for testing purposes.
- Brightness of neopixel now depends fully on brightness value set at class init.
- startup.py fully integrated into run_experiment.sh file. Now runs properly at startup 
- Neopixel init brightness lowered from 255 to 16
- Changed accelerometer hardware from Adafruit brand to Sparkfun brand
- Expanded To Do section of readme file

## [Alpha v0.0.2] - 2018-01-31
### Added
- Proper markdown tags for readme.
- Added settings.py file - central file to change all variables.
### Removed
- Removed the vdd.py and gnd.py's need for neopixel connections.
### Changed
- Docstrings are now updated to the numpy docstring format.
- All files with global variables now have variables in the settings.py file.
- Module intro comments expanded and explains more.
- startup.py now runs only one neopixel ring with test times seperated by a magenta color wipe.

## [Alpha v0.0.1] - 2018-01-30
### Added 
- Licensed code under MIT license.
- Added Readme file with improper title tags.
- Added file install.sh - execute to install all dependancies.
- Added file bluez_client.py - basic bluetooth connection functionality for client.
- Added file bluez_server.py - basic bluetooth connection functionality for server host.
- Added file gnd.py - to read accelerometer data on (0x53) i2c address.
- Added file vdd.py - to read accelerometer data on (0x1D) i2c address.
- Added file run_experiment.sh - to execute both gnd.py and vdd.py and logs data in .txt files.
- Added file startup.py - experimental initiation file to execute on startup. Not yet implimented.
- Added file neopixel_lib.py - the neopixel library derived from previous github page.
- Added file raspi\_accel_lib.py - the accelerometer library derived from previous github page.
- Added file install.sh - executable file that will download all libraries.
