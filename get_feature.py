# encoding:utf-8
# Author:shi
# @Time:2020/6/2 10:27

import os
import settings
import numpy as np
from PIL import Image


class Feature(object):

    @classmethod
    def get_feature(cls, img_dirname):
        """
        获取图片的特征值,特征值是图片width，height的行/列的黑色像素的个数
        :param img_dirname: 剪切后的图片的目录路径
        :return: array[feature], array[label]
        os.listdir(img_dirname) 获取文件夹下所有的文件名
        """
        feature = []
        label = []
        for label_dir in os.listdir(img_dirname):
            pic_dirname = img_dirname + "/" + label_dir
            # print("各个图片分类的文件夹路径", pic_dirname)
            for img in os.listdir(pic_dirname):  # img文件名
                img_filepath = os.path.join(pic_dirname, img)  # 每个分类图片的路径
                img_feature = cls.get_one_feature(img_filepath)
                feature.append(img_feature)
                label.append(label_dir)

        # print(feature)
        # print(label)

        return feature, label

    @classmethod
    def get_one_feature(cls, img_filepath):
        """
        按文件路径获取图片的特征矩阵
        :param img_filepath:
        :return: x,y轴黑色像素点的矩阵
        """
        img = Image.open(img_filepath)
        feature = []
        # print(img.size)  (24, 32) 图片的大小
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
        # print(feature)
        return feature


def get_feature():
    img_dirname = settings.FENLEI_IMG_PATH
    feature_array, label_array = Feature.get_feature(img_dirname)
    print("feature length--> ", len(feature_array))
    print("label length--> ", len(label_array))
    return feature_array, label_array


if __name__ == '__main__':
    get_feature()
