# АХТУНГ ТОЛЬКО ЛИНУКС
# НА ВИНДЕ НЕ ЗАВЕДЕТСЯ
# ВООБЩЕ
import contextlib

import Xlib.ext.xtest
import Xlib.display
display = Xlib.display.Display()

@contextlib.contextmanager
def display_manager():
    yield display
    display.flush()

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
    with display_manager() as dm:
        Xlib.ext.xtest.fake_input(dm, Xlib.X.MotionNotify, x=x, y=y)

def press(button):
    with display_manager() as dm:
        Xlib.ext.xtest.fake_input(dm, Xlib.X.ButtonPress, button)

def release(button):
    with display_manager() as dm:
        Xlib.ext.xtest.fake_input(dm, Xlib.X.ButtonRelease, button)
