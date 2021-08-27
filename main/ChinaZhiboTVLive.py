# -*- coding: UTF-8 -*-

# 中国体育直播 live

import re
import time
import requests
import json
from bs4 import BeautifulSoup


def main(url: str) -> str:
    resp = requests.get(url)
    doc = BeautifulSoup(resp.text, features="html.parser")
    script = doc.select_one("body>script")
    if script is None:
        return ""
    url_pattern = re.compile(
        r"window\.(?P<id>\w+)\s*=\s*'(?P<url>[\x00-\xff]+)';\s+window\.flvPollUrl\s*=\s*window\.(?P=id);"
    )
    id_pattern = re.compile(r"window\.ourStreamName\s*=\s*'(\w+)';")
    reso_pattern = re.compile(r"window\.rtmpHighSource\s*=\s*'([\w?=&]+)';\n")
    url_match = re.search(url_pattern, script.string)
    id_match = re.search(id_pattern, script.string)
    reso_match = re.search(reso_pattern, script.string)
    if url_match is not None and id_match is not None and reso_match is not None:
        return f"{url_match.group('url')}{id_match.group(1)}{reso_match.group(1)}.flv"
    return ""


if __name__ == "__main__":
    url = input("输入链接：")
    print(main(url))
