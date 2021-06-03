from socket_operate.send import send_msg
import json
import requests


def remind(title):
    url = "http://open.iciba.com/dsapi/"
    response = requests.get(url)
    trans_response = response.content.decode('UTF-8')
    ciba = json.loads(trans_response)
    en = ciba['content'].split(".")[0] + "."
    # en = "".join(ciba['content'].split())
    zh = ciba['note']
    text = "打卡小助手提醒您，卡和您总有一个要挨打(狗头"
    msg_dict = {
        "msg_type": "private",
        "number": "",
        "msg": text
    }
    send_msg(msg_dict)
    text = "每日一句%0a" + en + "%0a" + zh
    msg_dict = {
        "msg_type": "group",
        "number": "",
        "msg": text
    }
    send_msg(msg_dict)
    with open(title, "w") as fd:
        fd.write(text)
    return
