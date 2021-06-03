import requests


def en(word):
    word = word.split(" ")[-1]
    word = word.lower()
    if word.isalpha():
        word_url = 'https://fanyi.baidu.com/sug'
        print(word_url)
        # 准备参数
        word_headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/'
                          '83.0.4103.116 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',  # 异步请求
            'content-length': str(len(word) + 3),  # 百度固定
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',  # 响应正文 格式
        }
        data = {
            'kw': word,
        }
        response = requests.post(word_url, headers=word_headers, data=data)
        result = ''
        print(response.json())
        for data in response.json()['data']:
            result += data['k'] + ' '
            result += data['v'] + '\n'
        print(result)

        mp3_url = 'https://fanyi.baidu.com/gettts?lan=uk&text=' + word + '&spd=3&source=web'
        mp3_headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; '
                                     'x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/''83.0.4103.116 Safari/537.36'}
        mp3_response = requests.get(mp3_url, headers=mp3_headers)
        print(response.status_code)
        store_url = "E:\\data\\word\\" + word + ".mp3"
        with open(store_url, "wb") as fd:
            fd.write(mp3_response.content)
        result = result.replace(';', ',')
        local_mp3_url = "[CQ:record,file=file:///" + store_url + "]"
        text1 = result

        text2 = local_mp3_url
        return text1, text2
    else:
        text1 = "非法字符"
        text2 = "爬"
        return text1, text2
