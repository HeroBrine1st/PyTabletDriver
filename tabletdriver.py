import evdev
import pyautogui
import mouse

from pynput.mouse import Controller, Button

path = "/dev/input/event8"
# top bottom left right
area_pos = [80, 8.57]
area_size = [30.47, 17.139375]

device = evdev.InputDevice(path)
cap = device.capabilities()
tablet = [cap[3][0][1].max, cap[3][1][1].max]
tablet_size_physical = [tablet[0] / cap[3][0][1].resolution, tablet[1] / cap[3][1][1].resolution, ]
display = pyautogui.size()
area_size[1] = area_size[0] * (display.height / display.width)
full_size = [display.width / 10, display.height / 10]
modifier = (tablet[0] * tablet_size_physical[1] / tablet_size_physical[0]) / tablet[1]
map_x = 1 / tablet[0] * full_size[0]
map_y = 1 / tablet[0] * full_size[0]
map_x_2 = 1 / area_size[0] * display.width
map_y_2 = 1 / area_size[1] * display.height

def map_to_display(x, y):
    x = x * map_x
    y = y * map_y
    x_retraction = 0
    y_retraction = 0
    if x < area_pos[0]:
        x = area_pos[0]
    if y < area_pos[1]:
        y = area_pos[1]
    if x > area_pos[0] + area_size[0]:
        x = area_pos[0] + area_size[0]
        x_retraction = 1
    if y > area_pos[1] + area_size[1]:
        y = area_pos[1] + area_size[1]
        y_retraction = 1
    x = x - area_pos[0]
    y = y - area_pos[1]
    return int(x * map_x_2) - x_retraction, int(y * map_y_2) - y_retraction



def main():
    mouse2 = Controller()
    data_collected = [1, 1]
    print("Running tabletdriver on device %s (%s)" % (path, device.name))
    print("Physical size: %sx%s" % tuple(tablet_size_physical))
    print("System size: %sx%s" % tuple(tablet))
    print(area_pos, area_size)
    while True:
        event = device.read_one()
        if event is None:
            continue
        if event.type == 3:
            if event.code == 0:
                data_collected[0] = event.value
            elif event.code == 1:
                data_collected[1] = event.value
            # if data_collected[0] > -1 and data_collected[1] > -1:
            raw_x, raw_y = data_collected[0], data_collected[1]
            x, y = map_to_display(raw_x, raw_y)
            mouse.move(x, y, True, 0)
                # data_collected = [-1, -1]
        elif event.type == 1:
            button = None
            if event.code == 330:
                button = Button.left
            elif event.code == 331:
                button = Button.right
            elif event.code == 332:
                button = Button.middle
            if button is not None:
                if event.value == 1:
                    mouse2.press(button)
                elif event.value == 0:
                    mouse2.release(button)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        device.close()
        raise e
    device.close()