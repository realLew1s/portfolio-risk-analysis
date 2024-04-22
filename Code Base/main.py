import sys
import json 
import time
import os

from modules.StockAnalysis import StockStatAnalyser
from modules.StockAnalysis import RSquaredCalculator
from modules.StockAnalysis import AssetBetas
from modules.PortfolioAnalysis import WeightedPortfolioStats
from modules.Visualisations import BreachStdVisual

from modules.StockAnalysis import DataPreparation


from utils.DataFetcher import DataFetcher


def main():
    if sys.argv != None and sys.argv[1] != None and sys.argv[2] != None:
        menu()
    else:
        sys.exit('Fatal Error: Missing arg2 & 3 : python.exe main.py <holdings_file> <api_key>')


def menu():
    os.system('cls')
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
    print("    [4] Weighted Portfolio Statistics         ")
    print("    [5] Visualize Distribution around mean    ")
    print("                                              ")
    print("    [EXIT] to exit the application...         ")
    print("                                              ")
    print("----------------------------------------------")

    selection = input("Select an option: ")
    
    api_key = sys.argv[2]
    
    with open(sys.argv[1], "r") as f:
        datafile = json.load(f)

    if selection == '1':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        outcome = stock_stats(datafile, api_key, fetched_data_period)
        if outcome == True:
            print('Generated Successfully (Indiv Stock Attributes.json), returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '2':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        index = input('Please input a index to score against: ')
        outcome = rsquared_calculator(datafile, index, api_key, fetched_data_period)
        if outcome == True:
            print('Generated RSquared figures (rsquared_data.json). Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '3':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        index = input('Please select index to calculate Beta against: ')
        outcome = beta_calculations(datafile, index, api_key, fetched_data_period)
        if outcome == True:
            print('Generated Beta figures (Asset Betas.json). Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '4':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        outcome = weighted_variance(datafile, api_key, fetched_data_period)
        if outcome == True:
            print('Generated weighted portfolio figures (Portfolio Statistics.json). Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '5':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        outcome = v_distribution_around_mean(datafile, api_key, fetched_data_period)
        if outcome == True:
            print('Completed. Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection.upper() == 'EXIT':
        sys.exit('Exiting...')

def stock_stats(holdings_file, api_key, fetched_data_period):
    fetcher = DataFetcher(api_key, fetched_data_period)
    get_stock_data = fetcher.get_stock_dfs(holdings_file)
    cleaner = DataPreparation()
    stock_df = cleaner.daily_price_change(get_stock_data)

    analysis_instance = StockStatAnalyser(stock_df, holdings_file)
    analysis_instance.stock_attributes()

    return True

def rsquared_calculator(datafile, index_code, api_key, fetched_data_period):
    fetcher = DataFetcher(api_key, fetched_data_period)
    cleaner = DataPreparation()
    
    stock_initial_df = fetcher.get_stock_dfs(datafile)
    index_initial_df = fetcher.index_data_fetcher(index_code)

    stock_df = cleaner.daily_price_change(stock_initial_df)
    index_df = cleaner.daily_price_change(index_initial_df)

    analysis_instance = RSquaredCalculator(stock_df, index_df)
    analysis_instance.calculate_rsquared()

    return True

def beta_calculations(datafile, index, api_key, fetched_data_period):
    fetcher = DataFetcher(api_key, fetched_data_period)
    cleaner = DataPreparation()

    stock_initial_df = fetcher.get_stock_dfs(datafile)
    index_initial_df = fetcher.index_data_fetcher(index)

    stock_df = cleaner.daily_price_change(stock_initial_df)
    index_df = cleaner.daily_price_change(index_initial_df)
    
    analysis_instance = AssetBetas(stock_df, index_df)
    analysis_instance.get_beta()

    return True

def weighted_variance(holdings, api_key, fetched_data_period):
    fetcher = DataFetcher(api_key, fetched_data_period)
    cleaner = DataPreparation()
    stock_data = fetcher.get_stock_dfs(holdings)
    stock_df = cleaner.daily_price_change(stock_data)

    w_portfolio_stats = WeightedPortfolioStats(stock_df, holdings)
    w_portfolio_stats.weighted_portfolio_statistics()

    return True

def v_distribution_around_mean(datafile, api_key, fetched_data_period):
    fetcher = DataFetcher(api_key, fetched_data_period)
    cleaner = DataPreparation()
    stock_data = fetcher.get_stock_dfs(datafile)
    stock_df = cleaner.daily_price_change(stock_data)

    analysis_instance = StockStatAnalyser(stock_df, datafile)
    stock_attributes = analysis_instance.stock_attributes()

    visualisation = BreachStdVisual(stock_df, stock_attributes)
    visualisation.stock_picker()

    return True

if __name__ == '__main__':
    main()