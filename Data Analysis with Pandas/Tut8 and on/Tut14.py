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
    df.rename(columns={'United States':'US_HPI'}, inplace=True)
    pickle_out = open('HPI_bench.pickle','wb')
    pickle.dump(df, pickle_out)
    pickle_out.close() 

##HPI_Benchmark()

def mortgage_30y():
    df = quandl.get("FMAC/MORTG", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    df.rename(columns={'Value':'M30'}, inplace=True)
    pickle_out = open('mortgage_30y.pickle','wb')
    pickle.dump(df, pickle_out)
    pickle_out.close()        

##mortgage_30y()

def sp500_data():
    df = quandl.get("YAHOO/INDEX_GSPC", trim_start="1975-01-01", authtoken=api_key)
    df["Adjusted Close"] = (df["Adjusted Close"]-df["Adjusted Close"][0]) / df["Adjusted Close"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Adjusted Close':'sp500'}, inplace=True)
    df = df['sp500']
    pickle_out = open('sp500.pickle','wb')
    pickle.dump(df, pickle_out)
    pickle_out.close()        

##sp500_data()

def gdp_data():
    df = quandl.get("BCB/4385", trim_start="1975-01-01", authtoken=api_key)
    df["Value"] = (df["Value"]-df["Value"][0]) / df["Value"][0] * 100.0
    df=df.resample('M').mean()
    df.rename(columns={'Value':'GDP'}, inplace=True)
    df = df['GDP']
    pickle_out = open('gdp.pickle','wb')
    pickle.dump(df, pickle_out)
    pickle_out.close()        

##gdp_data()

def us_unemployment():
    df = quandl.get("ECPI/JOB_G", trim_start="1975-01-01", authtoken=api_key)
    df["Unemployment Rate"] = (df["Unemployment Rate"]-df["Unemployment Rate"][0]) / df["Unemployment Rate"][0] * 100.0
    df=df.resample('1D').mean()
    df=df.resample('M').mean()
    pickle_out = open('unemployment.pickle','wb')
    pickle.dump(df, pickle_out)
    pickle_out.close()        

##us_unemployment()

HPI_Data = pd.read_pickle('fiddy_states3.pickle')
m30 = pd.read_pickle('mortgage_30y.pickle')
sp500 = pd.read_pickle('sp500.pickle')
gdp = pd.read_pickle('gdp.pickle')
unemployment = pd.read_pickle('unemployment.pickle')
HPI_Bench = pd.read_pickle('HPI_Bench.pickle')

HPI = HPI_Data.join([HPI_Bench, m30,sp500,gdp,unemployment])
HPI.dropna(inplace=True)
HPI.to_pickle('HPI_Data.pickle')

