from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.svm import SVC
from sklearn.utils import column_or_1d
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import numpy as np

# 旧版
# from sklearn import cross_validation
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
    # acc = metrics.accuracy_score(y_test, pred)
    # pre = metrics.precision_score(y_test,pred, average=None)
    # rec = metrics.recall_score(y_test,pred, average=None)
    # f1 = metrics.f1_score(y_test, pred,average=None)
    # # auc = metrics.roc_auc_score(y_test, pred,average=None)

    acc = metrics.accuracy_score(y_test, pred)
    pre = metrics.precision_score(y_test,pred)
    rec = metrics.recall_score(y_test,pred)
    f1 = metrics.f1_score(y_test, pred)
    auc = metrics.roc_auc_score(y_test, pred)

    print('\tAccuracy:', acc)
    print('\tPrecision:', pre)
    print('\tRecall:', rec)
    print('\tF1-score:', f1)
    print('\tAUC ROC:', auc)
    return acc, pre, rec, f1, auc
    # return acc, pre, rec, f1

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
def RandomForestTrain(X_train, y_train, X_test):
    clf = RandomForestClassifier(n_estimators=10)
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

# def plot_confusion_matrix(cm, title='Confusion Matrix', cmap=plt.cm.Blues):
def plot_confusion_matrix(cm, labels,method, title='Confusion Matrix', cmap=plt.cm.Blues):
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()   #热度显示仪，旁边的颜色条
    xlocations = np.array(range(len(labels)))
    plt.xticks(xlocations, labels, rotation=90)
    plt.yticks(xlocations, labels)
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    # plt.show()
    plt.savefig('../eImage/d_RF_GridSearchCV_confusion_matrix_%s.png'%method)

def confusionFunc(y_test, pred, labels, method):
    ind_array = np.arange(len(labels))
    x, y = np.meshgrid(ind_array, ind_array)
    cm = confusion_matrix(y_test, pred, labels=labels)
    print(cm)

    #将每一个值除以其所在行的总和
    # cm_normalized = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    for x_val, y_val in zip(x.flatten(), y.flatten()):
        # c = cm_normalized[y_val][x_val]
        c = cm[y_val][x_val]
        if (c > 0.01):
            # plt.text(x_val, y_val, "%0.2f" % (c,), color='red', fontsize=10, va='center', ha='center')
            plt.text(x_val, y_val, "%d" % (c,), color='red', fontsize=10, va='center', ha='center')

    tick_marks = np.array(range(len(labels))) + 0.5
    plt.gca().set_xticks(tick_marks, minor=True)
    plt.gca().set_yticks(tick_marks, minor=True)
    plt.gca().xaxis.set_ticks_position('none')
    plt.gca().yaxis.set_ticks_position('none')
    plt.grid(True, which='minor', linestyle='-')
    plt.gcf().subplots_adjust(bottom=0.15)

    plot_confusion_matrix(cm, labels,method, title='RF_confusion matrix')
    # plot_confusion_matrix(cm_normalized, labels,method, title='Normalized confusion matrix')
    # plot_confusion_matrix(cm_normalized, labels,method, title='confusion matrix')


def machineLearningWays(labels, method):
    #分割训练集和测试集
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=15)
    #设置参数
    tunned_parameters = {
        "n_estimators": [10,50, 100],
        "criterion": ["gini", "entropy"],
        # "criterion": ["gini"],
        "min_samples_leaf": [1, 10, 20],
        "max_depth":[5,10,15]
    }

    # scores = ['precision_macro', 'recall_macro']  # 这是我们使用的评分策略,因为是多分类问题，所以最后的评分策略为precision_macro 和 recall_macro 见下面
    scores = ['recall_macro']  # 这是我们使用的评分策略,因为是多分类问题，所以最后的评分策略为precision_macro 和 recall_macro 见下面

    for score in scores:
        print("# Tuning hyper-parameters for %s" % score)
        clf = GridSearchCV(RandomForestClassifier(), tunned_parameters, cv=3, scoring=score)
        # clf = GridSearchCV(RandomForestClassifier(), tunned_parameters, cv=3, scoring='%s_macro' % score)
        clf.fit(x_train, y_train)
        # clf.fit(x, y)

        print("The best parameters are %s with a %s score of %f"
              % (clf.best_params_, score, clf.best_score_))
        print("Grid scores on x_train set:")
        means = clf.cv_results_['mean_test_score']
        stds = clf.cv_results_['std_test_score']
        # 这里输出了各种参数在使用交叉验证的时候得分的均值和方差
        for mean, std, params in zip(means, stds, clf.cv_results_['params']):
            print("%0.3f (+/-%0.03f) for %r"
                  % (mean, std * 2, params))

        print("Detailed classification report:")
        # print()
        # print("The model is trained on the full development set.")
        # print("The scores are computed on the full evaluation set.")
        # print()
        # 这里是使用训练出来的最好的参数进行预测
        y_true, y_pred = y_test, clf.predict(x_test)
        print(classification_report(y_true, y_pred))
        print()

        #生成混淆矩阵
        confusionFunc(y_true, y_pred, labels, method)


if __name__ == "__main__":
    # 数据集的类别，用于混淆矩阵的轴数据
    labels = [1, 0, -1]
    # labels = [-1, 0, 1]

    #读取词向量后的文件
    # fname = r'../eFiles/cLabelToVector_word2vec.txt'
    # fname = r'../eFiles/cLabelToVector_word2vec_Only_Word.txt'
    # fname = r'../eFiles/cLabelToVector_word2vec_use_sentiWord.txt'
    fname = r'../eFiles/cLabelToVector_word2vec_use_sentiWordAndDegWord.txt'
    fsrc = open(fname,'r',encoding='utf-8')
    x,y = generateDataSet(fsrc)
    #训练集的特征列，测试集的特征列，训练集的label列，测试集的label列
    y = column_or_1d(y, warn=True)

    method = 'RF'
    #确定参数 test_size,random_state
    machineLearningWays(labels, method)




