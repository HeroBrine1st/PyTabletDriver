# PyTabletDriver
XP-PEN Star G640 driver written in python. 

Potentially supports all (at least more than one) graphic tablets, I didn't test it (because I have only one).

This driver providing only customizing tablet area. If your distro doesn't have integrated tablet drivers this driver won't work.
Maybe I will create option for such distros so that driver will send event directly to xorg without virtual device, but pressure sensivity won't available.   

Work in progress.

# Installing

Disclaimer: I'm **not** responsible for any damages. You're doing this at your own risk.

1. Place [this file](https://github.com/HeroBrine1st/PyTabletDriver/blob/master/rules/60-pytabletdriver.rules) into ``/etc/udev/rules.d/`` folder
    * You can skip steps 1 and 2, but then you have to execute step 6 by superuser
2. Reboot system or run ``sudo udevadm control --reload-rules && sudo udevadm trigger``
3. Install all requirements from file ``requirements.txt``
    * Python 3.6 recommended
4. Run file ``finddevices.py`` and get your tablet's path 
    * For me it was ``device /dev/input/event11, name "XP-PEN STAR G640 Pen", phys "usb-XXXX:XX:XX.X-X.X/input1"`` and path was ``/dev/input/event11``
5. Open file ``tabletdriver.py`` and insert path. Edit settings if needed.
6. Run ``tabletdriver.py``
    * I didn't create autostart so you need to run driver manually.
    
# Future plans

* Auto-searching for tablets
* Option for not using virtual tablet (sending event directly to xorg)
* GUI
* Autostart and daemon process