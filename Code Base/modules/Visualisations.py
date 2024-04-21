import matplotlib.pyplot as plt
import pandas as pd # type: ignore

class BreachStdVisual:
    def __init__(self, stock_data, stock_attributes):
        self.stock_data = stock_data
        self.stock_attributes = stock_attributes
    
    def stock_picker(self):
        for item in self.stock_attributes:
            data_set = []
            stock_df = self.stock_data[self.stock_data['stock_code'] == item['stock_code']]
            for index, row in stock_df.iterrows():
                z_score = ((row['change_percentage'] - item['mean_returns']) / item['std_returns'])
                data_set.append(z_score)
            
            plt.hist(data_set, bins=300)
            plt.xlabel('Z-Score')
            plt.ylabel('Frequency')
            plt.title(f"{item['stock_code']} | Distribution of change percentage around the mean")
            plt.show()

