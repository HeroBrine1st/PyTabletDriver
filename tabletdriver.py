import evdev
import mouseulits

path = "/dev/input/event8"
# top bottom left right
area_pos = [80, 8.57]
area_size = [30.47, 17.139375]

device = evdev.InputDevice(path)
cap = device.capabilities()
tablet = [cap[3][0][1].max, cap[3][1][1].max]
tablet_size_physical = [tablet[0] / cap[3][0][1].resolution, tablet[1] / cap[3][1][1].resolution]
display = mouseulits.size()
area_size[1] = area_size[0] * (display[1] / display[0])
map_x = 1 / tablet[0] * tablet_size_physical[0]
map_y = 1 / tablet[1] * tablet_size_physical[1]
map_x_2 = 1 / area_size[0] * display[0]
map_y_2 = 1 / area_size[1] * display[1]



def map_to_display(x, y):
    x = x * map_x
    y = y * map_y
    if x < area_pos[0]:
        x = area_pos[0]
    if y < area_pos[1]:
        y = area_pos[1]
    if x > area_pos[0] + area_size[0]:
        x = area_pos[0] + area_size[0]
    if y > area_pos[1] + area_size[1]:
        y = area_pos[1] + area_size[1]
    x = x - area_pos[0]
    y = y - area_pos[1]
    return int(x * map_x_2), int(y * map_y_2)

def main():
    data_collected = [1, 1]
    print("Running tabletdriver on device %s (%s)" % (path, device.name))
    print("Physical size: %sx%s" % tuple(tablet_size_physical))
    print("System size: %sx%s" % tuple(tablet))
    while True:
        event = device.read_one()
        if event is None:
            continue
        if event.type == 3:
            if event.code == 0:
                data_collected[0] = event.value
            elif event.code == 1:
                data_collected[1] = event.value
            x, y = map_to_display(data_collected[0], data_collected[1])
            mouseulits.set_position(x, y)
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