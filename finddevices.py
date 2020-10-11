import evdev
from evdev.ecodes import EV_ABS

for d in evdev.list_devices():
  device = evdev.InputDevice(d)
  a = device.capabilities()
  tab = False
  if EV_ABS in a:
    if len(a[EV_ABS]) >= 3:
      tab = True
  print(device.path, device.name, tab)

