import os, cv2, random
import numpy as np

# ADB related
def tap(crd : (int, int)):
    cmdTap = 'adb shell input tap {x} {y}'.format(
        x=crd[0],
        y=crd[1]
    )
    print(cmdTap)
    os.system(cmdTap)

def swipe(org : (int, int), tar : (int, int), delay):
    cmdSwipe = 'adb shell input swipe {x1} {y1} {x2} {y2} {delay1}'.format(
        x1=org[0],
        y1=org[1],
        x2=tar[0],
        y2=tar[1],
        delay1=delay
    )
    print(cmdSwipe)
    os.system(cmdSwipe)

def screenshot() -> str:
    os.system('adb shell screencap -p /sdcard/sh.png')
    os.system('adb pull /sdcard/sh.png .')
    return "sh.png"

# helper function
def shifter(ord : (int, int), i : int) -> (int, int):
    return (ord[0] + random.randint(-i, i), ord[1] + random.randint(-i, i))

# OpenCV related
def standby(sh : str, tmp : str, threshold = 0.9) -> bool:
    img = cv2.imread(sh, 0)
    template = cv2.imread(tmp, 0)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    if (res >= threshold).any():
        return True
    return False

def get_crd(sh : str, tmp : str, threshold = 0.9) -> (int, int):
    img = cv2.imread(sh, 0)
    template = cv2.imread(tmp, 0)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    pos = []
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        pos.append(pt)
    return pos[0]