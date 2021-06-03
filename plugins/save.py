import re
import requests


def save(message):
    text = ''
    all_category = ["方舟", "原神", "赛马娘", "崩三"]
    title = ''
    for item in all_category:
        if item in message:
            title = item
            break
    part_urls = re.findall(r'url=(.*?)term=3', message)
    part_names = re.findall(r'file=(.*?).image', message)
    total_urls = []
    total_names = []
    # 所有图片的url
    for url in part_urls:
        total_urls.append(url + 'term=3')
    # 所有图片名
    for name in part_names:
        total_names.append(name + '.jpg')
    if len(total_urls) == 0 and len(total_names) == 0 or len(title) == 0:
        return text
    print(total_urls)
    print(total_names)
    for i in range(0, len(total_urls)):
        store_url = "E:\\data\\图\\" + title + "\\" + total_names[i]
        print(store_url)
        response = requests.get(total_urls[i])
        with open(store_url, "wb") as fd:
            fd.write(response.content)
    text = "共接受到" + str(len(total_urls)) + "张" + title + "图片，感谢"
    return text
