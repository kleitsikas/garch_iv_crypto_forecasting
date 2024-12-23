import pandas as pd
import numpy as np
from datetime import timedelta

#symbols = ['XBT','XET','XAU'] #'OVX'
symbols = ['USOUSD'] # because of different source than Bloomberg
for symbol in symbols:
    data = pd.read_csv(f'new_datasets/{symbol}_30m.csv')
    data['datetime'] = pd.to_datetime(data['datetime'])
    data = data.sort_values(by='datetime')

    #manipulation for bloomberg data
    '''
    data = pd.read_csv(f'new_datasets/{symbol}_30min.csv', delimiter=';')
    data['datetime'] = pd.to_datetime(data['datetime'], format='%d/%m/%y %H:%M')
    data = data.sort_values(by='datetime')
    data['datetime'] = data['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
    data['datetime'] = pd.to_datetime(data['datetime'])
    #data['open'] = data['open'].str.replace(',', '.')
    data['close'] = data['close'].str.replace(',', '.')
    #data['open'] = pd.to_numeric(data['open'])
    data['close'] = pd.to_numeric(data['close'])
    data.set_index('datetime', inplace=True)
    '''

    #'''
    data['open'] = pd.to_numeric(data['open'])
    data['close'] = pd.to_numeric(data['close'])
    data.set_index('datetime', inplace=True)
    #convert to UTC (minus 2 hours) for non-bloomberg data
    #data.index = data.index - timedelta(hours=2)
    data = data.drop(['symbol','open','high','low','volume'], axis=1)
    resampled_data = data

    missing_intervals = data[data.isnull().any(axis=1)]
    missing_intervals = missing_intervals.loc[missing_intervals.index < pd.Timestamp('2024-12-01 00:00:00')]
    missing_intervals = missing_intervals.loc[missing_intervals.index >= pd.Timestamp('2022-09-20 00:00:00')]
    print(len(missing_intervals))
    #'''

    #bloomberg manipulations
    '''
    data = data.resample('30T').first() # just to print the NaN dates for checking
    missing_intervals = data[data.isnull().any(axis=1)]
    missing_intervals = missing_intervals.loc[missing_intervals.index < pd.Timestamp('2024-12-01 00:00:00')]
    missing_intervals = missing_intervals.loc[missing_intervals.index >= pd.Timestamp('2022-09-20 00:00:00')]
    print(len(missing_intervals))
    resampled_data = data.resample('30T').first()
    resampled_data = resampled_data.sort_values(by='datetime')
    resampled_data = resampled_data.interpolate(method='linear')
    '''

    #calculate squared returns
    resampled_data['close_t-1'] = resampled_data['close'].shift(+1)
    resampled_data = resampled_data.tail(-1) #drop first row due to shift
    resampled_data['return^2'] = np.log(resampled_data['close']/resampled_data['close_t-1'])
    resampled_data['return^2'] = resampled_data['return^2']**2

    # drop first n rows that dont start at 00:00:00 and k last rows that dont end at 23:30:00
    resampled_data = resampled_data.loc[resampled_data.index < pd.Timestamp('2024-12-01 00:00:00')]
    resampled_data = resampled_data.loc[resampled_data.index >= pd.Timestamp('2022-09-20 00:00:00')]
    print(len(resampled_data))

    daily_variance = np.sqrt(resampled_data['return^2'].resample('D').sum())
    #print(daily_variance.loc[daily_variance.index >= pd.Timestamp('2023-01-01')])

    #'''
    #print(resampled_data)
    print(daily_variance.head(20))
    # Filter the last entry of each day
    final_data = resampled_data.resample('D').last()
    #print(final_data)
    #print(final_data)
    # Merge the daily variance with the last entries
    final_data['realized_volatility'] = daily_variance
    #print(final_data)
    # include only the trading days
    final_data = final_data.dropna(subset=['close'])
    final_data.drop(['close_t-1', 'return^2'], inplace=True, axis=1)
    #print(final_data)
    final_data.to_csv(f"new_datasets/{symbol}_RV_NEW.csv")
    #'''