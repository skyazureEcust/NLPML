from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.utils import column_or_1d
# import xgboost as xgb

# 旧版
# from sklearn import cross_validation
from tensorflow.contrib import slim
import numpy as np

NB_accuracy = []
NB_precision = []
NB_recall = []
NB_f1_score = []
NB_auc_roc = []

SVM_accuracy = []
SVM_precision = []
SVM_recall = []
SVM_f1_score = []
SVM_auc_roc = []

RAMF_accuracy = []
RAMF_precision = []
RAMF_recall = []
RAMF_f1_score = []
RAMF_auc_roc = []

xgBoost_accuracy = []
xgBoost_precision = []
xgBoost_recall = []
xgBoost_f1_score = []
xgBoost_auc_roc = []

def evaluate(y_test, pred):
    sum = 0
    for test,pr in zip(y_test, pred):
        sum = sum + test +  pr

    print('y_text + pred=',sum)
    acc = metrics.accuracy_score(y_test, pred)
    pre = metrics.precision_score(y_test,pred, average='micro')
    rec = metrics.recall_score(y_test,pred, average='micro')
    f1 = metrics.f1_score(y_test, pred,average='micro')
    # auc = metrics.roc_auc_score(y_test, pred,average=None)

    # acc = slim.metrics.streaming_accuracy(pred, y_test)
    # pre = slim.metrics.streaming_precision(pred, y_test)
    # rec = slim.metrics.streaming_recall(pred, y_test)
    # f1 = 1

    print(type(acc))
    print('\tAccuracy:', acc)
    print('\tPrecision:', pre)
    print('\tRecall:', rec)
    print('\tF1-score:', f1)
    # print('\tAUC ROC:', auc)
    # return acc, pre, rec, f1, auc
    return acc, pre, rec, f1

# Train the algorithm
# Naive Bayes
def NaiveBayesTrain(X_train, y_train, X_test):
    clf = GaussianNB()
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    # print('NaiveBayesTrain',pred)
    return pred

# SVM
def SVMTrain(X_train, y_train, X_test, c, g):
    clf = SVC(C=c, kernel='rbf', gamma=g)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    # print(pred)
    return pred

# Random Forest
def RandomForestTrain(X_train, y_train, X_test, cr, msl, ne):
    clf = RandomForestClassifier(n_estimators=ne, criterion=cr, min_samples_leaf= msl)
    clf.fit(X_train, y_train)
    pred = clf.predict(X_test)
    return pred

def generateDataSet(fsrc):
    #计算各个极性的数量
    zero_number = 0
    positive_number = 0
    negtive_number = 0
    #生成数据集
    x = []  #存储数据
    y = []  #存储极性
    for each in fsrc.readlines():
        each = each.strip().split('\t')
        # print(each[65:66])
        xr = []
        if each[65:66] == ['0']:
            # 记录 0 情感个数
            zero_number = zero_number + 1
            # continue
        elif each[65:66] == ['1']:
            # 记录正向情感个数
            positive_number = positive_number + 1
        elif each[65:66] == ['-1']:
            # 记录负向情感个数
            negtive_number = negtive_number + 1

        for each1 in each[1:65]:
            xr.append(float(each1))
        x.append(xr)
        for each2 in each[65:66]:
            y.append(int(each2))

    print('0情感个数：', zero_number)
    print('1情感个数：', positive_number)
    print('-1情感个数：', negtive_number)
    print('总标注个数（1151）情感个数：', zero_number + positive_number + negtive_number)
    return x, y

def machineLearningWays(method):
    #存放指标结果---画图
    accuracyList = []
    precisionList = []
    recallList = []
    fList = []
    auc_rocList = []
    #分割训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=15)
    crList = ["gini"]
    neList = [10, 15, 20]
    mslList = [2, 4, 6]
    # 设置x轴的数据
    xList = []
    for cr in crList:
        for msl in mslList:
            for ne in neList:
                crr = 'cr=%s' % cr  #该列表只有一个参数
                msll = 'msl=%s' % msl
                nee = 'ne=%s' % ne
                xv = msll + '\n' + nee
                xList.append(xv)
                pred = RandomForestTrain(x_train, y_train, x_test,cr, msl, ne)
                # acc, pre, rec, f1, auc = evaluate(y_test, pred)
                acc, pre, rec, f1 = evaluate(y_test, pred)
                accuracyList.append(acc)
                precisionList.append(pre)
                recallList.append(rec)
                fList.append(f1)
                # auc_rocList.append(auc)

    # return xList,accuracyList,precisionList, recallList, fList, auc_rocList
    return xList,accuracyList,precisionList, recallList, fList

# def figureImage(method, xList,accuracyList,precisionList, recallList, fList, auc_rocList):
def figureImage(method, xList,accuracyList,precisionList, recallList, fList):
    tag = ''
    if method == 'NaiveBayesTrain':
        tag = 'NB'
    elif method == 'SVMTrain':
        tag = 'SVM'
    elif method == 'RandomForestTrain':
        tag = 'RF'
    print('-------------------------------------------------')
    print(xList)
    print(precisionList)
    plt.figure()
    plt.plot(xList,accuracyList , label='%s'%tag +'_accuracy')
    plt.plot(xList, precisionList, label='%s'%tag +'_precision')
    plt.plot(xList, recallList, label='%s'%tag +'_recall')
    plt.plot(xList, fList, label='%s'%tag +'_F1')
    # plt.plot(xList, auc_rocList, label='%s'%tag +'_auc_roc')
    # plt.xlabel('percentage of testing set')
    plt.ylabel('value')
    plt.title(method)
    plt.legend(loc='upper left')
    plt.savefig('../eImage/RF_different_para/%s.png'%method)

# def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.Blues):
def plot_confusion_matrix(cm, labels, title='Confusion Matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()   #热度显示仪，旁边的颜色条
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    # plt.show()
    plt.savefig('../eImage/RF_different_para/confusion_matrix.png')


def confusionFunc(y_test, pred, labels):
    ind_array = np.arange(len(labels))
    x, y = np.meshgrid(ind_array, ind_array)
    cm = confusion_matrix(y_test, pred, labels=labels)

    cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    for x_val, y_val in zip(x.flatten(), y.flatten()):
        c = cm_normalized[y_val][x_val]
        if (c > 0.01):
            plt.text(x_val, y_val, "%0.2f" % (c,), color='red', fontsize=7, va='center', ha='center')

    tick_marks = np.array(range(len(labels))) + 0.5
    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.grid(True, which='minor', linestyle='-')
    plt.gcf().subplots_adjust(bottom=0.15)

    plot_confusion_matrix(cm_normalized, labels, title='Normalized confusion matrix')
    # show confusion matrix
    # plt.show()

if __name__ == "__main__":
    #数据集的类别，用于混淆矩阵的轴数据
    labels =[1, 0, -1]

    #读取词向量后的文件
    fname = r'../eFiles/cLabelToVector_word2vec.txt'
    fsrc = open(fname,'r',encoding='utf-8')
    x,y = generateDataSet(fsrc)
    #训练集的特征列，测试集的特征列，训练集的label列，测试集的label列
    y = column_or_1d(y, warn=True)

    #确定参数 test_size,random_state
    method = 'RandomForestTrain'
    # xList, accuracyList, precisionList, recallList, fList, auc_rocList = machineLearningWays(method)
    xList, accuracyList, precisionList, recallList, fList = machineLearningWays(method)
    # figureImage(method, xList,accuracyList,precisionList, recallList, fList,auc_rocList)
    figureImage(method, xList,accuracyList,precisionList, recallList, fList)


