import requests
def dog():
    url = "https://cloud.qqshabi.cn/api/tiangou/api.php"
    response = requests.get(url)
    content = response.text
    return content