import os
from random import choice
def picture(title):
    title = title[1:]
    path = "E:\data\\"+ title +"\\"#用自己的本地图片地址替换
    ghs_list = os.listdir(path)
    local_img_url = "[CQ:image,file=file:///" + path + choice(ghs_list) + "]"
    print(local_img_url)
    return local_img_url