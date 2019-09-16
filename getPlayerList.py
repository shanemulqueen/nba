import pandas as pd
import requests
from bs4 import BeautifulSoup

alphabet_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
                 't', 'u', 'v', 'w', 'x', 'y', 'z']

df_full = pd.DataFrame()

for i in alphabet_list:
    r = requests.get("https://www.basketball-reference.com/players/" + i + "/", verify=False)

    soup = BeautifulSoup(r.content, 'html.parser')
    table = soup.find_all("tr")
    player_list = []
    birthday_list = []
    for row in table:
        columns = row.find_all('a')
        col_no = 0
        for column in columns:
            if 'player' in str(column):
                player_list.append(column.get_text())
            elif 'birthday' in str(column):
                birthday_list.append(column.get_text())
            elif col_no == 1:
                birthday_list.append('')
            col_no += 1
            if len(columns) == 1:
                birthday_list.append('')

    year_min_list = []
    year_max_list = []
    pos_list = []
    height_list = []
    weight_list = []
    for row in table:
        columns = row.find_all('td')
        col_no = 0
        for column in columns:
            if 'year_min' in str(column):
                year_min_list.append(column.get_text())
            elif 'year_max' in str(column):
                year_max_list.append(column.get_text())
            elif 'pos' in str(column):
                pos_list.append(column.get_text())
            elif 'height' in str(column):
                height_list.append(column.get_text())
            elif 'weight' in str(column):
                weight_list.append(column.get_text())
            elif col_no == 4:
                weight_list.append('')
        col_no += 1

    df = pd.DataFrame()
    df['player'] = player_list
    df['birthday'] = birthday_list
    df['year_min'] = year_min_list
    df['year_max'] = year_max_list
    df['pos'] = pos_list
    df['height'] = height_list
    df['weight'] = weight_list

    df_full = df_full.append(df)

#print(df_full[df_full['player'] == 'Jae Crowder'])

df_full.to_csv('~\Documents\BasketballBetting/PlayerList.csv', header=True)