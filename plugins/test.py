from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def nao(picturl_url):
    chrome_options = Options()
    #chrome_options.add_argument('--headless')
    wd = webdriver.Chrome(r'D:\selenium-driver\chromedriver.exe', options=chrome_options)
    wd.get('https://saucenao.com/')
    url_input = wd.find_element_by_id('urlInput')
    url_input.send_keys(picturl_url)
    botton = wd.find_element_by_id('searchButton')
    botton.click()
    percents_list = []
    pic_intro = 'None'
    author_intro = 'None'
    pic_title = 'None'
    pic_id = 'None'
    author_id = 'None'
    pic_link = 'None'
    author_link = 'None'
    # 定位相似度最高的图

    print("正在定位相似度最高的图")
    similar_percents = wd.find_elements_by_class_name('resultsimilarityinfo')
    for item in similar_percents:
        percent = item.get_attribute('textContent')
        percents_list.append(percent)
    number = len(percents_list)

    for i in range(2,number):
        try:
            pic_info = wd.find_element_by_xpath('//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/strong[1]')
            pic_intro = pic_info.get_attribute('textContent')
        except:
            print("无pixiv信息")
            pass
        try:
            author_info = wd.find_element_by_xpath('//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/strong[2]')
            author_intro = author_info.get_attribute('textContent')
        except:
            print("无作者信息")
            pass
        if(pic_intro == "Pixiv ID: " and author_intro == "Member: "):

            title_find = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[1]')
            pic_title = title_find.get_attribute('textContent')

            pic_content_find = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/a')

            pic_id = pic_content_find.get_attribute('textContent')
            pic_link = pic_content_find.get_attribute('href')

            author_content_find = wd.find_element_by_xpath(
                '//*[@id="middle"]/div[' + str(i) + ']/table/tbody/tr/td[2]/div[2]/div[2]/a[2]')

            author_id = author_content_find.get_attribute('textContent')
            author_link = author_content_find.get_attribute('href')
            break
    text = "图片:" + pic_title + " " + "\n" + pic_intro + pic_id + pic_link +\
           " " + " \n" + author_intro + author_id + author_link
    if (i == 7):
        text = "Mai没有找到合适的链接呢"
    return text
