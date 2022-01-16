import Data.stock as st
import strategy.base as strat
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def bull_strategy(data, window):
    # 获取股票代码在指定时间段的价格数据
    data = pd.DataFrame(data)
    data['ma'] = data['close'].rolling(window=window, min_periods=1).mean()
    data['std'] = data['close'].rolling(window=window, min_periods=1).std()
    data['upper'] = data['ma'] + 2 * data['std']
    data['lower'] = data['ma'] - 2 * data['std']
    data['buy_signal'] = np.where((data['close'] < data['lower']), 1, 0)
    data['sell_signal'] = np.where((data['close'] > data['upper']), -1, 0)

    data=strat.compose_signal(data)  # 整理信号
    data=strat.calculate_profit_pct(data)  # 计算单次收益率
    data=strat.calculate_cum_prof(data)  # 计算累计收益率
    # 存储收益率数据，可视化bull线
    # data_adj.to_csv('/Users/zhongbo/Desktop/data_adj.csv')
    # data['upper'].plot(label='upper')
    # data['mid'].plot(label='mid')
    # data['lower'].plot(label='lower')
    # data['close'].plot(label='close')
    # plt.legend()
    # plt.show()
    return data


if __name__ == '__main__':

    # 股票列表
    stocks = ['000858.XSHE', '002594.XSHE', '600519.XSHG',
              "300015.XSHE"]

    # 存放累计收益率
    cum_profits = pd.DataFrame()
    # 循环获取数据
    for code in stocks:
        df = st.get_single_stock_price(code, 'daily', '2021-01-01',
                                       '2022-01-01')
        df = bull_strategy(df,20)  # 调用 bull_strategy
        cum_profits[code] = df['cum_profit'].reset_index(drop=True)  # 存储累计收益率
        # 折线图
        df['cum_profit'].plot(label=code)
        # 筛选有信号点
        # df = df[df['signal'] != 0]
        # print(df[['close', 'short_ma', 'long_ma', 'signal']])

        # 预览数据
        print("开仓次数：", int(len(df)))
        # print(df[['close', 'signal', 'profit_pct', 'cum_profit']])

    # 预览
    print(cum_profits)
    # 可视化
    cum_profits.plot()
    plt.legend()
    plt.title('Comparison of boll Strategy Profits')
    plt.show()