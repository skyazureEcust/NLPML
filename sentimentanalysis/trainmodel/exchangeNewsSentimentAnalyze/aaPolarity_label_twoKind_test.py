
def comFunc(fSrc, fSave, fSaveDataSet):
    total = 0.0
    same = 0.0
    differ = 0.0
    for every in fSrc.readlines():
        total = total + 1
        every = every.strip().split('\t')
        newsTime = every[0]
        newsContent =  every[1]
        obj = every[2]
        pol = every[3]
        try:
            pol2 = every[4]
            # 将两种极性写到一个文件
            fSave.write(str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + pol + '\t' + pol2 + '\n')
            differ = differ + 1

        except:
            #实验文件
            fSaveDataSet.write(str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + pol  + '\n')


            fSave.write(str(newsTime) + '\t' + str(newsContent) + '\t' + obj + '\t' + pol + '\t' + pol + '\n')
            same = same + 1

    fSave.close()
    fSrc.close()
    print('total=', total)
    print('same=', same)
    print('differ=', differ)

    acc = same / total
    print('准确率=', acc)

if __name__ == "__main__":
    #读取源文件
    file = '../eFiles/polarity_two_people.txt'
    fSrc = open(file, 'r', encoding='utf-8')

    # 保存文件
    filename = '../eFiles/aaPolarity_label_twoKind_test_polarity_tother.txt'
    fSave = open(filename, 'w', encoding='utf-8')

    # # 实验文件
    file = '../eFiles/aaPolarity_label_twoKind_test_polarity_DataSet.txt'
    fSaveDataSet = open(file, 'w', encoding='utf-8')

    comFunc(fSrc,fSave, fSaveDataSet)