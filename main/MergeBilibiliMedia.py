# -*- coding: UTF-8 -*-
# by luxiu
# 2021-07-30
# 合并bilibili客户端下载的音视频文件
import os
import json
import time
import Utils

# 文件名特殊字符
SPECIAL_CHARACTER = ("?", "*", ":", '"', "<", ">", "\\", "/", "|")


def validate_filename(name: str) -> str:
    """
    使文件名字有效
    """
    # ? * : " < > \ / |
    for c in SPECIAL_CHARACTER:
        name = name.replace(c, "")
    return name.strip()


def get_filename(filepath: str) -> str:
    """
    获取文件名
    """
    with open(filepath, mode="rt", encoding="utf-8") as f:
        text = f.read()
    obj = json.loads(text)
    return validate_filename(obj["page_data"]["download_subtitle"].replace(obj['title'], ''))


def main(out_dir, root_dir):
    dir_items = os.listdir(root_dir)
    for index, item in enumerate(dir_items):
        entry_path = os.path.join(root_dir, item, "entry.json")
        video_path = os.path.join(root_dir, item, "80", "video.m4s")
        audio_path = os.path.join(root_dir, item, "80", "audio.m4s")
        dist_path = os.path.join(out_dir, f"{get_filename(entry_path)}.mp4")
        if os.path.exists(dist_path):
            os.remove(dist_path)
        command = (
            f'ffmpeg -i "{video_path}" -i "{audio_path}" -codec copy "{dist_path}"'
        )
        print("processing command " + command)
        os.popen(command)
        time.sleep(0.5)
        # os.system(command)


if __name__ == "__main__":
    root_dir = input("输入视频根目录路径：").strip()
    while not Utils.is_path_valid(root_dir):
        print("路径无效！")
        root_dir = input("输入视频根路径：").strip()
    out_dir = input("输入保存目录路径：").strip()
    while not Utils.is_path_valid(out_dir):
        print("路径无效！")
        out_dir = input("输入保存目录路径：").strip()
    main(out_dir, root_dir)
