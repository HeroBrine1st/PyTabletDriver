import evdev

for d in evdev.list_devices():
  device = evdev.InputDevice(d)
  print(device)
