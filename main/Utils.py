import ctypes
import sys
import os
import re


FILE_REGEXP = r"^(?P<path>.*[/\\])(?P<name>.*)(?P<ets>\..+)$"

STD_INPUT_HANDLE = -10
STD_OUTPUT_HANDLE = -11
STD_ERROR_HANDLE = -12

# 字体颜色定义 text colors
FOREGROUND_BLUE = 0x09  # blue.
FOREGROUND_GREEN = 0x0A  # green.
FOREGROUND_RED = 0x0C  # red.
FOREGROUND_YELLOW = 0x0E  # yellow.
FOREGROUND_SKYBLUE = 0x0B  # skyblue.
FOREGROUND_PINK = 0x0D  # pink.
# 背景颜色定义 background colors
BACKGROUND_YELLOW = 0xE0  # yellow.


# get handle
std_out_handle = ctypes.windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)


def set_cmd_text_color(color, handle=std_out_handle):
    Bool = ctypes.windll.kernel32.SetConsoleTextAttribute(handle, color)
    return Bool


# reset white
def reset_color():
    set_cmd_text_color(FOREGROUND_RED | FOREGROUND_GREEN | FOREGROUND_BLUE)


def print_error(text):
    set_cmd_text_color(FOREGROUND_RED)
    print(text)
    reset_color()


def print_sky_blue(text: str):
    set_cmd_text_color(FOREGROUND_SKYBLUE)
    print(text)
    reset_color()


def is_path_valid(path: str) -> bool:
    """
    检查路径是否合法
    """
    return path != "" and os.path.exists(path)


