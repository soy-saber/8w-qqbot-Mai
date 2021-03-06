import random
def rand(message,id):
    limit = message.split(" ")[-1]
    if(limit == '冲'):
        number = random.randint(0, 1)
        if(number == 0):
            text = "冲！准了"
        elif(number == 1):
            text = "不许冲！憋回去"
    else:
        nlimit = int(limit)
        number = random.randint(0,nlimit)
        text = str(number)
        if(number <= 5 and nlimit >= 100):
            text = str(number) + "%0a只有这么小吗(笑"
    return text
