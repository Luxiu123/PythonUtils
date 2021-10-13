# -*- coding: UTF-8 -*-
# by luxiu
# 2021-10-13
# 合并文件


import os
import sys
import logging

logging.basicConfig(level=logging.DEBUG, format="%(message)s")


class FileMerge:
    def start(self, source_dir: str, out_file=None):
        """
        source_dir: 分割文件夹
        out_file: 输出文件路径
        """
        if out_file is None:
            extension = os.path.splitext(os.listdir(source_dir)[0])[1]
            out_file = source_dir.strip("/").strip("\\") + extension
        self._merge(source_dir, out_file)

    def _merge(self, source_dir: str, out_file: str):
        """
        source_dir: 分割文件夹
        out_file: 输出文件路径
        """
        file_list = os.listdir(source_dir)
        file_list.sort(
            key=lambda a: os.path.getctime(os.path.join(source_dir, a))
        )  # 根据文件创建时间排序

        buffer_size = 1024
        out = open(out_file, mode="wb")
        logging.info(f"merging {source_dir}")
        for file in file_list:
            f = open(os.path.join(source_dir, file), mode="rb")
            buffer = f.read(buffer_size)
            while buffer != b"":
                out.write(buffer)
                buffer = f.read(buffer_size)
            logging.info(f"merging {file} successfully")
        out.close()
        logging.info(f"merging {source_dir} successfully")


if __name__ == "__main__":
    FileMerge().start(r"E:\Temp\a")
