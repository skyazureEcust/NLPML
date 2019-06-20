#!/usr/bin/env python
# -*- coding: utf-8 -*-
from util import CommonUtil
import ltpmanner

# 读取文件新闻数据
def  splitRawNews(fsrc, fobj):
    for eachNews in fsrc.readlines():
        eachNews = eachNews.strip().split('\t')
        newsTime = eachNews[0]
        # newsTime = CommonUtil.get_datetime_from_cell(newsTime)
        newsContent = eachNews[1]
        print(newsTime)
        print(newsContent)
        # 分句
        sentence = ltpmanner.newssplitsentence(newsContent)    #返回一条新闻内容被分割的句子列表
        for childNews in sentence:
            fobj.write(str(newsTime) + '\t' + childNews +'\n')

    #分句结束关闭原文件
    fsrc.close()
    # 分句结束保存文件
    fobj.close()

if __name__ == "__main__":
    # 读取原始新闻文件10_totalnewssplitsentence.txt
    filename = '../eFiles/10_totalNewsFile.txt'
    fsrc = open(filename,'r',encoding='utf-8')

    #保存分句后的文件
    file = '../eFiles/aSplitRawNews_splitNewsResult.txt'
    fobj = open(file, 'w', encoding='utf-8')

    #调用函数
    splitRawNews(fsrc, fobj)

    #本函数的目的：
    # 对原始新闻10_totalnewssplitsentence.txt利用ltp分句
    # 保存到文件
