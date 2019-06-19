#!/usr/bin/python
# -*- coding: utf-8 -*-
from util import CommonUtil
import warnings
warnings.filterwarnings(action='ignore', category=UserWarning, module='gensim')
import connect
import jieba
import numpy as np

# RAW_NEWS_PATH = 'news_20160630_20171229_demo.xlsx'
# VEC_NEWS_PATH = 'seg_vec.csv'
# # 新闻分词后保存路径
# SEGMENTED_NEWS_PATH = './segment_news.csv'
# # 新闻分词并且量化后保存路径
# SEGMENTED_NEWS_VEC_PATH = './seg_vec.csv'
# CSV_FILE_SUFFIX = '.csv'
# # 新闻列表：[1, 2018/6/17  20:17:46, 伊朗：三个OPEC成员国将投票反对增产。]
# newsList = list()
# # 新闻分词后列表：[1, 2018/6/17  20:17:46, 伊朗, ：, 三个, OPEC, 成员国, 将, 投票, 反对, 增产, 。]
# newsSegmentationList = list()
# # 停用词列表
# stopwords = []
# # 货币对精度
# CURRENCY_PAIR_PRECISION = 4

# seg_news_vec = []
#

# PROCESSED_NEWS_PATH = './PROCESSED_SENTI'

def dict_from_SQL_to_sentiment(tuple, st, et):  #  list[0] is time list[1] is dict
    #keyword_info = CommonUtil.read_csv('./doc/keyword_info.csv')
    db = connect.write_read()
    keyword_info = db.sql_exe('select * from keyword_info')
    keyword_info = list(keyword_info)
    list_SQL = list(tuple)
    list_news_vec = []
    temp = []
    for each_data in list_SQL:
        T = each_data[0]
        dict = eval(each_data[1])
        for each_keyword in dict.keys():
            for i in range(0,len(keyword_info)):
                # print("each_keyword:", each_keyword, "keyword_info[i]:", keyword_info[i])
                if each_keyword == keyword_info[i][0]:
                    temp.append(T)
                    temp.append(each_keyword)
                    temp.append(dict[each_keyword])
                    list_news_vec.append(temp)
                    temp = []
                    break

    # print("list_news_vec:", list_news_vec)
    VEC_news = process_original_news_vec(list_news_vec, st,et)
    return VEC_news

# 对原始新闻数据进行预处理，采样（请注意设置采样频率）
def process_original_news_vec(seg_news_vec, st, et):
    MARKET_OPEN_TIME = '09:30:00'
    MARKET_CLOSE_TIME = '23:30:00'
    NEWS_SAMPLE_MINUTE = 60
    processedNewsList = []
    # seg_news_vec = CommonUtil.read_csv('./doc/1209/news_sentivalue.csv')
    NEWS_START_TIME = st
    NEWS_END_TIME = et
    sample_datetime = None
    sample_news_list = []
    # 对每一个原始价格
    for original_vec in seg_news_vec:
        news_datetime = CommonUtil.get_datetime_from_string_(original_vec[0])
        # print(news_datetime)
        news_vec = original_vec[1::]
        if sample_datetime is None:
            sample_datetime = CommonUtil.get_datetime_from_string_(NEWS_START_TIME)
        time_interval = CommonUtil.get_interval_seconds(news_datetime, sample_datetime)
        # 价格时间在采集区间外(价格对应时间远早于采集时刻点)，取下一个价格
        if time_interval < -NEWS_SAMPLE_MINUTE * 60 / 2:
            continue
        # 如果当前时间超过采样区间（晚于），先计算上一个采样时间的平均价格，再寻找下一个采样点
        while time_interval >= NEWS_SAMPLE_MINUTE * 60 / 2:
            # 如果当前采样点有价格
            if len(sample_news_list) > 0:
                vec_sum = {}
                for news_item in sample_news_list:
                    # print("news_item:", news_item, "vec_sum:", vec_sum)
                    if news_item[0] in vec_sum.keys():
                        vec_sum[news_item[0]] += float(news_item[1])
                    else:
                        vec_sum[news_item[0]] = float(news_item[1])
                news_sentiment_list = dict_to_vec(vec_sum)
                sample_datetime_str = CommonUtil.get_string_from_datetime(sample_datetime)
                average_news_item = [sample_datetime_str] + news_sentiment_list
                # 将采样时间及对应的计算后的价格加入列表
                processedNewsList.append(average_news_item)
                # 重置采样点价格列表
                sample_news_list = []
            # 计算下一个采样点
            sample_datetime = CommonUtil.get_next_sample_time(sample_datetime, NEWS_SAMPLE_MINUTE,
                                                               MARKET_OPEN_TIME, MARKET_CLOSE_TIME)
            time_interval = CommonUtil.get_interval_seconds(news_datetime, sample_datetime)
        # 价格时间在采集区间外
        if sample_datetime > CommonUtil.get_datetime_from_string_(NEWS_END_TIME):
            break
        # 属于当前采样点，加入当前采样点价格列表，前闭后开[,)
        sample_news_list.append(news_vec)
    # 处理最后一个采集时刻的价格列表
    # 如果当前采样点有价格
    if len(sample_news_list) > 0:
        vec_sum = {}
        for news_item in sample_news_list:
            if news_item[0] in vec_sum.keys():
                vec_sum[news_item[0]] += float(news_item[1])
            else:
                vec_sum[news_item[0]] = float(news_item[1])
        news_sentiment_list = dict_to_vec(vec_sum)
        sample_datetime_str = CommonUtil.get_string_from_datetime(sample_datetime)
        average_news_item = [sample_datetime_str] + news_sentiment_list
        # 将采样时间及对应的计算后的价格加入列表
        processedNewsList.append(average_news_item)
    # file_path = PROCESSED_NEWS_PATH + '_' + str(NEWS_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    # CommonUtil.write_csv(file_path, processedNewsList)
    # 89个维度对应数据
    # print("processedNewsList:", processedNewsList)
    list_out = dimension89(processedNewsList)
    return list_out

def dict_to_vec(d):
    temp = []
    list_news = []
    for (key,value) in d.items():
        temp.append(key)
        temp.append(value)
        list_news.append(temp)
        temp = []
    return list_news

def dimension89(list_in):
    # print("list in :", list_in[0:100])
    #news_sentiment = CommonUtil.read_csv('./doc/keyword_info.csv')
    db = connect.write_read()
    news_sentiment = db.sql_exe('select * from keyword_info')
    news_sentiment = list(news_sentiment)
    list_1 = [0] * len(news_sentiment)
    temp = []
    list_out = []
    for each1 in list_in:
        t = each1[0]
        senti = each1[1::]
        for each2 in senti:
            for i in range(0,len(news_sentiment)):
                # print("news_sentiment[i]:",news_sentiment[i][0],"each2[0]:",each2[0])
                # print("type news_sentiment[i]:", type(news_sentiment[i][0]), "type each2[0]:", type(each2[0]))
                if news_sentiment[i][0] == each2[0]:
                    # print("true 1")
                    list_1[i] = each2[1]
        temp.append(t)
        for each3 in list_1:
            temp.append(each3)
        list_out.append(temp)
        temp = []
        list_1 = [0] * len(news_sentiment)
    # print("list_out:", list_out)
    # file_path = './doc/1209/dimension89' + '_' + str(NEWS_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    # CommonUtil.write_csv(file_path, list_out)
    return list_out





def link_vec(NEWS_VEC, PRICE_VEC, p):
    ALL_VEC = []
    # print(NEWS_VEC[0][1])
    # print(PRICE_VEC[0][0])
    for each_price_vec in PRICE_VEC:
        flag = 0
        for each_news_vec in NEWS_VEC:
            # print("each_news_vec[0] , each_price_vec[0]", each_news_vec[0] , each_price_vec[0])
            if each_news_vec[0] == each_price_vec[0]:
                print("matched!")
                vec_of_all = each_news_vec[::]
                vec_of_all.append(each_price_vec[1])
                vec_of_all.append(each_price_vec[2])
                ALL_VEC.append(vec_of_all)
                flag = 1
                break
        if flag == 0:
            print("not matched! Created!")
            list_temp = []
            list_temp.append(each_price_vec[0])
            list_temp += [0] * (len(each_news_vec)-1)
            list_temp.append(each_price_vec[1])
            list_temp.append(each_price_vec[2])
            ALL_VEC.append(list_temp)

    CommonUtil.write_csv(p, ALL_VEC)



if __name__ == "__main__":
    # news_sentiment = []
    # f = open('./doc/qtm_data/result_four_tuple_3_RF_W.txt', 'r', encoding='utf-8')
    # for line in f:
    #     L = line.split('\t')
    #     L[-1] = L[-1].strip('\n')
    #     temp = L[0:2] + L[3:] # 过滤掉极性
    #     news_sentiment.append(temp)
    #     # print(type(L))
    # CommonUtil.write_csv('./doc/1205/news_sentivalue.csv', news_sentiment)

    process_original_news_vec()

    # SENTIMENT_VEC = CommonUtil.read_csv('./doc/1209/dimension89' + '_' + str(NEWS_SAMPLE_MINUTE) + CSV_FILE_SUFFIX)
    # PRICE_VEC = CommonUtil.read_csv('./doc/1209/DEAL_PRICE' + '_' + str(NEWS_SAMPLE_MINUTE) + CSV_FILE_SUFFIX)   #  吧时间列拉大再保存一次
    # PATH = './doc/1209/VEC_VALUE' + '_' + str(NEWS_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    # link_vec(SENTIMENT_VEC, PRICE_VEC, PATH)


