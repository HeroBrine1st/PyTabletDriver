# АХТУНГ ТОЛЬКО ЛИНУКС
# НА ВИНДЕ НЕ ЗАВЕДЕТСЯ
# ВООБЩЕ
import Xlib.ext.xtest
import Xlib.display
display = Xlib.display.Display()

# Справочник кнопочек-хуёпочек
#         ('unknown', None),
#         ('left', 1),
#         ('middle', 2),
#         ('right', 3),
#         ('scroll_up', 4),
#         ('scroll_down', 5),
#         ('scroll_left', 6),
#         ('scroll_right', 7)] + [
#             ('button%d' % i, i)
#             for i in range(8, 31)])

def set_position(x, y):
    Xlib.ext.xtest.fake_input(display, Xlib.X.MotionNotify, x=x, y=y)
    display.flush()

def press(button):
    Xlib.ext.xtest.fake_input(display, Xlib.X.ButtonPress, button)
    display.flush()

def release(button):
    Xlib.ext.xtest.fake_input(display, Xlib.X.ButtonRelease, button)
    display.flush()

def size():
    return display.screen().width_in_pixels, display.screen().height_in_pixels