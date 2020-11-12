# PyTabletDriver
XP-PEN Star G640 driver written in python. 

Potentially supports all (at least more than one) graphic tablets, I didn't test it (because I have only one).

This driver is a layer between xorg and device, so if your distro doesn't have integrated drivers, this driver won't work (no chance, only if you use very old linux kernel)   

Work in progress.

# Features

* Custom tablet area
* Auto-connecting if you plugged out and in tablet's cable

# Requirements

* Linux
* udev
* evdev

# Installing

Disclaimer: I'm **not** responsible for any damages. You're doing this at your own risk.

1. Place [this file](https://github.com/HeroBrine1st/PyTabletDriver/blob/master/rules/60-pytabletdriver.rules) into ``/etc/udev/rules.d/`` folder
    * You can skip steps 1 and 2, but then you have to execute step 6 by superuser
2. Reboot system or run ``sudo udevadm control --reload-rules && sudo udevadm trigger``
3. Install all requirements from file ``requirements.txt``
    * Python 3.6 recommended
4. Run file ``finddevices.py`` and get your tablet's path
    * ``True`` at the end of line explains device is tablet
    * For me it was ``/dev/input/event15 XP-PEN STAR G640 Pen True`` and path was ``/dev/input/event15``
5. Create config file (or enter commands directly to driver process standard input)
    * ``DEVICE <path>`` will set device for driver
    * ``AREA <left> <top> <right> <bottom>`` will set area
    * See example [here](https://github.com/HeroBrine1st/PyTabletDriver/blob/master/test.txt)
6. Run ``daemon.py``
    * You can provide config file as argument instead of entering commands
    
# Future plans

* GUI
* Autostart
