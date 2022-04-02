# -*- coding = utf-8 -*-
# @Time :4/21/0021 19:43
# @Author: peanut
# @FIle : tomorrowWithIFTTT.py
# @Software : PyCharm


from bs4 import BeautifulSoup
import urllib.request,urllib.error
import re
import requests
from time import sleep

def main():
    baseurl = "http://i.tianqi.com/index.php?c=code&id=34&icon=1&py=guangan&id=8"
    # weather = getData(baseurl)
    text = getData(baseurl)
    send_notice('notice_phone', 'dorPo2O1rB7WFZkmzdK7bv', text[1])
    sleep(1)
    send_notice('notice_phone', 'dorPo2O1rB7WFZkmzdK7bv', text[2])

findInfo = re.compile(r'<div class="wtline" .*?">(.*?)</div>')


def send_notice(event_name, key, text):
    url = "https://maker.ifttt.com/trigger/" + event_name + "/with/key/" + key + ""
    payload = "{\n    \"value1\": \"" + text + "\"\n}"
    headers = {
        'Content-Type': "application/json",
        'User-Agent': "PostmanRuntime/7.15.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "a9477d0f-08ee-4960-b6f8-9fd85dc0d5cc,d376ec80-54e1-450a-8215-952ea91b01dd",
        'Host': "maker.ifttt.com",
        'accept-encoding': "gzip, deflate",
        'content-length': "63",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
    }

    response = requests.request("POST", url, data=payload.encode('utf-8'), headers=headers)

    print(response.text)


# text = "天气预报:"
# send_notice('notice_phone', 'dorPo2O1rB7WFZkmzdK7bv', text)


def getData(url):

    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    data = []
    for item in soup.find_all("div",class_="wtline"):
        item = str(item)
        Info = re.findall(findInfo,item)[0]
        data.append(Info)
    return data


def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

    request = urllib.request.Request(url=url,headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except Exception as e:
        if hasattr(e,"code"):
            print(e.code)
        if hasattr(e,"reason"):
            print(e.reason)
        print("错误")
    return html


if __name__ == '__main__':
    main()
    # sleep(60)