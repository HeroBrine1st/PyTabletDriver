import sys
import Xlib.display
from evdev import InputDevice, UInput, AbsInfo
from evdev.ecodes import *


display = Xlib.display.Display()
display_size = (display.screen().width_in_pixels, display.screen().height_in_pixels)
area = tuple(map(int, sys.argv[2:6]))
area_size = [area[2] - area[0], area[3] - area[1]]
device = InputDevice(sys.argv[1])
print("Using device %s" % device.name)
cap = device.capabilities()
print("Max X: %s\nMax Y: %s\n%s button(s)" %
      (cap[3][0][1].max, cap[3][1][1].max, len(list(filter(lambda key: key != BTN_TOOL_PEN and key != BTN_TOUCH, cap[EV_KEY])))))
if BTN_TOOL_PEN in cap[EV_KEY]:
    print("Hover available")
if BTN_TOUCH in cap[EV_KEY]:
    print("Has BTN_TOUCH feature - %s pressure steps" % (cap[3][2][1].max + 1))

virtual_device = UInput({
    EV_KEY: cap[EV_KEY],
    EV_ABS: [(0, AbsInfo(value=0, min=0, max=display_size[0], fuzz=0, flat=0, resolution=1)),
             (1, AbsInfo(value=0, min=0, max=display_size[1], fuzz=0, flat=0, resolution=1)),
             (24, AbsInfo(value=0, min=0, max=cap[EV_ABS][2][1].max, fuzz=0, flat=0, resolution=0))]
})

def main():
    while True:
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


if __name__ == '__main__':
    with device.grab_context():
        try:
            main()
        except KeyboardInterrupt:
            print("Exit")
        except BaseException:
            device.close()
            raise
    device.close()