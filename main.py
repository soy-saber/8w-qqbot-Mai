import socket_operate.receive
import handle.main_handle
import pymysql

status = True
flag = False

def main():
    while 1:
        all_message = socket_operate.receive.rev_msg()
        try:
            handle.main_handle.main_handle(all_message)
        except:
            continue

if(__name__ == "__main__"):
    main()
