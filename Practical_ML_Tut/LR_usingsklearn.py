import pandas as pd
import numpy as np 
import quandl, pickle, datetime
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

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

days = int(90)
##Set the label field to be our "forecasted" adj. close price for 10 days out
df['label'] = df['Adj. Close'].shift(-days)

##create an np array of the last 90 days of data 
shifted_data_df = df.drop(['label'], 1)[-days:]
shifted_data = np.array(shifted_data_df)

##remove last 90 days of data 
df.dropna(inplace=True)
##print(df.tail())

##set X feature vectors and y label vector for regression
y = np.array(df['label'])
X = np.array(df.drop(['label'], 1))

##define testing and training datasets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)

##select classifier to use with maximum threading because we can 
clf = LinearRegression(n_jobs=-1)

##train the classifier, print score (R^2 on test data)
clf.fit(X_train, y_train)
print(clf.score(X_test, y_test))

##predict prices for the next 90 days and put that in a dataframe 
predicted_prices = clf.predict(shifted_data)
##print(predicted_prices)

last_date = datetime.datetime.fromtimestamp(shifted_data_df.iloc[-1].name.timestamp()+86400)
##print(last_date)
Dates = pd.date_range(start=last_date, periods=90, freq='D')
Forecast = pd.DataFrame(index=Dates, columns=['Prices'])
Forecast['Prices'] = predicted_prices

##print(Prediction_df.tail())
##print(Forecast.head())
##print(Forecast.tail())
##print(Forecast.loc[datetime.datetime.fromtimestamp(shifted_data_df.iloc[-1].name.timestamp() + 86400*10)])
print(Forecast.loc['2016-12-25']['Prices'])
print(Forecast.loc['2016-12-25']['Prices'])
