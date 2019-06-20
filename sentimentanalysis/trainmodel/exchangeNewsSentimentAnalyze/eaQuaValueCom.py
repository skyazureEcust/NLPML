import math


def comFunc(fsave):

    std1 = 0
    row = 0
    for every in fsave.readlines():
        row = row + 1
        every = every.strip().split('\t')
        newsTime = every[0]  #新闻时间
        newsContent = every[1]  #新闻内容
        obj = every[2]  #新闻评价对象
        pol = every[3]  #新闻极性,后面写等级时用
        qua1 = int(every[4])  #第二种
        qua2 = int(every[5])  #第二种

        std1 = std1 + (abs(qua1) - abs(qua2)) * (abs(int(qua1)) - abs(qua2))

    v1 = math.sqrt(std1) / row
    print('方差',v1)

if __name__ == "__main__":
    #读取原文件
    file = '../eFiles/eaSetQua_10_deg_2_people.txt'
    fsave = open(file, 'r', encoding='utf-8')

    comFunc(fsave)