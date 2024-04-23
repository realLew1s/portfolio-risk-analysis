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
from modules.StockAnalysis import AssetBetas

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

class PortfolioWeightedBeta:
    def __init__(self, stock_data, index_data, stock_list):
        fetch_betas = AssetBetas(stock_data, index_data)
        self.beta_data = fetch_betas.get_beta()
        self.stock_list = stock_list

    def weighted_portfolio_beta(self):
        weighted_portfolio_beta = 0
        for item in self.stock_list:
            for x in self.beta_data:
                if item['stock_code'] == x['stock_code']:
                    weighted_portfolio_beta += item['weighting'] * x['beta']
        
        with open('Weighted Portfolio Beta.json', "w") as f:
            json.dump(weighted_portfolio_beta, f, indent=1)

        print(f"Weighted Portfolio Beta: {weighted_portfolio_beta}")
        return weighted_portfolio_beta
    
class AdditionalStockImpact:
    def __init__(self, stock_data, index_data, stock_list, shortlist_data, shortlist):
        self.stock_data = stock_data
        self.index_data = index_data
        self.shortlist_data = shortlist_data

        self.shortlist = shortlist
        self.stock_list = stock_list
    
    def calculate_best_option(self):
        
        # I under stand this is double handling of the betas -> gets calculated again in PortfolioWeightedBeta (this will be updated at a later date)
        portfolio_asset_betas = AssetBetas(self.stock_data, self.index_data)
        asset_betas = portfolio_asset_betas.get_beta()
        asset_betas_df = pd.DataFrame().from_dict(asset_betas)

        portfolio_weighted_beta = PortfolioWeightedBeta(self.stock_data, self.index_data, self.stock_list)
        weighted_pf_beta = portfolio_weighted_beta.weighted_portfolio_beta()
        
        shortlist_asset_betas = AssetBetas(self.shortlist_data, self.index_data)
        shortlist_betas = shortlist_asset_betas.get_beta()
        shortlist_betas_df = pd.DataFrame().from_dict(shortlist_betas)

        effect_of_new_asset = []
        for item in self.shortlist:
            adj_folio_weightings = []
            for x in self.stock_list:
                new_weighting = x['weighting'] / (1 + item['proposed_weighting'])
                asset_beta = asset_betas_df[asset_betas_df['stock_code'] == x['stock_code']]['beta'].values[0]
                returned_dict = {
                    "stock_code": x['stock_code'],
                    "adj_weighting": new_weighting,
                    "beta": asset_beta
                }
                adj_folio_weightings.append(returned_dict)
            
            new_weighted_beta = shortlist_betas_df[shortlist_betas_df['stock_code'] == item['stock_code']]['beta'].values[0]

            new_folio_weighting = new_weighted_beta * item['proposed_weighting']

            for j in adj_folio_weightings:
                new_folio_weighting += j['adj_weighting'] * j['beta']
                
            potential_beta = {
                "additional_asset": item['stock_code'],
                "asset_beta": new_weighted_beta,
                "proposed_weighting": item['proposed_weighting'],
                "portfolio_weighted_beta_with_asset": new_folio_weighting,
                "original_portfolio_weighted_beta": weighted_pf_beta,
            }
            effect_of_new_asset.append(potential_beta)
        
        with open('Effect of new asset.json', "w") as f:
            json.dump(effect_of_new_asset, f, indent=1)
        
        return effect_of_new_asset


            