# -*- coding: UTF-8 -*-
"""
中文简体繁体转换
"""
import json
trad_simp_map = {}  # {繁体: 简体}
simp_trad_map = {}  # {简体: 繁体}
with open('./WordMap.json', 'r', encoding='utf-8') as f:
    trad_simp_map = json.loads(f.read())
for key, val in trad_simp_map.items():
    simp_trad_map[val] = key


class Transform:
    @staticmethod
    def simplified_to_traditional(text: str) -> str:
        """
        简体转繁体
        """
        return Transform.replace(text, simp_trad_map)

    @staticmethod
    def traditional_to_simplified(text: str) -> str:
        """
        繁体转简体
        """
        return Transform.replace(text, trad_simp_map)

    @staticmethod
    def replace(text: str, word_map: dict) -> str:
        """
        替换
        """
        word_arr = []
        for word in text:
            word_arr.append(word_map.get(word, word))
        return ''.join(word_arr)


if __name__ == "__main__":
    text = "这是一段测试用例"
    print(Transform.simplified_to_traditional(text))
