from jqdatasdk import *
import time
import pandas as pd
import datetime
auth('17621171968','171968') #账号是申请时所填写的手机号；密码为聚宽官网登录密码

# 设置行列不忽略
pd.set_option("display.max_rows",100000)
pd.set_option("display.max_columns",1000)

# 上海证券交易所	.XSHG	600519.XSHG	贵州茅台
# 深圳证券交易所	.XSHE	000001.XSHE	平安银行

# 获取所有A股行情数据
# stocks = list(get_all_securities(['stock']).index)
#
# 获取股票行情数据
# for stock_ticker in stocks:
#     print("getting the stock data, stock ticker: ", stock_ticker)
#     df = get_price(stock_ticker, end_date='2021-12-27',count=10, frequency=
#     'daily',panel=False)
#     print(df)
#     time.sleep(3)

""" resample函数的使用 """

# 转换周期：日K转换为周K
# 获取日K
# df = get_price('000001.XSHG', end_date='2021-02-22',count=20, frequency=
#     'daily',panel=False)
# df["weekday"]=df.index.weekday
# print(df)
# # 获取周K （当周的）：开盘价（当周第一天），收盘价（当周最后一天），最高价（当周），最低价（当周）
# df_week=pd.DataFrame()
# df_week["open"]=df["open"].resample("W").first()
# df_week["close"]=df["close"].resample("W").last()
# df_week["high"]=df["high"].resample("W").max()
# df_week["low"]=df["low"].resample("W").min()

# # 汇总统计：统计一下月成交量，成交额（sum)
# df_week["volume(sum)"]=df["volume"].resample("W").sum()
# df_week["money(sum)"]=df["money"].resample("W").sum()

# print(df_week)

"""获取股票财务指标"""
df=get_fundamentals(query(indicator),statDate="2020") #获取财务指标数据

# df.to_csv("C:/Users/17147/Documents/myHW/Python/DataQuant/Data/finance_indicator/finance2020.csv") #存储数据

#基于盈利指标选股： eps, operating_profit, roe, inc_net_profit_year_on_year
df=df[(df["eps"]>0) & (df["operating_profit"]>927796754.1) &
      (df["roe"]>11) & (df["inc_net_profit_year_on_year"]>10)]
df.index=df["code"]


"""获取股票估值指标"""
df_valuation=get_fundamentals(query(valuation),date=datetime.datetime.today())
df_valuation.index=df_valuation["code"]


df["pe_ratio"]=df_valuation["pe_ratio"]
df=df[df["pe_ratio"]<50]
# print(df.head())
