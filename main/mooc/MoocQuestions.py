# -*- coding: UTF-8 -*-

# mooc习题文本格式处理
# 需要将文本复制下来
import re


def strip(string: str) -> str:
    return "\n".join(
        [line.strip() for line in string.split("\n") if line.strip() != ""]
    )  # 去掉空行


def main(filepath: str) -> str:
    text = ""
    with open(filepath, encoding="utf-8") as f:
        text = f.read()
    comp1 = re.compile(r"\(\d+分\)\n", re.M)  # 单选(1分)
    comp2 = re.compile(r"(\d+\.\d+|该题无法得分)/\d+\.\d+")  # 1.00/1.00
    comp3 = re.compile("得分/总分")  # 得分/总分
    comp4 = re.compile(r"(?P<p>[A-Za-z]\.\n)", re.M)  # A.\n
    comp5 = re.compile(r"(?P<p>\d+\.)")  # 在每题前换行
    comp6 = re.compile(r"(?P<p>[单多]选)")  # 多选
    comp7 = re.compile(r"正确答案：.+(你选对了|你错选为.+)\n?")  # 正确答案
    comp8 = re.compile(r"(?P<p>\w\.\n)")  # 替换 'A.\n' 为 'A.'
    comp9 = re.compile(r"(?P<p>\d+\.\[[单多]选\]\n\d+)")  # '14.[单选]\n1949'
    text = re.sub(comp1, "", text)
    text = re.sub(comp2, "", text)
    text = re.sub(comp3, "", text)
    text = re.sub(comp7, "", text)
    text = re.sub(comp4, lambda s: s.group(1)[:-1], text)
    text = strip(text)
    text = re.sub(comp6, lambda s: ".[" + s.group(1) + "]", text)
    text = re.sub(comp8, lambda s: s.group(1)[0:-1], text)
    # text = re.sub(comp9, lambda s: s.group(1).replace("\n", ""), text)
    text = re.sub(comp5, lambda s: "\n" + s.group(1), text)
    return text


if __name__ == "__main__":
    print(main("./../../src/mooc/MoocQuestions.txt"))
