# encoding:utf-8
# Author:shi
# @Time:2020/6/2 14:08

import requests
import time
import os
from predict_img import predict
from PIL import Image


def get_code():
    url = 'https://bj.122.gov.cn/m/tmri/captcha/math?nocache=1590988354893'
    headers = {
        'Usre-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    response = requests.get(url=url, headers=headers)
    # 图片绝对路径
    # 获取文件当前路径
    file_path = os.getcwd()
    now_file_path = file_path + r'/img/org_imgs/{}.png'
    now_time = time.time()
    img_file_path = now_file_path.format(now_time)
    with open(img_file_path, 'wb') as f:
        f.write(response.content)
    try:
        img = Image.open(img_file_path)
        text, result = predict(img)
        print(text, result)
    except Exception as e:
        pass
    # 识别图片后删除
    if os.path.exists(img_file_path):
        os.remove(img_file_path)
    time.sleep(1)


if __name__ == '__main__':
    get_code()
