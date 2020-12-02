from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time

cids=[]
Urls=[]
with open('Urls/Link.txt', 'r') as f:
    for line in f.readlines():
        Urls.append(line.strip())

print("开始爬取《睡前消息》第110-124期视频的Cid")

# chrome驱动，需要放在Python安装的目录下
driver = webdriver.Chrome(r"E:\Python\chromedriver.exe")

for url in Urls:
    driver.get(url)
    data = driver.page_source
    soup = BeautifulSoup(data, 'lxml')

    all = soup.find_all('script')
    for a in all:
        if str(a).startswith("<script>window."):
           res=a

    links=re.split(r'\:',str(res))
    for url in links:
        # 这个链接前面是域名，中国的都是以cn开头
        if url.startswith("//cn"):
            link=url
            break

    cid=re.findall(".*/(.*)-1-.*", link)

    # 获取到视频的cid，存进数组然后一起存进Cid.txt文件中
    cid=cid[0]

    # 处理特殊情况下，长度不符合cid，去除尾部部分
    if len(cid)>9:
        length=len(cid)
        a=length-9
        cid=cid[:-a]

    cids.append(cid)

    # 每抓完一个网页休眠5秒
    time.sleep(5)

with open('Urls/Cid.txt', 'w') as f:
    for id in cids:
        f.write(id + '\n')

print("已将全部视频的Cid放入到Cid.txt文件中")





