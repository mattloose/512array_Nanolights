# 512array_Nanolights
Development code for a light interface to the ONT minION device

![light box image](images/LightBox.jpg?raw=true "The Light Box")

Currently only tested on a raspberry pi!

To build the hardware needed go to: https://www.adafruit.com/products/2345

A guide to assembling the hardware is here: https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi

To build a case for this you can 3D print using the model in the 3dPrintFiles folder.

To clone repository:

	git clone --recursive https://github.com/mattloose/512array_Nanolights

then:

	cd rpi-rgb-led-matrix
	make
	cp rgbmatrix.so ../
	cd fonts
	pilfont *.bdf
	cd ..
	cd ..

then:

	sudo python minION_view.py -ip ip.of.your.minknow

Note that the ip address is the ip of your minKNOW running computer.

Currently MinKNOW MUST BE RUNNING before you launch this for it to work. 

Also this MUST be run as sudo.

For full help:

	python minION_view.py -h
	
	usage: minION_view.py [-h] -ip IP [-v] [-r] [-n] [-b]

	interaction: A program to provide real time interaction for minION runs. Args
	that start with '--' (eg. --ip-address) can also be set in a config file
	(/path/to/512array_Nanolights/minup_posix.config or ) by
	using .ini or .yaml-style syntax (eg. ip-address=value). If an arg is
	specified in more than one place, then command-line values override config
	file values which override defaults.

	optional arguments:
	  -h, --help            show this help message and exit
	  -ip IP, --ip-address IP
	                        The IP address of the minKNOW machine.
	  -v, --verbose         Display debugging information.
	  -r, --ratio           This option prints the ratio of in strand to
	                        available.
	  -n, --no_lights       Inactivate lights for testing and development
	                        purposes.
	  -b, --brightness      Halves brightness for comfort!
	


