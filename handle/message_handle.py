from socket_operate.send import send_msg
from handle.msg_handle import get_message_type,get_number,get_raw_message,get_nickname,get_card,get_user_id
from plugins.pa import pa
from plugins.dog import dog
from plugins.help import help
from plugins.anime import anime
from plugins.picture import picture
from plugins.rand import rand
from plugins.beauty import beauty
from plugins.trans import trans
from plugins.ban import ban
from plugins.abs import abs
from plugins.unban import unban
from plugins.hello import hello
import pymysql
from itertools import chain
import sys
sys.path.append('E:\\robot\\Mai')
import main
#私聊信息回复
def private_msg_handle(msg):
    msg_dict={
        "msg_type":"private",
        "number":get_number(msg),
        "msg":"你好，这里是梓川家"
    }
    send_msg(msg_dict)
    return

def group_msg_handle(msg):
    if(main.flag == False):
        #从数据库中提取ban_list列表
        db = pymysql.connect("", "", "", "")
        cursor = db.cursor()
        sql = '''select * from ban'''
        cursor.execute(sql)
        tuple_list = cursor.fetchall()
        global ban_list
        ban_list = list(chain.from_iterable(tuple_list))
        cursor.close()
        main.flag = True

    message = get_raw_message(msg)
    id = str(get_user_id(msg))
    id_in_group = get_card(msg)
    title = ['#ark', '#bh3', '#ghs', '#fgo']
    print(ban_list)
    if(main.status == True):
        if(id not in ban_list):
            #爬
            if('#pa' in message):
                text = pa(message,id_in_group)
                msg_dict={
                    "msg_type":"group",
                    "number":get_number(msg),
                    "msg": text
                    }
                send_msg(msg_dict)
                return

            #舔狗日记
            elif(message == '#dog'):
                text = dog()
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return


            #abs
            elif('#abs' in message):
                text = abs(message)
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #ban 管理员权限 id填qq号
            elif ('#ban' in message and id == ""):
                text = ban(message)
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #unban 同上
            elif ('#unban' in message and id == ""):
                text = unban(message)
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #菜单
            elif(message == '#help'):
                text = help()
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            elif (message == '#hello'):
                text = hello()
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #追番功能
            elif ('#anime' in message):
                text = anime(message)
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #picture
            elif(message in title):
                text = picture(message)
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #beauty
            elif (message == '#beauty'):
                text = beauty()
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            # trans
            elif ("#trans" in message):
                text = trans(message)
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #随机数
            elif('#rand' in message):
                text = rand(message,id)
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                send_msg(msg_dict)
                return

            #简单的互动功能
            elif('下班' in message and id == ""):
                text = "那我就先走啦"
                msg_dict = {
                    "msg_type": "group",
                    "number": get_number(msg),
                    "msg": text
                }
                main.status = False
                send_msg(msg_dict)
                return

            else:
                return

        else:
            return

    elif(main.status == False and id == "" and '上班' in message):
        main.status = True
        text = "嗯?这么想我吗"
        msg_dict = {
            "msg_type": "group",
            "number": get_number(msg),
            "msg": text
        }
        send_msg(msg_dict)
        return

    else:
        return


def message_handle(msg):
    if get_message_type(msg) == 'private':
        private_msg_handle(msg)
    elif get_message_type(msg) == 'group':
        group_msg_handle(msg)
    return 0