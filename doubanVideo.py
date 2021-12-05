# -*- codeing = utf-8 -*-
# @Time : 2021/3/14 14:19
# @File : doubanVideo.py

from bs4 import BeautifulSoup    #网页解析
import re#正则表达式,进行文字匹配
import urllib.request,urllib.error #指定url，获取活页数据
import xlwt  #Excel
import sqlite3 #sql


#正则表达式的规则
# <span class="title">肖申克的救赎</span>
findName = re.compile(r'<span class="title">(.*?)</span>',re.S)
#<a href="https://movie.douban.com/subject/1308767/">
#re.S忽略换行符
findLink = re.compile(r'<a href="(.*?)">',re.S)
#<img src="https://img2.doubanio.com/view/photo/m/public/p480747492.webp">

def main():
    baseurl = "https://movie.douban.com/top250?start="
    # 保存位置
    savepath = "豆瓣电影.xls"
    # 1、爬取网页
    print("----开始")
    datalist = getData(baseurl)
    #保存信息
    #saveDataToExcel(datalist, savepath)

    #保存在sqltie数据库
    datapath = "video250.db"
    saveToDB(datalist,datapath)


def getData(beasurl):
    print("--调用页面信息--")
    datalist = []
    for i in range(0,10):
        url = beasurl + str(i*25)
        print(url)#查看将要发送请求
        html = askURL(url)

        print("--调取完毕--开始解析")
        # 2、逐一解析数据
        #把整个文档放在内存里，形成soup解析器
        soup = BeautifulSoup(html,"html.parser")
        for i in soup.find_all("div",class_="item"):  #查找符合要求的字符串，形成列表
            #print(i)#查看电影的所有信息
            data = []
            item = str(i)
            name = re.findall(findName,item)[0]
            data.append(name)
            link = re.findall(findLink,item)[0]
            data.append(link)
            #print("电影："+str(name)+"，视频链接："+str(link))
            datalist.append(data)

    return datalist


    # 得到指定url网页内容
def askURL(url):

    head = {
        # 模拟浏览器，像豆瓣服务发送消息
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        # 用户代理，告诉浏览器我们是什么类型的机器
    }
    req = urllib.request.Request(url=url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode("utf-8")
        #print(html)
    except Exception as e:
        print(e)

    return html
    #3、保存数据
# --------------------------------------------------------

def saveDataToExcel(datalit,savepath):
    print("开始保存信息")
    # 创建workbook对象
    Excel = xlwt.Workbook(encoding="utf-8")
    # 创建工作表
    sheet = Excel.add_sheet('豆瓣电影Top250',cell_overwrite_ok=True)
    #设定列
    col = ("电影名","电影链接")
    for i in range(0,2):
        sheet.write(0,i,col[i])
    for i in range(0,250):
        print("第%d条"%(i+1))
        data = datalit[i]
        for j in range(0,len(data)):
            sheet.write(i+1,j,data[j])
    Excel.save("豆瓣电影.xls")
    print("保存完成")

#初始化DB
def initDB():
    print("initDB")
    #打开或创建数据库文件
    conn = sqlite3.connect('video250.db')
    print("创建数据库连接")
    c = conn.cursor()
    sql = '''
        CREATE TABLE "video250" (
          "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
          "video_name" text,
          "url" text
)
    )
    '''
    c.execute(sql)
    conn.commit()
    conn.close()



def saveToDB(datalist,datapath):
    print("saveToDB")
    conn = sqlite3.connect(datapath)
    c = conn.cursor()

    for data in datalist:
        for i in range(len(data)):
            data[i] = '"'+data[i]+'"'
        print("sql要插入的数据"+str(data))
        insertSql = '''
            insert into video250 (video_name,url) values(%s)
        '''%",".join(data)
        c.execute(insertSql)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    #initDB()
    main()
    print("爬取完毕")



