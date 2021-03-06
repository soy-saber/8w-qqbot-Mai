import pymysql
import sys
from itertools import chain
sys.path.append('')#bot所在目录
import main


def unban(message):
    left_locat = message.find("=")
    right_locat = message.find("]")
    number = message[left_locat + 1 : right_locat]

    db = pymysql.connect("","","","")#用自己的数据库信息替换
    cursor = db.cursor()
    sql = '''select * from ban'''
    cursor.execute(sql)
    tuple_list = cursor.fetchall()
    ban_list = list(chain.from_iterable(tuple_list))
    if(number in ban_list):
        try:
            cursor.execute('delete from ban where list = %s' ,[number])
            print('Successful')
            text = "这就放了他"
            db.commit()
        except:
            print('Failed')
            db.rollback()
            text = "可惜没放成"
    else:
        text = "诶，还没ban呢，这就ban~"
    cursor.close()
    main.flag = False
    return text