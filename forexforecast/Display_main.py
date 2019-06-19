#!/usr/bin/env python
# -*- coding:utf-8 -*-
from util import CommonUtil
import numpy as np
import re
import matplotlib.pyplot as plt
from sklearn import datasets,preprocessing
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import connect
import Display_pricedata
import Display_news_senti
import joblib
import warnings
import time
import datetime
import json
warnings.filterwarnings('ignore')

def stopwd_reduction(infilepath, outfilepath):
    infile = open(infilepath, 'r')
    outfile = open(outfilepath, 'w')
    stopwordslist = []
    for str in infile.read().split('\n'):
        if str not in stopwordslist:
            stopwordslist.append(str)
            outfile.write(str + '\n')

def link_vec(NEWS_VEC, PRICE_VEC):
    ALL_VEC = []
    # print(NEWS_VEC[0][1])
    # print(PRICE_VEC[0][0])
    for each_price_vec in PRICE_VEC:
        flag = 0
        for each_news_vec in NEWS_VEC:
            # print("each_news_vec[0] , each_price_vec[0]", each_news_vec[0] , each_price_vec[0])
            if each_news_vec[0] == each_price_vec[0]:
                # print("matched!")
                vec_of_all = each_news_vec[::]
                vec_of_all.append(each_price_vec[1])
                # vec_of_all.append(each_price_vec[2])
                ALL_VEC.append(vec_of_all)
                flag = 1
                break
        if flag == 0:
            # print("not matched! Created!")
            list_temp = []
            list_temp.append(each_price_vec[0])
            list_temp += [0] * (len(each_news_vec)-1)
            list_temp.append(each_price_vec[1])
            # list_temp.append(each_price_vec[2])
            ALL_VEC.append(list_temp)
    # print("ALL_VEC:", ALL_VEC)
    return ALL_VEC
    # CommonUtil.write_csv(p, ALL_VEC)

def VECtoTrainTest(VEC,dim,slide_win):
    test = VEC

    x_test_item = []
    x_test = []
    # display_test = data[test_start + slide_win + test_win - 1:test_start + test_num + slide_win + test_win - 1]
    # display_predict = data[test_start + slide_win + test_win:test_start + test_num + slide_win + test_win]


    for k2 in range(1, len(test)):
        n3 = np.array(test[k2][1:dim - 1])
        n4 = np.array(test[k2 - 1][1:dim - 1])
        n3 = n3.astype('float64')
        n4 = n4.astype('float64')
        news_rate = n3 - n4
        for each2 in news_rate:
            x_test_item.append(each2)
        x_test_item.append(float(test[k2][dim - 1]))
    x_test.append(x_test_item)
    print("x_test from VECtoTrainTest:", x_test)


    x_test = np.array(x_test)
    x_test = x_test.astype('float64')
    # global scale_x, scale_y
    # x_test = scale_x.fit_transform(x_test)
    return x_test

def model_fit(dim, slide_win, x_train, y_train):
    # 3 ceng
    global scale_x, scale_y, model
    print('-----model fit-----------')
    model = Sequential()
    model.add(Dense(7, activation='sigmoid', input_dim=(dim - 1) * (slide_win - 1)))
    model.add(Dense(7, activation='sigmoid'))
    model.add(Dense(1, activation='linear'))
    model.compile(optimizer='adam', loss='mse')

    model.fit(x_train, y_train, epochs=100, batch_size=200, verbose=0)
    # predict_train = scale_y.inverse_transform(model.predict(x_train, batch_size=200))
    # actual_train = scale_y.inverse_transform(y_train)
    # train_acc = mean_squared_error(actual_train, predict_train)
    print('-----fit  over-----------')

def model_predict(x_test):
    global scale_x, scale_y, model
    predict_test = scale_y.inverse_transform(model.predict(x_test, batch_size=200))
    # actual_test = scale_y.inverse_transform(y_test)
    # test_acc = mean_squared_error(actual_test, predict_test)
    # test_mae = mean_absolute_error(actual_test, predict_test)
    # print('网络层数:{} 优化算法:adam'.format(len(model.layers)))
    # print('MAE  = ', round(test_mae, 6))
    return predict_test
    
if __name__ == "__main__":
    global scale_x, scale_y, model
    scale_x = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scale_y = preprocessing.MinMaxScaler(feature_range=(0, 1))
    model = None

    Collect_intervel = 60  #  60 second
    LastID = 1

    dim = 43  # 一共43维(无交易量)，除去时间42维，除去标签值41维
    slide_win = 5  #  输入向量的窗口值

    #  connect to SQL
    flag = 1
    while (flag):
        try:
            data_os = connect.write_read()
            flag = 0
        except Exception as e:
            print(e)

    #  get the row number
    res = data_os.sql_exe('select count(*) from raw_price')
    row_num_rate = res[0][0] - 1  # the last data of rate
    res = data_os.sql_exe('select count(*) from raw_news')
    row_num_news = res[0][0] - 1  # the last data of news
    # print(row_num[0][0], type(row_num[0][0]))
    print("row_num_rate:", row_num_rate, "row_num_news:", row_num_news)

    if type(row_num_rate) == int:
        lastData_rate = data_os.sql_exe('select id, status from raw_price limit ' + str(row_num_rate) + ',1')
        NowID_rate = lastData_rate[0][0]
        status_rate = lastData_rate[0][1]
        lastData_news = data_os.sql_exe('select id, sastatus from raw_news limit ' + str(row_num_news) + ',1')
        NowID_news = lastData_news[0][0]
        # NowStatus_news = lastData_news[0][1]
        num_extract_rate = 3 * 12 * 60 * 1.5
        num_extract_news = 3 * 12 * 12 * 1.5
        if NowID_rate < num_extract_rate:  #  数据不够时
            num_extract_rate = NowID_rate - 1
        if NowID_news < num_extract_news:
            num_extract_news = NowID_news - 1
        print("num_extract_rate:", num_extract_rate, "num_extract_news:", num_extract_news)
        print("NowID:", NowID_rate, NowID_news, "status:", status_rate)
        if status_rate == 0:   #  or NowStatus_news == 1:
            raw_rate = data_os.sql_exe('select time, mid from raw_price where id  BETWEEN ' + str(NowID_rate - num_extract_rate) + ' AND ' + str(NowID_rate))
            raw_news = data_os.sql_exe('select time,satuples from raw_news where satuples IS NOT NULL AND id  BETWEEN ' + str(NowID_news - num_extract_news) + ' AND ' + str(NowID_news))
            # print(data_os.sql_exe('select time, mid from raw_price where id  BETWEEN 15 AND 20'))  #  type tuple
            # print("raw_rate:", raw_rate)
            # for each in raw_rate:
            #     print("each:",each[0],each[1])
            #     if each[1] == '':
            #         print("each1 = null")
            start_time_news = raw_news[0][0].split(' ')[0] + '  09:30:00'
            end_time_news = raw_news[-1][0].split(' ')[0] + '  23:30:00'
            #  raw_news convert to sentiment vector
            newsVEC = Display_news_senti.dict_from_SQL_to_sentiment(raw_news, start_time_news,end_time_news)

            start_time_rate = raw_rate[0][0].split(' ')[0] + '  09:30:00'
            end_time_rate = raw_rate[-1][0].split(' ')[0] + '  23:30:00'
            # print("start end time:", start_time_rate,end_time_rate,start_time_news,end_time_news)
            priceVEC = Display_pricedata.process_original_price(list(raw_rate),start_time_rate,end_time_rate)

            # print("newsVEC:", newsVEC)
            # print("priceVEC:", priceVEC)
            VEC = link_vec(newsVEC, priceVEC)
            T0 = time.time()
            if len(VEC) > 5:
                Test = VEC[-5:]  #  take the last 5th data
                #  process the vec to train and test
                x_test = VECtoTrainTest(Test, dim, slide_win)
                # print("x_test from main1:", x_test)
            else:
                print("data is not enough!!!")

            #  detect the model exist or not
            try:
                model = load_model('/root/wjx/dnn_cloud.model')
                # model.load_weights('model_weight.h5')
            except:
                if model == None:
                    print("model is none!!!")
                    model = load_model('dnn.model')
                else:
                    T1 = time.time()
                    if (T1 - T0 > 3600):  #  3600sec = 1 hour
                        T0 = T1
                        model = load_model('dnn.model')

            predict_test = model.predict(x_test, batch_size=200)
            # predict_test = model_predict(x_test)
            print("predict_result:", predict_test)

            rate_now = VEC[-1][-1]
            rate_next = predict_test[0][0]
            time_now = VEC[-1][0]
            if re.match('(.+) 23:(.+)', time_now):
                time_now = CommonUtil.get_datetime_from_string(time_now)
                time_next = time_now + datetime.timedelta(hours=10)
            else:
                time_now = CommonUtil.get_datetime_from_string(time_now)
                time_next = time_now + datetime.timedelta(hours=1)

            # Display_predict = []
            # Display_predict.append(time_now)
            # Display_predict.append(rate_now)
            # Display_predict.append(time_next)
            # Display_predict.append(rate_next)
            # print("Display_predict:", Display_predict)

            #  updata the data
            #  展示预测结果  判断是否重复  更新而不是单纯写入
            res = data_os.sql_exe('select count(*) from RMB_rate_predict')
            print("res:", res)
            if res[0][0] == 0:
                print("last time is none!!!")
                sql_insert = "insert into RMB_rate_predict (time_test,rate_test,time_predict,rate_predict,status) values('%s','%s','%s','%s','%d')" % \
                             (time_now, rate_now, time_next, rate_next, 0)
                data_os.sql_exe(sql_insert)
            else:
                row_num_pre = res[0][0] - 1  # the last data of predict
                lastData_pre = data_os.sql_exe('select time_test from RMB_rate_predict limit ' + str(row_num_pre) + ',1')
                lastTime = lastData_pre[0][0]
                lastTime = datetime.datetime.strptime(lastTime, "%Y-%m-%d %H:%M:%S")
                lastTime = time.mktime(lastTime.timetuple())
                insertTime = time.mktime(time_now.timetuple())
                print("lastTime:", lastTime, "insertTime:", insertTime)
                if insertTime > lastTime:
                    print("insert!")
                    sql_insert = "insert into RMB_rate_predict (time_test,rate_test,time_predict,rate_predict,status) values('%s','%s','%s','%s','%d')" % \
                                 (time_now, rate_now, time_next, rate_next,0)
                    data_os.sql_exe(sql_insert)
                else:
                    print("update!")
                    # print(rate_now, rate_next, time_now)
                    sql_update = "UPDATE RMB_rate_predict SET rate_test = " + str(rate_now) + ", rate_predict = " + str(rate_next) + " where time_test = '" + str(time_now) + "'"
                    print(sql_update)
                    data_os.sql_exe(sql_update)

            #  更新一些表的status
            data_os.sql_exe('UPDATE raw_price SET status = 1 where id  BETWEEN ' + str(
                NowID_rate - num_extract_rate) + ' AND ' + str(NowID_rate))
            data_os.sql_exe(
                'UPDATE raw_news SET pre_status = 1 where satuples IS NOT NULL AND id  BETWEEN ' + str(
                    NowID_news - num_extract_news) + ' AND ' + str(
                    NowID_news))
            pre_data = data_os.sql_exe('select * from RMB_rate_predict')
            print("pre_data:", pre_data)

    #  get the row number failed
    else:
        print("no data")

    # lastID = data_os.sql_exe('select * from RMB_rate_collect limit ' + str(row_num-19) + ',20')  # take the last 20 data
    # print(lastID)
