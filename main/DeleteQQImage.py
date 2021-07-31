# -*- coding: UTF-8 -*-
# by luxiu
# 2021-07-31
# 删除QQ图片数据

import os
import shutil
import threading
import time


# 不用考虑线程安全问题
running_thread_num = 0


def remove(path: str):
    global running_thread_num
    running_thread_num += 1
    try:
        shutil.rmtree(path)
        print(f"{path} removed")
    except Exception as e:
        print(e)
    running_thread_num -= 1


def main(root_dir: str):
    for dir1 in os.listdir(root_dir):
        child_dir = os.path.join(root_dir, dir1)
        print("当前运行线程数: " + str(running_thread_num))
        while running_thread_num > 16:
            time.sleep(0.1)
        threading.Thread(target=remove, args=(child_dir,)).start()


if __name__ == "__main__":
    root_path = input("输入qq 'Group2' 文件夹路径：").strip()
    if root_path == "" or not os.path.exists(root_path):
        print("路径有误！")
        root_path = input("输入qq 'Group2' 文件夹路径：").strip()
    print("即将删除的路径为：" + os.path.abspath(root_path))
    result = input("是否继续(y/n)：").strip()
    if result == "y":
        main(root_path)
