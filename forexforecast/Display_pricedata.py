
from util import CommonUtil

ORIGINAL_PRICE_PATH = 'ORIGINAL_PRICE.csv'
# 预处理后价格文件路径
PROCESSED_PRICE_PATH = './doc/1209/PROCESSED_PRICE'



# 对原始价格数据进行预处理，采样（请注意设置采样频率）
def process_original_price(originalPriceList, PRICE_START_TIME, PRICE_END_TIME):
    # start_time and end_time 要注意时间区域（ORIGINAL_PRICE表格中的起始结束时间）
    # PRICE_START_TIME = originalPriceList[0][0]  #  '2016/06/30  09:30:00'
    # PRICE_END_TIME = originalPriceList[-1][0]  #  '2017/12/29  23:27:00'
    PRICE_SAMPLE_MINUTE = 60
    CURRENCY_PAIR_PRECISION = 4
    # 开市时间
    MARKET_OPEN_TIME = '09:30:00'
    # 闭市时间
    MARKET_CLOSE_TIME = '23:30:00'
    # 预处理后价格列表：[2018/6/30 15:00:00, 6.6433]
    processedPriceList = list()
    CSV_FILE_SUFFIX = '.csv'


    # logger.info("In Process Original Price...")
    # global originalPriceList
    # originalPriceList = CommonUtil.read_csv(ORIGINAL_PRICE_PATH)
    sample_datetime = None
    sample_price_list = list()
    # 对每一个原始价格
    for original_price in originalPriceList:
        #logger.debug('price time: ' + original_price[0])
        price_datetime = CommonUtil.get_datetime_from_string_(original_price[0])
        # print(original_price[1])
        if original_price[1] == '':
            print('null')
        price_value = float(original_price[1])
        if sample_datetime is None:
            sample_datetime = CommonUtil.get_datetime_from_string_(PRICE_START_TIME)
        time_interval = CommonUtil.get_interval_seconds(price_datetime, sample_datetime)
        # 价格时间在采集区间外(价格对应时间远早于采集时刻点)，取下一个价格
        if time_interval < -PRICE_SAMPLE_MINUTE * 60 / 2:
            continue
        # 如果当前时间超过采样区间（晚于），先计算上一个采样时间的平均价格，再寻找下一个采样点
        while time_interval >= PRICE_SAMPLE_MINUTE * 60 / 2:
            # 如果当前采样点有价格
            if len(sample_price_list) > 0:
                price_sum = 0
                for price_item in sample_price_list:
                    price_sum += price_item
                average_price = round(price_sum / len(sample_price_list), CURRENCY_PAIR_PRECISION + 2)
                sample_datetime_str = CommonUtil.get_string_from_datetime(sample_datetime)
                average_price_item = [sample_datetime_str, average_price]
                # 将采样时间及对应的计算后的价格加入列表
                processedPriceList.append(average_price_item)
                # 重置采样点价格列表
                sample_price_list = list()
            # 计算下一个采样点
            sample_datetime = CommonUtil.get_next_sample_time(sample_datetime, PRICE_SAMPLE_MINUTE,
                                                               MARKET_OPEN_TIME, MARKET_CLOSE_TIME)
            time_interval = CommonUtil.get_interval_seconds(price_datetime, sample_datetime)
        #logger.debug('sample datetime:' + CommonUtil.get_string_from_datetime(sample_datetime))
        # 价格时间在采集区间外
        if sample_datetime > CommonUtil.get_datetime_from_string_(PRICE_END_TIME):
            break
        # 属于当前采样点，加入当前采样点价格列表，前闭后开[,)
        sample_price_list.append(price_value)
    # 处理最后一个采集时刻的价格列表
    # 如果当前采样点有价格
    if len(sample_price_list) > 0:
        price_sum = 0
        for price_item in sample_price_list:
            price_sum += price_item
        average_price = round(price_sum / len(sample_price_list), CURRENCY_PAIR_PRECISION + 2)
        sample_datetime_str = CommonUtil.get_string_from_datetime(sample_datetime)
        average_price_item = [sample_datetime_str, average_price]
        # 将采样时间及对应的计算后的价格加入列表
        processedPriceList.append(average_price_item)
    return processedPriceList
    # file_path = PROCESSED_PRICE_PATH + '_' + str(PRICE_SAMPLE_MINUTE) + CSV_FILE_SUFFIX
    # CommonUtil.write_csv(file_path, processedPriceList)
    #logger.info("Process Original Price Done!")
    
    
if __name__ == "__main__":
    process_original_price()