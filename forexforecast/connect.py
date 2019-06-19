#!/usr/bin/env python
# -*- coding:utf-8 -*-

import pandas as pd
import requests
import xlrd
import xlwt
import csv
import re
import os
import pymysql
import time
import urllib.request
import logging
import logging.config
from pyquery import PyQuery as pq
import io
import importlib, sys
importlib.reload(sys)





class write_read(object):
    # def __init__(self):
    #     self.conn

    def __init__(self):
        print("init")
        self.conn = pymysql.connect(user='root', passwd='123456', db='zhonghui', host='fx2.huilab.cn', port=3306,
                               charset='utf8')

    def sql_conn(self):
        print("conn again")
        self.conn = pymysql.connect(user='root', passwd='123456', db='zhonghui', host='fx2.huilab.cn', port=3306,
                               charset='utf8')

    def sql_close(self):
        print("sql_close")
        self.conn.close()

    def sql_exe(self, text):
        cur = self.conn.cursor()
        try:
            cur.execute(text)
        except Exception as e:
            print(e)
            return
        res = cur.fetchall()
        cur.close()
        self.conn.commit()
        return res


    def wt_title(self, path, title):
        # 写入列名
        # title需是列表
        csvFile3 = open(path, 'a+')
        writer2 = csv.writer(csvFile3)
        writer2.writerow(title)
        csvFile3.close()

    def read_xlsx(p, sheet_name, col):
        # 读表格
        file = xlrd.open_workbook(p)
        table = file.sheet_by_name(sheet_name)  # 通过名称获取
        data = table.col_values(col)
        # nrows = table.nrows #行数
        return data

    def write_excel(self,dict):
        d = [0, 0, 0, 0, 0, -1]
        # T = (time.strftime('%Y%m%d', time.localtime(time.time())))
        # csvFile = open('1to2' + T + '.csv', 'ab')
        csvFile = open('1to2' + '.csv', 'a')
        writer2 = csv.writer(csvFile)
        for key in dict:
            if key == u'ID':
                d[0] = dict[u'ID']
            if key == u'主办':
                d[1] = dict[u'主办']
            if key == u'父亲链接':
                d[2] = dict[u'父亲链接']
            if key == u'链接':
                d[3] = dict[u'链接']
            if key == u'完整链接':
                d[4] = dict[u'完整链接']
            if key == u'敏感度':
                d[5] = dict[u'敏感度']
        writer2.writerow(d)
        csvFile.close()



class log(object):
    def setLogger(log_name):
        # 创建一个logger,可以考虑如何将它封装
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.ERROR)

        # 创建一个handler，用于写入日志文件
        T = (time.strftime('%Y%m%d', time.localtime(time.time())))
        fh = logging.FileHandler(os.path.join(os.getcwd(), log_name + T + '.txt'))
        fh.setLevel(logging.ERROR)

        # 再创建一个handler，用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)

        # 定义handler的输出格式
        formatter = logging.Formatter('%(asctime)s - %(module)s.%(funcName)s.%(lineno)d - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 给logger添加handler
        logger.addHandler(fh)
        logger.addHandler(ch)

        # 记录一条日志
        logger.info('hello world, i\'m log helper in python')
        return logger