import sys
import json 
import time

from modules.StockAnalysis import StockStatAnalyser
from modules.StockAnalysis import RSquaredCalculator
from modules.StockAnalysis import AssetBetas

from modules.StockAnalysis import DataPreparation


from utils.DataFetcher import DataFetcher


def main():
    if sys.argv != None and sys.argv[1] != None and sys.argv[2] != None:
        menu()
    else:
        sys.exit('Fatal Error: Missing arg2 & 3 : python.exe main.py <holdings_file> <api_key>')


def menu():
    print("----------------------------------------------")
    print("   ______           __     ______       __    ")
    print("  / __/ /____  ____/ /__  / __/ /____ _/ /____")
    print(" _\ \/ __/ _ \/ __/  '_/ _\ \/ __/ _ `/ __(_-<")
    print("/___/\__/\___/\__/_/\_\ /___/\__/\_,_/\__/___/")
    print("                                              ")
    print("----------------------------------------------")
    print("                                              ")
    print("    [1] Std Deviation, Var & Avg Returns      ")
    print("    [2] R Squared Calculator (against a index)")
    print("    [3] Asset Beta's                          ")
    print("                                              ")
    print("    [EXIT] to exit the application...         ")
    print("                                              ")
    print("----------------------------------------------")

    selection = input("Select an option: ")
    
    api_key = sys.argv[2]
    
    with open(sys.argv[1], "r") as f:
        datafile = json.load(f)

    if selection == '1':
        outcome = stock_stats(datafile, api_key)
        if outcome == True:
            print('Generated Successfully (Indiv Stock Attributes.json), returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '2':
        index = input('Please input a index to score against: ')
        outcome = rsquared_calculator(datafile, index, api_key)
        if outcome == True:
            print('Generated RSquared figures (rsquared_data.json). Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '3':
        index = input('Please select index to calculate Beta against: ')
        outcome = beta_calculations(datafile, index, api_key)
        if outcome == True:
            print('Generated Beta figures (Asset Betas.json). Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection.upper() == 'EXIT':
        sys.exit('Exiting...')

def stock_stats(holdings_file, api_key):
    fetcher = DataFetcher(api_key)
    get_stock_data = fetcher.get_stock_dfs(holdings_file)
    cleaner = DataPreparation()
    stock_df = cleaner.daily_price_change(get_stock_data)

    analysis_instance = StockStatAnalyser(stock_df, holdings_file)
    analysis_instance.stock_attributes()

    return True

def rsquared_calculator(datafile, index_code, api_key):
    fetcher = DataFetcher(api_key)
    cleaner = DataPreparation()
    
    stock_initial_df = fetcher.get_stock_dfs(datafile)
    index_initial_df = fetcher.index_data_fetcher(index_code)

    stock_df = cleaner.daily_price_change(stock_initial_df)
    index_df = cleaner.daily_price_change(index_initial_df)

    analysis_instance = RSquaredCalculator(stock_df, index_df)
    analysis_instance.calculate_rsquared()

    return True

def beta_calculations(datafile, index, api_key):
    fetcher = DataFetcher(api_key)
    cleaner = DataPreparation()

    stock_initial_df = fetcher.get_stock_dfs(datafile)
    index_initial_df = fetcher.index_data_fetcher(index)

    stock_df = cleaner.daily_price_change(stock_initial_df)
    index_df = cleaner.daily_price_change(index_initial_df)
    
    analysis_instance = AssetBetas(stock_df, index_df)
    analysis_instance.get_beta()

    return True

if __name__ == '__main__':
    main()