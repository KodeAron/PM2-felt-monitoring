# -*- coding: utf-8 -*- python3
""" feature importance of merged dataframe

Calculate feature importance on features in the merged dataframe from extractcombiner.

Created on Apr 7 2021 17:42
@author: Aron, Luleå University of Technology
"""
import sklearn
# print(sklearn.__version__)
from sklearn.datasets import make_classification
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from matplotlib import pyplot

import extractombiner as extcom

df_original = extcom.combiner()

df = df_original[[('kurtosis','P001D'),('kurtosis','P001F'),('AverageSpeed',''),('Trimproblem','')]].copy()
# print(df_original.columns)
# df = df_original.xs(('kurtosis','P001D'), level=[0,'NodeName'])

print(df.head())

y = df['Trimproblem']
X = df.drop('Trimproblem',1,inplace=False)

# X, y = make_regression(n_samples=1000, n_features=10, n_informative=5, random_state=1)
# X, y = make_classification(n_samples=1000, n_features=10, n_informative=5, n_redundant=5, random_state=1)

print(X.shape, y.shape)
print(X)
print(y)

# model = RandomForestRegressor()
model = RandomForestClassifier()

model.fit(X,y)

print(model)

importance = model.feature_importances_

for i,v in enumerate(importance):
    print('Feature: %0d, Score: %.5f' % (i,v))

pyplot.bar([x for x in range(len(importance))], importance)
pyplot.show()