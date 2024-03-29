import requests
from lxml import html


def save_to_file(file_name, contents):
    fh = open(file_name, 'w')
    fh.write(contents)
    fh.close()


# 需要爬数据的网址
url = 'https://wallstreetcn.com/live/forex'
page = requests.Session().get(url)
tree = html.fromstring(page.text)
# 获取所有新闻条目
allDivs = tree.xpath('//div[@class="wscn-tabs__content"]/div[5]/div')
i = 0
file_content = ''
for myDiv in allDivs:
    timeList = myDiv.xpath('./div/div[@class="live-item__time"]/span[@class="live-item__time__text"]/text()')
    contentList = myDiv.xpath('./div/div[@class="live-item__main"]/div[@class="live-item__main__content"]/'
                              'div[@class="content-html"]/p/text()')
    if len(timeList and len(contentList)):
        time = timeList[0]
        content = contentList[0]
        i = i + 1
        print(i, ",", time, ",", content)
        file_content = file_content + str(i) + "," + time + "," + content + "\n"
save_to_file('D:/news.csv', file_content)
