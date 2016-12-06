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
    pickle_out = open('HPI_bench.pickle','wb')
    pickle.dump(df, pickle_out)
    pickle_out.close() 

##HPI_Benchmark()

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    pickle_out = open('mortgage_30y.pickle','wb')
    pickle.dump(df, pickle_out)
    pickle_out.close()        

##mortgage_30y()

HPI_data = pd.read_pickle('fiddy_states3.pickle')
m30 = pd.read_pickle('mortgage_30y.pickle')
m30.columns= ['M30']
HPI_Bench = pd.read_pickle('HPI_bench.pickle')
HPI = HPI_Bench.join(m30)
##print(HPI.corr())
state_HPI_m30 = HPI_data.join(m30)
print(state_HPI_m30.corr()['M30'].describe())
