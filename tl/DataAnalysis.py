from sys import path

path.append('../')
from tl.Feature import Feature
import pandas as pd
from tl.util import read_data, save, plt_encoding_error, error, normal
import matplotlib.pyplot as plt

train, test_A, _ = read_data()

num_train = len(train)
num_test_A = len(test_A)

train_m = pd.concat([train, test_A])

diaFeature = Feature(train_m)
diaFeature.normal_value()
diaFeature.statistics()
drop_list = ['id', '血糖','体检日期','性别', '血小板比积', '血小板计数', '嗜酸细胞%']
diaFeature.drop_feature(drop_list)
train_m = diaFeature.get_train()
train_y = train['血糖']

# 重新切分训练与测试数据
train_x = train_m.iloc[:num_train]
test_A_new = train_m.iloc[num_train:num_test_A + num_train]

features = train_x.columns.tolist()
train_X = train_x.as_matrix()
train_Y = train_y.as_matrix()

test_X = test_A_new.as_matrix()

from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(train_X, train_Y, test_size=0.2, random_state=1)

import lightgbm as lgb

# create dataset for lightgbm
lgb_train = lgb.Dataset(X_train, y_train, feature_name=features)
lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train, feature_name=features)

train_all = lgb.Dataset(train_X, train_Y, feature_name=features)

# specify your configurations as a dict
params = {
    'task': 'train',
    'boosting_type': 'gbdt',
    'objective': 'regression',
    'metric': {'mse'},
    'num_leaves': 31,
    'learning_rate': 0.02,
    'lambda_l1': 1,
    # 'lambda_l2': 1,
    'cat_smooth': 10,
    'feature_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

print('Start training...')
# train
gbm = lgb.train(params,
                lgb_train,
                num_boost_round=1000,
                valid_sets=lgb_eval,
                early_stopping_rounds=20)

print('Start predicting...')
# predict
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
# eval
error(y_test, y_pred)

# online

predict = gbm.predict(test_X, num_iteration=gbm.best_iteration)
data1 = pd.DataFrame(predict)
# save
# save(data1, 'lgb')

# gbm_online = lgb.train(params,
#                        train_all,
#                        num_boost_round=235)
# # predict
# predict = gbm_online.predict(test_X, num_iteration=gbm_online.best_iteration)
# data1 = pd.DataFrame(predict)
# save
# save(data1, 'lgb')

# 解决中文乱码
plt_encoding_error()

lgb.plot_importance(gbm)
plt.show()
