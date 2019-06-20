import re

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
    degreeHighList = []
    with open('../dictionary/chengduci_high.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degreeHighList.append(each)

    degreeLowList = []
    with open('../dictionary/chengduci_low.txt', 'r', encoding='utf-8') as f:
        words = f.readlines()
        for w in words:
            each = w.encode('utf-8').decode('utf-8-sig').strip()  # 去掉txt第一行奇怪的字符 \ufeff
            degreeLowList.append(each)

    return degreeHighList, degreeLowList

def ThreeKindWeight(data,newsContent,  highWeightList, middleWeightList, lowWeightList):
    global firstWeight, secondWeight, thirdWeight
    flag = 0
    for ch in highWeightList:
        if ch in newsContent:
            data = data * firstWeight
            flag = 1
            break
    if flag == 0:
        for ch in middleWeightList:
            if ch in newsContent:
                data = data * secondWeight
                flag = 1
                break
    if flag == 0:
        for ch in lowWeightList:
            if ch in newsContent:
                data = data * thirdWeight
                flag = 1
                break
    return data

def chengduWeight(data,newsContent,  degreeHighList, degreeLowList):
    global firstWeight, thirdWeight
    flag = 0
    for ch in degreeHighList:
        if ch in newsContent:
            data = data * firstWeight
            flag = 1
            break
    if flag == 0:
        for ch in degreeLowList:
            if ch in newsContent:
                data = data * (2-thirdWeight)
                flag = 1
                break
    return data

def data_number(fsave, data, newsTime,newsContent, obj, pol):
    global w1, w2, w3, w4, w5, w6, w7, w8, w9, w10
    # print(data)
    value_0 = 0
    # #设置分割范围

    value_1 = 0.001

    value_2 = 0.007

    value_3 = 0.013

    value_4 = 0.019

    value_5 = 0.025

    #计算各范围的值
    number_v1 = 0
    number_v2 = 0
    number_v3 = 0
    number_v4 = 0
    number_v5 = 0


    if data == 0:
        value_0 = value_0 + 1
        if pol == 0:
            fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol + '\t'  + str(w1 * int(pol)) + '\n')
        else:
            fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol + '\t' + str(w1 * int(pol)) + '\n')

    elif data <= value_1:
        # print(data)
        number_v1 = number_v1 + 1
        # print(newsContent)
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol  + '\t'  + str(w1 * int(pol))  + '\n')

    elif data <= value_2:
        number_v2 = number_v2 + 1
        # print(newsContent)
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol  + '\t'  + str(w2 * int(pol)) + '\n')
    elif data <= value_3:
        number_v3 = number_v3 + 1
        # print(newsContent)
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol  + '\t'  + str(w3 * int(pol)) + '\n')
    elif data <= value_4:
        number_v4 = number_v4 + 1
        # print(newsContent)
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol  + '\t'  + str(w4 * int(pol)) + '\n')
    elif data > value_4:
        number_v5 = number_v5 + 1
        # print(newsContent)
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol  + '\t' + str(w5 * int(pol)) + '\n')


    return number_v1, number_v2,number_v3, number_v4,number_v5, value_0
    # return number_v1, number_v2,number_v3, number_v4, number_v5



def data_distribute(fobj,fsave, highWeightList, middleWeightList, lowWeightList, degreeHighList, degreeLowList):
    value_0 = 0
    # 设置分割范围
    value_1 = 0.001

    value_2 = 0.007

    value_3 = 0.013

    value_4 = 0.019

    counter1 = 0
    counter2 = 0
    counter3 = 0
    counter4 = 0
    counter5 = 0

    total_data = 0

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

    for every in fobj.readlines():
        every = every.strip().split('\t')
        newsTime = every[0]  #新闻时间
        newsContent = every[1]  #新闻内容
        obj = every[2]  #新闻评价对象
        # pol = every[3]  #新闻极性,后面写等级时用 -----  people1使用
        pol = every[4]  #新闻极性,后面写等级时用 -----  people2使用
        total_data = total_data + 1
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

        n1 = 0
        n2 = 0
        n3 = 0
        n4 = 0
        n5 = 0
        n6 = 0
        n7 = 0
        n8 = 0
        n9 = 0
        n10 = 0
        data = 0

        if res1:
            start = res1[0]
            data = float(start) / 100
        elif res2:

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

        # 程度词权重计算
        data = ThreeKindWeight(data,newsContent,  highWeightList, middleWeightList, lowWeightList)
        data = chengduWeight(data,newsContent,  degreeHighList, degreeLowList)
        # n1, n2, n3, n4, n5, value0 = data_number(data,newsContent)
        n1, n2, n3, n4, n5, value0 = data_number(fsave, data,newsTime,newsContent,obj, pol)
        counter1 = counter1 + n1
        counter2 = counter2 + n2
        counter3 = counter3 + n3
        counter4 = counter4 + n4
        counter5 = counter5 + n5

        value_0 = value_0 + value0

    print("<=",value_1,"=",counter1)
    print("<=",value_2,"=",counter2)
    print("<=",value_3,"=",counter3)
    print("<=",value_4,"=",counter4)
    print(">",value_4,"=",counter5)

    # print(counter1,counter2,counter3,counter4,counter5,counter7)
    print('五类总数：',counter1 + counter2 + counter3 + counter4 + counter5)
    print('total_data',total_data)
    print('value_0',value_0)

    fsave.close()


if __name__ == "__main__":

    # 权重等级
    w1 = 1
    w2 = 2
    w3 = 3
    w4 = 4
    w5 = 5

    # 舆情B---情感量化
    highWeightList, middleWeightList, lowWeightList, threeWeight_B = weight_B()

    # 程度词----高、低
    degreeHighList, degreeLowList = degreeWord()

    fn = '../eFiles/aaPolarity_label_twoKind_test_polarity_tother.txt'
    fobj = open(fn, 'r', encoding='utf-8')

    # #people1
    # file = '../eFiles/eaSetQuaValueSencond_raw_people1_quaValue.txt'
    # fsave = open(file, 'w', encoding='utf-8')
    # # 第一种---people1
    # firstWeight = 1.5
    # secondWeight = 1.3
    # thirdWeight = 1.1

    # people2
    file = '../eFiles/eaSetQuaValueSencond_raw_people2_quaValue.txt'
    fsave = open(file, 'w', encoding='utf-8')
    # 第二种---people2
    firstWeight = 2
    secondWeight = 1.5
    thirdWeight = 1.3

    data_distribute(fobj, fsave, highWeightList, middleWeightList, lowWeightList, degreeHighList, degreeLowList)