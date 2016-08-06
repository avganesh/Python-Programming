import quandl
import pandas as pd
import numpy as np
import pickle 
import matplotlib.pyplot as plt
from matplotlib import style
style.use('fivethirtyeight')

api_key = '5E7KjVEBYcSGrwzxrVU8'

def country_list():
    countries = pd.read_html('https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3#Current_codes')
    return countries[0][0][1:]

def grab_initial_country_data():
    countries = country_list()

    main_df = pd.DataFrame()

    for abbv in countries:
        try:
            query = "ECONOMIST/BIGMAC_"+str(abbv)
            df = quandl.get(query, authtoken=api_key)

            c_name = [str(abbv)+"_"]
            k = []
            for i in range(0, len(df.columns)):
                k.append(str(c_name[0])+str(df.columns[i]))

            df.columns = k 
            print(query)

            if main_df.empty:
                main_df = df
            else:
                main_df = pd.concat([main_df,df], axis=1)

        except Exception:
            print(query, ' failed')

    pickle_out = open('BIGMAC_countries.pickle', 'wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()
    
##grab_initial_country_data()
bigmac_data = pd.read_pickle('BIGMAC_countries.pickle')

def save_column_to_pickle(n):
    bigmac_col = pd.DataFrame()
    name = bigmac_data.columns[n][4:]
    for i in range(n, 540, 10):
        bigmac_col[bigmac_data.columns[i]]= bigmac_data[bigmac_data.columns[i]]

    bigmac_col.to_pickle('bigmac_'+str(name)+'.pickle')    

##save_column_to_pickle(5)
##bigmac_local = pd.read_pickle('bigmac_local.pickle')
##PPP is local price divide by USD price; USD ppp is 1. 
##bigmac_ppp = pd.read_pickle('bigmac_ppp.pickle')
bigmac_dollar = pd.read_pickle('bigmac_dollar.pickle')
##bigmac_dollex = pd.read_pickle('bigmac_dollex.pickle')
##print(bigmac_dollex.ix[19])
##print(bigmac_dollar.ix[9])


exclude = ['VNM_dollar_ppp', 'TUR_dollar_ppp','KOR_dollar_ppp','IDN_dollar_ppp','COL_dollar_ppp', 'VEN_dollar_ppp', 'HUN_dollar_ppp', 'CRI_dollar_ppp', 'CHL_dollar_ppp']
##bigmac_ppp[bigmac_ppp.columns.difference(exclude)].fillna(method='bfill').plot()
bigmac_dollar_2015 = bigmac_dollar[bigmac_dollar.columns.difference(exclude)].fillna(method='bfill').ix[18].sort_values()
##print(bigmac_dollar_2015)
bigmac_dollar_2015.plot.bar()
##plt.legend().remove()
plt.show()

