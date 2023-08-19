#coding=utf-8
import pandas as pd

# 读取Excel文件
df = pd.read_excel('RQ2-KGQS.xlsx', sheet_name='Sheet1')

# 打开list_1_60.txt
with open('list_1_60.txt', 'r') as f:
    text = f.read()
    # 得到list_1_60
    list_1_60 = eval(text.split('=')[1])
    for i in range(len(list_1_60)):
        # 每一行存入对应df中的Round列
        df.loc[i, 'Round1'] = str(list_1_60[i])
# 存入Excel文件
df.to_excel('RQ2-KGQS.xlsx', sheet_name='Sheet1', index=False)