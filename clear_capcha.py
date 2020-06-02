# encoding:utf-8
# Author:shi
# @Time:2020/6/1 13:52

import os
import time
import settings

from PIL import Image


class CleanCapcha(object):

    @staticmethod
    def get_img_filepath(dirname_path: str) -> list:
        """
        获取图片的文件名
        :dirname_path: 图片所在目录路径
        :return:  list[filepath]
        """
        img_filename_list = os.listdir(dirname_path)  # 获取原始图片所有文件名
        # print('文件名',img_filename_list)
        img_filepath_list = [dirname_path + "/" + file for file in img_filename_list]
        print(img_filepath_list)
        return img_filepath_list

    @staticmethod
    def get_new_img(img, threshold=100):
        """
        图片二值化
        :param threshold: 阈值，pixel表示黑白颜色的分界点
        :param img: PIL.Image对象
        :return: PIL.Image对象
        """
        # 新建一个纯白色的空图片，用来存放二值化的图片
        new_img = Image.new("L", img.size, 255)
        # 灰度处理, RGB三通道转换为单通道
        img = img.convert("L")
        # 通过设置pixel阈值， 将图片转化为黑白的img，黑色：pixel=0，白色：pixel=255
        # 由于最外圈一个像素值不会有验证码，有的会有一个黑边，这边在处理的时候直接转化为白色
        for y in range(1, img.size[1] - 1):
            for x in range(1, img.size[0] - 1):
                pixel = img.getpixel((x, y))  # 像素值
                if pixel < threshold:
                    new_img.putpixel((x, y), 0)

        # new_img.save('1.png')
        return new_img

    @staticmethod
    def clean_hot_pixel(img):
        """
        处理噪点，利用的算法是，在一个黑色点的四周八个像素如果黑色像素的数量小于等于2个的点被清除
        :param img: PIL.Image对象
        :return: 清理后的图像
        """
        for x in range(img.size[0]):
            for y in range(img.size[1]):
                pixel = img.getpixel((x, y))
                if pixel == 0:
                    black_count = 0
                    # 检测黑色像素四周的黑色像素点的个数
                    for current_x in range(x - 1, x + 2):
                        for current_y in range(y - 1, y + 2):
                            if img.getpixel((current_x, current_y)) == 0:
                                black_count += 1
                    if black_count <= 2:
                        img.putpixel((x, y), 255)
        # img.save('2.png')
        return img

    @staticmethod
    def get_split_dot_position(img):
        """
        分割图片, 垂直投影法切割图片
        :param img: PIL.Image
        :return: 分割后的图片列表
        """
        x_line = []  # 投影后，黑色像素点的个数

        for x in range(img.size[0]):
            count = 0
            for y in range(img.size[1]):
                if img.getpixel((x, y)) == 0:
                    count += 1
            x_line.append(count)

        # 按x轴位置这一列上都是白色像素之间的连续黑色像素为一个字符
        position = []
        start = 0
        for i in range(len(x_line)):
            if x_line[i] != 0 and start == 0:
                # 如果一个黑色像素两边都是黑色像素，则跳过
                if x_line[i - 1] == 0 and x_line[i + 1] == 0:
                    continue
                start = i  # 记录字符的起始位置

            if x_line[i] == 0 and start != 0:
                end = i
                # 如果一个字符大于5个像素，则认为是一个合法的字符
                if end - start > 5:
                    position.append((start, end))
                    # 重置起始位置
                    start = 0
                    end = 0
        # print(position)
        return position

    @staticmethod
    def check_handle_many_char(img, position, new_size):
        """
        判断图片是否黏连，并处理
        :param img: PIL.Image
        :param new_size: 切割后的图片大小
        :return: 分割后的图片列表
        """

        length = 4
        # 分割完后判断是否有粘连的字符
        new_position = []
        for pos in position:
            # 如果字符的起始位置大于平均字符长度，则认为是有粘连的
            if pos[1] - pos[0] > img.size[0] / length:
                new_position.append((pos[0], pos[0] + int((pos[1] - pos[0]) / 2)))
                new_position.append((pos[0] + int((pos[1] - pos[0]) / 2) + 1, pos[1]))
            else:
                new_position.append(pos)

        # print("cut position --> ", new_position)
        # 通过起始位置切割图片
        char_img_list = []
        # new_size = (24,32)
        for idx, pos in enumerate(new_position):
            # print(idx, pos)
            new_img = Image.new("L", (24, 32), 255)
            crop_img = img.crop((pos[0], 0, pos[1], img.size[1]))
            new_img.paste(crop_img, (int((25 - pos[1] + pos[0]) / 2), 0))
            char_img_list.append(new_img)
        # print(char_img_list)
        return char_img_list

    @staticmethod
    def clean_capcha_one(img):
        """
        清理并分割图片
        :param img:
        """
        # 二值化 获得黑白图片
        img = CleanCapcha.get_new_img(img, 50)
        # 清楚噪点
        img = CleanCapcha.clean_hot_pixel(img)
        # 寻找字符的起始位置，切割图片
        position = CleanCapcha.get_split_dot_position(img)
        # 检测是否有粘连的字符,并处理
        result_list = CleanCapcha.check_handle_many_char(img, position, new_size=(24, 32))
        return result_list


def deal_img():
    img_filepath_list = CleanCapcha.get_img_filepath(settings.org_img_file_path)
    for img_filepath in img_filepath_list:
        try:
            img = Image.open(img_filepath)
            char_img_list = CleanCapcha.clean_capcha_one(img)
            for char_img in char_img_list:
                filepath = settings.SPLIT_IMG_PATH + "/" + str(int(time.time() * 1000)) + ".png"
                # print(filepath)
                time.sleep(0.01)
                char_img.save(filepath)
        except Exception as e:
            pass


def get_new_img():
    img = Image.open(r'D:\tools\quanmin\train_img\1590994364.6231692.png')
    img = CleanCapcha.get_new_img(img, 50)
    img = CleanCapcha.clean_hot_pixel(img)
    position = CleanCapcha.get_split_dot_position(img)
    result = CleanCapcha.check_handle_many_char(img, position, new_size=(24, 32))
    for new_img in result:
        time.sleep(1)
        filepath = str(int(time.time())) + '.png'
        # print(filepath)
        new_img.save(filepath)


if __name__ == '__main__':
    deal_img()
