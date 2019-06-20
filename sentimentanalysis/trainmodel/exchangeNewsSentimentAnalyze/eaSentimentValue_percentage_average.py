def  compareQua(fsrc,fsave):
    total = 0
    same = 0
    for every in fsrc.readlines():
        total = total + 1
        every = every.strip().split('\t')
        newsTime = every[0]  # 新闻时间
        newsContent = every[1]  # 新闻内容
        obj = every[2]  # 新闻评价对象
        pol = every[3]  #新闻极性,后面写等级时用 -----  people1使用
        qua1 = float(every[4])
        qua2 = float(every[5])
        print(qua1,qua2)
        result = (qua1 + qua2)/2
        resultQua = '%0.4f' % (result)
        fsave.write(str(newsTime) + '\t' + newsContent + '\t' + obj + '\t' + pol + '\t' + str(resultQua) + '\n')

    fsave.close()

if __name__ == "__main__":
    #people1
    file = '../eFiles/eaSetIntensityValue_percentage_first_second_people_label.txt' #手动合成的文件
    fsrc = open(file, 'r', encoding='utf-8')

    file = '../eFiles/eGet_first_second_average_intensity_DataSet.txt'
    fsave = open(file, 'w', encoding='utf-8')
    compareQua(fsrc,fsave)