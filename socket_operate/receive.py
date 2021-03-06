import socket
import json

#定义socket
ListenSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ListenSocket.bind(('127.0.0.1', 5701))
ListenSocket.listen(100)

#定义http响应头
HttpResponseHeader = '''HTTP/1.1 200 OK
Content-Type: text/html
'''


def json_to_info(msg):
    for i in range(len(msg)):
        if(msg[i]=="{" and msg[-1]=="}"):
            return json.loads(msg[i:])
    return None

def rev_msg():
    conn,addr = ListenSocket.accept()
    data = conn.recv(2048).decode(encoding='utf-8')

    #json转dict格式
    rev_dict=json_to_info(data)
    conn.sendall((HttpResponseHeader).encode(encoding='utf-8'))
    conn.close()
    print(rev_dict)
    return rev_dict