from bs4 import BeautifulSoup
import time
import pandas as pd
import requests
import datetime

headers={
    "User-Agent":"",
    "Connection": "keep-alive",
    # 这个cookie的获取方法在文档中已说明
    "Cookie":""
}
sets=124  # 最新一期的数字

dates=[]  # 日期数组，用于填充url
# 遍历日期  包括begin和end的日期  生成类似2020-05-03的格式的日期
begin = datetime.date(2020,5,3)
end = datetime.date(2020,6,9)
d = begin
delta = datetime.timedelta(days=1)
while d <= end:
    dates.append(str(d.strftime("%Y-%m-%d")))
    d += delta


Cids=[]  # Cid数组，用于填充url
with open('Urls/Cid.txt', 'r') as f:
    for line in f.readlines():
        Cids.append(line.strip())

for cid in Cids:
    # 每次都要重置这些数据
    dm_data = []  # 弹幕数据
    dm_text = []  # 弹幕本体
    # 弹幕的八个参数和弹幕本体
    DM_time = []
    DM_mode = []
    DM_font = []
    DM_color = []
    DM_realTime = []
    DM_pool = []
    DM_userID = []
    DM_id = []
    DM_text = []
    print("正在爬取第" + str(sets) + "期的《睡前消息》弹幕...")
    for date in dates:
        url="https://api.bilibili.com/x/v2/dm/history?type=1&oid="+cid+"&date="+date

        html=requests.get(url=url,headers=headers) #返回文本信息
        html.encoding='utf8'
        soup=BeautifulSoup(html.text,'lxml') #建立soup对象

        all=soup.find_all("d")
        for d in all:
            # 弹幕数据
            dm_data.append(str(d.get("p")).split(","))
            # 弹幕本体
            dm_text.append(d.get_text())

    # 分别把数据存进这几个数组
    for i in dm_data:
        DM_time.append(i[0])
        DM_mode.append(i[1])
        DM_font.append(i[2])
        DM_color.append(i[3])
        DM_realTime.append(i[4])
        DM_pool.append(i[5])
        DM_userID.append(i[6])
        DM_id.append(i[7])
    for i in dm_text:
        DM_text.append(i)

    dt={"DM_time":DM_time,"DM_mode":DM_mode,"DM_font":DM_font,"DM_color":DM_color,
        "DM_realTime":DM_realTime,"DM_pool":DM_pool,"DM_userID":DM_userID,"DM_id":DM_id,"DM_text":DM_text}

    d=pd.DataFrame(dt)

    d.to_csv('./Danmu/Danmu-'+str(sets)+'.csv',encoding='utf-8-sig') #存储弹幕信息
    print("已将弹幕放入到Danmu-"+str(sets)+".csv文件中")
    sets-=1

    # 每抓完一个网页休眠7秒
    print("缓冲中...")
    time.sleep(7)

print("已将《睡前消息》第110-124期的弹幕爬取完毕")







