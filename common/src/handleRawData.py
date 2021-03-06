import pandas as pd

train_B = pd.read_csv("D:/contest/diabetes/d_test_B_20180128.csv", encoding='gb2312')

train_B['性别'] = train_B['性别'].map({'男':1, '女':0, '？？':1})
train_B = train_B.rename(columns={'性别':'gender','年龄':'age','体检日期':'date'})

train_B.to_csv("../data/raw/d_test_B.csv", index=False, encoding="utf-8")