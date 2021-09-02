# -*- coding: UTF-8 -*-

# 字幕时间对齐
import re
import time
import os

comp = re.compile(r"(?P<t>\d{1,2}:\d{2}:\d{2})")


class SubtitleAdjust:
    def __init__(self, source_path, dist_path, second):
        self.source = source_path
        self.dist = dist_path
        self.second = second

    def __adjust(self, rep):
        t = "2020-01-01 " + rep.group("t")
        t = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        time_stamp = time.mktime(t) + self.second
        t = time.localtime(time_stamp)
        t = time.strftime("%H:%M:%S", t)
        return t

    def __read_lines(self):
        lines = []
        with open(self.source, encoding="utf-8") as f:
            lines = f.readlines()
        return lines

    def replace(self):
        repl_list = []
        for line in self.__read_lines():
            repl_list.append(re.sub(comp, self.__adjust, line[:40]) + line[40:])
        self.__write("".join(repl_list))

    def __write(self, string):
        with open(self.dist, mode="wt", encoding="utf-8") as f:
            f.write(string)
        print("success")


if __name__ == "__main__":
    while True:
        src = input("请输入字幕路径(默认为'../src/SubtitleAdjust.srt'):")
        if src.strip() == "":
            src = "../src/SubtitleAdjust.srt"
        dirname, filename = os.path.split(src)
        suffix = os.path.splitext(filename)
        try:
            t = float(input("请调节时间(字幕超前, 为正):"))
            SubtitleAdjust(src, os.path.join(dirname, "dist" + suffix[1]), t).replace()
        except Exception as e:
            print(e)
