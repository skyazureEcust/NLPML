
def funcW(fsrc, fsave):
    number0 = 0
    positive = 0
    negtive = 0

    for each in fsrc.readlines():
        eachitems = each.strip().split('\t')
        each = int(eachitems[3])
        print(each)
        if each == 0:
            number0 = number0 + 1

        if each == 1:
            positive = positive + 1
            if positive <= 1160:
                fsave.write(str(eachitems[0]) + '\t' + eachitems[1] + '\t' + eachitems[2] + '\t' + eachitems[3] + '\n')

        if each == -1:
            negtive = negtive + 1
            if negtive <= 1160:
                fsave.write(str(eachitems[0]) + '\t' + eachitems[1] + '\t' + eachitems[2] + '\t' + eachitems[3] + '\n')


    print('零:', number0)
    print('正', positive)
    print('负', negtive)



if __name__ == "__main__":

    # 打开文件，原始量化文件
    fname = '../eFiles/aaPolarity_label_twoKind_test_polarity_DataSet.txt'
    fsrc = open(fname, 'r', encoding='utf-8')

    file = '../eFiles2/aaPolarity_label_twoKind_test_polarity_DataSet_erfenlei.txt'
    fsave = open(file, 'w', encoding='utf-8')
    # funcW(fsrc)
    funcW(fsrc, fsave)
    fsrc.close()
    fsave.close()


# 计算标签个数

# 计算机工程与设计使用数据集：1160负向，1160正向，做二分类