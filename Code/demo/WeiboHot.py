# -*- codeing = utf-8 -*-
# @Time :4/12/0012 21:08
# @Author: peanut
# @FIle : WeiboHot.py
# @Software : PyCharm

from bs4 import BeautifulSoup
import urllib.request,urllib.error
import re
from time import sleep

def main():
    baseurl = "https://s.weibo.com/top/summary"
    # print("1")
    hotSearch = getData(baseurl)

findHS = re.compile(r'<a href=".*>(.*?)</a>')

def getData(url):

    html = askURL(url)
    soup = BeautifulSoup(html,"html.parser")
    i = 1
    data = []

    for item in soup.find_all("td",class_="td-02"):

        item = str(item)
        HS = re.findall(findHS,item)
        if HS == []:
            continue
        data.append(HS[0])
    print("微博热搜榜")
    # print(data)
    i = 1
    for x in data:
        print(i,x)
        i += 1


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
    print("done")
    sleep(60)
