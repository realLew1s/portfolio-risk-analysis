import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Enables access to utils from this dir


from modules.StockAnalysis import StockStatAnalyser

import pandas as pd # type: ignore
import numpy as np
import json
import math
from itertools import combinations 

from utils.DataFetcher import DataFetcher
from modules.StockAnalysis import DataPreparation


class WeightedPortfolioStats:
    def __init__(self, stock_data, stock_list):
        self.stock_data = stock_data
        self.stock_list = stock_list

    def weighted_portfolio_statistics(self):
        unique_stocks = self.stock_data['stock_code'].unique()

        combos = combinations(unique_stocks, 2)
        
        data_list = []

        for item in combos:
            stock_one, stock_two = item
            stock_one_weighting, stock_two_weighting = self.fetch_weightings(stock_one, stock_two)
            

            stock_one_df = self.stock_data[self.stock_data['stock_code'] == stock_one].copy()
            stock_two_df = self.stock_data[self.stock_data['stock_code'] == stock_two].copy()
            
            stock_one_returns, stock_two_returns = self.match_timescales(stock_one_df, stock_two_df)

            stock_one_avg_ret = np.mean(stock_one_returns)
            stock_two_avg_ret = np.mean(stock_two_returns)

            stock_one_std = np.std(stock_one_returns)
            stock_two_std=  np.std(stock_two_returns)

            covariance = sum((s1 - stock_one_avg_ret)*(s2 - stock_two_avg_ret) for s1, s2 in zip(stock_one_returns, stock_two_returns)) / (len(stock_one_returns) - 1)

            temp_dictionary = {
                "stockA": stock_one,
                "stockB": stock_two,
                "s1_std": stock_one_std,
                "s2_std": stock_two_std,
                "s1_mean": stock_one_avg_ret,
                "s2_mean": stock_two_avg_ret,
                "s1_weighting": stock_one_weighting,
                "s2_weighting": stock_two_weighting,
                "covariance": covariance
            }

            data_list.append(temp_dictionary)

        weighted_var = self.construct_weighted_variance(data_list, unique_stocks)

        output = {
            "weighted_variance": weighted_var,
            "weighted_std": math.sqrt(weighted_var)
        }

        with open('Portfolio Statistics.json', "w") as f:
            json.dump(output, f, indent=1)

        print(f"Portfolio Standard Deviation: {round(math.sqrt(weighted_var) * 100, 2)}%")

    def construct_weighted_variance(self, data_list, unique_stocks):
        # I am concious the below doesn't take into account the differing timescales (not sure on a way around this at this stage, as each combination has a different timescale. Unless I fix it which I don't wish to do currently)
        data = []
        for item in self.stock_list:
            stock_df = self.stock_data[self.stock_data['stock_code'] == item['stock_code']]

            stock_var = stock_df['change_percentage'].var()
            seg_one = item['weighting']*stock_var
            data.append(seg_one)

        part_one = sum(data)
        
        weighted_variance = part_one

        for x in data_list:
            weighted_variance += 2*(x['s1_weighting'])*(x['s2_weighting'])*(x['covariance'])

        return weighted_variance

    def fetch_weightings(self, stock_one, stock_two):
        for item in self.stock_list:
            
            if item['stock_code'] == stock_one:
                stock_one_weighting = item['weighting']
            elif item['stock_code'] == stock_two:
                stock_two_weighting = item['weighting']
        
        return stock_one_weighting, stock_two_weighting
    
    def match_timescales(self, stock_one_df, stock_two_df):
        merged_df = stock_one_df.merge(stock_two_df, on='date', how='inner')

        stock_one_returns = merged_df['change_percentage_x'].tolist()
        stock_two_returns = merged_df['change_percentage_y'].tolist()

        return stock_one_returns, stock_two_returns

