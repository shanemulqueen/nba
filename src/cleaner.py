import pandas as pd
import numpy as np
import fantasy_scoring as fs


class Cleaner(object):

    def __init__(self):
        self.lag_cols = ['minutes','dk_score','dk_per_min','dk_no_fg','dk_no_fg_per_min','assists','assists_per_min',
                    'blocks','blocks_per_min','or_per_min','dr_per_min','steals_per_min','turnovers_per_min','doubles',
                    'fg_pct','ft_pct','two_pct','three_pct','game_score','attempted_field_goals','attempted_three_point_field_goals','w']

    def bb_ref_to_dk(self,data):
        """will take raw bb ref data and output to put into the dk scorer"""
        data['points']=data['made_field_goals']*2+data['made_free_throws']+data['made_three_point_field_goals']
        data['rebounds']=data['offensive_rebounds']+data['defensive_rebounds']
        data['doubles']=data.apply(lambda x: self.count_doubles(x), axis = 1)
        data['dd']=data.apply(lambda x: 1 if x['doubles']>1 else 0,axis = 1)
        data['td']=data.apply(lambda x: 1 if x['doubles']>2 else 0, axis = 1)
        return data

    def count_doubles(self, x,points='points',rbd='rebounds',assists='assists',steals='steals',
                blocks='blocks'):
        #for use as a lambda function
        return int((x[points]>=10))+ int((x[rbd]>=10))+int((x[assists]>=10))+int((x[steals]>=10))+int((x[blocks]>=10))


    def transform1(self,data):
        data['dk_score']= data.apply(lambda x: fs.dk_score(x),axis = 1)
        data['dk_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['dk_score']*60/x['seconds_played'],axis = 1)

        data['dk_no_fg']= data.apply(lambda x: fs.dk_score_no_fg(x),axis = 1)
        data['dk_no_fg_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['dk_no_fg']*60/x['seconds_played'],axis = 1)
        data['assists_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['assists']*60/x['seconds_played'],axis = 1)
        data['blocks_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['blocks']*60/x['seconds_played'],axis = 1)
        data['or_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['offensive_rebounds']*60/x['seconds_played'],axis = 1)
        data['dr_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['defensive_rebounds']*60/x['seconds_played'],axis = 1)
        data['steals_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['steals']*60/x['seconds_played'],axis = 1)
        data['turnovers_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['turnovers']*60/x['seconds_played'],axis = 1)
        data['points_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['points']*60/x['seconds_played'],axis = 1)
        data['double_per_min']=data.apply(lambda x: 0 if x['seconds_played']==0 else x['steals']*60/x['seconds_played'],axis = 1)

        data['minutes']=data['seconds_played']/60
        data['fg_pct']=data.apply(lambda x: 0 if x['attempted_field_goals']==0
                                  else x['made_field_goals']/x['attempted_field_goals'],
                                  axis = 1)
        data['w']=data['outcome'].apply(lambda x: 1 if x == 'Outcome.WIN' else 0)
        data['three_pct']=data.apply(lambda x: 0 if x['attempted_three_point_field_goals']==0
                                  else (x['made_three_point_field_goals'])/x['attempted_three_point_field_goals'],
                                  axis = 1)
        data['two_pct']=data.apply(lambda x: 0 if (x['attempted_field_goals']-x['attempted_three_point_field_goals'])==0
                                  else (x['made_field_goals']-x['made_three_point_field_goals'])/
                                   (x['attempted_field_goals']-x['attempted_three_point_field_goals']),
                                  axis = 1)
        data['ft_pct']=data.apply(lambda x: 0 if x['attempted_free_throws']==0
                                  else x['made_free_throws']/x['attempted_free_throws'],
                                  axis = 1)
        data['dt']=pd.to_datetime(data['date'])
        return data
    def get_roll(self, x, win_length):
        #lambda function
        return x.rolling(window = win_length,min_periods = 1).mean()
    def get_roll_median(self, x, win_length):
        #lambda function
        return x.rolling(window = win_length,min_periods = 1).median()

    def gameplay_stats(self,data,lag = 6,minute_floor = 5,player_col='player',date_col='date'):
        temp_data = data[(data['seconds_played']>=60*minute_floor)].sort_values(by = date_col).copy(deep = True)

        lags = pd.DataFrame()
        self.agg_dict = {elem:[np.sum] for elem in self.lag_cols}
        for player in data[player_col].unique():
            grp = data[data[player_col]==player].groupby(by=[player_col,date_col])
            thing2 = grp.aggregate(self.agg_dict).apply(lambda x: self.get_roll(x, lag)).fillna(0).reset_index()
            try:
                lags = lags.append(thing2,ignore_index = True,sort = False)
            except:
                pass
        temp_cols = [col+"_{:02}".format(lag) for col in self.lag_cols]
        lags.columns = [player_col,date_col]+temp_cols
        return lags
    def fit(self,data):
        self.hist = self.bb_ref_to_dk(raw_data.copy(deep=True))
        self.hist = self.transform1()
        return none
    def transform(self,raw_data):
        data = self.bb_ref_to_dk(raw_data.copy(deep=True))
        data = self.transform1(data)
        return data
