import pandas as pd
import numpy as np
#symbols = ['XBT', 'XET', 'XAU', 'USOUSD']
symbols = ['XAU']
for symbol in symbols:
    iv_df = pd.read_csv(f'new_datasets/{symbol}_IV_NEW.csv')
    rv_df = pd.read_csv(f'new_datasets/{symbol}_RV_NEW.csv')
    iv_df['datetime'] = pd.to_datetime(iv_df['datetime'])
    rv_df['datetime'] = pd.to_datetime(rv_df['datetime'])
    merged_df = pd.merge(rv_df, iv_df, on='datetime', how='left')
    merged_df = merged_df.sort_values(by='datetime')
    merged_df.set_index('datetime', inplace=True)
    if symbol == 'USOUSD':
        full_date_range = pd.date_range(start=merged_df.index.min(), end=merged_df.index.max(), freq='D')  
        merged_df = merged_df.reindex(full_date_range)
        merged_df = merged_df.interpolate(method='linear')
        merged_df.index.name = 'datetime'
    else:
        merged_df = merged_df.interpolate(method='linear')
    #merged_df = merged_df.drop(['open'], axis=1)
    #calculate returns
    merged_df['realized_volatility_t-1'] = merged_df['realized_volatility'].shift(1)
    merged_df['returns'] = np.log(merged_df['close'] / merged_df['close'].shift(1))
    #print(merged_df['implied_volatility'])
    if symbol == 'XBT' or symbol == 'XET':
        trading_days = 365
    else:
        trading_days = 252
    merged_df['implied_volatility'] = merged_df['implied_volatility']/(100*np.sqrt(trading_days)) #365 for BTC, 252 for GOLD/OIL
    #print(merged_df['implied_volatility'])
    merged_df['iv_returns'] = np.log(merged_df['implied_volatility'] / merged_df['implied_volatility'].shift(1))
    merged_df.dropna(inplace=True)
    merged_df.to_csv(f'new_datasets/{symbol}_FINAL_NEW.csv')
