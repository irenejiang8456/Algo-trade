"""
获取价格，并计算涨跌幅
"""

import Data.stock as st

# 本地读取数据
data=st.get_csv_price("000001.XSHE","2020-01-01","2021-02-01")
print(data)
exit() # 中断程序

# 获取平安银行的行情数据（日K）
data=st.get_single_stock_price("000001.XSHE","daily","2021-12-01","2021-12-31")
# print(data)

# 计算涨跌幅， 验证准确性
data=st.calculate_change_pct(data)
# print(data) # 多了一列 close pct change

# 获取周K
data=st.convert_price_period(data,"w")
print(data)

# 计算涨跌幅，验证准确性
data=st.calculate_change_pct(data)
print(data)