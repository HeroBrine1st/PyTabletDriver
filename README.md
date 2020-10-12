# PyTabletDriver
XP-PEN Star G640 driver written in python. 

Potentially supports all (at least more than one) graphic tablets, I didn't test it (because I have only one).

This driver is a layer between xorg and device, so if your distro doesn't have integrated drivers, this driver won't work (no chance, only if you use very old linux kernel)   

Work in progress.

# Features

* Custom tablet area

# Requirements

* Linux
* udev
* xorg

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
5. Run ``daemon.py`` with arguments
    1. Tablet's path
    2. Tablet area start X
    3. Area start Y
    4. Area end X
    5. Area end Y
    * Command example: ``python daemon.py /dev/input/event15 0 0 32000 18000``
    * I didn't create autostart so you need to run driver manually.
    
# Future plans

* Auto-searching for tablets
* GUI
* Autostart and daemon process
