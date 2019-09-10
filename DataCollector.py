import datetime
from datetime import timedelta
import pandas as pd

from basketball_reference_web_scraper import client

stat_df = pd.DataFrame()
start_year = 2018
run_date = datetime.date(year=start_year, day=1, month=1)
i = 1
while run_date <= datetime.datetime.today().date():
    df = pd.DataFrame.from_dict(client.player_box_scores(day=run_date.day, month=run_date.month, year=run_date.year))
    df['date'] = run_date
    stat_df = stat_df.append(df)
    run_date = run_date + timedelta(days=1)

stat_df.to_csv('~\Documents\BasketballBetting/LatestData.csv')
