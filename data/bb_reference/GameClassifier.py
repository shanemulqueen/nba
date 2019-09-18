import pandas as pd
import datetime
df1 = pd.read_csv('~\Documents\BasketballBetting/2016to2019Data.csv', encoding="ISO-8859-1")

df1['min_played'] = df1['seconds_played']/60


def get_season(inp_date):
    if int(inp_date.split('/')[0]) > 8:
        return inp_date.split('/')[2] + '-' + str(int(inp_date.split('/')[2]) + 1)
    return str(int(inp_date.split('/')[2]) - 1) + '-' + inp_date.split('/')[2]

df1['season'] = df1.date.apply(get_season)


team_list = df1.team.unique()
season_list = df1.season.unique()
top_3_list = []

disp_cols = ['min_played']

for team in team_list:
    for season in season_list:
        team_df = df1[df1.team == team]
        team_df = team_df[team_df.season == season]
        team_df_grouped = team_df.groupby(['name']).sum()
        team_df_sorted = team_df_grouped.sort_values(['min_played'], ascending=False)
        top_3_list.append([team, season, team_df_sorted.head(3).index.values[0],
                          team_df_sorted.head(3).index.values[1], team_df_sorted.head(3).index.values[2]])

top_3_df = pd.DataFrame([i for i in top_3_list], columns=['team', 'season', 'p1', 'p2', 'p3'])

day_list = df1.date.unique()

count = 1
game_df = pd.DataFrame(columns=['p1', 'p2', 'p3', 'team', 'date', 'venue'])
for day in day_list:
    for season in season_list:
        for team in team_list:
            day_df = df1[df1.season == season]
            day_df = day_df[day_df.date == day]
            if len(day_df) == 0:
                continue
            day_df = day_df[day_df.team == team]
            day_df = day_df[day_df.min_played > 10]
            team_top_3_df = top_3_df[top_3_df.team == team]
            team_top_3_df = team_top_3_df[team_top_3_df.season == season]
            team_top_3_list = []
            team_top_3_list.append(list(team_top_3_df.p1)[0])
            team_top_3_list.append(list(team_top_3_df.p2)[0])
            team_top_3_list.append(list(team_top_3_df.p3)[0])
            if all(elem in list(day_df.name) for elem in team_top_3_list):
                team_top_3_list.append(team)
                team_top_3_list.append(day)
                team_top_3_list.append(list(day_df.location)[0])
                game_df.loc[count] = team_top_3_list
                count += 1
            else:
                day_df_sorted = day_df.sort_values(['min_played'], ascending=False)
                if len(list(day_df_sorted.head(3).name)) == 3:
                    team_top_3_list = list(day_df_sorted.head(3).name)
                    team_top_3_list.append(team)
                    team_top_3_list.append(day)
                    team_top_3_list.append(list(day_df.location)[0])
                    game_df.loc[count] = team_top_3_list
                    count += 1
