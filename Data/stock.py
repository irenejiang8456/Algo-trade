
from jqdatasdk import *
import time
import pandas as pd
import datetime
import os

auth('17621171968','171968') #账号是申请时所填写的手机号；密码为聚宽官网登录密码

# 全局变量
data_root="C:/Users/17147/Documents/myHW/Python/DataQuant/Data/"

# 设置行列不忽略
pd.set_option("display.max_rows",100000)
pd.set_option("display.max_columns",1000)

def init_db():
    """
    初始化股票数据库
    :return:
    """
    # 1.获取所有股票代码
    stocks = get_stock_list()
    # 2.存储到csv文件中
    for ticker in stocks:
        df = get_single_stock_price(ticker, 'daily')
        export_data(df,ticker,"price")
        print(ticker)
        print(df.head())
        # or update_daily_price(ticker,"price")


def get_stock_list():
    """
    获取所有A股股票列表;
    上海证券交易所:	.XSHG,
    深圳证券交易所:	.XSHE
    :return: stock_list
    """
    stocks_list = list(get_all_securities(['stock']).index)
    return stocks_list

def get_index_list(index_symbol="000300.XSHG"):
    """
    获取指数成分股，指数代码查询网址：https://www.joinquant.com/help/api/help#index:%E6%B2%AA%E6%B7%B1%E6%8C%87%E6%95%B0%E5%88%97%E8%A1%A8
    :param index_symbol: 指数代码, 默认沪深300
    :return: list，成分股代码
    """
    stocks=get_index_stocks(index_symbol)
    return stocks

def get_single_stock_price(ticker, timePeriod, stadate=None,endate=None):
    """
    获取单个股票行情数据
    :param ticker:
    :param timePeriod:
    :param stadate:
    :param endate:
    :return:
    """
    # 如果 stardate=None, 默认为上市日期开始
    if stadate is None:
        stadate = get_security_info(ticker).start_date
    if endate is None:
        endate=datetime.datetime.today()
    # 获取行情数据
    data = get_price(ticker, start_date=stadate,end_date=endate,
                  frequency=timePeriod,panel=False)
    return data

def export_data(data,filename,type,mode=None):
    """
    导出股票相关数据
    :param data:
    :param filename:
    :param type: 股票数据类型，可以是：price,finance
    :param mode:
    :return:
    """
    file_root=data_root + type+ "/"+filename+".csv"
    data.index.names=["date"]

    if mode == 'a':  # 判断file存在---> 如果存在：append； 不存在：保持
        data.to_csv(file_root, mode=mode, header=False)
        # 删除重复值
        data = pd.read_csv(file_root)  # 读取数据
        data = data.drop_duplicates(subset=['date'])  # 以日期列为准
        data.to_csv(file_root, index=False)  # 重新写入
    else:
        data.to_csv(file_root)
    print('已经成功存储至：', file_root)



# def get_csv_data(ticker,type):
#     file_root = data_root + type + "/" + ticker + ".csv"
#     return pd.read_csv(file_root)

def get_csv_price(ticker,start_date,end_date,columns=None):
    """
    获取本地数据，且顺便完成数据更新工作
    :param ticker: str, stock ticker
    :param start_date: str,
    :param end_date: str
    :param columns:
    :return: dataframe
    """
    # 读取数据库对应的股票csv文件
    file_root = data_root +"price/" + ticker + ".csv"
    # 使用update直接更新
    update_daily_price(ticker)
    # 读取数据
    file_root = data_root + 'price/' + ticker + '.csv'
    if columns is None:
        data = pd.read_csv(file_root, index_col='date')
    else:
        data = pd.read_csv(file_root, usecols=columns, index_col='date')
    # print(data)
    # 根据日期筛选股票数据
    return data[(data.index >= start_date) & (data.index <= end_date)]


def convert_price_period(data, time_freq):
    """
    转换股票行情周期:开盘价（周期第一天），收盘价（周期最后一天），最高价（周期），最低价（周期内）
    :param data:
    :param time_freq:
    :return:
    """
    df_converted=pd.DataFrame()
    df_converted["open"]=data["open"].resample(time_freq).first()
    df_converted["close"]=data["close"].resample(time_freq).last()
    df_converted["high"]=data["high"].resample(time_freq).max()
    df_converted["low"]=data["low"].resample(time_freq).min()

    return df_converted

def get_single_financeIndicator(ticker,date,statDate):
    """
    获取单个股票财务指标
    :param ticker:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(indicator).filter(indicator.code==ticker), date=date, statDate=statDate)  # 获取财务指标数据
    return data

def get_single_valuation(ticker,date,statDate):
    """
    获取单个股票估值指标
    :param ticker:
    :param date:
    :param statDate:
    :return:
    """
    data = get_fundamentals(query(valuation).filter(valuation.code == ticker),
                            date=date, statDate=statDate)  # 获取财务指标数据
    return data

def calculate_change_pct(data):
    """
    涨跌幅=（当期收盘价-当期收盘价）/前期收盘价
    :param data: dataframe,带有收盘价
    :return: dataframe. 带有涨跌幅
    """
    data["close_pct"]=(data["close"]-data["close"].shift(1))/\
                      data["close"].shift(1)
    return data

def update_daily_price(ticker,type="price"):
    # 3.1 是否存在文件：不存在-->重新获取, 存在--->3.2
    file_root = data_root + type + "/" + ticker + ".csv"
    if os.path.exists(file_root):
        # 3.2获取增量数据（code，startsdate=对应股票csv中最新日期，enddate=今天）
        startdate = pd.read_csv(file_root, usecols=['date'])['date'].iloc[-1]
        df = get_single_stock_price(ticker, 'daily', startdate,
                              datetime.datetime.today())
        # 3.3追加到已有文件中
        export_data(df, ticker, 'price', 'a')
    else:
        # 重新获取该股票行情数据
        df=get_single_stock_price(ticker,"daily")
        export_data(df,ticker,"price")
        print("股票数据已经更新成功：", ticker)


if __name__ == '__main__':

    # data=get_fundamentals(query(indicator),statDate="2020") # 获取财务指标数据
    # print(data)

    # 5.3获取沪深300指数成分股代码
    # print (get_index_list())
    print(len(get_index_list()))



