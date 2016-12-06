import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
from statistics import mean
from sklearn import svm, preprocessing, model_selection
style.use('fivethirtyeight')

housing_data = pd.read_pickle('HPI_Data.pickle')
housing_data = housing_data.pct_change()
##print(housing_data.head())

housing_data.replace([np.inf, -np.inf], np.nan, inplace=True)
housing_data['US_HPI_future'] = housing_data['US_HPI'].shift(-1)
housing_data.dropna(inplace=True)

def label_hpi_inc(cur_hpi, fut_hpi):
    if fut_hpi > cur_hpi:
        return 1
    else:
        return 0


housing_data['HPI_inc_label'] = list(map(label_hpi_inc,housing_data['US_HPI'], housing_data['US_HPI_future']))

def moving_average(values):
    ma = mean(values)
    return ma

housing_data['ma_apply_example'] = housing_data['M30'].rolling(center=False, window=10).apply(func=moving_average)

##print(housing_data.tail())
housing_data.dropna(inplace=True)
##print(housing_data.head())

##Use sklearn to create an SVM for ML classifier
X = np.array(housing_data.drop(['HPI_inc_label','US_HPI_future'], 1))
X = preprocessing.scale(X)

y = np.array(housing_data['HPI_inc_label'])

X_train, X_test, y_train, y_test = model_selection.train_test_split(X, y, test_size=0.2)

clf = svm.SVC(kernel='linear')
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))
