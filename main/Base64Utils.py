# -*- coding: UTF-8 -*-

import os
import base64


class Base64Utils:
    @staticmethod
    def data_to_img(file, output):
        """
        base64转图片
        """
        with open(file, encoding='utf-8') as f:
            img_data = base64.b64decode(f.read())
            file = open(output, 'wb')
            file.write(img_data)
            file.close()

    @staticmethod
    def img_to_data(file, output):
        """
        图片转base64
        """
        with open(file, "rb") as f:  #转为二进制格式
            img_data = base64.b64encode(f.read())  #使用base64进行加密
            file = open(output, 'wb')  #写成文本格式
            file.write(img_data)
            file.close()


if __name__ == "__main__":
    Base64Utils.data_to_img("./../src/Base64Utils.txt", './../src/Base64Utils.jpg')
