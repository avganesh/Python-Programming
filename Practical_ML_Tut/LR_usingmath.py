import pandas as pd
import numpy as np 
import quandl, pickle
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split


def LR_func(X, y):
    pass

def predict_func(X):
    pass

def score_func(ybar, y):
    variance = y.var()*(y.count()-1)
    sq_dif = (ybar - y)**2
    score = 1 - sq_dif.sum()/variance
    return (score)

##Get data from quandl and save to pickle 
##df = quandl.get('WIKI/GOOGL')
##df.to_pickle('GOOGL.pickle')

##open WIKI/GOOGL data that we saved from Quandl and apply transformations to keep useful columns and stats
df = pd.read_pickle('GOOGL.pickle')
##print(df.head())
df['HL_PCT'] = (df['Adj. High'] - df['Adj. Low']) / df['Adj. Low'] 
df['DoD_PCT'] = (df['Adj. Close'] - df['Adj. Open']) / df['Adj. Open']
df = df[['Adj. Close','HL_PCT','DoD_PCT','Adj. Volume']]

##print(df.isnull().any())
##print(df.head())

##Fill Nan values with outliers
df.fillna(value=-99999, inplace=True)

##Set the label field to be our "forecasted" adj. close price for 10 days out
df['label'] = df['Adj. Close'].shift(-10)

##create an np array of the last 20 rows of data 
X_test1 = np.array(df.drop(['label'], 1)[-20:-10])
X_test2 = np.array(df.drop(['label'], 1)[-10:])

##save last 10 non-Nan labels
y_test1 = np.array(df['label'][-20:-10])


##ignore last 20 rows of data for training
df_train = df[:-20]
##print(df_train.tail())

##set X feature vectors and y label vector for regression
y_train = np.array(df_train['label'])
X_train = np.array(df_train.drop(['label'], 1))

##select classifier to use with maximum threading because we can 
clf = LinearRegression(n_jobs=-1)

##train the classifier
##clf.fit(X_train, y_train)
clf.fit(X_train, y_train)

##test the classifier
##print(clf.score(X_test, y_test))

##score with scikit learn (takes feature amounts and correct amount [calculates prediction], outputs R^2)
Test_df = pd.DataFrame()
Test_df['real_prices'] = y_test1
Test_df['predicted_prices'] = clf.predict(X_test1)

##Test1_df.set_index(pd.DatetimeIndex(, periods=Test1_df['real_prices'].count(), freq='D'), inplace=True)

##score with my function (takes prediction and correct amount, outputs R^2)
A = Test_df['predicted_prices']
B = Test_df['real_prices']
##print(score_func(A, B))

print(Test_df)
