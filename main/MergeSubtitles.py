# -*- coding: UTF-8 -*-

# 合并字幕
import re
import os
import Utils


class MergeSubtitles:
    def __init__(self, en_file: str, ch_file: str, dist_file: str = None):
        self.__meta = """[Script Info]
ScriptType: v4.00+
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,微软雅黑,22,&Hffffff,&Hffffff,&H0,&H0,0,0,0,0,100,100,0,0,1,0.5,0,2,10,10,10,0

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"""
        self.__en_file = en_file
        self.__ch_file = ch_file
        self.__file_type = "srt"
        prename = "./../src/MergeSubtitles/dist"
        self.__dist_file = prename if dist_file is None else dist_file
        self.__init()

    class TextList:
        text_list = []
        time_line = []

        def __init__(self, text_list, time_line):
            self.text_list = text_list
            self.time_line = time_line

    def __init(self):
        """
        初始化
        """
        self.__file_type = self.__get_file_type(self.__en_file)

    def __get_file_type(self, file: str) -> str:
        """
        获取文件类型
        """
        basename = os.path.basename(file)
        return os.path.splitext(basename)[1]

    def __get_ass_subtitles(self, text: str) -> TextList:
        text_list = text.split("\n")
        sub_list = []
        time_list = []
        pattern = (
            r"(\d+,\d+:\d+:\d+\.\d+,\d+:\d+:\d+\.\d+,(?:.+)?,(?:.+)?,\d+,\d+,\d+,,)(.*)"
        )
        pattern = re.compile(pattern, re.S)
        prefix = "Dialogue: "
        for line in text_list:
            # 正文都是以 prefix 开头
            if line.startswith(prefix):
                matches = re.search(pattern, line)
                if matches is not None:
                    time_list.append(prefix + matches.group(1))
                    sub_list.append(matches.group(2))
        return self.TextList(sub_list, time_list)

    def __merge_ass(self, ch_list: list, en_list: list, time_list: list) -> str:
        sub_list = []
        for i in range(len(ch_list)):
            sub_list.append(f"{time_list[i]}{ch_list[i]}\\N{en_list[i]}")
        return self.__meta + "\n".join(sub_list)

    def __get_srt_subtitles(self, text: str) -> TextList:
        text_list = text.split("\n")
        sub_list = []
        time_list = []
        pattern = r"^\d+$"  # 序号
        is_time = False
        is_text = False
        text_buffer = None
        pattern = re.compile(pattern)
        for line in text_list:
            line = line.strip()
            if line == "":
                continue
            matches = re.match(pattern, line)
            # 匹配序号
            if matches is not None:
                is_time = True
                is_text = False
                # 起始，为false
                if text_buffer is not None:
                    sub_list.append(text_buffer)
                text_buffer = ""
                continue
            if is_time:
                time_list.append(line)
                is_time = False
                is_text = True
                continue
            if is_text:
                text_buffer += line + " "
        sub_list.append(text_buffer.strip())
        return self.TextList(sub_list, time_list)

    def __merge_srt(self, ch_list: list, en_list: list, time_list: list) -> str:
        sub_list = []
        for i in range(len(ch_list)):
            sub_list.append(f"{i+1}\n{time_list[i]}\n{ch_list[i]}\n{en_list[i]}\n\n")
        return "".join(sub_list)

    def __read(self, file: str) -> str:
        text = ""
        try:
            f = open(file, encoding="utf-8")
            text = f.read()
        except Exception as e:
            f.close()
            try:
                f = open(file, encoding="gbk")
                text = f.read()
            except Exception as e:
                f.close()
                raise e
        return text

    def merge(self):
        dist_file = open(
            self.__dist_file + self.__file_type, mode="wt", encoding="utf-8"
        )
        en_text = self.__read(self.__en_file)
        ch_text = self.__read(self.__ch_file)
        if self.__file_type == ".ass":
            en_list = self.__get_ass_subtitles(en_text)
            ch_list = self.__get_ass_subtitles(ch_text)
            print(len(en_list.text_list), len(en_list.time_line))
            print(len(ch_list.text_list), len(ch_list.time_line))
            dist_file.write(
                self.__merge_ass(
                    ch_list.text_list, en_list.text_list, en_list.time_line
                )
            )
        elif self.__file_type == ".srt":
            en_list = self.__get_srt_subtitles(en_text)
            ch_list = self.__get_srt_subtitles(ch_text)
            dist_file.write(
                self.__merge_srt(
                    ch_list.text_list, en_list.text_list, en_list.time_line
                )
            )
        dist_file.close()


if __name__ == "__main__":
    en_path = input("输入英文字幕路径：").strip()
    while not Utils.is_path_valid(en_path):
        print("路径无效！")
        en_path = input("输入英文字幕路径：").strip()
    ch_path = input("输入中文字幕路径：").strip()
    while not Utils.is_path_valid(ch_path):
        print("路径无效！")
        ch_path = input("输入中文字幕路径：").strip()
    MergeSubtitles(en_path, ch_path).merge()
