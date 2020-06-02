# encoding:utf-8
# Author:shi
# @Time:2020/6/1 13:10

import requests
import time
import os


# print(os.getcwd())
# print(os.path.abspath('.'))
# print(os.path.abspath(os.curdir))


def get_imgs():
    url = 'https://bj.122.gov.cn/m/tmri/captcha/math?nocache=1590988354893'
    headers = {
        'Usre-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    for i in range(0, 40):
        response = requests.get(url=url, headers=headers)
        # 图片绝对路径
        # 获取文件当前路径
        now_file_path = os.getcwd()
        img_file_path = now_file_path + r'/img/org_imgs/{}.png'
        now_time = time.time()
        print(img_file_path)
        with open(img_file_path.format(now_time), 'wb') as f:
            f.write(response.content)
        time.sleep(1)
    print('图片保存完毕')


get_imgs()
