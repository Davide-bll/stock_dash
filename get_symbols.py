import pandas as pd
from pytickersymbols import PyTickerSymbols

# parameters
path_out = 'data/symbols.csv'

# get stock by index
stock_data = PyTickerSymbols()
nasdaq = stock_data.get_stocks_by_index('NASDAQ 100')

# to pandas dataframe
df_nasdaq = pd.DataFrame(list(nasdaq))

# save csv
df_nasdaq.to_csv(path_out)