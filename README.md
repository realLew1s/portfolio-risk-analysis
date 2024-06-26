# Fundamental Portfolio Statistics

A very basic application to showcase pythons use for calcualting commonly used statistics for portfolio risk from a third party price history api, current features include:
  - Asset Standard Deviation, Variance & Average Returns
  - R Squared Calculation (against your target index i.e AXJO.INDX)
  - Asset Beta's (against your target index i.e. AXJO.INDX)
  - Weighted Portfolio Statistics (weighted standard deviation)
  - Visualisation of distribution of movements away from the mean
  - Weighted Portfolio Beta
  - Additional Asset impact on overall weighted portfolio Beta
  - Correlation Coefficient between each individual assets
  - Calculate CAPM based on your set Risk Free Rate & Expected Market Return

![image](https://github.com/realLew1s/portfolio-risk-analysis/assets/131590570/c1770286-d0e8-46c3-a948-d7a0f9fb1479)

## Requirements

Requires an API key to EODHD which is an API provider of EOD historical price data (open / close price since data of listing).

## Usage

```
python main.py <portfolio_assets> <api_key>
```

Requires you to create a JSON file with the following elements, for dynamic data sourcing. Please note any portfolios total weighting should add to 1, additionally the classification is up to you but is a mandatory element now. If anyone is actually using this, and you dont have a weighting just set them all to "GENERIC" or any placeholder.

```
{
  "stock_code": "CBA",
  "exchange_code": "AU",
  "classification": "Diversified"
  "weighting": 1
}
```

for shortlist data (i.e. for testing the effect of additional assets on weighted portfolio beta). It's important that you use a consistent weighting for all assets to ensure the output is accurate. (I personally use this when it is a marginal decision between the purchase of two assets and I either want to increase/decrease my weighted portfolio beta)

```
{
  "stock_code": "BHP",
  "exchange_code": "AU",
  "proposed_weighting": 0.25
}
```


## TODO

- ~~Add a visualisation to show the distribution of an asset exceeding 1 std deviation in daily shareprice movement~~
- ~~Ability to set your period for the data/calculations i.e. daily/weekly/monthly/quarterly~~
- Ability to load assets, and holding commencement date to get the retrospective daily return of your portfolio (assuming there is reinvestment this I believe is useful)
- ~~Ability to load a shortlist and identify the best option to add to your portfolio based on the new portfolio beta as a result of the new addition~~

## Final Notes

This project was created to showcase python/statistical knowledge. There is no guarantee the output is correct, and should not be used to make investment decisions.
