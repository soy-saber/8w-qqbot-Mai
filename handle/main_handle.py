import handle.msg_handle
import handle.message_handle
import handle.notice_handle
import handle.request_handle
# 将不同的事件分发给不同的情况
def main_handle(msg):
    post_type = handle.msg_handle.get_post_type(msg)  # 获取上报类型
    if post_type == 'message':  # 消息事件
        handle.message_handle.message_handle(msg)
    elif post_type == 'notice':  # 通知事件
        handle.notice_handle.notice_handle(msg)
    elif post_type == 'request':  # 请求事件
        handle.request_handle.request_handle(msg)
    else:
        return 0
    return 0