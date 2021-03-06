import socket

#参数中要指定好类型、回复信息、账号
def send_msg(resp_dict):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ip = "127.0.0.1"
    client.connect(("127.0.0.1",5700))

    msg_type = resp_dict['msg_type']
    number = resp_dict['number']
    msg = resp_dict['msg']

    #特殊字符进行url编码
    msg = msg.replace(" ", "%20")
    msg = msg.replace("\n", "%0a")
    if msg_type == 'group':
        payload = "GET /send_group_msg?group_id=" + str(number) + \
                  "&message=" + msg + " HTTP/1.1\r\nHost:" + ip +":5700\r\nConnection: close\r\n\r\n"

    elif msg_type == 'private':
        payload = "GET /send_private_msg?user_id=" + str(number) + \
                  "&message=" + msg + " HTTP/1.1\r\nHost:" + ip + ":5700\r\nConnection: close\r\n\r\n"
    print("已发送")
    client.send(payload.encode("utf-8"))
    client.close()
    return 0
