import json
import pandas as pd # type: ignore
import statsmodels.api as sm # type: ignore
import os
import sys
import numpy as np
import itertools

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Enables access to utils from this dir

from utils.DataFetcher import DataFetcher

class DataPreparation:
    def daily_price_change(self, data_frame):
        data_frame['change_percentage'] = (data_frame['close'] - data_frame['open']) / data_frame['open']
        return data_frame
    
class StockStatAnalyser: 
    def __init__(self, stock_data, stock_list):
        self.stock_data = stock_data
        self.stock_list = stock_list

    def average_returns(self):
        average_returns = []
        for entry in self.stock_list:
            stock_df = self.stock_data[self.stock_data['stock_code'] == entry['stock_code']].copy()
            stock_avg_return = stock_df['change_percentage'].mean()
            temp_dictionary = {
                "stock_code": entry['stock_code'],
                "avg_return": stock_avg_return
            }
            average_returns.append(temp_dictionary)
        return average_returns
    
    def std_deviation(self):
        std_deviation = []
        for entry in self.stock_list:
            stock_df = self.stock_data[self.stock_data['stock_code'] == entry['stock_code']].copy()
            stock_std_deviation = stock_df['change_percentage'].std()
            temp_dictionary = {
                "stock_code": entry['stock_code'],
                "std_deviation": stock_std_deviation
            }
            std_deviation.append(temp_dictionary)
        return std_deviation
    
    def variance(self):
        variance = []
        for entry in self.stock_list:
            stock_df = self.stock_data[self.stock_data['stock_code'] == entry['stock_code']].copy()
            stock_variance = stock_df['change_percentage'].var()
            temp_dictionary = {
                "stock_code": entry['stock_code'],
                "variance": stock_variance
            }
            variance.append(temp_dictionary)
        return variance
    
    def stock_attributes(self):
        all_attributes = []
        for entry in self.stock_list:
            stock_df = self.stock_data[self.stock_data['stock_code'] == entry['stock_code']].copy()
            stock_mean = stock_df['change_percentage'].mean()
            stock_std = stock_df['change_percentage'].std()
            stock_var = stock_df['change_percentage'].var()

            temp_dictionary = {
                "stock_code": entry['stock_code'],
                "mean_returns": stock_mean,
                "std_returns": stock_std,
                "var_returns": stock_var
            }
            all_attributes.append(temp_dictionary)
        
        with open('Indiv Stock Attributes.json', "w") as f:
            json.dump(all_attributes, f, indent = 1)

        return all_attributes

class RSquaredCalculator:
    def __init__(self, stock_data, index_data):
        self.stock_data = stock_data
        self.index_data = index_data
        self.unique_stocks = self.stock_data['stock_code'].unique()

    def calculate_rsquared(self):
        data = []
        for entry in self.unique_stocks:
            stock_df = self.stock_data[self.stock_data['stock_code'] == entry].copy()
            y_axis, x_axis = self.match_timescale(stock_df)

            x_axis = sm.add_constant(x_axis)
            model = sm.OLS(y_axis, x_axis)
            fitted = model.fit()

            temp_dictionary = {
                "stock_code": entry,
                "r_squared": fitted.rsquared
            }
            data.append(temp_dictionary)
        
        with open('rsquared_data.json', "w") as f:
            json.dump(data, f, indent=1)

    def match_timescale(self, stock_df):
        merged_df = stock_df.merge(self.index_data, on='date', how='inner')
        stock_returns = merged_df['change_percentage_x'].tolist()
        index_returns = merged_df['change_percentage_y'].tolist()
        return stock_returns, index_returns
        
class AssetBetas:
    def __init__(self, stock_data, index_data):
        self.stock_data = stock_data
        self.index_data = index_data

    def get_beta(self):
        unique_data = self.stock_data['stock_code'].unique()
        data = []
        for entry in unique_data:
            stock_df = self.stock_data[self.stock_data['stock_code'] == entry].copy()
            stock_returns, index_returns = self.match_timescale(stock_df)

            stock_mean = np.mean(stock_returns)
            index_mean = np.mean(index_returns)

            index_variance = np.var(index_returns)
            if index_variance == 0:
                beta = 0
            else:
                covariance = sum((s_ret - stock_mean)*(i_ret - index_mean) for s_ret, i_ret in zip(stock_returns, index_returns)) / (len(stock_returns) - 1)
                beta = covariance / index_variance
        
            temp_dict = {
                "stock_code": entry,
                "beta": beta
            }
            
            data.append(temp_dict)
        
        with open('Asset Betas.json', "w") as f:
            json.dump(data, f, indent=1)
        return data


    def match_timescale(self, stock_df):
        merged_df = stock_df.merge(self.index_data, on='date', how='inner')
        returns_stock = merged_df['change_percentage_x'].tolist()
        returns_index = merged_df['change_percentage_y'].tolist()
        print(f"{len(returns_stock)} vs {len(returns_index)}")
        print(merged_df.head())

        return returns_stock, returns_index 
