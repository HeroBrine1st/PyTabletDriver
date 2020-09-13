from evdev import UInput, InputDevice, AbsInfo
from evdev.ecodes import *
import mouseulits

path = "/dev/input/event11"
# top bottom left right
wacom_area = [16000, 22094, 1714, 5140]


wacom_size = [wacom_area[1] - wacom_area[0], wacom_area[3] - wacom_area[2]]

device = InputDevice(path)

def main():

    print("Running tabletdriver on device %s (%s)" % (path, device.name))
    cap = device.capabilities()
    display = mouseulits.size()
    print("============================ DEBUG INFO ============================")
    print(cap)
    print(display)
    print(device)
    print("====================================================================")
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
        with device.grab_context():
            main()
    except KeyboardInterrupt:
        print("Exiting")
        pass
    except BaseException:
        device.close()
        raise
    device.close()
