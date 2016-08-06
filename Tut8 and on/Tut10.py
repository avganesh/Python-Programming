import quandl
import pandas as pd
import pickle 
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

api_key = '5E7KjVEBYcSGrwzxrVU8'

def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]
    

def grab_initial_state_data():
    states = state_list()

    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken=api_key)
        df.columns = [abbv]
        df[abbv] = (df[abbv]-df[abbv][0])/df[abbv][0]*100.0
        print(query)
        if main_df.empty:
            main_df = df
        else:
            main_df = pd.concat([main_df,df], axis=1)

    pickle_out = open('fiddy_states3.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()        

##grab_initial_state_data()

def HPI_Benchmark():
    df = quandl.get("FMAC/HPI_USA", authtoken=api_key)
    df.columns = ['United States']
    df["United States"] = (df["United States"]-df["United States"][0]) / df["United States"][0] * 100.0
    return df


fig = plt.figure()
ax1 = plt.subplot2grid((1,1), (0,0))
HPI_data = pd.read_pickle('fiddy_states3.pickle')
##benchmark = HPI_Benchmark()
HPI_State_Correlation = HPI_data.corr()

HPI_data['TX1yr'] = HPI_data['TX'].resample('A').mean()
print(HPI_data[['TX','TX1yr']].head())
##HPI_data.dropna(inplace=True)
##HPI_data.fillna(method='ffill', inplace=True)
##HPI_data.fillna(method='bfill', inplace=True)
HPI_data.fillna(value=-99999, limit=10, inplace=True)
##we would do this for ML problems to identify these items as outliers
print(HPI_data[['TX','TX1yr']].head())

print(HPI_data.isnull().values.sum())

HPI_data[['TX','TX1yr']].plot(ax=ax1)

plt.legend().remove()
plt.show()

