# -*- coding = utf-8 -*-
# @Time :4/21/0021 19:43
# @Author: peanut
# @FIle : WeatherGuangan.py
# @Software : PyCharm


from bs4 import BeautifulSoup
import urllib.request, urllib.error
import re
from time import sleep


def main():
    baseUrl = "http://www.weather.com.cn/weather/101270107.shtml"
    weather = getData(baseUrl)


findHighTemper = re.compile(r'<span>(.*?)</span>')
findLowTemper = re.compile(r'<i>(\d.*?)</i>')
findData = re.compile(r'<h1>(.*?)</h1>')
findRays = re.compile(r'<p>(.*?)</p>')
findWear = re.compile(r'<p>(.*?)</p>')


def getData(url):
    html = askURL(url)
    soup = BeautifulSoup(html, "html.parser")
    datas = []
    i = 0
    for item, item2 in zip(soup.find_all("li", class_="sky skyid lv3"), soup.find_all("div", class_='hide show')):
        item = str(item)
        item2 = str(item2)

        data = re.findall(findData, item)[0]
        print("数据"+data)
        datas.append(data)
        highTemp = re.findall(findHighTemper, item)[0]
        datas.append("最高温度:")
        datas.append(highTemp)
        lowTemp = re.findall(findLowTemper, item)[0]
        datas.append("最低温度:")
        datas.append(lowTemp)
    print(datas)


def askURL(url):
    heads = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

    request = urllib.request.Request(url=url, headers=heads)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except Exception as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
        print("错误")
    return html


if __name__ == '__main__':
    main()
    sleep(60)
