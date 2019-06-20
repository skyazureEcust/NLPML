import re

import jieba
import jieba.posseg as pseg
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import numpy as np
from util import CommonUtil

#准备1 评价对象识别 列表
def objectList_A():
    threeObject_A =[]
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

    return highObjectList, middleObjectList, lowObjectList, threeObject_A

#准备2 情感词--用于加权重
def sent_word_list():
    # 读取权重文件
    weightWord = []
    fweight = open('../dictionary/sentimentdict/sentiword_1.txt', 'r', encoding='utf-8')
    for wgt in fweight.readlines():
        weightWord.append(wgt.strip())
    # print(weightWord)
    return  weightWord

# 量化词
def  weight_B():
    threeWeight_B = []
    highWeightList = []
    with open('../dictionary/highobjectdict_B.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            highWeightList.append(each)
            threeWeight_B.append(each)

    middleWeightList = []
    with open('../dictionary/middleobjectdict_B.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            middleWeightList.append(each)
            threeWeight_B.append(each)

    lowWeightList = []
    with open('../dictionary/lowobjectdict_B.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            lowWeightList.append(each)
            threeWeight_B.append(each)

    return highWeightList, middleWeightList, lowWeightList, threeWeight_B

def degreeWord():
    degreeList = []
    with open('../dictionary/sentimentdict/degreedict.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degreeList.append(each)

    return degreeList

def jieba_pos(newsContent):
    seg_list2 = pseg.cut(newsContent)
    # 词性标注词
    words_pseg = []
    # 给词加词性标注
    words_pos = []
    for w in seg_list2:
        words_pseg.append(w.word)
        words_pos.append(w.flag)
    # print(words_pseg)
    # print(words_pos)

    return words_pseg, words_pos

#删除括号里面的内容
def del_kuohao(newsContent):
    words_pseg, words_pos = jieba_pos(newsContent)
    index1 = 0
    index2 = len(newsContent)
    # newsContent = re.sub(u"（.*?）| 【.*?】", "", newsContent)
    newsContent = re.sub(u"（.*?）|【.*?】", "", newsContent)
    # newsContent2 = ''
    # if '('  in words_pseg:
    #     index1 = words_pseg.index('(')
    #     if ')' in words_pseg:
    #         index2 = words_pseg.index(')')
    #     elif '）' in words_pseg:
    #         index2 = words_pseg.index('）')
    #     for w in words_pseg[:index1]:
    #         newsContent2 = newsContent2 + w
    #     for ww in words_pseg[index2+1:]:
    #         newsContent2 = newsContent2 + ww
    #
    # elif '（' in words_pseg:
    #     index1 = words_pseg.index('（')
    #     if ')' in words_pseg:
    #         index2 = words_pseg.index(')')
    #     elif '）' in words_pseg:
    #         index2 = words_pseg.index('）')
    #
    #     for w in words_pseg[:index1]:
    #         newsContent2 = newsContent2 + w
    #     for ww in words_pseg[index2+1:]:
    #         newsContent2 = newsContent2 + ww

    return newsContent


# 1.找出评价对象
def findIdentify(newsContent, threeObject_A, special_word):
    # print('newsContent111',newsContent)
    # print(words_pseg)
    newsContent_List = []
    newsContent_List2 = []
    objectWordList = []
    objectIndexList = []
    objectDict = {}
    number = 0
    # print(threeObject_A)
    # print(len(threeObject_A))
    for each in special_word:
        if each in newsContent:
            news = newsContent.split(each)
            each = each.replace('/', '兑')
            counter = 0
            for each2 in news:
                if counter == 0:
                    newsContent = ''
                    newsContent = newsContent + each2 + each
                    counter = counter + 1
                else:
                    newsContent = newsContent + each2
    # print('newsContent222',newsContent)

    words_pseg, words_pos = jieba_pos(newsContent)
    # print('threeObject_A',threeObject_A)
    # print('words_pseg',words_pseg)
    for each in threeObject_A:
        each = each.strip()
        if each in words_pseg:
            # if each in objectWordList:
            #     continue
            # else:
            # 找到了一个评价对象,保存到列表中
            objectWordList.append(each)
            index = words_pseg.index(each)
            objectIndexList.append(index)
            # 以字典的形式存储评价对象和对应的index
            objectDict[each] = index
            number = number + 1

    # 按values排序
    objectDict = sorted(objectDict.items(), key=lambda x: x[1])
    # print('objectDict',objectDict)

    if objectDict:
        if len(objectDict) > 1:
            each = objectDict[0]
            r = 0
            md = 0
            onumber = -1
            for nextEach in objectDict:
                onumber =  onumber + 1
                print('test',objectDict[onumber][0])
                if r == 0:
                    r = r + 1
                    continue
                # dis = nextEach[1] - each[1]
                vNumber = 0
                for k in range(each[1], nextEach[1]):
                    # print('words_pos[k]',words_pos[k])
                    if words_pos[k] == 'v':
                        vNumber = vNumber + 1
                if vNumber > 0:
                    # print('222',words_pseg)
                    # print('111',words_pseg[each[1]:nextEach[1]])
                    # print('中间段',words_pseg[each[1]:nextEach[1]])
                    newsContent_List.append(words_pseg[each[1]:nextEach[1]])
                    each = nextEach
                    if len(objectDict) - len(newsContent_List) == 1:
                        # print('finally')
                        # print('最后一段',words_pseg[each[1]:])
                        newsContent_List.append(words_pseg[each[1]:])
                else:
                    # 针对多个评价对象共用同一个谓语？？？？
                    later = []
                    try:
                        if objectDict[onumber + 1][0]:
                            vNumber2 = 0
                            for k in range(nextEach[1], objectDict[onumber + 1][1]):
                                # print('words_pos[k]',words_pos[k])
                                if words_pos[k] == 'v':
                                    vNumber2 = vNumber2 + 1
                            if vNumber2 > 0:
                                later = words_pseg[nextEach[1] + 1: objectDict[onumber + 1][1]]
                                print('first_later', later)
                            else:
                                later = words_pseg[nextEach[1] + 1:]
                                print('first_later', later)

                    except:
                        later = words_pseg[nextEach[1] + 1:]
                        print('first_later', later)
                     #存在的其他评价对象删除
                    for each3 in objectDict:
                        if each3[0] in later:
                            later.remove(each3[0])
                   #插入真正的主语
                    later.insert(0,each[0])
                    print('middle_later',later)
                    newsContent_List.append(later)
                    # # 写上最后一段
                    # each = nextEach
                    # if len(objectDict) - len(newsContent_List) == 1:
                    #     # print('finally')
                    #     print('最后一段',words_pseg[each[1]:])
                    #     newsContent_List.append(words_pseg[each[1]:])

            # 将分词的结果连成句子
            # print('newsContent_List',newsContent_List)
            if newsContent_List:
                for each in newsContent_List:
                    if each:
                        # print('each',each)
                        news = ''
                        for w in each:
                            # print('wwwww',w)
                            news = news + w
                        # print('news',news)
                        newsContent_List2.append(news)
                # print('newsContent_List2',newsContent_List2)

        elif len(objectDict) == 1:
            newsContent_List2.append(newsContent)

    print('newsContent', newsContent)
    print('objectDict', objectDict)
    print('newsContent_List2', newsContent_List2)
    return newsContent_List2, objectDict

def main(threeObject_A, fsrc, fsave, special_word):
    #读取文件
    objectNumber = 0
    for eachNews in fsrc.readlines():
        eachNews = eachNews.strip().split('\t')
        # print(each[0],each[1])
        newsTime = eachNews[0]
        newsContent = eachNews[1]

        # print('111111111111111111111Rownews',newsContent)
        #去掉括号里面的内容
        newsContent = del_kuohao(newsContent)
        # print('222222222222222news',newsContent)
        #评价对象分句
        newsContent_List2, objectDict = findIdentify(newsContent, threeObject_A, special_word)
        if len(newsContent_List2) == len(objectDict):
            objectNumber = objectNumber + len(objectDict)
            # 2.得出这条新闻的情感极性
            objectPolarity = []
            for childNews, ob in zip(newsContent_List2, objectDict):
                # if (rawObj in childNews) and  (rawObj==ob[0]):
                #     # fsave.write(str(newsTime) + '\t' + childNews + '\t' + rawObj + '\t'+ob[0]  + '\t'+ pol + '\n')
                #     fsave.write(str(newsTime) + '\t' + childNews + '\t' + rawObj + '\t'+ob[0]  +  '\n')
                # else:
                #     flab.write(str(newsTime) + '\t' + childNews + '\t' +ob[0] + '\n')

                fsave.write(str(newsTime) + '\t' + childNews + '\t' +ob[0]  +  '\n')

        else:
            pass

    print('objectNumber',objectNumber)
    fsave.close()

if __name__ == "__main__":
    #舆情A中评价对象生成列表
    highObjectList, middleObjectList, lowObjectList, threeObject_A = objectList_A()

    #自定义分词词典
    filename = '../dictionary/splitworddict.txt'
    jieba.load_userdict(filename)

    file =  '../dictionary/splitworddict_2.txt'
    f2 = open(file,'r',encoding='utf-8')
    special_word = []
    for each in f2.readlines():
        each = each.strip()
        special_word.append(each)
    # print(special_word)

    # #打开文件 my_polarity.txt
    # fname = '../eFiles/my_polarity.txt'
    # fsrc = open(fname,'r',encoding='utf-8')

    # 打开文件 my_polarity.txt
    fname = '../eFiles/aSplitRawNews_splitNewsResult.txt'
    fsrc = open(fname, 'r', encoding='utf-8')

    #保存aSplitRawNews_splitNewsResult.txt评价对象分句后的结果
    filename = '../eFiles/bObjectSplitNews_my_polarity_aSplit.txt'
    fsave = open(filename, 'w', encoding='utf-8')

    main(threeObject_A,fsrc, fsave, special_word)
