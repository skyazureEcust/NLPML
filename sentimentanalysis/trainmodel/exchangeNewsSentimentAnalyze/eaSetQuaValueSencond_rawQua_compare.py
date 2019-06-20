def  compareQua(fsrc):
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
        qua1 = every[5]
        qua2 = every[6]
        print(qua1,qua2)
        if qua1 == qua2:
            same = same + 1

    print('same=',same)
    print('total',total)
    print('一致率=same/total,即%d/%d'%(same,total),same/total)


if __name__ == "__main__":
    #people1
    file = '../eFiles/people_1_2_raw_together.txt'
    fsrc = open(file, 'r', encoding='utf-8')
    compareQua(fsrc)