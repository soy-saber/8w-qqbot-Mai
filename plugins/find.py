import requests
from socket_operate.send import send_msg
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def find(qq_url, group_id):
    picture_url = picture_url_search(qq_url)
    print(picture_url)
    text = nao(picture_url, group_id)
    if text == "Mai没有找到合适的链接呢,去ascii2d再帮你找找":
        text = ascii2d(picture_url)
    return text


# 在nao找图
def nao(picturl_url, group_id):
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    wd = webdriver.Chrome(r'D:\selenium-driver\chromedriver.exe', options=chrome_options)
    wd.get('https://saucenao.com/')
    url_input = wd.find_element_by_id('urlInput')
    url_input.send_keys(picturl_url)
    botton = wd.find_element_by_id('searchButton')
    print("已开始搜索")
    botton.click()
    percents_list = []
    pic_intro = 'None'
    author_intro = 'None'
    pic_title = 'None'
    pic_link = 'None'
    author_link = 'None'
    i = 0
    print("查找该页面有几张图")
    similar_percents = wd.find_elements_by_class_name('resultsimilarityinfo')
    for item in similar_percents:
        percent = item.get_attribute('textContent')
        percents_list.append(percent)
    number = len(percents_list)


    for i in range(2, number):
        try:
            pic_info = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/strong[1]')
            pic_intro = pic_info.get_attribute('textContent')
        except Exception:
            print("无pixiv信息")
            pass
        try:
            author_info = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/strong[2]')
            author_intro = author_info.get_attribute('textContent')
        except Exception:
            print("无作者信息")
            pass
        if pic_intro == "Pixiv ID: " and author_intro == "Member: ":
            title_find = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[1]')
            pic_title = title_find.get_attribute('textContent')

            pic_content_find = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/a')

            pic_link = pic_content_find.get_attribute('href')

            author_content_find = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/a[2]')

            author_link = author_content_find.get_attribute('href')
            break
    text = "标题:" + pic_title + " " + "\n" + "图片: " + pic_link + "\n" + "作者: " + author_link
    print(text)
    if i == number + 1:
        text = "Mai没有找到合适的链接呢,去ascii2d再帮你找找"
        msg_dict = {
            "msg_type": "group",
            "number": group_id,
            "msg": text
        }
        send_msg(msg_dict)
    return text


def ascii2d(picture_url):
    search_url = "https://ascii2d.net/search/url/" + picture_url
    response = requests.get(search_url)
    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    try:
        picture_source_url = soup.select('body > div > div > div.col-xs-12.col-lg-8.col-xl-8 > div:nth-child(6) > div.col-xs-12.col-sm-12.col-md-8.col-xl-8.info-box > div.detail-box.gray-link > h6 > a:nth-child(2)')
        picture_author_url = soup.select('body > div > div > div.col-xs-12.col-lg-8.col-xl-8 > div:nth-child(6) > div.col-xs-12.col-sm-12.col-md-8.col-xl-8.info-box > div.detail-box.gray-link > h6 > a:nth-child(3)')
        # 原图片的urlbody > div > div > div.col-xs-12.col-lg-8.col-xl-8 > div:nth-child(6) > div.col-xs-12.col-sm-12.col-md-8.col-xl-8.info-box > div.detail-box.gray-link > h6 > a:nth-child(3)
        for item in picture_source_url:
            dest_url = item.get('href')
            print(dest_url)
        # 作者相关信息url
        for item in picture_author_url:
            author_url = item.get('href')
            author_name = item.get_text()
            print(author_url, author_name)
        text = "图片url:" + dest_url + "%0a" + "作者主页:" + author_url + "%0a" + "作者名:" + author_name
    except:
        text = "ascii2d也找不到，快爬"
    return text



    #返回找到的第一张图
    #response_dest = requests.get(dest_url)
    #html = response_dest.content.decode('utf-8')
    #dest_soup = BeautifulSoup(html, 'html.parser')
    #dest_picture = dest_soup('#root > div:nth-child(2) > div.sc-1nr368f-0.kCKAFN > div > div.sc-1nr368f-3.iHKGIi > main > section > div.sc-171jvz-0.ketmXG > div > figure > div > div.sc-1mz6e1e-1.QBVJO.gtm-medium-work-expanded-view > div.sc-1qpw8k9-0.yjBCb > a > img')
    #for item in dest_picture:
    #    raw_picture_url = item.get('src')
    #    print(raw_picture_url)


def picture_url_search(qq_url):
    start_pos = qq_url.find("url")
    end_pos = qq_url.find("]")
    pictur_url = qq_url[start_pos + 4: end_pos]
    return pictur_url