# -*- coding: utf-8 -*-
"""
Created on Wed Dec 13 11:06:13 2023

@author: hp
"""
""" This file contain all the condition including the shortsell condition also"""
import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import os
from datetime import datetime, timedelta
df = pd.DataFrame()

start_date = datetime(2023, 10, 1, 0, 0)  
end_date = datetime(2023, 10, 31, 23, 45)
datetime_series = pd.date_range(start=start_date, end=end_date, freq='15T')


df = pd.read_csv("BTCUSDT-15m-2023-10.csv")
df['datetime'] = datetime_series
# df = pd.read_csv("BTCUSDT-15m-2023-10.csv")
# df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)
df['EMA7'] = ta.EMA(df['close'], timeperiod=7)
df['EMA21'] = ta.EMA(df['close'],timeperiod=21)
df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=14)
df['signal'] = 0
inmarket = 0
buy = 0
# if inmarket == 1 and buy == 0 that is when we are taking shortsell condition

for i in range(1,len(df)-1):
    if inmarket==0:
        flag = 0
        if(df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]):
            flag = 1
        if(df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1]):
            flag = 1
        if(df['EMA21'][i-1]<df['EMA21'][i] and df['EMA21'][i+1] < df['EMA21'][i]):
            flag = 2
        if(df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1]):
            flag = 2 
        if flag == 1:
            buy = 1 
            inmarket = 1 
            df['signal'][i] = 1
        elif flag == 2:
            buy = 0
            inmarket = 1 
            df['signal'] = -1 
    elif inmarket == 1:
        if(df['signal'][i]!=0):
            continue
        if buy == 1:
            
            f = 0
            if(df['EMA21'][i-1]<df['EMA21'][i] and df['EMA21'][i+1] < df['EMA21'][i]):
                f = 1
            if(df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1]):
                f = 1 
            if f==1:
                buy = 0
                inmarket = 1 
                df['signal'][i] = -1 
                df['signal'][i+1] = -1 
        elif buy == 0:
            t= 0
            if(df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]):
                t=1 
            if(df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1]):
                t = 1 
            if t == 1 :
                buy = 1 
                inmarket = 1
                df['signal'][i] = 1 
                df['signal'][i+1] = 1

df.to_csv("ReturnShortSell-10.csv")

df['Close'] = df['close']
df['Open'] = df['open']
df['Low'] = df['low']
df['High'] = df['high']
df['Volume'] = df['volume']
df['Open'] /= 1e6
df['High'] /= 1e6
df['Low'] /= 1e6
df['Close'] /= 1e6
from backtesting import Backtest, Strategy

class MyStrat(Strategy):
    def init(self):
        # self.current_money = 500
        price = self.data.Close
    def next(self):
        if self.data['signal'] == 1:
            self.buy()
        elif self.data['signal'] == -1:
            self.sell()

bt = Backtest(df, MyStrat, cash=1000, commission=0.00)
result = bt.run()
#bt.plot()
print(result)

















