import json
from socket_operate.send import send_msg
import time


def send_picture():
    t = time.localtime()
    log_file_date = str(t.tm_year) + str(t.tm_mon) + str(t.tm_mday) + 'arknight.txt'
    with open('E:\\pixiv\\record.txt', 'r') as read_out:
        today_new_pic = json.loads(read_out.readline())
        ark_pic_url_list = today_new_pic['today_ark_new']
        fgo_pic_url_list = today_new_pic['today_fgo_new']
        blhx_pic_url_list = today_new_pic['today_blhx_new']
        tt_pic_url_list = today_new_pic['today_tt_new']
        ys_pic_url_list = today_new_pic['today_ys_new']
        xiao_pic_url_list = today_new_pic['today_xiao_new']
        miku_pic_url_list = today_new_pic['today_miku_new']

        text = '今日图片'
        msg_dict = {
            "msg_type": "group",
            "number": '',
            "msg": text
        }
        send_msg(msg_dict)
        time.sleep(3)

        if len(ark_pic_url_list) != 0:
            for pic_url in ark_pic_url_list:
                send_url = "[CQ:image,file=file:///" + pic_url + "]"

                # 开车群
                msg_dict = {
                    "msg_type": "group",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

        if len(tt_pic_url_list) != 0:
            for pic_url in tt_pic_url_list:
                send_url = "[CQ:image,file=file:///" + pic_url + "]"
                msg_dict = {
                    "msg_type": "group",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

        if len(ys_pic_url_list) != 0:
            for pic_url in ys_pic_url_list:
                send_url = "[CQ:image,file=file:///" + pic_url + "]"
                msg_dict = {
                    "msg_type": "group",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

                msg_dict = {
                    "msg_type": "private",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

        if len(fgo_pic_url_list) != 0:
            for pic_url in fgo_pic_url_list:
                send_url = "[CQ:image,file=file:///" + pic_url + "]"
                msg_dict = {
                    "msg_type": "group",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

        if len(blhx_pic_url_list) != 0:
            for pic_url in blhx_pic_url_list:
                send_url = "[CQ:image,file=file:///" + pic_url + "]"
                msg_dict = {
                    "msg_type": "group",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

        if len(xiao_pic_url_list) != 0:
            text = 'pixiv魈图'
            msg_dict = {
                "msg_type": "private",
                "number": '',
                "msg": text
            }
            send_msg(msg_dict)
            time.sleep(3)
            print("魈图")
            # 魈图发送
            for xiao_pic_url in xiao_pic_url_list:
                send_url = "[CQ:image,file=file:///" + xiao_pic_url + "]"
                msg_dict = {
                    "msg_type": "private",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

        if len(miku_pic_url_list) != 0:
            text = '江宝特供'
            msg_dict = {
                "msg_type": "group",
                "number": '',
                "msg": text
            }
            send_msg(msg_dict)
            time.sleep(3)
            # miku图发送
            for miku_pic_url in miku_pic_url_list:
                send_url = "[CQ:image,file=file:///" + miku_pic_url + "]"
                msg_dict = {
                    "msg_type": "group",
                    "number": '',
                    "msg": send_url
                }
                send_msg(msg_dict)
                time.sleep(3)

    with open('E:\\Mai\\status\\' + log_file_date, 'w') as write_in:
        write_in.write('今日图片发送完成啦')

# url = "http://api.btstu.cn/sjbz/?lx=dongman"
#     response = requests.get(url)
#     pic_url = response.url
#     filename = pic_url.split("/")[-1]
#     store_url = "E:\\data\\anime_picture\\" + filename
#     with open(store_url, "wb") as fd:
#         fd.write(response.content)
#     local_img_url = "[CQ:image,file=file:///" + store_url + "]"
#     text = local_img_url
#     return text