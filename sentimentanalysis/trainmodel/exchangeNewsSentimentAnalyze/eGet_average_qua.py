def  compareQua(fsrc,fsave):
    total = 0
    same = 0
    for every in fsrc.readlines():
        total = total + 1
        every = every.strip().split('\t')
        newsTime = every[0]  # 新闻时间
        newsContent = every[1]  # 新闻内容
        obj = every[2]  # 新闻评价对象
        pol1 = every[3]  #新闻极性,后面写等级时用 -----  people1使用
        pol2 = every[4]  # 新闻极性,后面写等级时用 -----  people2使用
        qua1 = int(every[5])
        qua2 = int(every[6])
        print(qua1,qua2)
        resultQua = int((qua1 + qua2)/2)
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol1 + '\t' + str(resultQua) + '\n')

    fsave.close()

if __name__ == "__main__":
    #people1
    file = '../eFiles/people_1_2_qua_same_polarity.txt'
    fsrc = open(file, 'r', encoding='utf-8')

    file = '../eFiles/eGet_average_qua_average_quaValue_DataSet.txt'
    fsave = open(file, 'w', encoding='utf-8')
    compareQua(fsrc,fsave)