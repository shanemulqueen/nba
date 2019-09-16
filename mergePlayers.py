import pandas as pd
df1 = pd.read_csv('~\Documents\BasketballBetting/2016to2019Data.csv', encoding="ISO-8859-1")
print(len(df1['name']))
df2 = pd.read_csv('~\Documents\BasketballBetting/PlayerList.csv', encoding="ISO-8859-1")

df_merged = pd.merge(df1, df2, left_on='name', right_on='player')
print(len(df_merged['name']))

df_merged.to_csv('~\Documents\BasketballBetting/2016to2019Data_merged.csv')