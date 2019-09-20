import pandas as pd

df1 = pd.read_csv('~\Documents\BasketballBetting/2016to2019Data_merged.csv', encoding="ISO-8859-1")


df1['min_played'] = df1['seconds_played']/60


def get_season(inp_date):
    if int(inp_date.split('/')[0]) > 8:
        return inp_date.split('/')[2] + '-' + str(int(inp_date.split('/')[2]) + 1)
    return str(int(inp_date.split('/')[2]) - 1) + '-' + inp_date.split('/')[2]

df1['season'] = df1['date'].apply(get_season)

team_list = df1['team'].unique()
season_list = df1['season'].unique()
top_3_list = []

for team in team_list:
    for season in season_list:
        team_df = df1[df1['team'] == team]
        team_df = team_df[team_df['season'] == season]
        team_df_G = team_df[team_df['pos'].str.contains('G')]
        team_df_C = team_df[team_df['pos'].str.contains('C')]
        team_df_grouped_G = team_df_G.groupby(['name', 'pos']).sum()
        team_df_grouped_C = team_df_C.groupby(['name', 'pos']).sum()
        team_df_sorted_G = team_df_grouped_G.sort_values(['game_score'], ascending=False)
        team_df_sorted_C = team_df_grouped_C.sort_values(['game_score'], ascending=False)
        top_G = list(team_df_sorted_G.head(1).index.values)[0][0]
        top_C = list(team_df_sorted_C.head(1).index.values)[0][0]
        team_df = team_df[team_df['player'] != top_G]
        team_df = team_df[team_df['player'] != top_C]
        team_df_grouped = team_df.groupby(['name', 'pos']).sum()
        team_df_sorted = team_df_grouped.sort_values(['game_score'], ascending=False)
        other_top = list(team_df_sorted.head(1).index.values)[0][0]
        top_3_list.append([team, season, top_G, top_C, other_top])

top_3_df = pd.DataFrame([i for i in top_3_list], columns=['team', 'season', 'p1', 'p2', 'p3'])

day_list = df1['date'].unique()

count = 1
game_df = pd.DataFrame(columns=['p1', 'p2', 'p3', 'team', 'date', 'venue'])
for day in day_list:
    for season in season_list:
        for team in team_list:
            day_df = df1[df1['season'] == season]
            day_df = day_df[day_df['date'] == day]
            if len(day_df) == 0:
                continue
            day_df = day_df[day_df['team'] == team]
            day_df = day_df[day_df['min_played'] > 10]
            team_top_3_df = top_3_df[top_3_df['team'] == team]
            team_top_3_df = team_top_3_df[team_top_3_df['season'] == season]
            team_top_3_list = []
            team_top_3_list.append(list(team_top_3_df['p1'])[0])
            team_top_3_list.append(list(team_top_3_df['p2'])[0])
            team_top_3_list.append(list(team_top_3_df['p3'])[0])
            if all(elem in list(day_df['name']) for elem in team_top_3_list):
                team_top_3_list.append(team)
                team_top_3_list.append(day)
                team_top_3_list.append(list(day_df['location'])[0])
                game_df.loc[count] = team_top_3_list
                count += 1
            elif len(day_df) != 0:
                G_df = day_df[day_df['pos'].str.contains('G')]
                C_df = day_df[day_df['pos'].str.contains('C')]
                G_df_sorted = G_df.sort_values(['game_score'], ascending=False)
                C_df_sorted = C_df.sort_values(['game_score'], ascending=False)
                top_G = list(G_df_sorted.head(1)['name'])[0]
                if len(C_df_sorted) == 0:
                    day_df = day_df[day_df['player'] != top_G]
                    day_df_sorted = day_df.sort_values(['game_score'], ascending=False)
                    other_top = list(day_df_sorted.head(2)['name'])
                    team_top_3_list = []
                    team_top_3_list.append(top_G)
                    team_top_3_list.append(other_top[0])
                    team_top_3_list.append(other_top[1])
                    team_top_3_list.append(team)
                    team_top_3_list.append(day)
                    team_top_3_list.append(list(day_df['location'])[0])
                    game_df.loc[count] = team_top_3_list
                    count += 1
                else:
                    top_C = list(C_df_sorted.head(1)['name'])[0]
                    day_df = day_df[day_df['player'] != top_G]
                    day_df = day_df[day_df['player'] != top_C]
                    day_df_sorted = day_df.sort_values(['game_score'], ascending=False)
                    other_top = list(day_df_sorted.head(1)['name'])[0]
                    team_top_3_list = []
                    team_top_3_list.append(top_G)
                    team_top_3_list.append(top_C)
                    team_top_3_list.append(other_top)
                    team_top_3_list.append(team)
                    team_top_3_list.append(day)
                    team_top_3_list.append(list(day_df['location'])[0])
                    game_df.loc[count] = team_top_3_list
                    count += 1

game_df.to_csv('~\Documents\BasketballBetting/GameClassifier_new.csv', header=True)
