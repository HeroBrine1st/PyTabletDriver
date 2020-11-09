import select
import sys
from errno import *
from typing import Optional

import Xlib.display
from evdev import InputDevice, UInput, AbsInfo
from evdev.ecodes import *
from pyudev import Monitor, Context

display = Xlib.display.Display()

# CONFIGURATION VARIABLES #

display_size = (display.screen().width_in_pixels, display.screen().height_in_pixels)
display_pos = (0, 0)
area = (0, 0, 1, 1)
area_size = (area[2] - area[0], area[3] - area[1])

# ======================= #

device: Optional[InputDevice] = None
virtual_device: Optional[UInput] = None

device_searcher_info = {"vendor": 0, "product": 0, "name": ""}

monitor = Monitor.from_netlink(Context())
monitor.filter_by(subsystem='input')
monitor.start()



def update_device(new_device):
    global device
    global virtual_device
    new_device.grab() # Prevent xorg from overriding cursor pos
    cap = new_device.capabilities()
    virtual_device = UInput({
        EV_KEY: cap[EV_KEY],
        EV_ABS: [(0, AbsInfo(value=0, min=0, max=display_size[0], fuzz=0, flat=0, resolution=1)),
                 (1, AbsInfo(value=0, min=0, max=display_size[1], fuzz=0, flat=0, resolution=1)),
                 (24, AbsInfo(value=0, min=0, max=cap[EV_ABS][2][1].max, fuzz=0, flat=0, resolution=0))]
    })
    print("Using device %s" % new_device.name)
    cap = new_device.capabilities()
    print(" - Max X: %s\n - Max Y: %s\n - %s button(s)" %
          (cap[3][0][1].max, cap[3][1][1].max,
           len(list(filter(lambda key: key != BTN_TOOL_PEN and key != BTN_TOUCH, cap[EV_KEY])))))
    if BTN_TOOL_PEN in cap[EV_KEY]:
        print(" - Hover available")
    if BTN_TOUCH in cap[EV_KEY]:
        print(" - Has BTN_TOUCH feature - %s pressure steps" % (cap[3][2][1].max + 1))
    device = new_device

def process_command(cmd: str):
    args = cmd.split(" ")
    cmd = args.pop(0)
    if len(args) == 0:
        print("Invalid command")
        return
    if cmd == "AREA":
        if len(args) != 4:
            print("Invalid area")
            return
        global area
        global area_size
        try:
            area_temp = tuple(map(int, args))
            area_size_temp = (area_temp[2] - area_temp[0], area_temp[3] - area_temp[1])
            if area_size[0] > 0 and area_size[1] > 0:
                area = area_temp
                area_size = area_size_temp
                print("New area applied!")
                print(" - %s" % " ".join(args))
                print(f" - {area_size[0]}x{area_size[1]}")
            else:
                print("Invalid area")
        except ValueError:
            print("Invalid area")
    elif cmd == "DEVICE":
        global device
        if device is not None:
            device.close()
        path = args.pop(0)
        new_device = InputDevice(path)
        if EV_ABS not in new_device.capabilities() or len(new_device.capabilities()[EV_ABS]) < 3 \
                or new_device.capabilities()[EV_ABS][2][0] != ABS_PRESSURE:
            print("Invalid device")
            return
        update_device(new_device)

def main():
    global device
    global virtual_device
    global area
    global area_size
    while True:
        # if select.select([sys.stdin, ], [], [], 0)[0]:
        for line in sys.stdin.read().splitlines(keepends=False):
            process_command(line)
        if device is not None and virtual_device is not None:
            try:  # Faster than monitor.poll(timeout=0) then checking udev events
                event = device.read_one()
                if event is None:
                    continue
                if event.type == EV_ABS:
                    if event.code == ABS_X:
                        x = event.value
                        if x > area[2]:
                            x = area[2]
                        x = (x - area[0]) * display_size[0] // area_size[0]
                        virtual_device.write(EV_ABS, ABS_X, x)
                    elif event.code == ABS_Y:
                        y = event.value
                        if y > area[3]:
                            y = area[3]
                        y = (y - area[1]) * display_size[1] // area_size[1]
                        virtual_device.write(EV_ABS, ABS_Y, y)
                    elif event.code == ABS_PRESSURE:
                        virtual_device.write(EV_ABS, ABS_PRESSURE, event.value)
                    virtual_device.syn()
                elif event.type == EV_KEY:
                    virtual_device.write(EV_KEY, event.code, event.value)
                    virtual_device.syn()
            except OSError as e:
                if e.args[0] == ENODEV:
                    print(f"Got disconnected from {device.name}, saving info and waiting.")
                    device_searcher_info["vendor"] = device.info.vendor
                    device_searcher_info["product"] = device.info.product
                    device_searcher_info["name"] = device.name
                    device = None
                    virtual_device = None
        else: # Wait for device connect
            d = monitor.poll(timeout=0)
            if d and d.action == "add" and d.device_node and d.device_node.startswith("/dev/input/event"): # Last check used to avoid ENOTTY
                candidate = InputDevice(d.device_node)
                if candidate.info.vendor == device_searcher_info["vendor"] and candidate.info.product == device_searcher_info["product"]\
                        and candidate.name == device_searcher_info["name"]:
                    update_device(candidate)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Exit")
    except BaseException:
        raise
    finally:
        print("Closing device")
        if device:
            device.close()