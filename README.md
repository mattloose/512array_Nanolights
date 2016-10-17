# 512array_Nanolights
Development code for a light interface to the ONT minION device

Currently only tested on a raspberry pi!

To build the hardware needed go to: https://www.adafruit.com/products/2345



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

Currently MinKNOW MUST BE RUNNING for this to work.

Also this MUST be run as sudo.


