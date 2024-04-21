import json
import pandas as pd

class DataPreparation:
    def __init__(self, stock_data):
        self.stock_data = stock_data
    
    def daily_price_change(self):
        self.stock_data['change_percentage'] = (self.stock_data['close'] - self.stock_data['open']) / self.stock_data['open']
        return self.stock_data
    
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

