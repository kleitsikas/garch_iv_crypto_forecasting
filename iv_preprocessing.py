import pandas as pd
from datetime import datetime

#symbols = ['GVZ', 'OVX']
symbols = ['GVZ']
for symbol in symbols:
    df = pd.read_csv(f'new_datasets/{symbol}.csv', delimiter=';')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['datetime'] = df['datetime'].dt.date
    df = df.sort_values(by='datetime')
    df.set_index('datetime', inplace=True)
    df = df.loc[df.index < pd.Timestamp('2024-12-01').date()]
    df = df.loc[df.index >= pd.Timestamp('2022-09-20').date()]
    df['close'] = df['close'].str.replace(',', '.')
    df['close'] = pd.to_numeric(df['close'])
    #df.drop(['symbol','open','high','low','volume'], inplace=True, axis=1)
    df.rename(columns = {'close':'implied_volatility'}, inplace = True) 
    df.to_csv(f"new_datasets/{symbol}_IV_NEW.csv")

'''
symbols = ['bviv', 'eviv']
for symbol in symbols:
    df = pd.read_json(f'new_datasets/{symbol}.json')
    timestamps = df['t']
    values = df['o']
    dates = [datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d') for ts in timestamps]
    df = pd.DataFrame({'datetime': dates, 'implied_volatility': values})
    df.to_csv(f'new_datasets/{symbol}_IV_NEW.csv', index=False)
    '''