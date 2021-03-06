#获取上报消息信息
def get_post_type(msg):
    return msg['post_type']

#获取信息类型
def get_message_type(msg):
    return msg['message_type']

def get_number(msg):
    if get_message_type(msg) == 'group':
        return msg['group_id']
    elif get_message_type(msg) == 'private':
        return msg['user_id']
    else:
        print('未找到QQ号或群号')
        exit()

def get_user_id(msg):
    return msg['user_id']

def get_raw_message(msg):
    return msg['raw_message']

#多级字典
def get_nickname(msg):
    return msg['sender']['nickname']

def get_card(msg):
    return msg['sender']['card']

def get_message_id(msg):
    return msg['message_id']
