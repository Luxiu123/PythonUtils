# -*- coding: UTF-8 -*-

# 自动点击

import time
import pyautogui
import keyboard
import threading

x, y = 943, 935  # 鼠标需要移动到的位置

state = {"stop": False}


def stop():
    print("stop func")
    while True:
        print("loop")
        time.sleep(0.1)
        keyboard.wait("esc")
        state["stop"] = True
        print(f"esc down {time.time()}")


threading.Thread(target=stop).start()


def run(count: int):
    print("sleep 3 seconds")
    time.sleep(3)  # 延迟3秒
    print("started")
    state["stop"] = False
    pyautogui.moveTo(x, y)
    while count > 0 and not state["stop"]:
        pyautogui.click()
        count -= 1
        print(count)
    print("stoped")


while True:
    try:
        num = int(input("输入点击次数:"))
        run(num)
    except Exception as e:
        print(e)
