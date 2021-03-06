def pa(message,id):
    if(message == 'pa'):
        text = id + "给我爬"
    else:
        left_locat = message.find("[")
        right_locat = message.find("]")
        part = message[left_locat : right_locat+1]
        text = part + id + "让你爬哦"
    return text