import Data.stock as st
import pandas as pd
# 初始化变量
ticker="000001.XSHG"
# 调用一只股票的行情数据
data=st.get_single_stock_price(ticker=ticker,
                               timePeriod="daily",
                               stadate="2021-01-01",
                               endate="2021-02-01")
# 存入csv
st.export_data(data=data,filename=ticker,type="price")


#从csv中获取数据
# data=st.get_csv_data(ticker=ticker,type="price")
# print(data)

# 实时更新数据：假设每天更新日K数据 --> 存到csv文件里面 ---> data.to_csv(append)
'''
实时更新数据：假设每天更新日K数据 > 存到csv文件里面 > data.to_csv(append)
'''

# 1.获取所有股票代码
# stocks = st.get_stock_list()
#2.存储到csv文件中
# for ticker in stocks:
#     df = st.get_single_price(ticker, 'daily')
#     st.export_data(df)
# 1+2.
# st.init_db()

# 3.每日更新数据
st.update_daily_price(ticker,"price")

# for code in data:
#     st.update_daily_price(ticker, 'price')


# -*- coding: utf-8 -*-

# from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime
# import os.path
#
# data_root = st.data_root
# type = 'price'
#
#
# def job():
#     stock_list = st.get_stock_list()
#     for stock_code in stock_list:
#         file_root = data_root + type + '/' + stock_code + '.csv'
#         if not (os.path.isfile(file_root)):
#             df = st.get_single_stock_price(
#                 code=stock_code,
#                 time_freq='daily',
#                 start_date='2016-01-01',
#                 end_date=datetime.now().strftime("%Y-%m-%d"))
#             st.expot_stock_data(data=df, filename=stock_code, type=type)
#             print(datetime.now().strftime(
#                 "%Y-%m-%d %H:%M:%S") + '全量更新' + '========>' + stock_code)
#         else:
#             df = st.get_single_stock_price(
#                 code=stock_code,
#                 time_freq='daily',
#                 start_date=datetime.now().strftime("%Y-%m-%d"),
#                 end_date=datetime.now().strftime("%Y-%m-%d"))
#             st.expot_stock_data(data=df, filename=stock_code, type=type,
#                                 mode='a', header=False)
#             print(datetime.now().strftime(
#                 "%Y-%m-%d %H:%M:%S") + '增量更新' + '========>' + stock_code)


# job()

# 定义BlockingScheduler
# sched = BlockingScheduler()
# sched.add_job(job, 'cron', day_of_week='*', hour='15', minute='1')
# sched.start()