# Author: Peanut
# -*- codeing = utf-8 -*-
# @Time :4/2/0002 10:33
# @Author: peanut
# @FIle : spider.py
# @Software : PyCharm

from bs4 import BeautifulSoup  # 网页解析，获取数据
import re
import urllib.request, urllib.error  # 制定url，获取网页数据
import xlwt
import sqlite3


def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 1.爬取网页
    datalist = getData(baseurl)

    # savepath = ".\\豆瓣电影top250.xls"
    dbpath = "movie.db"
    # 3.保存数据
    # saveData(savepath,datalist)
    saveData2DB(datalist, dbpath)


# 影片详情链接的规则
findLink = re.compile(r'<a href="(.*?)">')  # 创建正则表达式对象，表示规则（字符串模式）
# 影片图片规则
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)  # re.S 忽略换行符
# 影片片名
findTitle = re.compile(r'<span class="title">(.*)</span>')
# 影片评分
findScore = re.compile(r'<span class="rating_num" property="v:average">(.*)</span>')
# 评价人数
findJudge = re.compile(r'<span>(\d*)人评价</span>')
# 找到概况
findInfo = re.compile(r'<span class="inq">(.*)</span>')
# 找到影片相关内容
findBd = re.compile(r'<p class="">(.*?)</p>', re.S)


# 爬取网页
def getData(baseurl):
    datalist = []
    for i in range(0, 10):
        url = baseurl + str(i * 25)
        html = askURL(url)

        # 2.逐一解析数据
        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all("div", class_='item'):  # 查找符合要求的字符串，形成列表

            data = []  # 保存一部电影的全部信息
            item = str(item)

            # 影片详情链接
            link = re.findall(findLink, item)[0]  # re库用通过正则表达式查找指定的字符串
            data.append(link)
            img = re.findall(findImgSrc, item)[0]  # 图片
            data.append(img)
            title = re.findall(findTitle, item)  # 电影名
            if (len(title) == 2):
                ctitle = title[0]
                data.append(ctitle)  # 添加中文名
                otitle = title[1].replace("/", "")
                data.append(otitle)  # 添加外国名
            else:
                data.append(title[0])
                data.append(' ')  # 留空
            score = re.findall(findScore, item)[0]  # 评分
            data.append(score)
            judge = re.findall(findJudge, item)[0]  # 评价人数
            data.append(judge)

            info = re.findall(findInfo, item)  # 概况

            if len(info) != 0:
                info = info[0].replace("。", "")  # 去掉句号
                data.append(info)
            else:
                data.append("")

            bd = re.findall(findBd, item)[0]  # 相关内容
            bd = re.sub('<br(\s+)?/>(\s+)?', " ", bd)  # 去掉br
            bd = re.sub('/', " ", bd)  # 替换/
            data.append(bd.strip())  # 去掉前后空格

            datalist.append(data)

    # print(datalist)
    return datalist


# 得到指定url网页内容
def askURL(url):
    head = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }
    request = urllib.request.Request(url=url, headers=head)
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
    finally:
        pass

    return html


# 3.保存数据
def saveData(savepath, datalist):
    workbook = xlwt.Workbook(encoding='utf-8', style_compression=0)
    worksheet = workbook.add_sheet('豆瓣电影top259', cell_overwrite_ok=True)
    col = ('电影详情链接', '图片链接', '影片中文名', '影片外国名', '评分', '评分人数', '概况', '相关信息')
    for i in range(0, 8):
        worksheet.write(0, i, col[i])

    i = 1
    for x in datalist:
        j = 0
        for y in x:
            worksheet.write(i, j, y)
            j += 1
        i += 1
    workbook.save(savepath)


def saveData2DB(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()

    for data in datalist:
        for index in range(len(data)):
            if index == 4 or index == 5:
                continue
            data[index] = '"' + data[index] + '"'
        sql = '''
                insert into movie(
                    info_link,pic_link,cname,ename,score,rated,introduction,info)
                    values (%s)''' % ",".join(data)
        # print(sql)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()



def init_db(dbpath):  # 创建数据库
    sql = '''
        create table movie(
            id integer primary key autoincrement ,
            info_link text ,
            pic_link text ,
            cname varchar ,
            ename varchar ,
            score numeric ,
            rated numeric ,
            introduction text ,
            info text);
    
    '''
    conn = sqlite3.connect(dbpath)
    cursor = conn.cursor()
    cursor.execute(sql)  # 执行
    conn.commit()  # 提交
    conn.close()  # 关闭


if __name__ == "__main__":
    main()
    print("done")
