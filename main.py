import requests
import json
import urllib.parse
import time

final_data_array = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
    'Referer': 'https://www.chinabond.com.cn/dfz/'
}

def get_url_data(params):
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
            'createTime': item['createTime']
            #,'uri': 'https://www.chinabond.com.cn/dfz/#/information/listDetail?title=' + item['title'] + '&id=' + item['id'] + '&time=' + item['createTime'] + '&name=' + item['title']
        })

    return final_data

def get_data(i):
    params = {
        '_tp_lgbInfo': i,
        'pageSize': 10,
        'channelPath': 'ROOT>业务操作>发行与付息兑付>债券种类>地方债信息披露>信息披露文件>发行前披露',
        'issuer': '',
        'depth': 3,
        't': int(time.time())
    }
    final_data = get_url_data(params)
    return final_data

def get_file_by_infoid(id):
    url_template = 'https://www.chinabond.com.cn/lgb/fileByInfoId?infoid={}&t={}'
    timestamp = int(time.time())
    url = url_template.format(id, timestamp)
    response = requests.get(url,  headers=headers)
    data = response.json()
    return data

def download_files(id, file_path):
    # 获取文件数组
    files = get_file_by_infoid(id)

    # 遍历文件数组
    for file in files:
        # 构造文件下载地址
        url = 'http://www.chinabond.com.cn/resource' + file['fjpath']

        # 构造 Aria2 下载命令
        params = {
            'jsonrpc': '2.0',
            'id': file['id'],
            'method': 'aria2.addUri',
            'params': [
                [url],
                {
                    'out': file['fjname'],
                    'dir': file_path
                }
            ],
            'headers': {
                "referer": 'https://www.chinabond.com.cn/dfz/',
            }
        }
        # 发送 JSON-RPC 包给 Aria2
        headers = {'Content-Type': 'application/json'}
        response = requests.post('http://localhost:6800/jsonrpc', data=json.dumps(params), headers=headers)
        print(response.json())

def main():
    final_data_array = []
    i = 1
    while True:
        final_data = get_data(i)
        if not final_data:
            break
        for record in final_data:
            final_data_array.append(record)
        i += 1

    with open('final_data_array.json', 'w') as f:
        json.dump(final_data_array, f)

    for record in final_data_array:
        file_path = f"G:\\{record['property3']}\\{record['property0']}\\{record['createTime']}"
        download_files(record['id'], file_path)

main()