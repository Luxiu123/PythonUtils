from pymouse import PyMouse
from pykeyboard import PyKeyboard
import time
import keyboard
import threading
import sys

m = PyMouse()
k = PyKeyboard()
stop = False

def exit_program():
    global stop
    print("exit_program func")
    keyboard.wait('esc')
    print("exit")
    stop = True
    
threading.Thread(target=exit_program).start()

print("enter loop")
while stop == False:
    time.sleep(0.3)
    m.click(1284, 771)
    k.tap_key(k.delete_key)
    k.tap_key(k.down_key)
    print(1)