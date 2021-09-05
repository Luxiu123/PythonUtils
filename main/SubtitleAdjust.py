# -*- coding: UTF-8 -*-

# 字幕时间对齐
import re
import time
import os
import datetime
import sys


class BaseType:
    def __init__(self, type_: str, offset: float, source: list):
        self.pattern = re.compile(r"")
        self.type_ = type_
        self.source = source
        self.offset = offset

    def replace(self) -> str:
        return ""

    def adjust(self, rep) -> str:
        return ""


class SRT(BaseType):
    def __init__(self, offset: float, source: list):
        super().__init__("srt", offset, source)
        # 00:00:24,830
        self.pattern = re.compile(r"(?P<t>\d{2}:\d{2}:\d{2}),(?P<milli>\d{3})")

    def replace(self) -> str:
        repl_list = []
        for line in self.source:
            repl_list.append(re.sub(self.pattern, self.adjust, line[:45]) + line[45:])
        return "".join(repl_list)

    def adjust(self, rep) -> str:
        t = "2020-01-01 " + rep.group("t")
        t = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        # 时间戳 / 1000
        time_stamp = (
            time.mktime(t) * 1000 + int(rep.group("milli"))
        ) / 1000 + self.offset
        t = datetime.datetime.fromtimestamp(time_stamp).strftime("%H:%M:%S,%f")[:-3]
        return t


class ASS(BaseType):
    def __init__(self, offset: float, source: list):
        super().__init__("ass", offset, source)
        # 0:04:49.72
        self.pattern = re.compile(r"(?P<t>\d{1,2}:\d{2}:\d{2})\.(?P<p>\d{2})")

    def replace(self) -> str:
        repl_list = []
        for line in self.source:
            repl_list.append(re.sub(self.pattern, self.adjust, line[:45]) + line[45:])
        return "".join(repl_list)

    def adjust(self, rep) -> str:
        t = "2020-01-01 " + rep.group("t")
        t = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        # 时间戳 / 1000
        time_stamp = (
            time.mktime(t) * 1000 + int(rep.group("p"))*10
        ) / 1000 + self.offset
        t = datetime.datetime.fromtimestamp(time_stamp).strftime("%H:%M:%S.%f")[:-4]
        return t


class SubtitleAdjust:
    def __init__(self, source_path, out_path, offset):
        self.__source = source_path
        self.__out = out_path
        self.__offset = offset
        self.__type = self.__get_type(source_path)

    def __get_type(self, path: str) -> str:
        """
        获取文件扩展名
        """
        return os.path.splitext(os.path.split(path)[1])[1]

    def __read_lines(self):
        """
        读取文件
        """
        lines = []
        try:
            with open(self.__source, encoding="utf-8") as f:
                lines = f.readlines()
        except Exception as e:
            print(e)
            sys.exit(0)
        return lines

    def __write(self, string):
        """
        写入文件
        """
        with open(self.__out, mode="wt", encoding="utf-8") as f:
            f.write(string)
        print("success")

    def replace(self):
        out = ""
        if self.__type.lower() == ".srt":
            out = SRT(self.__offset, self.__read_lines()).replace()
        elif self.__type.lower() == ".ass":
            out = ASS(self.__offset, self.__read_lines()).replace()
        self.__write(out)


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
