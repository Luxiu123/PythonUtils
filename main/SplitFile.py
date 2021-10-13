# -*- coding: UTF-8 -*-
# by luxiu
# 2021-10-13
# 分割文件


import os
import sys
import logging
import time

logging.basicConfig(level=logging.DEBUG, format="%(message)s")


class FileSplit:
    def start(self, file: str, dist_dir=None, per_size=None):
        """
        file: 文件路径
        dist_dir: 保存文件夹路径
        per_size: 分割后每个文件大小 MB，默认为源文件大小 10%
        """
        if dist_dir is None:
            split = os.path.split(file)
            source_dir = split[0]
            filename = os.path.splitext(split[1])[0]
            dist_dir = os.path.join(source_dir, filename)
        if per_size is None:
            per_size = os.path.getsize(file) / 10
        else:
            per_size = per_size * 1024 * 1024

        if not os.path.exists(dist_dir):
            os.mkdir(dist_dir)  # 创建文件夹
        self._split(file, dist_dir, per_size)

    def _split(self, file: str, dist_dir: str, per_size):
        """
        file: 文件路径
        dist_dir: 保存文件夹路径
        per_size: 分割后每个文件大小 byte
        """
        file_index = 1  # 文件索引
        size_count = 0  # 文件大小计数
        buffer_size = 65536  # 缓冲区大小
        # file_num = int(os.path.getsize() / (per_size * 1024 * 1024))  # 分割文件总数
        extension = os.path.splitext(os.path.split(file)[1])[1]  # 扩展名
        start_time = int(time.time() * 1000)  # 起始时间

        with open(file, mode="rb") as f:
            buffer = f.read(buffer_size)
            f2 = open(os.path.join(dist_dir, f"{file_index}{extension}"), mode="wb")
            while buffer != b"":
                f2.write(buffer)
                size_count += buffer_size
                buffer = f.read(buffer_size)
                # 文件写入完毕
                if size_count >= per_size:
                    logging.info(f"writing {f2.name} successfully")
                    f2.close()
                    file_index += 1
                    size_count = 0
                    f2 = open(
                        os.path.join(dist_dir, f"{file_index}{extension}"), mode="wb"
                    )
            f2.close()
            logging.info(f"writing {f2.name} successfully")
            end_time = int(time.time() * 1000)  # 起始时间
            print(f"总耗时 {end_time-start_time} ms")


if __name__ == "__main__":
    path = input("输入要分割的文件路径：")
    while not os.path.exists(path):
        path = input("输入要分割的文件路径：")
    size = input("输入分割大小(MB) (默认为源文件大小 10%)：")
    if size.strip() == "":
        FileSplit().start(path)
        sys.exit()

    while True:
        try:
            size = int(size)
            if size <= 0:
                raise ValueError()
            FileSplit().start(path, per_size=size)
            break
        except Exception as e:
            logging.error("非法数字！")
        size = input("输入分割大小(MB) (默认为源文件大小 10%)：")
