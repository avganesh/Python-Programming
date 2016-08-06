import quandl
import pandas as pd
import pickle 

api_key = '5E7KjVEBYcSGrwzxrVU8'

##df = quandl.get("FMAC/HPI_AK", authtoken=api_key)
##print(df.head())

##fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
##print(fiddy_states)

##for abbv in fiddy_states[0][0][1:]:
##    print(abbv)
##    print("FMAC/HPI_"+str(abbv))

##main_df = df

##for abbv in fiddy_states[0][0][1:]:
##    query = "FMAC/HPI_"+str(abbv)
##    df = quandl.get(query, authtoken=api_key)
    
##    if main_df.empty:
##        main_df = df
##
##    else:
##main_df = main_df.join(df) 
##main_df = pd.merge(main_df, df)
##print(df.head())
##joined_df = pd.merge(main_df, df)
##print(joined_df.head())
##
##    print(main_df.head())

##pickle_out = open('fiddy_states.pickle','wb')
##pickle.dump(main_df, pickle_out)
##pickle_out.close()



def state_list():
    fiddy_states = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
    return fiddy_states[0][0][1:]
    

def grab_initial_state_data():
    states = state_list()

    main_df = pd.DataFrame()

    for abbv in states:
        query = "FMAC/HPI_"+str(abbv)
        df = quandl.get(query, authtoken=api_key)
##        print(df.head())
        if main_df.empty:
            main_df = df
        else:
            main_df = pd.concat([main_df,df], axis=1)
##            print(main_df.head())
            
    pickle_out = open('fiddy_states.pickle','wb')
    pickle.dump(main_df, pickle_out)
    pickle_out.close()

##grab_initial_state_data()

pickle_in = open('fiddy_states.pickle','rb')
HPI_data = pickle.load(pickle_in)
print(HPI_data)

##HPI_data.to_pickle('pickle.pickle')
##HPI_data2 = pd.read_pickle('pickle.pickle')
##print(HPI_data2)

##HPI_data.to_csv('HPIstatedata.csv')
