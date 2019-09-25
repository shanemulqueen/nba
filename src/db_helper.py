from collections import Counter
from flask import Flask, request, render_template, jsonify
import pickle
import pandas as pd
from matplotlib import pyplot as plt
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
import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
from decimal import Decimal

from src.cleaner import Cleaner
import src.fantasy_scoring as fs


class DB_helper(object):
    def __init__(self):
        f = open('.env','r')
        self.env = {}
        print('reading env variables')
        for line in f.readlines():
            self.env[line.strip().split("=")[0]]=line.strip().split("=")[1]
        self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1',
            aws_access_key_id = self.env['aws_access_key_id'],
            aws_secret_access_key = self.env['aws_secret_access_key'])
        self.table = self.dynamodb.Table('nba_bbref')

    def get_player(self, slug,columns):
        kce = Key('slug').eq(slug)
        ea = {"#dt":"date"}
        pe = "slug, #dt, " + ", ".join(columns)
        resp = self.table.query(IndexName = 'slug-date-index', KeyConditionExpression = kce,
                ExpressionAttributeNames =ea,
                ProjectionExpression = pe,
                ScanIndexForward = True,
                )['Items']
        output = pd.DataFrame(resp)
        while len(resp)==391:
            max = output['date'].sort_values().iloc[-1]
            kce = Key('slug').eq(slug) & Key('date').gt(max)
            resp = self.table.query(IndexName = 'slug-date-index', KeyConditionExpression = kce,
                    ExpressionAttributeNames =ea,
                    ProjectionExpression = pe,
                    ScanIndexForward = True,
                    )['Items']
            if len(resp)>0:
                temp_df = pd.DataFrame(resp)
                output = output.append(temp_df)

        return output
