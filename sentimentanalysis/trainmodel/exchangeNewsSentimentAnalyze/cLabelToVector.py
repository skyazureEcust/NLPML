import jieba
import xlrd
from util import CommonUtil
import ltpmanner
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import gensim
import numpy as np


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

def splitwords_word2vec(filename,fname, weightWord):
    filetxt = open(filename,'a+',encoding='utf-8')
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    # fname = '../files/splitedsentence.xls'
    data = xlrd.open_workbook(fname)
    table = data.sheet_by_index(0)
    nrows = table.nrows
    ncols = table.ncols
    #一行一行读取新闻内容
    for i in range(0, nrows):
        #读取新闻的时间
        # newsTime = table.cell(i, 0).value
        news_time = table.cell(i,0).value
        newsTime = CommonUtil.get_datetime_from_cell(news_time)
        #读取新闻的内容
        newsContent = table.cell(i,1).value
        #获取极性值 -1，0,1
        polarity = int(table.cell(i,3).value)
        print(newsTime)
        # print(newsContent)
        # print(polarity)

        # 分词
        words,wordsList = ltpmanner.splitwords(newsContent)    #对这一条新闻进行分词
        #去停用词
        new_wordsList = ltpmanner.stopwords(wordsList)
        vec_array = np.zeros(64, dtype=float)  #一条新闻初始化词向量，为0
        #循环对词进行向量化
        total_array = []
        total_array.append(newsTime)
        length = len(new_wordsList)
        for each in new_wordsList:
            try:
                if each in weightWord:
                    value = word_vec[each] * 10/length
                    vec_array += value
                else:
                    value = word_vec[each]/length
                    vec_array += value
            except Exception as e:
                print("error:", e)

        #转成list
        vec_array = vec_array.tolist()
        #合并到一起 total_array
        for each in vec_array:
            total_array.append(each)

        total_array.append(polarity)
        # print(total_array)
        # print('len(total_array)',len(total_array))
        #向量化后写入文件
        for each in total_array:
            print(each)
            filetxt.write(str(each) + '\t')
        filetxt.write('\n')

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

def  Word2vec_onlyWord(fsrc, fOnlyWord):
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    for m in fsrc.readlines():
        m = m.strip().split('\t')
        # 读取新闻的时间
        newsTime = m[0]
        # 读取新闻的内容
        newsContent = m[1]
        # 获取极性值 -1，0,1
        polarity = m[3]
        #jieba分词
        seg_list = jieba.cut(newsContent)
        words = []
        for seg in seg_list:
            words.append(seg)
        # print('jieba:',words)

        # 去停用词
        new_wordsList = stopwords(words)
        vec_array = np.zeros(64, dtype=float)  # 一条新闻初始化词向量，为0
        # 循环对词进行向量化
        total_array = []
        total_array.append(newsTime)
        length = len(new_wordsList)
        for each in new_wordsList:
            try:
                value = word_vec[each] / length
                vec_array += value
            except Exception as e:
                print("error:", e)
        # 转成list
        vec_array = vec_array.tolist()
        # 合并到一起 total_array
        for each in vec_array:
            total_array.append(each)

        total_array.append(polarity)
        # print(total_array)
        # print('len(total_array)',len(total_array))
        # 向量化后写入文件
        for each in total_array:
            # print(each)
            fOnlyWord.write(str(each) + '\t')
        #写入换行符
        fOnlyWord.write('\n')

    #文件写入完毕，关闭文件
    fOnlyWord.close()

def  Word2vec_sentiWord(fsrc, fSentiWord,sentiWord, sentiWeight):
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    #文件指针回到文件开始的位置
    fsrc.seek(0)
    for m in fsrc.readlines():
        m = m.strip().split('\t')
        # 读取新闻的时间
        newsTime = m[0]
        # 读取新闻的内容
        newsContent = m[1]
        # 获取极性值 -1，0,1
        polarity = m[3]
        #jieba分词
        seg_list = jieba.cut(newsContent)
        words = []
        for seg in seg_list:
            words.append(seg)
        # print('jieba:',words)

        # 去停用词
        new_wordsList = stopwords(words)
        vec_array = np.zeros(64, dtype=float)  # 一条新闻初始化词向量，为0
        # 循环对词进行向量化
        total_array = []
        total_array.append(newsTime)
        length = len(new_wordsList)
        for each in new_wordsList:
            try:
                if each in sentiWord:
                    value = word_vec[each] * sentiWeight / length
                    vec_array += value
                else:
                    value = word_vec[each] / length
                    vec_array += value
            except Exception as e:
                print("error:", e)

        # 转成list
        vec_array = vec_array.tolist()
        # 合并到一起 total_array
        for each in vec_array:
            total_array.append(each)

        total_array.append(polarity)
        # print(total_array)
        # print('len(total_array)',len(total_array))
        # 向量化后写入文件
        for each in total_array:
            # print(each)
            fSentiWord.write(str(each) + '\t')
        #写入换行符
        fSentiWord.write('\n')

    #文件写入完毕，关闭文件
    fSentiWord.close()

def Word2vec_sentiWordAndDeg(fsrc, fDegWord, degWordH,degWordL,SentiDegH, SentiDegL):
    model = gensim.models.KeyedVectors.load_word2vec_format(
        '../word2veczzh/news_12g_baidubaike_20g_novel_90g_embedding_64.bin', binary=True)
    word_vec = model.wv
    del model

    # 文件指针回到文件开始的位置
    fsrc.seek(0)
    for m in fsrc.readlines():
        m = m.strip().split('\t')
        # 读取新闻的时间
        newsTime = m[0]
        # 读取新闻的内容
        newsContent = m[1]
        # 获取极性值 -1，0,1
        polarity = m[3]
        #jieba分词
        seg_list = jieba.cut(newsContent)
        words = []
        for seg in seg_list:
            words.append(seg)
        # print('jieba:',words)

        # 去停用词
        new_wordsList = stopwords(words)
        vec_array = np.zeros(64, dtype=float)  # 一条新闻初始化词向量，为0
        # 循环对词进行向量化
        total_array = []
        total_array.append(newsTime)
        length = len(new_wordsList)
        for each in new_wordsList:
            try:
                if each in degWordH:
                    value = word_vec[each] * SentiDegH / length
                    vec_array += value
                elif each in degWordL:
                    value = word_vec[each] * SentiDegL / length
                    vec_array += value
                else:
                    value = word_vec[each] / length
                    vec_array += value
            except Exception as e:
                print("error:", e)

        # 转成list
        vec_array = vec_array.tolist()
        # 合并到一起 total_array
        for each in vec_array:
            total_array.append(each)

        total_array.append(polarity)
        # print(total_array)
        # print('len(total_array)',len(total_array))
        # 向量化后写入文件
        for each in total_array:
            # print(each)
            fDegWord.write(str(each) + '\t')
        #写入换行符
        fDegWord.write('\n')

    #文件写入完毕，关闭文件
    fDegWord.close()
    fsrc.close()


if __name__ == "__main__":
    # #读取情感词和程度词
    # sentiWord, degWordH, degWordL = weightWordRead()
    #
    # # 读取文件----标注的数据集
    # fname = '../eFiles/aaPolarity_label_twoKind_test_polarity_DataSet.txt'  #
    # fsrc = open(fname, 'r', encoding='utf-8')
    #
    #
    # # 保存文件---只有词向量后的文件
    # filename = r'../eFiles/cLabelToVector_word2vec_Only_Word.txt'
    # fOnlyWord = open(filename, 'w', encoding='utf-8')
    #
    # # 保存文件-----给情感词加权重
    # filename = r'../eFiles/cLabelToVector_word2vec_use_sentiWord.txt'
    # fSentiWord = open(filename,'w', encoding='utf-8')
    #
    # # 保存文件-----给情感词和程度词加权重
    # filename = r'../eFiles/cLabelToVector_word2vec_use_SentiWordAndDegWord.txt'
    # fDegWord = open(filename, 'w', encoding='utf-8')
    #
    # # 自定义分词词典
    # file = '../dictionary/splitworddict.txt'
    # jieba.load_userdict(file)
    #
    # #词向量化----只是单纯的词向量化
    # Word2vec_onlyWord(fsrc, fOnlyWord)
    # # 词向量化----给情感词加权重
    # sentiWeight = 10  #情感词权重
    # Word2vec_sentiWord(fsrc, fSentiWord,sentiWord, sentiWeight)
    # # 词向量化----给情感词和程度词加权重
    # SentiDegH = 10  #高程度词权重
    # SentiDegL = 5   #低程度词权重
    # Word2vec_sentiWordAndDeg(fsrc, fDegWord,degWordH,degWordL, SentiDegH, SentiDegL)

    # -------------------------------------------------------------------------------------------------------
    #
    # 计算机工程与设计
    #
    # 读取情感词和程度词
    sentiWord, degWordH, degWordL = weightWordRead()
    # 读取文件----标注的数据集
    fname = '../eFiles2/aaPolarity_label_twoKind_test_polarity_DataSet_erfenlei.txt' #计算机工程与设计
    fsrc = open(fname, 'r', encoding='utf-8')

    # 保存文件---只有词向量后的文件
    filename = r'../eFiles2/cLabelToVector_word2vec_Only_Word.txt'
    fOnlyWord = open(filename, 'w', encoding='utf-8')

    # 保存文件-----给情感词加权重
    filename = r'../eFiles2/cLabelToVector_word2vec_use_sentiWord.txt'
    fSentiWord = open(filename, 'w', encoding='utf-8')

    # 保存文件-----给情感词和程度词加权重
    filename = r'../eFiles2/cLabelToVector_word2vec_use_SentiWordAndDegWord.txt'
    fDegWord = open(filename, 'w', encoding='utf-8')

    # 自定义分词词典
    file = '../dictionary/splitworddict.txt'
    jieba.load_userdict(file)

    # 词向量化----只是单纯的词向量化
    Word2vec_onlyWord(fsrc, fOnlyWord)
    # 词向量化----给情感词加权重
    sentiWeight = 10  # 情感词权重
    Word2vec_sentiWord(fsrc, fSentiWord, sentiWord, sentiWeight)
    # 词向量化----给情感词和程度词加权重
    SentiDegH = 10  # 高程度词权重
    SentiDegL = 5  # 低程度词权重
    Word2vec_sentiWordAndDeg(fsrc, fDegWord, degWordH, degWordL, SentiDegH, SentiDegL)







