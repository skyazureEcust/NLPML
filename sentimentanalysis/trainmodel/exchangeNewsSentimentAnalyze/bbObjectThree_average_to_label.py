#!/usr/bin/Python
# -*- coding: utf-8 -*-
import xlrd
from util import CommonUtil

# 准备1 评价对象识别 列表
def objectList_A():
    threeObject_A = []
    highObjectList = []
    with open('../dictionary/highobjectdict_A.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            highObjectList.append(each)
            threeObject_A.append(each)

    middleObjectList = []
    with open('../dictionary/middleobjectdict_A.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            middleObjectList.append(each)
            threeObject_A.append(each)

    lowObjectList = []
    with open('../dictionary/lowobjectdict_A.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            lowObjectList.append(each)
            threeObject_A.append(each)

    # print(highobjectList)
    # print(middleobjectList)
    # print(lowobjectList)
    return highObjectList, middleObjectList, lowObjectList, threeObject_A

def differentobjectidentify(filename,objectList,numberDict,fileNews):
    global num
    # 打开txt用于存储
    filetxt = open(filename, 'w', encoding='utf-8')

    # 打开新闻内容文件
    fileNewsContent = open(fileNews,'r',encoding='utf-8')

    #循环评价对象列表
    for eachobject in objectList:
        objectNumber = 0
        #将文件指针移到开头
        fileNewsContent.seek(0)
        #读取新闻内容
        for every in fileNewsContent.readlines():
            if objectNumber >= num:
                break
            every = every.strip()
            every = every.split('\t')
            # news_time = every[0]
            # newsTime = CommonUtil.get_datetime_from_cell(news_time)
            newsTime = every[0].strip()
            newsContent = every[1].strip()
            # print(newsContent)
            if eachobject in newsContent:
                filetxt.write(str(newsTime) + '\t' + newsContent + '\t' + eachobject + '\n')
                objectNumber = objectNumber + 1
        numberDict[eachobject] = [objectNumber]
    filetxt.close()
    fileNewsContent.close()
    return numberDict

if __name__ == "__main__":
    # 舆情A----- 评价对象
    highObjectList, middleObjectList, lowObjectList, threeObject_A = objectList_A()

    highDict = {}
    middleDict = {}
    lowDict = {}

    num = 100
    #读取原文件
    fileNews = '../eFiles/bObjectSplitNews_my_polarity_aSplit.txt'

    # 重新生成的评价对象----保存文件
    file = '../eFiles/bbObjectThree_average_to_label_file.txt'

    numberDict = differentobjectidentify(file,threeObject_A,highDict,fileNews)
    print(numberDict)
    # print('高影响评价对象搜索%d条新闻内容结束'%num,highDict)
    # middleDict = differentobjectidentify(file,middleObjectList,middleDict,fileNews)
    # print('中影响评价对象搜索%d条新闻内容结束'%num,middleDict)
    # lowDict = differentobjectidentify(file,lowObjectList,lowDict,fileNews)
    # print('低影响评价对象搜索%d条新闻内容结束'%num, lowDict)


