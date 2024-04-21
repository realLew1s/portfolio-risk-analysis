import requests # type: ignore
import pandas as pd # type: ignore
import sys

class DataFetcher:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = 'https://eodhd.com/api/eod/'

    def get_stock_dfs(self, holdings):
        dictionary_data = []
        for entry in holdings:
            stock_data = self.fetch_data(entry['stock_code'], entry['exchange_code'])
            stock_df = pd.DataFrame.from_dict(stock_data)
            stock_df['stock_code'] = entry['stock_code']
            dictionary_data.append(stock_df)
        return pd.concat(dictionary_data, ignore_index=True)

    def fetch_data(self, stock_code, exchange_code):
        try:
            data_request = requests.get(f"{self.base_url}{stock_code}.{exchange_code}?api_token={self.api_key}&fmt=json").json()
        except:
            sys.exit(f"Fatal Error: Could not fetch data for {stock_code}.{exchange_code}")
        return data_request
    
    def index_data_fetcher(self, index_code):
        try:
            data_request = requests.get(f"{self.base_url}{index_code}?api_token={self.api_key}&from=2020-01-01&fmt=json").json()
        except:
            sys.exit(f"Fatal Error: Could not fetch data for {index_code}")
        return pd.DataFrame.from_dict(data_request)

