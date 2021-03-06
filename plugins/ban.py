import pymysql
import sys
sys.path.append('E:\\robot\\Mai')
import main
def ban(message):
    left_locat = message.find("=")
    right_locat = message.find("]")
    number = message[left_locat + 1 : right_locat]
    #用自己的数据库信息替换
    db = pymysql.connect("","","","")
    cursor = db.cursor()
    sql = '''insert into ban values(%s)'''
    try:
        cursor.execute(sql, [number])
        print('Successful')
        text = "这就ban了他"
        db.commit()
    except:
        print('Failed')
        db.rollback()
        text = "可惜没ban成"
    cursor.close()
    main.flag = False
    return text