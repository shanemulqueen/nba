import pandas as pd

if __name__ == '__main__':

    gc_df = pd.read_csv('data/bb_reference/GameClassifier_new.csv', encoding="ISO-8859-1")

    df1 = pd.read_csv('data/bb_reference/2016to2019Data_merged.csv', encoding="ISO-8859-1")


    def getSlug1(inp_df, df1=df1):
        return list(df1[df1['player'] == inp_df['p1']]['slug'])[0]


    def getSlug2(inp_df, df1=df1):
    	return list(df1[df1['player'] == inp_df['p2']]['slug'])[0]


    def getSlug3(inp_df, df1=df1):
    	return list(df1[df1['player'] == inp_df['p3']]['slug'])[0]


    def getOpponent(inp_df, df1=df1):
    	team = inp_df['team']
    	date = inp_df['date']
    	df_temp = df1[df1['opponent'] == team]
    	df_temp = df_temp[df_temp['date'] == date]
    	return list(df_temp['team'])[0]


    def getOpp123(inp_df, gc_temp=gc_df):
    	team = inp_df['opponent']
    	date = inp_df['date']
    	gc_temp = gc_temp[gc_temp['team'] == team]
    	gc_temp = gc_temp[gc_temp['date'] == date]
    	rel_cols = ['p1', 'p2', 'p3']
    	return gc_temp[rel_cols]


    gc_df['p1'] = gc_df.apply(getSlug1, axis=1)
    gc_df['p2'] = gc_df.apply(getSlug2, axis=1)
    gc_df['p3'] = gc_df.apply(getSlug3, axis=1)
    gc_df['opponent'] = gc_df.apply(getOpponent, axis=1)
    gc_df['o123'] = gc_df.apply(getOpp123, axis=1)

    def geto1(inp_df):
        return list(inp_df['o123']['p1'])[0]
    def geto2(inp_df):
        return list(inp_df['o123']['p2'])[0]
    def geto3(inp_df):
        return list(inp_df['o123']['p3'])[0]
    
    gc_df['o1'] = gc_df.apply(geto1, axis=1)
    gc_df['o2'] = gc_df.apply(geto2, axis=1)
    gc_df['o3'] = gc_df.apply(geto3, axis=1)

    gc_df.to_csv('~/Documents/nba_data/gc_merged.csv')

