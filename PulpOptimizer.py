from pulp import *
import pandas as pd


def get_double_doubles(inp_df):
    doubles_count = 0
    if inp_df['points'] >= 10:
        doubles_count += 1
    if inp_df['rebounds'] >= 10:
        doubles_count += 1
    if inp_df['assists'] >= 10:
        doubles_count += 1
    if inp_df['steals'] >= 10:
        doubles_count += 1
    if inp_df['blocks'] >= 10:
        doubles_count += 1
    if doubles_count >= 2:
        return 1
    return 0


def get_triple_doubles(inp_df):
    doubles_count = 0
    if inp_df['points'] >= 10:
        doubles_count += 1
    if inp_df['rebounds'] >= 10:
        doubles_count += 1
    if inp_df['assists'] >= 10:
        doubles_count += 1
    if inp_df['steals'] >= 10:
        doubles_count += 1
    if inp_df['blocks'] >= 10:
        doubles_count += 1
    if doubles_count > 2:
        return 1
    return 0


def dk_score(data, points='points', threes='made_three_point_field_goals', rbd='rebounds', assists='assists',
             steals='steals',
             blocks='blocks', turnovers='turnovers', dd='dd', td='td'):
    return data[points] + data[threes] * 0.5 + 1.5 * data[assists] + 1.25 * data[rbd] + 2 * data[steals] + 2 * data[
        blocks] - 0.5 * data[turnovers] + 1.5 * data[dd] + 3 * data[td]


def getPG(inp):
    if inp.find('PG') != -1:
        return 1
    return 0


def getSG(inp):
    if inp.find('SG') != -1:
        return 1
    return 0


def getSF(inp):
    if inp.find('SF') != -1:
        return 1
    return 0


def getPF(inp):
    if inp.find('PF') != -1:
        return 1
    return 0


def getC(inp):
    if inp.find('C') != -1:
        return 1
    return 0


def getG(inp):
    if inp.find('G') != -1:
        return 1
    return 0


def getF(inp):
    if inp.find('F') != -1:
        return 1
    return 0


if __name__ == '__main__':

	df1 = pd.read_csv('data/salary_data2019.csv', encoding="ISO-8859-1")
	df2 = pd.read_csv('data/bb_reference/2019Data.csv', encoding="ISO-8859-1")
	map_df = pd.read_csv('data/dk_player_map.csv', encoding="ISO-8859-1")

	df2 = pd.merge(df2, map_df, how='left', on='name')

	df1['player_y'] = df1['player']
	date = '2019-04-27'
	df1 = df1[df1['date'] == date]

	df_merged = pd.merge(df1, df2, how='left', on=['date', 'player_y'])

	df_merged['points'] = df_merged['made_field_goals'] * 2 + df_merged['made_free_throws'] + \
				  df_merged['made_three_point_field_goals']
	df_merged['rebounds'] = df_merged['defensive_rebounds'] + df_merged['offensive_rebounds']
	df_merged['dd'] = df_merged.apply(get_double_doubles, axis=1)
	df_merged['td'] = df_merged.apply(get_triple_doubles, axis=1)
	df_merged['dk_score'] = df_merged.apply(lambda x: dk_score(x), axis=1)

	df_merged['PG'] = df_merged['pos'].apply(getPG)
	df_merged['SG'] = df_merged['pos'].apply(getSG)
	df_merged['SF'] = df_merged['pos'].apply(getSF)
	df_merged['PF'] = df_merged['pos'].apply(getPF)
	df_merged['C'] = df_merged['pos'].apply(getC)
	df_merged['G'] = df_merged['pos'].apply(getG)
	df_merged['F'] = df_merged['pos'].apply(getF)

	Util_df = df_merged
	Util_df = Util_df.dropna()

	players = list(Util_df['player_y'])
	dk_scores = list(Util_df['dk_score'])
	salaries = list(Util_df['salary'])
	PG = list(Util_df['PG'])
	SG = list(Util_df['SG'])
	SF = list(Util_df['SF'])
	PF = list(Util_df['PF'])
	C = list(Util_df['C'])
	G = list(Util_df['G'])
	F = list(Util_df['F'])

	model = pulp.LpProblem('race', pulp.LpMaximize)
	player_vars = pulp.LpVariable.dicts('include',
					(player for player in players),
					lowBound=0,
					upBound=1,
					   cat='Integer')
	model += (pulp.lpSum([player_vars[dr]*dk_scores[i] for i,dr in enumerate(players)]))
	model += (pulp.lpSum([player_vars[dr]*salaries[i] for i,dr in enumerate(players)])) <= 50000
	model += (pulp.lpSum([player_vars[dr]*PG[i] for i,dr in enumerate(players)])) >= 1
	model += (pulp.lpSum([player_vars[dr]*SG[i] for i,dr in enumerate(players)])) >= 1
	model += (pulp.lpSum([player_vars[dr]*SF[i] for i,dr in enumerate(players)])) >= 1
	model += (pulp.lpSum([player_vars[dr]*PF[i] for i,dr in enumerate(players)])) >= 1
	model += (pulp.lpSum([player_vars[dr]*C[i] for i,dr in enumerate(players)])) >= 1
	model += (pulp.lpSum([player_vars[dr]*G[i] for i,dr in enumerate(players)])) >= 3
	model += (pulp.lpSum([player_vars[dr]*F[i] for i,dr in enumerate(players)])) >= 3
	model += (pulp.lpSum([player_vars[dr] for i,dr in enumerate(players)])) == 8
	model.solve()
	choose = []
	for var in player_vars:
		choice = player_vars[var].varValue
		choose.append(int(choice)==1)
	print(Util_df[choose]['dk_score'].sum())
	print(Util_df[choose]['player_y'])
	print(Util_df[choose]['salary'].sum())
