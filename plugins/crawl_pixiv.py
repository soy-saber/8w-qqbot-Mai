import selenium
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import requests
import json
import time
import os


with open('E:\\pixiv\\record.txt', 'r') as last_max_id_get:
    last_record = json.loads(last_max_id_get.readline())
    last_max_id = last_record['last_max_id']
current_max_id = 0
today_ark_new = []
today_fgo_new = []
today_blhx_new = []
today_tt_new = []
today_ys_new = []
today_xiao_new = []
today_miku_new = []


def pixiv_info_get():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('lang=zh_CN.UTF-8')
    options.add_argument('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, li'
                         'ke Gecko) Chrome/90.0.4430.72 Mobile Safari/537.36 Edg/90.0.818.41')
    prefs = {
        'profile.default_content_setting_values': {
            'images': 2,
        }
    }
    options.add_experimental_option('prefs', prefs)
    pixiv_login = webdriver.Chrome(r'D:\selenium-driver\chromedriver.exe', chrome_options=options)
    url = "https://www.pixiv.net/bookmark_new_illust.php?=1"
    pixiv_login.get(url)
    time.sleep(10)
    # 第一层的登录按钮
    login_bottom1 = pixiv_login.find_element_by_xpath('//*[@id="wrapper"]/div[3]/div[2]/a[2]')
    login_bottom1.click()
    username = ""
    secret = ""
    # 用户名//*[@id="LoginComponent"]/form/div[1]/div[1]/input
    username_input = pixiv_login.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[1]/input')
    # 密码//*[@id="LoginComponent"]/form/div[1]/div[2]/input
    secret_input = pixiv_login.find_element_by_xpath('//*[@id="LoginComponent"]/form/div[1]/div[2]/input')
    username_input.send_keys(username)
    secret_input.send_keys(secret)
    # 第二层的登录按钮//*[@id="LoginComponent"]/form/button
    login_bottom2 = pixiv_login.find_element_by_xpath('//*[@id="LoginComponent"]/form/button')
    login_bottom2.click()
    time.sleep(5)
    print("账号已登录")
    # 获取cookie
    dict_cookie = {}
    for i in pixiv_login.get_cookies():
        dict_cookie[i["name"]] = i["value"]
    cookie = json.dumps(dict_cookie)
    # 48
    for current_page_number in range(1, 101):
        print('正在前往第{}页图片'.format(current_page_number))
        # https://www.pixiv.net/bookmark_new_illust_r18.php
        url = "https://www.pixiv.net/bookmark_new_illust.php?p=" + str(current_page_number)
        pixiv_login.get(url)
        time.sleep(20)
        # 图的id
        artworks_id = pixiv_login.find_elements_by_class_name("PKslhVT")
        artwork_id_list = []
        artwork_page_numbers_list = []
        # 获取页面图片的编号
        for item in artworks_id:
            artwork_id_list.append(item.get_attribute('href').split('/')[-1])
        if current_page_number == 1:
            global current_max_id
            current_max_id = int(artwork_id_list[0])
            print(current_max_id)
        for i in range(1, 21):
            try:
                # 有几张图
                artworks_page_numbers = pixiv_login.find_element_by_xpath('//*[@id="js-mount-point-latest-following"]/div/div[' + str(i) + ']/figure/div/a/div[1]/span')
                artwork_page_numbers_list.append(artworks_page_numbers.text)
            except selenium.common.exceptions.NoSuchElementException:
                artwork_page_numbers_list.append(1)
        # 若返回false 直接结束
        print(artwork_id_list)
        if picture_tags_judge(cookie, artwork_id_list, artwork_page_numbers_list):
            print("未更新完毕")
            pass
        else:
            print("更新完毕")
            pixiv_login.quit()
            return


# 参数 cookie 所有画的id 每张画有几张
def picture_tags_judge(cookie, artwork_id_list, artwork_page_numbers_list):
    ark_num = 0
    teio_num = 0
    ys_num = 0
    b3_num = 0
    blue_num = 0
    fgo_num = 0
    flag = True
    # 一页20张图
    for pic_num in range(0, 20):
        print(pic_num)
        if int(artwork_id_list[pic_num]) <= last_max_id:
            print("新图已更新完毕")
            flag = False
            return flag
        else:
            print("pid={}".format(artwork_id_list[pic_num]))
            header = {
                    "authority": "www.pixiv.net",
                    "path": "/artworks/" + artwork_id_list[pic_num],
                    "sec-ch-ua": "\"Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
                    "sec-ch-ua-mobile": "?0",
                    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTM"
                                  "L, like Gecko) Chrome/90.0.4430.72 Safari/537.36",
                    "cookie": cookie
                }
            tag_url = "https://www.pixiv.net/ajax/illust/" + artwork_id_list[pic_num] + "?lang=zh"
            tag_response = ''
            while 1:
                try:
                    tag_response = requests.get(tag_url, headers=header)
                    break
                except requests.exceptions.ProxyError as connect_error:
                    print("请求失败", connect_error)
                    time.sleep(30)
                    continue
            # 字符串形式的\u直接保存
            pic_info_list = json.loads(tag_response.text)
            tag_len = (len(pic_info_list['body']['tags']['tags']))
            tags_list = []
            for i in range(0, tag_len):
                tags_list.append(pic_info_list['body']['tags']['tags'][i]['tag'])
            print(tags_list)
            if 'R-18' in tags_list:
                limitation = 'R-18'
                if '明日方舟' in tags_list or 'arknight' in tags_list or 'Arknights' in tags_list:
                    print("方舟图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '方舟'
                    ark_num += 1
                elif 'ダイワスカーレット' in tags_list or 'ウマ娘' in tags_list or 'ウマ娘プリティーダービー' in tags_list:
                    print("赛马娘图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '赛马娘'
                    teio_num += 1
                elif '原神' in tags_list:
                    print("原神图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '原神'
                    ys_num += 1
                elif '崩坏3rd' in tags_list:
                    print("崩三图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '崩三'
                    b3_num += 1
                elif '碧蓝航线' in tags_list:
                    print("碧蓝图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '碧蓝航线'
                    blue_num += 1
                elif 'FGO' in tags_list or 'Fate/GrandOrder' in tags_list:
                    print("FGO图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = 'fgo'
                    fgo_num += 1
                else:
                    continue
                picture_download(pic_download_url, limitation, category, artwork_page_numbers_list[pic_num], cookie)

            else:
                limitation = 'normal'
                if '明日方舟' in tags_list or 'arknight' in tags_list or 'Arknights' in tags_list:
                    print("方舟图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '方舟'
                    ark_num += 1
                elif 'ダイワスカーレット' in tags_list or 'ウマ娘' in tags_list or 'ウマ娘プリティーダービー' in tags_list:
                    print("赛马娘图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '赛马娘'
                    teio_num += 1
                elif '原神' in tags_list:
                    print("原神图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '原神'
                    
                    if '魈' in tags_list or 'Xiao' in tags_list:
                        today_xiao_new.append('E:\\pixiv\\normal\\原神\\' + pic_download_url.split('/')[-1])
                    ys_num += 1
                elif '崩坏3rd' in tags_list:
                    print("崩三图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '崩三'
                    b3_num += 1
                elif '碧蓝航线' in tags_list:
                    print("碧蓝图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = '碧蓝航线'
                    blue_num += 1
                elif 'FGO' in tags_list or 'Fate/GrandOrder' in tags_list:
                    print("FGO图片一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = 'fgo'
                    fgo_num += 1
                elif '初音ミク' in tags_list or '初音未来' in tags_list or 'Miku' in tags_list:
                    print("初音一张")
                    pic_download_url = pic_info_list['body']['urls']['original']
                    category = 'miku'
                else:
                    continue
                picture_download(pic_download_url, limitation, category, artwork_page_numbers_list[pic_num], cookie)
        print("方舟{}，赛马娘{}，原神{}，崩三{}，碧蓝航线{}，fgo{}".format(ark_num, teio_num, ys_num, b3_num, blue_num, fgo_num))
    return flag


def picture_download(origin_pic_url, age_limitation, category, page_numbers, cookie):
    # 接受 pic_url = "https://i.pximg.net/c/1080x600_70_a2_u1/img-
    # master/img/2020/02/07/13/49/42/79331454_p0_master1200.jpg"
    # 目的 pic_url = "https://i.pximg.net/img-original/img/2021/04/29/12/13/59/89462959_p0.png"
    # pos1 = pic_url.find('c')
    # pos2 = pic_url.find('img-master')
    # 截去/c/1080x600_70_a2_u1/
    # pic_url_origin = pic_url[0:pos1] + pic_url[pos2:]
    # 改变后缀名
    # pic_url_origin = pic_url_origin.replace('_master1200.jpg', '.png')
    # pic_url_origin = pic_url_origin.replace('img-master', 'img-origin')
    for number in range(0, (int(page_numbers))):
        sign_part = 'p' + str(number)
        pic_url = origin_pic_url.replace('p0', sign_part)
        store_url = "E:\\pixiv\\" + age_limitation + "\\" + category + "\\" + pic_url.split('/')[-1]
        if category == '方舟':
            today_ark_new.append(store_url)
        elif category == 'fgo':
            today_fgo_new.append(store_url)
        elif category == 'miku':
            today_miku_new.append(store_url)
        elif category == '碧蓝航线':
            today_blhx_new.append(store_url)
        elif category == '赛马娘':
            today_tt_new.append(store_url)
        elif category == '原神':
            today_ys_new.append(store_url)
        else:
            pass
        path = "/img-original" + pic_url.split('img-original')[-1]
        if os.path.exists(store_url):
            print("此图已存")
            return
        else:
            pass
        header = {
            "authority": "i.pximg.net",
            "referer": "https://www.pixiv.net/",
            "path": path,
            "sec-ch-ua": "\"Not A;Brand\";v=\"99\", \"Chromium\";v=\"90\", \"Google Chrome\";v=\"90\"",
            "sec-ch-ua-mobile": "?0",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/90.0.4430.72 Safari/537.36",
            "cookie": cookie
        }
        pixiv_crawl = requests.session()
        pixiv_crawl.keep_alive = False
        sleep_time = 10
        while 1:
            try:
                response = pixiv_crawl.get(pic_url, headers=header)
                with open(store_url, "wb") as fd:
                    fd.write(response.content)
                    print(store_url + "已保存完毕")
                time.sleep(5)
                break
            except requests.exceptions.ProxyError as connect_error:
                print("请求失败,休眠{}秒".format(sleep_time), connect_error)
                time.sleep(sleep_time)
                sleep_time += 10
                continue


def crawl_pixiv():
    print('捕捉今日方舟的图片')
    pixiv_info_get()
    dest_dict = {'last_max_id': current_max_id, 'today_ark_new': today_ark_new,
                 'today_xiao_new': today_xiao_new, 'today_miku_new': today_miku_new,
                 'today_fgo_new': today_fgo_new, 'today_blhx_new': today_blhx_new,
                 'today_tt_new': today_tt_new, 'today_ys_new': today_ys_new
                 }
    with open('E:\\pixiv\\record.txt', 'w') as today_record:
        today_record.write(json.dumps(dest_dict))
