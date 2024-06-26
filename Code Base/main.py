import sys
import json 
import time
import os

from modules.StockAnalysis import StockStatAnalyser
from modules.StockAnalysis import RSquaredCalculator
from modules.StockAnalysis import AssetBetas
from modules.PortfolioAnalysis import WeightedPortfolioStats
from modules.Visualisations import BreachStdVisual
from modules.PortfolioAnalysis import PortfolioWeightedBeta
from modules.PortfolioAnalysis import AdditionalStockImpact
from modules.StockAnalysis import AssetCovariances
from modules.StockAnalysis import CAPM
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
    print("    [6] Weighted Portfolio Beta               ")
    print("    [7] Additional Asset Beta Impact          ")
    print("    [8] Correlation Coefficient               ")
    print("    [9] Calculate CAPM for each asset         ")
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
    elif selection == '6':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        index = input('Please input index to calculate Beta against: ')
        outcome = weighted_portfolio_beta(datafile, index, api_key, fetched_data_period)
        if outcome == True:
            print('Completed. Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '7':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        index = input('Please input index to calculate Beta against: ')
        shortlist_input = input('Please input the name of the shortlist file (i.e. shortlist.json): ')
        try:
            with open(shortlist_input, "r") as f:
                shortlist = json.load(f)
        except:
            print('Error, unk file sending back to menu..')
            time.sleep(0.5)
            menu()
        outcome = additional_stock_impact(datafile, index, shortlist, api_key, fetched_data_period)
        if outcome == True:
            print('Outputted options, and impact on the overall portfolio (Effect of new asset.json). Returning to menu in 5 seconds')
            time.sleep(5)
            menu()
    elif selection == '8':
        fetched_data_period = input('Please input time period, day = d, week = w, m = month: ')
        outcome = assess_covariance_inst(datafile, fetched_data_period, api_key)
        if outcome == True:
            print("Outputted asset correlations... returning to menu in 5 seconds")
            time.sleep(5)
            menu()
    elif selection == '9':
        risk_free = input('Please input a Risk Free Rate (i.e. 3month T-Bond): ')
        mr = input('Please input expected market return (i.e. avg ASX200 return over 5 yrs): ')
        outcome = capm_calculator(float(risk_free), float(mr))
        if outcome == True:
            print("Outputted required returns (CAPM), returning to menu in 5 seconds...") 
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

def weighted_portfolio_beta(datafile, index, api_key, fetched_data_period):
    fetcher = DataFetcher(api_key, fetched_data_period)
    cleaner = DataPreparation()

    stock_data = fetcher.get_stock_dfs(datafile)
    stock_df = cleaner.daily_price_change(stock_data)

    index_data = fetcher.index_data_fetcher(index)
    index_df = cleaner.daily_price_change(index_data)

    weighted_beta = PortfolioWeightedBeta(stock_df, index_df, datafile)
    weighted_beta.weighted_portfolio_beta()

    return True

def additional_stock_impact(datafile, index, shortlist, api_key, fetched_data_period):
    fetcher = DataFetcher(api_key, fetched_data_period)
    cleaner = DataPreparation()

    stock_data = fetcher.get_stock_dfs(datafile)
    stock_df = cleaner.daily_price_change(stock_data)

    shortlist_data = fetcher.get_stock_dfs(shortlist)
    shortlist_df = cleaner.daily_price_change(shortlist_data)

    index_data = fetcher.index_data_fetcher(index)
    index_df = cleaner.daily_price_change(index_data)

    asset_testing_inst = AdditionalStockImpact(stock_df, index_df, datafile, shortlist_df, shortlist)
    asset_testing_inst.calculate_best_option()
    
    return True

def assess_covariance_inst(datafile, fetched_data_period, api_key):
    fetcher = DataFetcher(api_key, fetched_data_period)
    cleaner = DataPreparation()

    stock_data = fetcher.get_stock_dfs(datafile)
    stock_df = cleaner.daily_price_change(stock_data)

    covar_inst = AssetCovariances(stock_df, datafile)
    
    covariance_out = covar_inst.assess_covariance()

    return True

def capm_calculator(rf, mr):
    try:
        with open('Asset Betas.json', "r") as f:
            beta_data = json.load(f)
    except:
        print('[ERROR] Please generate asset beta data first :)')
        exit()
    
    capm_instance = CAPM(beta_data, rf, mr)
    capm_instance.calc_capm()

    return True


if __name__ == '__main__':
    main()