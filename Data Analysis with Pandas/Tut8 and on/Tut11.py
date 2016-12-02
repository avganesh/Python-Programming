import quandl
import pandas as pd
import pickle 
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')


fig = plt.figure()
ax1 = plt.subplot2grid((2,1), (0,0))
ax2 = plt.subplot2grid((2,1), (1,0), sharex=ax1)

HPI_data = pd.read_pickle('fiddy_states3.pickle')

##HPI_data['TX12MA'] = HPI_data['TX'].rolling(window=12, center=False).mean()
##HPI_data['TX12STD'] = pd.rolling_std(HPI_data['TX'], 12)
##
##HPI_data['TX'].plot(ax=ax1)
##HPI_data['TX12MA'].plot(ax=ax1)
##HPI_data['TX12STD'].plot(ax=ax2)

TX_AK_12corr = HPI_data['TX'].rolling(window=12).corr(HPI_data['FL'])

HPI_data['TX'].plot(ax=ax1, label="TX HPI")
HPI_data['FL'].plot(ax=ax1, label="FL HPI")
ax1.legend(loc=4)

TX_AK_12corr.plot(ax=ax2)

##plt.legend().remove()
plt.show()

