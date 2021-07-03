import re
import time
import numpy
import csv
import requests
import threading
import json
from bs4 import BeautifulSoup


def test():
    url = input("input link:")
    # url = "http://static.zhibo.tv/detail/video/16ef86e0-c47e-11eb-a307-0c42a1da69f6"
    header = {}
    resp = requests.get(url, headers=header).text
    soup = BeautifulSoup(resp, features="html.parser")
    text = soup.find("head").find("script")
    if text is not None:
        text = text.string
        pattern = re.compile(r"window\.vurl = '(.+)';")
        res = re.search(pattern, text)
        # print(res.group(1))
        return res.group(1)
    else:
        text = soup.find('body').find('script').string
        pattern = re.compile(r'videourl:"(.+)",imgurl')
        res = re.search(pattern, text)
        # print(res.group(1).encode().decode(encoding='unicode_escape'))
        return res.group(1).encode().decode(encoding='unicode_escape')
    # with open("./../src/a.html", encoding="utf-8", mode='wt') as f:
    #     f.write(resp)
    # print(text)


def download(filepath: str, url: str) -> None:
    print(url)
    header = {
        "Referer": "http://video.zhibo.tv/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41",
    }
    file = open(filepath, mode="wb")
    count = 0
    resp = requests.get(url, headers=header, stream=True)
    total_size = int(resp.headers["Content-Length"])
    resp.close()
    with requests.get(url, headers=header, stream=True) as r:
        for chunk in r.iter_content(chunk_size=1024):
            count+=len(chunk)
            file.write(chunk)
            print("\r进度：{:.2f}%".format(count/total_size*100),end='')
    file.close()


if __name__ == "__main__":
    # download(
    #     "E:/temp/a.mp4",
    #     "http://1252040487.vod2.myqcloud.com/8bdce988vodtransgzp1252040487/55db59135285890818144980752/v.f30.mp4?t=60c39c65&us=88999&sign=1a94e0db9c205f4272347db3ca4f677b",
    # )
    filepath = input("输入保存路径：")
    download(filepath, test())
    # data = {
    #     "videourl": "http:\u002F\u002F1252040487.vod2.myqcloud.com\u002F8bdce988vodtransgzp1252040487\u002F03a707535285890819024597291\u002Fv.f30.mp4?t=60c3ac4e&us=43333&sign=9878b07832505ae77679a0b9e5e16436",
    #     "imgurl": "http:\u002F\u002F1252040487.vod2.myqcloud.com\u002F8bdce988vodtransgzp1252040487\u002F03a707535285890819024597291\u002Fsnapshot\u002FsnapshotByTimeOffset_10_3.jpg",
    # }
    # print(data)
