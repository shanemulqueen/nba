from collections import Counter
from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
import numpy as np
import requests
import re
from bs4 import BeautifulSoup
import argparse
import time
from splinter import Browser
import time
from collections import defaultdict
import json
import re


if __name__ == '__main__':
    f = open('.env','r')
    env = {}
    print('reading env variables')
    for line in f.readlines():
        env[line.strip().split("=")[0]]=line.strip().split("=")[1]
    print('logging into site')
    br = Browser("firefox")
    br.visit("https://www.fantasycruncher.com/login?referer=/")
    br.find_by_id('user_email').fill(env['fc_login'])
    br.find_by_id('user_password').fill(env['fc_pw'])
    br.find_by_id('submit').click()
    rewind_base = "https://www.fantasycruncher.com/lineup-rewind/draftkings/NBA/"
    date = "2018-10-29"
    br.visit(rewind_base+date)
    all_players = "/html/body/div[3]/div[1]/div[1]/div/div[2]/div[8]/div[2]/div[2]/div[2]/div[2]/div/label/select/option[7]"
    br.find_by_name("ff_length").click()
    br.find_by_xpath(all_players).click()
    tr_selector = "/html/body/div[3]/div[1]/div[1]/div/div[2]/div[8]/div[1]/div[2]/table/tbody/tr"
    print('Opening Data')
    f = open('data/empty_dates.txt','r')
    dates = []
    for line in f.readlines():
        dates.append(line.strip())
    salary_data = pd.read_csv('data/salary_data_gaps.csv')
    data = pd.DataFrame()
    salary_data2 = pd.DataFrame()
    for date in dates[20:]:
        time.sleep(1)
        br.visit(rewind_base+date)
        table = br.find_by_xpath(tr_selector)
        try:
            if len(table) > 0:
                print(len(table))
                temp_dict = {}
                temp_dict['player'] = []
                temp_dict['pos'] = []
                temp_dict['salary'] = []
                for ind, row in enumerate(table):
                    temp_dict['player'].append(row.find_by_css(".player-stats").text)
                    temp_dict['salary'].append(row.find_by_css(".salaryCol").text)
                    try:
                        temp_dict['pos'].append(row.find_by_css("td select.pos-select option")[0].text)
                    except:
                        temp_dict['pos'].append(row.find_by_css("td")[1].text)
                temp_df = pd.DataFrame(temp_dict)
                temp_df['date']=date
                salary_data2 = salary_data2.append(temp_df)
            else:
                print("empty {}".format(date))
        except:
            print("error {}".format(date))
    print("Done!")
    salary_data = salary_data.append(salary_data2)
    salary_data.to_csv('data/salary_data_gaps.csv',index = False)
