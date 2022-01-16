#!/usr/bin/env python
# encoding: utf-8
'''
@author: DeltaF
@software: pycharm
@file: comp_sharpe_ratio.py
@time: 2021/3/16 22:20
@desc:
'''
import Data.stock as st
import strategy.base as stb
import pandas as pd
import matplotlib.pyplot as plt


# 获取3只股票的数据：比亚迪、宁德时代、隆基
tickers = ['002594.XSHE', '300750.XSHE', '601012.XSHG']

# 容器：存放夏普
sharpes = []
for ticker in tickers:
    data = st.get_single_stock_price(ticker, 'daily', '2018-10-01', '2021-01-01')
    print(data.head())
    # 获取price数据的同时，画出close的折线图，并标明图例
    plt.plot(data.index, data['close'],
             label=ticker)  # 这句用data['close'].plot(label=code)效果相同
    plt.xticks(rotation=30)

    # 计算每只股票的夏普比率
    daily_sharpe, annual_sharpe = stb.calculate_sharpe(data)
    sharpes.append([ticker, annual_sharpe])  # 存放 [[c1,s1],[c2,s2]..]
    print(sharpes)
plt.legend()


# 可视化3只股票并比较
sharpes = pd.DataFrame(sharpes, columns=['ticker', 'sharpe']).set_index('ticker')
print(sharpes)

# 绘制bar图
sharpes.plot.bar(title='Compare Annual Sharpe Ratio')
plt.xticks(rotation=10)
plt.show()