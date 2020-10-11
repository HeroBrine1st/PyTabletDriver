import sys

from evdev import UInput, InputDevice, AbsInfo
from evdev.ecodes import *
import os
import json
import evdev
import mouseulits

path = ""
# top bottom left right
# wacom_area = [16000, 22094, 1714, 5140]
wacom_area = [0, 32000, 0, 18000]


wacom_size = [wacom_area[1] - wacom_area[0], wacom_area[3] - wacom_area[2]]
device = None
key_mapping = {
    BTN_TOUCH: BTN_TOUCH,
    BTN_STYLUS: BTN_STYLUS2,
    BTN_STYLUS2: BTN_STYLUS,
}

def find_tablet():
    for dev in evdev.list_devices():
        dev = InputDevice(dev)
        a = dev.capabilities()
        if EV_ABS in a:
            if len(a[EV_ABS]) >= 3:
                return dev
    return None

def load_tablet(query):
    try:
        dev = InputDevice(query["path"])
    except FileNotFoundError:
        dev = None
        for dev in evdev.list_devices():
            dev = InputDevice(dev)
            if dev.info.vendor == query["vendor"] and dev.info.product == query["product"]:
                break
        if dev is None:
            return None
    cap = dev.capabilities()
    if EV_ABS in cap and len(cap[EV_ABS]) >= 3:
        return dev
    return None

def save_config():
    config = {
        "device": {
            "path": device.path,
            "product": device.info.product,
            "vendor": device.info.vendor,
        },
        "area": wacom_area,
    }
    with open("profile.json", "w") as f:
        json.dump(config, f)


def init():
    global device
    global wacom_area
    global wacom_size
    if os.path.exists("profile.json"):
        with open("profile.json") as f:
            config = json.load(f)
        device = load_tablet(config["device"])
        if device is None:
            print("Couldn't load tablet from config.", file=sys.stderr)
            exit(0)
        wacom_area = config["area"]
        wacom_size = [wacom_area[1] - wacom_area[0], wacom_area[3] - wacom_area[2]]
    else:
        print("No config found.")
        device = find_tablet()
        if device is None:
            print("No tablets connected.", file=sys.stderr)
            exit(0)
        print("Found tablet %s (Vendor %s, Product %s) on %s" % (device.name, device.info.vendor, device.info.product, device.path))
        print("Using default config")
        save_config()
        print("Config saved")




def main():
    print("Running tabletdriver on device %s (%s)" % (device.path, device.name))
    cap = device.capabilities()
    display = mouseulits.size()
    uinput = UInput({
        1: [320, 330, 331, 332], # Без этого не работает. Не знаю, почему, это вроде бы EV_KEY
        3: [(0, AbsInfo(value=0, min=0, max=display[0], fuzz=0, flat=0, resolution=1)),
            (1, AbsInfo(value=0, min=0, max=display[1], fuzz=0, flat=0, resolution=1)),
            (24, AbsInfo(value=0, min=0, max=cap[EV_ABS][2][1].max, fuzz=0, flat=0, resolution=0))]
    }, name="PyTabletDriver's Virtual Tablet")
    while True:
        event = device.read_one()
        if event is None:
            continue
        if event.type == EV_ABS:
            if event.code == ABS_X:
                x = event.value
                if x > wacom_area[1]:
                    x = wacom_area[1]
                x = (x - wacom_area[0]) * display[0] // wacom_size[0]
                uinput.write(EV_ABS, ABS_X, x)
            elif event.code == ABS_Y:
                y = event.value
                if y > wacom_area[3]:
                    y = wacom_area[3]
                y = (y - wacom_area[2]) * display[1] // wacom_size[1]
                uinput.write(EV_ABS, ABS_Y, y)
            elif event.code == ABS_PRESSURE:
                uinput.write(EV_ABS, ABS_PRESSURE, event.value)
            uinput.syn()
        elif event.type == 1:
            if event.code in range(330, 333):
                if event.value == 1:
                    mouseulits.press(event.code - 329)
                elif event.value == 0:
                    mouseulits.release(event.code - 329)

if __name__ == '__main__':
    try:
        init()
        with device.grab_context():
            main()
    except KeyboardInterrupt:
        print("Exiting")
        pass
    except BaseException:
        device.close()
        raise
    device.close()
