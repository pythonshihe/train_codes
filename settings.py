# encoding:utf-8
# Author:shi
# @Time:2020/6/1 13:52
import os

# # 项目路径
# PROJECT_PATH = os.path.dirname(__file__)
# print(PROJECT_PATH)

# print(os.getcwd())

# 原始图片路径
org_img_file_path = os.getcwd() + r'/img/org_imgs'
print(org_img_file_path)

# 分割后的验证码路径
SPLIT_IMG_PATH = os.getcwd() + r"/img/split_imgs"

# 分类后的验证码路径
FENLEI_IMG_PATH = os.getcwd() + r"/img/fenlei"

# 模型保存路径
MODAL_PATH = os.getcwd() + r"/modal/jt_122_modal"

