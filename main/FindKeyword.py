# -*- coding: UTF-8 -*-
# by luxiu
# 2021-07-03
# 关键词文件搜索
import os
import re
import Utils


def load_text():
    """
    加载文本
    """
    for file in file_list:
        # 过滤 1M 以上文件
        if os.path.getsize(file["path"]) > 1048576:
            continue
        try:
            with open(file["path"], mode="rt", encoding="utf-8") as f:
                file["data"] = f.readlines()
        except Exception as e:
            continue


def load_file():
    """
    加载文件
    """
    file_list.clear()
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in files:
            obj = {"path": os.path.join(root, name), "rel": "", "data": []}
            obj["rel"] = "/" + os.path.relpath(obj["path"], directory).replace(
                "\\", "/"
            )
            file_list.append(obj)


def reload_filelist():
    """
    重新加载文件
    """
    print('reloading files...')
    load_file()
    load_text()
    print("reload success")


def find_keyword(pattern: str):
    try:
        pattern = re.compile(pattern, re.I)
    except Exception as e:
        Utils.print_error(e)
        return
    for file in file_list:
        if file["data"] == []:
            continue
        matched = False
        for index, line in enumerate(file["data"]):
            # 匹配文字
            if (matches := re.findall(pattern, line)) != []:
                # 输出一次文件名
                if not matched:
                    matched = True
                    print(file["rel"])
                Utils.print_sky_blue(f"\tline: {index+1}, {matches}")


directory = ""
file_list = []
while not os.path.isdir(directory := input("请输入搜索目录:")):
    Utils.print_error("给定路径不为目录!")
print("加载文件中...")
load_file()
load_text()
print("文件加载完成...")

while True:
    print("---------------------------------------------------")
    pattern = input("请输入正则表达式(输入'r'重新加载文件)：")
    if pattern.strip() == "r":
        reload_filelist()
        continue
    find_keyword(pattern)
