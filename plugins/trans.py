import requests
import hashlib
import urllib
import random
def trans(message):
    left_space = message.find(" ")
    right_space = message.rfind(" ")
    dest_lan = message[right_space + 1 : len(message)]
    qurey = message[left_space + 1 : right_space]
    basic_url = "https://fanyi-api.baidu.com/api/trans/vip/translate"
    #申请百度翻译的开发者权限
    appid = ""
    key = ""
    salt = random.randint(32768, 65536)
    string = appid + qurey + str(salt) + key
    sign = hashlib.md5(string.encode()).hexdigest()
    final_url = basic_url + "?appid=" + appid + "&q=" + urllib.parse.quote(qurey) + "&from=auto" + "&to=" + dest_lan + "&salt=" \
                + str(salt) + "&sign=" + sign
    response = requests.get(final_url)
    result = response.content.decode()
    text = json_to_result(result)
    print(text)
    return text

def json_to_result(sentense):
        last_one = sentense.rfind("}") - 1
        #寻找倒数第二个}
        end_pos = sentense.rfind("}", 0, last_one)
        start_pos = search(sentense)
        result = sentense[start_pos + 2: end_pos - 1]
        trans_result = result.encode('utf-8').decode("unicode_escape")
        return trans_result

#寻找正数第五个{
def search(sentence):
    pos=0
    for i in range(1,6):
        pos = sentence.find(":", pos + 1, len(sentence))
    return pos


