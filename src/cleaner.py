import pandas as pd
import numpy as np


class Cleaner(object):

    def __init__(self):
        pass

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
