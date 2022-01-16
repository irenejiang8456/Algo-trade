"""
用来创建交易策略、生成交易信号
"""
import Data.stock as st
import numpy as np
import datetime
import matplotlib.pyplot as plt
import pandas as pd

def compose_signal(data):
    # 整合信号
    data["buy_signal"] = np.where((data["buy_signal"] == 1) &
                                  (data["buy_signal"].shift(1) == 1), 0,
                                  data["buy_signal"])
    data["sell_signal"] = np.where(
        (data["sell_signal"] == -1) & (data["sell_signal"].shift(1) == -1), 0,
        data["sell_signal"])

    data["signal"] = data["buy_signal"] + data["sell_signal"]

    return data

def calculate_profit_pct(data):
    # 计算单次收益率：开仓、平仓（开仓的全部股数）
    data.loc[data["signal"]!=0,"profit_pct"]=data["close"].pct_change()
    # data = data[data["signal"] != 0]  # 筛选
    # data["profit_pct"] = (data["close"] - data["close"].shift(1)) / data[
    #     "close"].shift(1)
    data = data[data["signal"] == -1] # 筛选平仓后的数据：单次收益

    return data

def calculate_cum_prof(data):
    """
    计算累计收益率
    :param data: dataframe
    :return:
    """
    data["cum_profit"]=pd.DataFrame(1+data["profit_pct"]).cumprod()-1
    return data

def calculate_max_drawdown(data):
    """
    计算最大回撤比
    :param data:
    :return:
    """
    # 选取时间周期 （时间窗口）
    window=252
    # 计算时间周期中的最大净值
    data["roll_max"]=data["close"].rolling(window=window,min_periods=1).max()
    # 计算当天回撤比 (谷值-峰值）/ 峰值 = 谷值/峰值-1
    data["daily_dd"]=data["close"]/data["roll_max"]-1
    # 选取时间周期内最大的回撤比，即最大回撤
    data["max_dd"]=data["daily_dd"].rolling(window=window,min_periods=1).min()

    return data

def calculate_sharpe(data):
    """
    计算夏普比率，返回的是年化的夏普比率
    :param data: dataframe, stock
    :return: float
    """
    # 公式 sharpe= （回报率的均值 - 无风险利率） / 回报率的标准差
    # 因子项
    daily_return=data["close"].pct_change()
    avg_return=daily_return.mean() # 回报率的均值=日涨跌幅。mean（）
    std_return= daily_return.std()   # 回报率的标准差=日涨跌幅。std（）
    # 计算夏普
    sharpe=avg_return/std_return    # sharpe= 回报率的均值/ 回报率的标准差
    sharpe_year=sharpe*np.sqrt(252)
    return sharpe,sharpe_year


def week_period_strategy(ticker,timePeriod,stadate,endate):
    data=st.get_single_stock_price(ticker,timePeriod,stadate,endate)
    # 新建周期字段
    data["weekday"]=data.index.weekday
    # 周四买入 (1 ----> buy) (0 ---> do nothing)
    data["buy_signal"]=np.where((data["weekday"] ==3),1,0)
    # 周一卖出 (-1 -----> sell)
    data["sell_signal"] = np.where((data["weekday"] == 0), -1, 0)

    # 模拟重复买入：周五再次买入, 周二再次卖出
    # data["buy_signal"]=np.where((data["weekday"] ==3) | (data["weekday"] ==4),1,0)
    # data["sell_signal"] = np.where(
    #     (data["weekday"] == 0) | (data["weekday"] == 1), -1, 0)


    data= compose_signal(data) # 整合信号
    data=calculate_profit_pct(data) # 计算收益
    data= calculate_cum_prof(data) # 计算累计收益率
    # data=calculate_max_drawdown(data) # 计算最大回撤
    return data

if __name__ == '__main__':
    df=week_period_strategy("000001.XSHE","daily",None,datetime.date.today())
    print(df[["close","signal","profit_pct","cum_profit"]])
    print(df.describe())
    df["cum_profit"].plot()
    plt.show()

    # 查看平安银行最大回撤
    # df = st.get_single_stock_price("000001.XSHE","daily","2006-01-01","2021-01-01")
    # df= calculate_max_drawdown(df)
    # print(df[["close","roll_max","daily_dd","max_dd"]])
    # df[["daily_dd","max_dd"]].plot()
    # plt.show()

    # 计算夏普比率
    df = st.get_single_stock_price("000001.XSHE", "daily", "2006-01-01",
                                   "2021-01-01")
    df = calculate_sharpe(df)
    print(df)
