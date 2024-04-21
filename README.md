# Fundamental Portfolio Statistics

A very basic application to showcase pythons use for getting statistical attributes dynamically from a third party api, current features include:
  - Asset Standard Deviation, Variance & Average Returns
  - R Squared Calculation (against your target index i.e AXJO.INDX)
  - Asset Beta's (against your target index i.e. AXJO.INDX)
  - Weighted Portfolio Statistics (weighted standard deviation)

![image](https://github.com/realLew1s/portfolio-risk-analysis/assets/131590570/c9f8a6d4-5dfd-409b-825a-437516849d0d)

## Requirements

Requires an API key to EODHD which is an API provider of EOD historical price data (open / close price since data of listing).

## Usage

```
python main.py <portfolio_assets> <api_key>
```

Requires you to create a JSON file with the following elements, for dynamic data sourcing. Please note any portfolios total weighting should add to 1:

```
{
  "stock_code": "CBA",
  "exchange_code": "AU",
  "weighting": 1
}
```

## TODO

- Add a visualisation to show the distribution of an asset exceeding 1 std deviation in daily shareprice movement
- Ability to set your period for the data/calculations i.e. daily/weekly/monthly/quarterly
- Ability to load a shortlist and identify the best option to add to your portfolio based on the new portfolio beta as a result of the new addition
- Look at adding simulation/portfolio testing i.e. (Monte Carlos)

## Final Notes

This project was created to showcase python/statistical knowledge. There is no guarantee the output is correct, and should not be used to make investment decisions.
