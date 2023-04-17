import time

from ppadb.client import Client
from numpy import asarray
from PIL import Image

adb = Client(host="127.0.0.1", port=5037)
device = adb.device("emulator-5554")
if device is None:
    print("no device")
    quit()

while True:
    screenshot = device.screencap()
    with open("screen.png", "wb") as fp:
        fp.write(screenshot)

    image = Image.open('screen.png')
    data = asarray(image)

    # only r,g,b
    pixels = [list(i[:3]) for i in data[1600]]

    transitions = []
    black = True
    ignore = True

    for i, pixel in enumerate(pixels[1:]):
        r, g, b = [int(i) for i in pixel]
        if ignore and (r + g + b) != 0:
            continue
        ignore = False

        if black and (r + g + b) != 0:
            black = False
            transitions.append(i)
            continue
        if not black and (r + g + b) == 0:
            black = True
            transitions.append(i)
            continue

    start, first_corner, second_corner = transitions
    goal_width = second_corner - first_corner
    goal = (goal_width / 2) + first_corner
    distance = goal - start
    print(f"Coordinates: {start}, {first_corner} - {second_corner}, Distance: {distance}, Goal-width: {goal_width}, Goal: {goal}")

    device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance * 0.96)}')
    time.sleep(3)
