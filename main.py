# -*- coding: utf8 -*-
# @project : jt_122_capcha
# @author  : allen
# @file    : main.py
# @ide     : PyCharm
# @time    : 2019-12-05 13:50:06

import settings
from train import trainModel
from get_feature import get_feature


def main():
    feature, label = get_feature()  # 获取分割图片的特征值和对应的标签
    # 将特征值和标签加入模型进行训练
    result = trainModel(feature, label)  # 训练模型


if __name__ == '__main__':
    main()
