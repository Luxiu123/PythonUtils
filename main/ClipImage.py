# -*- coding: UTF-8 -*-
# by luxiu
# 2021-11-01
# 裁剪图片
import PIL.Image as img
import os
import re
import Utils


def clip(src_path: str, rect, out_path=None):
    """
    out_path: 默认输出到源文件夹
    """
    image = img.open(src_path)
    if rect is None:
        raise Exception("rect 为 None")
    for i in range(4):
        rect[i] = int(rect[i])
    if out_path is None:
        res = re.findall(Utils.FILE_REGEXP, src_path)
        if len(res) != 1:
            raise Exception("路径有误")
        res = res[0]
        out_path = os.path.join(res[0], f"{res[1]} - clip{res[2]}")
    image.crop(rect).save(out_path)


def clip_batch(src_dir: str, rect, out_dir: str):
    for file in os.listdir(src_dir):
        try:
            out_path = os.path.join(out_dir, file)
            res = re.findall(Utils.FILE_REGEXP, out_path)
            if len(res) != 1:
                raise Exception("路径有误")
            res = res[0]
            out_path = os.path.join(res[0], f"{res[1]} - clip{res[2]}")
            clip(os.path.join(src_dir, file), rect, out_path)
            print("finish", file)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    str1 = "输入裁剪目录："
    str2 = "输入保存目录(默认源路径)："
    str3 = "输入裁剪的坐标(xmin,ymin,xmax,ymax 以空格分隔)："
    src_path = input(str1)
    while not os.path.exists(src_path):
        src_path = input(str1)
    out_path = input(str2).strip()
    while out_path != "" and not os.path.exists(src_path):
        out_path = input(str2).strip()
    if out_path == "":
        out_path = src_path
    rect = re.split(r"\s+", input(str3))
    while len(rect) != 4:
        print("坐标错误！")
        rect = re.split(r"\s+", input(str3))
    clip_batch(src_path, rect, out_path)
