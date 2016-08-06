import pandas as pd

df = pd.read_html('test2.html')
print(df.head())
##df.to_csv('CATOlist.csv')
