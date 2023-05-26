import requests
import json
import urllib.parse
import time

final_data_array = []

def get_url_data(params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'Referer': 'https://www.chinabond.com.cn/dfz/'
    }

    url = "https://www.chinabond.com.cn/lgb/infoListByPath?" + urllib.parse.urlencode(params)

    response = requests.post(url, headers=headers)
    data = response.json()
    lgbInfoList = data['lgbInfoList']

    final_data = []

    for item in lgbInfoList:
        if item['property3'] == '2021':
            break
        final_data.append({
            'property3': item['property3'],
            'property0': item['property0'],
            'id': item['id'],
            'title': item['title'],
            'createTime': item['createTime'],
            'uri': 'https://www.chinabond.com.cn/dfz/#/information/listDetail?title=' + item['title'] + '&id=' + item['id'] + '&time=' + item['createTime'] + '&name=' + item['title']
        })

    return final_data

i = 1

while True:
    params = {
        '_tp_lgbInfo': i,
        'pageSize': 10,
        'channelPath': 'ROOT>业务操作>发行与付息兑付>债券种类>地方债信息披露>信息披露文件>发行前披露',
        'issuer': '',
        'depth': 3,
        't': int(time.time())
    }

    final_data = get_url_data(params)
    if not final_data:
        break
    for record in final_data:
        final_data_array.append(record)
        print(record['uri'])

    i += 1

with open('final_data_array.json', 'w') as f:
    json.dump(final_data_array, f)