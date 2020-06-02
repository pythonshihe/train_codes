# encoding:utf-8
# Author:shi
# @Time:2020/6/2 13:27

import settings
import os
from PIL import Image
import joblib
from clear_capcha import CleanCapcha


def get_feature(img):
    """获取验证码的特征值"""
    feature = []
    for x in range(img.size[0]):
        black_count = 0
        for y in range(img.size[1]):
            pixel = img.getpixel((x, y))
            if pixel == 0:
                black_count += 1
        feature.append(black_count)

    for y in range(img.size[1]):
        black_count = 0
        for x in range(img.size[0]):
            pixel = img.getpixel((x, y))
            if pixel == 0:
                black_count += 1
        feature.append(black_count)
    return feature


def predict(img):
    # 图片预处理 并切割
    img_split_list = CleanCapcha.clean_capcha_one(img)
    # 获取特征值
    feature = [get_feature(img) for img in img_split_list]
    # 预测
    model = joblib.load(settings.MODAL_PATH)
    predict_array = model.predict(feature)  # 识别到的内容列表['7' 'b' '1' 'e']
    char_txt = "".join(predict_array[:-1]).replace("a", "+").replace("b", "-").replace("c", "*").replace("d", "//")
    return char_txt, eval(char_txt)


if __name__ == '__main__':
    img_path = r'D:\tools\quanmin\train_img\1590994364.6231692.png'
    img = Image.open(img_path)
    text,result = predict(img)
    print(text,result)
