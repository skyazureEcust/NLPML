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

    return sentiWord

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
    # 读取程度词---“extreme”
    D1 = []
    with open('../dictionary/eDictionary/degree_6_kinds/D1.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            D1.append(each.strip())

    # 读取程度词---“over”
    D2 = []
    with open('../dictionary/eDictionary/degree_6_kinds/D2.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            D2.append(each.strip())

    # 读取程度词---“very”
    D3 = []
    with open('../dictionary/eDictionary/degree_6_kinds/D3.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            D3.append(each.strip())

    # 读取程度词---“more”
    D4 = []
    with open('../dictionary/eDictionary/degree_6_kinds/D4.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            D4.append(each.strip())

    # 读取程度词---“few”
    D5 = []
    with open('../dictionary/eDictionary/degree_6_kinds/D5.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            D5.append(each.strip())

    # 读取程度词---“insufficiently”
    D6 = []
    with open('../dictionary/eDictionary/degree_6_kinds/D6.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for wgt in words:
            each = wgt.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            D6.append(each.strip())
    return D1, D2, D3, D4, D5,D6

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

def panduan(newsContent, highWeightList, middleWeightList, lowWeightList, D1, D2, D3, D4, D5,D6):
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
        for h in D1:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in D2:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in D3:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in D4:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in D5:
            if h in newsContent:
                flag = 1
    if flag == 0:
        for h in D6:
            if h in newsContent:
                flag = 1
    return flag

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

    data = 0.001
    if res1:
        # print('newsContent',newsContent)
        for start in res1:
            if '-' in start:
                start = str(start[0]).split('-')[0]
            # print('newsContent', newsContent)
            data = float(start)
            break
    elif res2:
        # print('res2', res2)
        # quantifyValue = quantifyValue + '+' + res2[0] + '%'  #与上面同理
        for start in res2:
            data = float(start)
            break
    elif res3:
        data = float(res3[0]) / 100

    elif res4:
        data = float(res4[0]) / 10000
    elif res5:
        data = float(res5[0]) / 100
    elif res6:
        data = float(res6[0]) / 100
    elif res7:
        data = float(res7[0]) / 100
    elif res8:
        data = float(res8[0]) / 100
    elif res9:
        data = float(res9[0]) / 100
    elif res10:
        data = float(res10[0]) / 100

    return data

def sentimentIntensity_degree(newsContent, D1, D2, D3, D4, D5,D6, D1V, D2V, D3V,D4V,D5V,D6V):
    global base_degree
    # 程度副词
    flag = 0
    degData = base_degree
    for each in D1:
        if each in newsContent:
            degData = D1V
            flag = 1
            break
    if flag == 0:
        for each in D2:
            if each in newsContent:
                degData = D2V
                flag = 1
                break
    if flag == 0:
        for each in D3:
            if each in newsContent:
                degData = D3V
                flag = 1
                break
    if flag == 0:
        for each in D4:
            if each in newsContent:
                degData = D4V
                flag = 1
                break
    if flag == 0:
        for each in D5:
            if each in newsContent:
                degData = D5V
                flag = 1
                break
    if flag == 0:
        for each in D6:
            if each in newsContent:
                degData = D6V
                flag = 1
                break

    return degData

def sentimentIntensity_institutions(newsContent, highWeightList, middleWeightList, lowWeightList, HEW,MEW,LEW):
    global base_institutions
    flag2 = 0
    # 权威机构等
    suData = base_institutions
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

    return suData

def func_degree_constant(fsrc,fsave,sentiWord,D1, D2, D3, D4, D5,D6,clf, word_vec):
    global scope,scopeHalf
    D1V = 2
    D2V = 1.7
    D3V = 1.5
    D4V = 1.3
    D5V = 1.1
    D6V = 0.8

    row = 0
    std = 0
    # fsrc.seek(0)
    for each in fsrc.readlines():
        row = row + 1
        each = each.strip().split('\t')
        newsTime = each[0]
        newsContent = each[1]
        # flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, D1, D2, D3, D4, D5,D6)
        # if flag == 1:
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
        # probaValue = clf.predict_proba(vec_array)
        MP = clf.predict(vec_array)
        # # print('probaValue', probaValue)
        # normalList = []
        # # 第一种量化值
        # MP = 0  # 存储概率值 MP
        # for k in probaValue[0]:
        #     if k > MP:
        #         MP = k
        deg = sentimentIntensity_degree(newsContent, D1, D2, D3, D4, D5,D6, D1V, D2V, D3V,D4V,D5V,D6V)
        middleValue = MP * deg
        # data = getSentimentIntensity(middleValue, pol)
        data = middleValue
        std = std + abs((float(quaRaw)) - (float(data)))
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol + '\t' + quaRaw +  '\t' + str(float(data)) + '\n')
    print('行数1',row)
    if row != 0:
        k = std / row
    else:
        k = 65535
        print('行数为0')
    print('总结-----实验(MP * deg)权重设置最小V=%0.4f,权值为D1V=%0.4f, D2V=%0.4f, D3V=%0.4f, D4V= %0.4f, D5V=%0.4f, D6V=%0.4f '%(k,D1V, D2V, D3V,D4V,D5V,D6V))
    fsave.close()
    # fsrc.close()
    return D1V, D2V, D3V,D4V,D5V,D6V

def func_degree_institutions(fsrc,sentiWord,D1, D2, D3, D4, D5,D6,clf, word_vec,D1V, D2V, D3V,D4V,D5V,D6V):
    global scope,scopeHalf
    HEW_min = 0
    MEW_min = 0
    LEW_min = 0
    max = 0
    min = 65535
    for i in range(1, scope):
        for j in range(1, scope):
            for k in range(1, scope):
                sum = i + j + k
                if (sum == scope) & (i > j+2 > k+2 > 10):
                    HEW = float(i) / scopeHalf
                    MEW = float(j) / scopeHalf
                    LEW = float(k) / scopeHalf
                    row = 0
                    std = 0
                    fsrc.seek(0)
                    for each in fsrc.readlines():
                        row = row + 1
                        each = each.strip().split('\t')
                        newsTime = each[0]
                        newsContent = each[1]
                        # flag = panduan(newsContent, highWeightList, middleWeightList, lowWeightList, D1, D2, D3, D4, D5,D6)
                        # if flag == 1:
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
                        # probaValue = clf.predict_proba(vec_array)
                        MP = clf.predict(vec_array)
                        # print('probaValue', probaValue)
                        normalList = []
                        # 第一种量化值
                        # MP = 0  # 存储概率值 MP
                        # for k in probaValue[0]:
                        #     if k > MP:
                        #         MP = k
                        deg = sentimentIntensity_degree(newsContent, D1, D2, D3, D4, D5,D6, D1V, D2V, D3V,D4V,D5V,D6V)

                        institutions = sentimentIntensity_institutions(newsContent, highWeightList,
                                                                       middleWeightList, lowWeightList, HEW, MEW,
                                                                       LEW)
                        middleValue = MP * deg * institutions
                        data = middleValue
                        # print('float(quaRaw)',float(quaRaw))
                        # print('float(data)',float(data))
                        std = std + abs((float(quaRaw)) - (float(data)))

                    k = std / row
                    print('实验(MP * deg * institutions),V=%0.4f,权值为HEW=%0.4f,MEW=%0.4f,LEW=%0.4f' % (
                    min, HEW_min, MEW_min, LEW_min))
                    if k < min:
                        min = k
                        HEW_min = HEW
                        MEW_min = MEW
                        LEW_min = LEW
    print('总结-----实验(MP * deg * institutions)权重设置最小V=%0.4f,权值为HEW=%0.4f,MEW=%0.4f,LEW=%0.4f' % (min, HEW_min, MEW_min, LEW_min))
    # fsrc.close()
    return HEW_min, MEW_min, LEW_min

def func_degree_institutions_write_txt(fsrc, fsave,sentiWord, D1, D2, D3, D4, D5,D6, clf, word_vec, D1V, D2V, D3V,D4V,D5V,D6V,HEW_min, MEW_min, LEW_min):
    global scope, scopeHalf
    row = 0
    std = 0
    fsrc.seek(0)
    for each in fsrc.readlines():
        row = row + 1
        each = each.strip().split('\t')
        newsTime = each[0]
        newsContent = each[1]
        # flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, D1, D2, D3, D4, D5,D6)
        # if flag == 1:
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
        # probaValue = clf.predict_proba(vec_array)
        # print('probaValue', probaValue)
        MP = clf.predict(vec_array)
        normalList = []
        # 第一种量化值
        # MP = 0  # 存储概率值 MP
        # for k in probaValue[0]:
        #     if k > MP:
        #         MP = k
        deg = sentimentIntensity_degree(newsContent, D1, D2, D3, D4, D5,D6, D1V, D2V, D3V,D4V,D5V,D6V)
        institutions = sentimentIntensity_institutions(newsContent, highWeightList,
                                                       middleWeightList, lowWeightList, HEW_min, MEW_min,
                                                       LEW_min)

        middleValue = MP * deg * institutions
        data = middleValue
        fsave.write(
            str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol + '\t' + quaRaw + '\t' + str(float(data))+ '\n')

    print('行数3',row)
    fsave.close()
    # fsrc.close()

def func_degree_institutions_Per(fsrc,fsave,sentiWord,highWeightList, middleWeightList, lowWeightList,clf, word_vec, D1V, D2V, D3V,D4V,D5V,D6V, HEW_min, MEW_min, LEW_min, attrList):
    row = 0
    std = 0
    fsrc.seek(0)
    for each in fsrc.readlines():
        row = row + 1
        each = each.strip().split('\t')
        newsTime = each[0]
        newsContent = each[1]
        # flag = panduan(newsContent,highWeightList, middleWeightList, lowWeightList, D1, D2, D3, D4, D5,D6)
        # if flag == 1:
        obj = each[2]
        pol = each[3]
        quaRaw = each[4]
        attr = findAttr(newsContent, attrList)
        # 新闻分词
        seg_list = jieba.cut(newsContent)
        words = []
        for each2 in seg_list:
            words.append(each2)
        # print('jieba:',words)
        vec_array = word2vec_W(word_vec, words, sentiWord)
        probaValue = clf.predict_proba(vec_array)
        # print('probaValue', probaValue)
        MP = clf.predict(vec_array)
        # normalList = []
        # # 第一种量化值
        # MP = 0  # 存储概率值 MP
        # for k in probaValue[0]:
        #     if k > MP:
        #         MP = k
        deg = sentimentIntensity_degree(newsContent, D1, D2, D3, D4, D5,D6, D1V, D2V, D3V,D4V,D5V,D6V)
        Per = percentageValue(newsContent)  # 新闻中的百分数、基点值
        institutions = sentimentIntensity_institutions(newsContent, highWeightList, middleWeightList, lowWeightList, HEW_min,MEW_min,LEW_min)
        middleValue = MP * deg * institutions *Per
        data = middleValue
        std = std + abs((float(quaRaw)) - (float(data)))
        fsave.write(
            str(newsTime) + '\t' + newsContent + '\t' + obj  + '\t' + attr + '\t' + pol + '\t' + quaRaw + '\t' + str(float(data)) + '\n')

    k = std / row
    print('行数4',row)
    print('总结-----实验(MP * deg * Per * institutions)权重设置最小V=%0.4f,权值为HEW=%0.4f,MEW=%0.4f,LEW=%0.4f,D1V=%0.4f, D2V=%0.4f, D3V=%0.4f, D4V= %0.4f, D5V=%0.4f, D6V=%0.4f ' % (k, HEW_min, MEW_min, LEW_min,D1V, D2V, D3V,D4V,D5V,D6V))
    fsave.close()
    # fsrc.close()

if __name__ == "__main__":

    scope = 50
    scopeHalf = scope / 5

    base_degree = 1  #在考虑程度词时，如果句子中没有程度词，则设置权重为1
    base_institutions = 1   #在考虑机构词时，如果句子中没有机构词，则设置权重为1
    Per_base = 0.001
    # 情感极性分析模型
    # clf = joblib.load('../eSentimentModel/LogisticReg_W_model.m')
    clf = joblib.load('../eSentimentModel/LogisticReg_W_model_jisuanjiGCYSJ.m')  # 计算机工程与设计

    # 词向量模型
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    # 属性列表
    attrList = readAttr()

    # 读取情感词
    sentiWord = weightWordRead()
    sentiWeight = 10  # 情感词权重

    # 舆情B---情感量化
    highWeightList, middleWeightList, lowWeightList, threeWeight_B = weight_B()
    #读取程度词
    D1, D2, D3, D4, D5,D6 = degreeWord()

    # 打开文件，原始量化文件
    # fname = '../eFiles/eGet_first_second_average_intensity_DataSet.txt'
    # fsrc = open(fname, 'r', encoding='utf-8')
    fname = '../eFiles2/eGet_first_second_average_intensity_DataSet.txt'  # 计算机工程与设计
    fsrc = open(fname, 'r', encoding='utf-8')

    file1 =  '../eFiles2/jisuanji/eGetIntensity_degree.txt'
    fsave1 = open(file1, 'w', encoding='utf-8')
    D1V, D2V, D3V, D4V, D5V, D6V = func_degree_constant(fsrc,fsave1,sentiWord,D1, D2, D3, D4, D5,D6,clf, word_vec)


    HEW_min, MEW_min, LEW_min = func_degree_institutions(fsrc,sentiWord,D1, D2, D3, D4, D5,D6,clf, word_vec,D1V, D2V, D3V,D4V,D5V,D6V)


    file2 = '../eFiles2/jisuanji/eGetIntensity_degree_institutions.txt'
    fsave2 = open(file2, 'w', encoding='utf-8')
    func_degree_institutions_write_txt(fsrc, fsave2,sentiWord, D1, D2, D3, D4, D5,D6, clf, word_vec, D1V, D2V, D3V,D4V,D5V,D6V,HEW_min, MEW_min, LEW_min)


    file3 = '../eFiles2/jisuanji/eGetIntensity_degree_institutions_Per.txt'
    fsave3 = open(file3, 'w', encoding='utf-8')
    func_degree_institutions_Per(fsrc,fsave3,sentiWord,highWeightList, middleWeightList, lowWeightList,clf, word_vec, D1V, D2V, D3V,D4V,D5V,D6V, HEW_min, MEW_min, LEW_min, attrList)


    #说明
    #情感倾向概率值 * 程度词 （对比实验）

