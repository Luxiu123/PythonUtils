# -*- coding: UTF-8 -*-
# by luxiu
# 2022-5-16
# 图片添加文字
import subprocess
import sys

text = 'hello world'

subprocess.call(
    f'ffmpeg -i "{sys.argv[1]}" -vf drawtext=fontfile="c\\\\:windows/fonts/msyhl.ttc":fontcolor="#2A8CD3":fontsize=70:text="{text}":x=50:y=650 out.jpg'
)
