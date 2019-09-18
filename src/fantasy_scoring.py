import pandas as pd
import numpy as np

def dk_score(data,points = 'points',threes='made_three_point_field_goals',rbd='rebounds',assists='assists',steals='steals',
            blocks='blocks',turnovers='turnovers',dd='dd',td='td'):
            return data[points]+data[threes]*0.5+1.5*data[assists]+1.25*data[rbd]+2*data[steals]+2*data[blocks]-0.5*data[turnovers]+1.5*data[dd]+3*data[td]
def dk_score_no_fg(data,points = 'points',threes='made_three_point_field_goals',rbd='rebounds',assists='assists',steals='steals',
            blocks='blocks',turnovers='turnovers',dd='dd',td='td'):
            return 1.5*data[assists]+1.25*data[rbd]+2*data[steals]+2*data[blocks]-0.5*data[turnovers]+1.5*data[dd]+3*data[td]
