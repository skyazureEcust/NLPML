import math
from sklearn.externals import joblib
import re
import jieba
import jieba.posseg as pseg
from sklearn.externals import joblib
import warnings

warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import numpy as np
from util import CommonUtil


def weightWordRead():
    # 读取情感词（正负情感词）
    sentiWord = []
    with open('../dictionary/eDictionary/sentimentWordZF.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            sentiWord.append(each.strip())

    # 读取高程度的程度词
    degWordH = []
    with open('../dictionary/eDictionary/degreeWordH.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degWordH.append(each.strip())

    # 读取低程度的程度词
    degWordL = []
    with open('../dictionary/eDictionary/degreeWordL.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degWordL.append(each.strip())

    return sentiWord, degWordH, degWordL

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

#准备2 属性列表
def readAttr():
    attrList = []
    with open('../dictionary/attributedict.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            attrList.append(each)
    return attrList

# 准备3 情感词--用于加权重
def sent_word_list():
    # 读取权重文件
    weightWord = []
    fweight = open('../dictionary/sentimentdict/sentiword_1.txt', 'r', encoding='utf-8')
    for wgt in fweight.readlines():
        weightWord.append(wgt.strip())
    # print(weightWord)
    return weightWord


# 量化词
def weight_B():
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
    deg1 = []
    with open('../dictionary/eDictionary/HD.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            deg1.append(each)

    deg2 = []
    with open('../dictionary/eDictionary/MD.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            deg2.append(each)

    deg3 = []
    with open('../dictionary/eDictionary/LD.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            deg3.append(each)

    return deg1, deg2, deg3

def load_model():
    # 词向量模型
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    # SVM_W_model    分类模型
    clf = joblib.load('../sentimentmodel/SVM_W_model.m')
    return word_vec, clf


def jieba_pos(newsContent):
    seg_list2 = pseg.cut(newsContent)
    # 词性标注词
    words_pseg = []
    # 给词加词性标注
    words_pos = []
    for w in seg_list2:
        words_pseg.append(w.word)
        words_pos.append(w.flag)
    # print(newsContent)
    # print(words_pseg)
    # print(words_pos)
    return words_pseg, words_pos

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
            if each in objectWordList:
                continue
            else:
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
            for nextEach in objectDict:
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
                    later = words_pseg[nextEach[1]+1:]
                    # print('first_later',later)
                    for each3 in objectDict:
                        if each3[0] in later:
                            later.remove(each3[0])

                    later.insert(0,each[0])
                    # print('middle_later',later)
                    newsContent_List.append(later)
                    # 写上最后一段
                    each = nextEach
                    if len(objectDict) - len(newsContent_List) == 1:
                        # print('finally')
                        # print('最后一段',words_pseg[each[1]:])
                        newsContent_List.append(words_pseg[each[1]:])

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

    # print('newsContent', newsContent)
    # print('objectDict', objectDict)
    # print('newsContent_List2', newsContent_List2)

    return newsContent_List2, objectDict

#识别属性
def findAttr(news, attrList):
    attr = ''
    for attribute in attrList:
        if attribute in news:
            attr = attribute
            break
    if attr == '':
        attr = '价格'  #默认属性为价格

    return attr

def stopwords(words):
    #读取停用词
    stopWord = []
    for word in open('../dictionary/stopwords.txt', 'r', encoding='utf-8').readlines():
        stopWord.append(word)
    # seg_list = "/".join(seg_gen).split('/')
    #去停用词，生成去停用词之后的分词结果
    new_seg_list = []
    for w in words:
        if w in stopWord:
            continue
        else:
            new_seg_list.append(w)
    # print(new_seg_list)
    return new_seg_list

def panduan(newsContent, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3):
    flag = 0
    for h in highWeightList:
        if h in newsContent:
            flag = 1
    if flag == 0:
        for h in middleWeightList:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in lowWeightList:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in deg1:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in deg2:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in deg3:
            if h in newsContent:
                flag = 1
    return flag

def findAttr(news, attrList):
    attr = ''
    for attribute in attrList:
        if attribute in news:
            attr = attribute
            break
    if attr == '':
        attr = '价格'  #默认属性为价格

    return attr

def word2vec_W(word_vec, words, sentiWord):
    global  sentiWeight
    # 去停用词
    new_wordsList = stopwords(words)
    vec_array = np.zeros(64, dtype=float)  # 一条新闻初始化词向量，为0
    # 循环对词进行向量化
    length = len(words)
    for each in new_wordsList:
        try:
            if each in sentiWord:
                value = word_vec[each] * sentiWeight / length
                vec_array += value
            else:
                value = word_vec[each] / length
                vec_array += value
        except Exception as e:
            pass
            # print("error:", e)

    # 转成list
    vec_array = vec_array.tolist()
    return [vec_array]

def percentageValue(newsContent):
    # 百分数形式，基点形式
    way1 = re.compile('[^\x00-\xff](\d+\.\d+)%')
    way2 = re.compile('[^\x00-\xff](\d+)%')
    way3 = re.compile('[^\x00-\xff](\d+)点')
    way4 = re.compile('[^\x00-\xff](\d+)基点')
    way5 = re.compile('[^\x00-\xff](\d+)个点')
    way6 = re.compile('[^\x00-\xff](\d+)个基点')
    way7 = re.compile('[^\x00-\xff](\d+\.\d+)点')
    way8 = re.compile('[^\x00-\xff](\d+\.\d+)基点')
    way9 = re.compile('[^\x00-\xff](\d+\.\d+)个点')
    way10 = re.compile('[^\x00-\xff](\d+\.\d+)个基点')

    res1 = way1.findall(newsContent)
    res2 = way2.findall(newsContent)
    res3 = way3.findall(newsContent)
    res4 = way4.findall(newsContent)
    res5 = way5.findall(newsContent)
    res6 = way6.findall(newsContent)
    res7 = way7.findall(newsContent)
    res8 = way8.findall(newsContent)
    res9 = way9.findall(newsContent)
    res10 = way10.findall(newsContent)

    data = 0
    if res1:
        # print('newsContent',newsContent)
        for start in res1:
            if '-' in start:
                start = str(start[0]).split('-')[0]
            # print('newsContent', newsContent)
            data = float(start) / 100
            break
    elif res2:
        # print('res2', res2)
        # quantifyValue = quantifyValue + '+' + res2[0] + '%'  #与上面同理
        for start in res2:
            data = float(start) / 100
            break
    elif res3:
        data = float(res3[0]) / 10000

    elif res4:
        data = float(res4[0]) / 10000
    elif res5:
        data = float(res5[0]) / 10000
    elif res6:
        data = float(res6[0]) / 10000
    elif res7:
        data = float(res7[0]) / 10000
    elif res8:
        data = float(res8[0]) / 10000
    elif res9:
        data = float(res9[0]) / 10000
    elif res10:
        data = float(res10[0]) / 10000

    return data

def getSentimentIntensity(data,pol):
    global  value_0, value_1,value_2,value_3,value_4
    global  w1,w2,w3,w4,w5
    # 计算各范围的值
    number_v1 = 0
    number_v2 = 0
    number_v3 = 0
    number_v4 = 0
    number_v5 = 0

    val = 0
    if data == 0:
        value_0 = value_0 + 1
        if pol == 0:
            val = str(w1 * int(pol))
        else:
            val = str(w1 * int(pol))

    elif data <= value_1:
        # print(data)
        number_v1 = number_v1 + 1
        # print(newsContent)
        val = str(w1 * int(pol))
    elif data <= value_2:
        number_v2 = number_v2 + 1
        # print(newsContent)
        val = str(w2 * int(pol))
    elif data <= value_3:
        number_v3 = number_v3 + 1
        # print(newsContent)
        val = str(w3 * int(pol))
    elif data <= value_4:
        number_v4 = number_v4 + 1
        # print(newsContent)
        val = str(w4 * int(pol))
    elif data > value_4:
        number_v5 = number_v5 + 1
        # print(newsContent)
        val = str(w5 * int(pol))

    return val

def sentimentIntensity_degree(Per, newsContent, deg1,deg2, deg3, HD, MD, LD):
    global baseValue
    # 程度副词
    flag = 0
    degData = baseValue
    for each in deg1:
        if each in newsContent:
            degData = HD
            flag = 1
            break
    if flag == 0:
        for each in deg2:
            if each in newsContent:
                degData = MD
                flag = 1
                break
    if flag == 0:
        for each in deg3:
            if each in newsContent:
                degData = LD
                flag = 1
                break
    data = Per * degData
    return data

def sentimentIntensity_institutions(Per, newsContent, highWeightList, middleWeightList, lowWeightList, HEW,MEW,LEW):
    global baseValue
    flag2 = 0
    # 权威机构等
    suData = baseValue
    # 高影响
    for each in highWeightList:
        if each in newsContent:
            suData = HEW
            flag2 = 1
            break
    # 中影响
    if flag2 == 0:
        for each in middleWeightList:
            if each in newsContent:
                suData = MEW
                flag2 = 1
                break
    # 低影响
    if flag2 == 0:
        for each in lowWeightList:
            if each in newsContent:
                suData = LEW
                flag2 = 1
                break
    data = Per * suData
    return data

def sentimentIntensity_degree_institutions(Per,newsContent, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3,HEW,MEW,LEW,HD,MD,LD):
    global baseValue
    # 程度副词
    flag = 0
    degData = baseValue
    for each in deg1:
        if each in newsContent:
            degData = HD
            flag = 1
            break
    if flag == 0:
        for each in deg2:
            if each in newsContent:
                degData = MD
                flag = 1
                break
    if flag == 0:
        for each in deg3:
            if each in newsContent:
                degData = LD
                flag = 1
                break

    flag2 = 0
    # 权威机构等
    suData = baseValue
    # 高影响
    for each in highWeightList:
        if each in newsContent:
            suData = HEW
            flag2 = 1
            break
    # 中影响
    if flag2 == 0:
        for each in middleWeightList:
            if each in newsContent:
                suData = MEW
                flag2 = 1
                break
    # 低影响
    if flag2 == 0:
        for each in lowWeightList:
            if each in newsContent:
                suData = LEW
                flag2 = 1
                break
    data = Per * degData * suData
    return data

def func_base(fsrc,fsave,sentiWord,clf,word_vec):
    global baseValue
    row = 0
    std1 = 0
    for each in fsrc.readlines():
        each = each.strip().split('\t')
        newsTime = each[0]
        newsContent = each[1]
        flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3)
        if flag == 1:
            obj = each[2]
            pol = each[3]
            quaRaw = each[4]
            #新闻分词
            seg_list = jieba.cut(newsContent)
            words = []
            for each2 in seg_list:
                words.append(each2)
            # print('jieba:',words)
            vec_array = word2vec_W(word_vec, words, sentiWord)
            probaValue = clf.predict_proba(vec_array)
            # 第一种量化值
            MP = 0      #存储概率值 MP
            for k in probaValue[0]:
                if k > MP:
                    MP = k
            Per = percentageValue(newsContent) #新闻中的百分数、基点值
            if Per == 0:
                continue
            row = row + 1
            middleValue = MP * Per * baseValue * 2
            # print(Per)
            data1 = getSentimentIntensity(middleValue,pol)
            std1 = std1 + abs((int(quaRaw)) - (int(data1)))
            fsave.write(str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + '\t' + pol + '\t' + quaRaw + '\t' + str(data1) + '\n')
    k1 = std1 / row
    print('row=',row)
    print('实验1（只考虑百分数）的V值：',k1)
    fsave.close()

def func_degree(fsrc,fsave_degree, sentiWord,deg1, deg2, deg3,clf, word_vec):
    global scope,baseValue
    HD_max = 0
    MD_max = 0
    LD_max = 0
    HD_min = 0
    MD_min = 0
    LD_min = 0
    max = 0
    min = 65535
    for i in range(1,scope):
        for j in range(1,scope):
            for k in range(1,scope):
                sum = i + j + k
                if sum == scope:
                    HD = float(i)/scope
                    MD = float(j)/scope
                    LD = float(float(k))/scope
                    print('HD_MD_LD的值', HD, MD, LD)
                    row = 0
                    std2 = 0
                    fsrc.seek(0)
                    for each in fsrc.readlines():
                        each = each.strip().split('\t')
                        newsTime = each[0]
                        newsContent = each[1]
                        flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3)
                        if flag == 1:
                            obj = each[2]
                            pol = each[3]
                            quaRaw = each[4]
                            # 新闻分词
                            seg_list = jieba.cut(newsContent)
                            words = []
                            for each2 in seg_list:
                                words.append(each2)
                            # print('jieba:',words)
                            vec_array = word2vec_W(word_vec, words, sentiWord)
                            probaValue = clf.predict_proba(vec_array)
                            # print('probaValue', probaValue)
                            normalList = []
                            # 第一种量化值
                            MP = 0  # 存储概率值 MP
                            for k in probaValue[0]:
                                if k > MP:
                                    MP = k
                            Per = percentageValue(newsContent)  # 新闻中的百分数、基点值
                            if Per == 0:
                                continue
                            row = row + 1
                            v2 = sentimentIntensity_degree(Per, newsContent, deg1,deg2, deg3, HD, MD, LD)
                            middleValue = MP * v2
                            data2 = getSentimentIntensity(middleValue, pol)
                            std2 = std2 + abs((int(quaRaw)) - (int(data2)))
                            # fsave.write(
                            #     str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + '\t' + pol + '\t' + quaRaw + '\t' + str(
                            #         data2) + '\n')
                    k2 = std2 / row
                    print('实验2权值设置HD=%f,MD=%f,LD=%f的V值=%f：'%(HD,MD,LD,k2))
                    if k2 > max:
                        max = k2
                        HD_max = HD
                        MD_max = MD
                        LD_max = LD
                    if k2 < min:
                        min = k2
                        HD_min = HD
                        MD_min = MD
                        LD_min = LD
    print('总结-----实验2权重设置最大V=%f,权值为HD=%f,MD=%f,LD=%f'%(max,HD_max,MD_max,LD_max))
    print('总结-----实验2权重设置最小V=%f,权值为HD=%f,MD=%f,LD=%f'%(min,HD_min,MD_min,LD_min))


def func_institutions(fsrc,fsave_institutions, sentiWord,highWeightList, middleWeightList, lowWeightList,clf, word_vec):
    global scope,baseValue
    HEW_max = 0
    MEW_max = 0
    LEW_max = 0
    HEW_min = 0
    MEW_min = 0
    LEW_min = 0
    max = 0
    min = 65535
    for i in range(1, scope):
        for j in range(1, scope):
            for k in range(1, scope):
                sum = i + j + k
                if sum == scope:
                    HEW = float(i)/scope
                    MEW = float(j)/scope
                    LEW = float(k)/scope
                    row = 0
                    std3 = 0
                    fsrc.seek(0)
                    for each in fsrc.readlines():
                        each = each.strip().split('\t')
                        newsTime = each[0]
                        newsContent = each[1]
                        flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3)
                        if flag == 1:
                            obj = each[2]
                            pol = each[3]
                            quaRaw = each[4]
                            # 新闻分词
                            seg_list = jieba.cut(newsContent)
                            words = []
                            for each2 in seg_list:
                                words.append(each2)
                            # print('jieba:',words)
                            vec_array = word2vec_W(word_vec, words, sentiWord)
                            probaValue = clf.predict_proba(vec_array)
                            # print('probaValue', probaValue)
                            normalList = []
                            # 第一种量化值
                            MP = 0  # 存储概率值 MP
                            for k in probaValue[0]:
                                if k > MP:
                                    MP = k
                            Per = percentageValue(newsContent)  # 新闻中的百分数、基点值
                            if Per == 0:
                                continue
                            row = row + 1
                            v3 = sentimentIntensity_institutions(Per, newsContent, highWeightList, middleWeightList, lowWeightList, HEW,MEW,LEW)
                            middleValue = MP * v3
                            data3 = getSentimentIntensity(middleValue, pol)
                            std3 = std3 + abs((int(quaRaw)) - (int(data3)))
                            # fsave.write(
                            #     str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + '\t' + pol + '\t' + quaRaw + '\t' + str(
                            #         data2) + '\n')
                    k3 = std3 / row
                    # print('实验3权值设置HD=%d,MD=%d,LD=%d的V值=%f：' % (HEW, MEW, LEW, k3))
                    if k3 > max:
                        max = k3
                        HEW_max = HEW
                        MEW_max = MEW
                        LEW_max = LEW
                    if k3 < min:
                        min = k3
                        HEW_min = HEW
                        MEW_min = MEW
                        LEW_min = LEW
    print('总结-----实验3权重设置最大V=%f,权值为HEW=%f,MEW=%f,LEW=%f' % (max, HEW_max, MEW_max, LEW_max))
    print('总结-----实验3权重设置最小V=%f,权值为HEW=%f,MEW=%f,LEW=%f' % (min, HEW_min, MEW_min, LEW_min))

def  func_degree_institutions(fsrc, fsave_degree_institutions, sentiWord, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3, attrList):
    global scope, baseValue
    HD_max = 0
    MD_max = 0
    LD_max = 0
    HEW_max = 0
    MEW_max = 0
    LEW_max = 0
    HD_min = 0
    MD_min = 0
    LD_min = 0
    HEW_min = 0
    MEW_min = 0
    LEW_min = 0
    max = 0
    min = 65535
    for i in range(1, scope):
        for j in range(1, scope):
            for k in range(1, scope):
                for m in range(1,scope):
                    for n in range(1,scope):
                        for p in range(1,scope):
                            sum1 = i + j + k
                            sum2 = m + n + p
                            sum = i + j + k + m + n + p
                            if sum == scope:
                                HEW = float(i)/scope
                                MEW = float(j)/scope
                                LEW = float(k)/scope
                                HD = float(m)/scope
                                MD = float(n)/scope
                                LD = float(p)/scope
                            elif (sum1==scope) & (sum2 == scope):
                                HEW = float(i) / scope
                                MEW = float(j) / scope
                                LEW = float(k) / scope
                                HD = float(m) / scope
                                MD = float(n) / scope
                                LD = float(p) / scope
                            else:
                                continue
                            row = 0
                            std4 = 0
                            fsrc.seek(0)
                            for each in fsrc.readlines():
                                each = each.strip().split('\t')
                                newsTime = each[0]
                                newsContent = each[1]
                                flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3)
                                if flag == 1:

                                    obj = each[2]
                                    pol = each[3]
                                    quaRaw = each[4]
                                    # 新闻分词
                                    seg_list = jieba.cut(newsContent)
                                    words = []
                                    for each2 in seg_list:
                                        words.append(each2)
                                    # print('jieba:',words)
                                    vec_array = word2vec_W(word_vec, words, sentiWord)
                                    probaValue = clf.predict_proba(vec_array)
                                    # print('probaValue', probaValue)
                                    normalList = []
                                    # 第一种量化值
                                    MP = 0  # 存储概率值 MP
                                    for k in probaValue[0]:
                                        if k > MP:
                                            MP = k
                                    Per = percentageValue(newsContent)  # 新闻中的百分数、基点值
                                    if Per == 0:
                                        continue
                                    row = row + 1
                                    v4 = sentimentIntensity_degree_institutions(Per,newsContent, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3,HEW,MEW,LEW,HD,MD,LD)
                                    middleValue = MP * v4
                                    data4 = getSentimentIntensity(middleValue, pol)
                                    std4 = std4 + abs((int(quaRaw)) - (int(data4)))
                                    # fsave.write(
                                    #     str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + '\t' + pol + '\t' + quaRaw + '\t' + str(
                                    #         data2) + '\n')
                            k4 = std4 / row
                            # print('实验4权值设置HEW=%d,MEW=%d,LEW=%d,HD=%d,MD=%d,LD=%d的V值=%f：' % (HEW, MEW, LEW,HD, MD, LD, k4))
                            if k4> max:
                                max = k4
                                HEW_max = HEW
                                MEW_max = MEW
                                LEW_max = LEW
                                HD_max = HD
                                MD_max = MD
                                LD_max = LD
                            if k4 < min:
                                min = k4
                                HEW_min = HEW
                                MEW_min = MEW
                                LEW_min = LEW
                                HD_min = HD
                                MD_min = MD
                                LD_min = LD
    print('总结-----实验4权重设置最大V=%f,权值为HEW=%f,MEW=%f,LEW=%f,HD=%f,MD=%f,LD=%f' % (max, HEW_max, MEW_max, LEW_max,HD_max, MD_max, LD_max))
    print('总结-----实验4权重设置最小V=%f,权值为HEW=%f,MEW=%f,LEW=%f,HD=%f,MD=%f,LD=%f' % (min, HEW_min, MEW_min, LEW_min,HD_min, MD_min, LD_min))
    return HEW_min, MEW_min, LEW_min,HD_min, MD_min, LD_min

def main(fsrc, fsave, sentiWord, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3, attrList, HEW_min, MEW_min, LEW_min, HD_min, MD_min, LD_min):
    row = 0
    for each in fsrc.readlines():
        each = each.strip().split('\t')
        newsTime = each[0]
        newsContent = each[1]

        flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3)
        if flag == 1:
            attr = findAttr(newsContent, attrList)

            obj = each[2]
            pol = each[3]
            quaRaw = each[4]
            #新闻分词
            seg_list = jieba.cut(newsContent)
            words = []
            for each2 in seg_list:
                words.append(each2)
            vec_array = word2vec_W(word_vec, words, sentiWord)
            probaValue = clf.predict_proba(vec_array)
            # print('probaValue',probaValue)
            MP = 0      #存储概率值 MP
            for k in probaValue[0]:
                if k > MP:
                    MP = k
            Per = percentageValue(newsContent) #新闻中的百分数、基点值
            if Per == 0:
                continue
            row = row + 1
            v4 = sentimentIntensity_degree_institutions(Per,newsContent, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3, HEW_min, MEW_min, LEW_min, HD_min, MD_min, LD_min)
            middleValue = MP * v4
            data_degree_institutions = getSentimentIntensity(middleValue, pol)
            fsave.write(str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + attr + '\t' + pol + '\t' + quaRaw + '\t' + str(data_degree_institutions) + '\n' )

    fsave.close()

if __name__ == "__main__":
    Per_base = 0.001
    baseValue = 0.5
    scope = 20
    # 情感极性分析模型
    clf = joblib.load('../eSentimentModel/LogisticReg_W_model.m')

    # 词向量模型
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    value_0 = 0
    value_1 = 0.0013
    value_2 = 0.01
    value_3 = 0.018
    value_4 = 0.026

    w1=1
    w2=2
    w3=3
    w4=4
    w5=5

    noDeg = 0.1
    noImpact = 0.1
    # 属性列表
    attrList = readAttr()

    # 读取情感词和程度词
    sentiWord, degWordH, degWordL = weightWordRead()
    sentiWeight = 10  # 情感词权重

    # 舆情B---情感量化
    highWeightList, middleWeightList, lowWeightList, threeWeight_B = weight_B()

    deg1, deg2, deg3 = degreeWord()

    # 打开文件，原始量化文件
    fname = '../eFiles/eGet_average_qua_average_quaValue_DataSet.txt'
    fsrc = open(fname, 'r', encoding='utf-8')

    # #保存文件
    # fsavename = '../eFiles/eGetQuaValue_all_quaValue.txt'
    # fsave = open(fsavename, 'w', encoding='utf-8')


    file = '../eFiles/eGetQuaValue_Per.txt'
    fsave_Per = open(file, 'w', encoding='utf-8') #存储只考虑百分数的情况，基础实验
    func_base(fsrc,fsave_Per, sentiWord,clf, word_vec)
    file = '../eFiles/eGetQuaValue_degree_Per.txt'
    fsave_degree = open(file, 'w', encoding='utf-8')  # 存储只考虑程度词的情况
    func_degree(fsrc,fsave_degree, sentiWord,deg1, deg2, deg3,clf, word_vec)
    file = '../eFiles/eGetQuaValue_institutions_Per.txt'
    fsave_institutions = open(file, 'w', encoding='utf-8')  # 存储只考虑机构类词的情况
    func_institutions(fsrc,fsave_institutions, sentiWord,highWeightList, middleWeightList, lowWeightList,clf, word_vec)
    file = '../eFiles/eGetQuaValue_degree_institutions_Per.txt'
    fsave_degree_institutions = open(file, 'w', encoding='utf-8')  # 存储考虑程度词和机构类词的情况
    HEW_min, MEW_min, LEW_min, HD_min, MD_min, LD_min = func_degree_institutions(fsrc, fsave_degree_institutions, sentiWord, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3, attrList)

    # 保存文件
    fsavename = '../eFiles/eGetQuaValue_degree_institutions_2018-12-29.txt'
    fsave = open(fsavename, 'w', encoding='utf-8')
    main(fsrc, fsave, sentiWord, highWeightList, middleWeightList, lowWeightList, deg1, deg2, deg3, attrList, HEW_min, MEW_min, LEW_min, HD_min, MD_min, LD_min)

    #说明
    #设置权重范围0-2，步长0.1,(在没有程度词和机构词时，设置基权重0.1)----scope=10

