import requests
import re
import random


def get_number():
    number = random.randint(0, 100)
    if number > 90:
        sign = 1
        level = "大吉"
    elif 90 >= number > 65:
        sign = 2
        level = "中吉"
    elif 65 >= number > 35:
        sign = 3
        level = "小吉"
    elif 40 >= number > 10:
        sign = 4
        level = "半吉"
    else:
        sign = 5
        level = "末吉"
    return sign, level


def luck():
    page_number, lucky_level = get_number()
    url = "http://www.paopaoche.net/sj/153170_" + str(page_number) + ".html"
    response = requests.get(url)
    print("luck函数请求网址完毕")
    html = response.content.decode('gbk')
    shtml = str(html)
    part_re_sign = re.findall(r'签文：(.*)。', shtml)
    part_de_sign = re.findall(r'解签：(.*)。', shtml)
    choice = random.randint(0, len(part_de_sign) - 1)
    re_sign = "签诗:" + part_re_sign[choice] + "。"
    de_sign = "解签:" + part_de_sign[choice] + "。"
    text = lucky_level + "%0a" + re_sign + "%0a" + de_sign
    return text
