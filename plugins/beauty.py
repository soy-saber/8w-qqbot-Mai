import requests
def beauty():
    url = "http://api.btstu.cn/sjbz/?lx=dongman"
    response = requests.get(url)
    pic_url = response.url
    filename = pic_url.split("/")[-1]
    store_url = "E:\data\\anime_picture\\" + filename
    with open(store_url,"wb") as fd:
        fd.write(response.content)
    local_img_url = "[CQ:image,file=file:///" + store_url + "]"
    text = local_img_url
    return text