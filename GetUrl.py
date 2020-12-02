from bs4 import BeautifulSoup
from selenium import webdriver

url = 'https://space.bilibili.com/54992199/channel/detail?cid=82529'

print("开始爬取《睡前消息》第110-124期视频地址")

# chrome驱动，需要放在Python安装的目录下
driver = webdriver.Chrome(r"E:\Python\chromedriver.exe")

driver.get(url)
data = driver.page_source
soup = BeautifulSoup(data, 'lxml')

count=1
res = []
all = soup.find_all('li', attrs={'class': 'small-item fakeDanmu-item'})
for li in all:
    if count<=15:
        a=li.find('a',attrs={'class':'cover cover-normal'})
        res.append('https:'+a.get("href"))
        count+=1
    else:
        break

with open('Urls/Link.txt', 'w') as f:
    for link in res:
        f.write(link+'\n')

print("已将全部链接放入到Link.txt文件中")

