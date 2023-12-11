# -*- coding: utf-8 -*-
"""
Created on Sun Nov 19 09:45:24 2023

@author: hp
"""

import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import os

# print(os.getcwd())

df = pd.read_csv("btcusdt_15m19-20.csv")
df['datetime'] = pd.to_datetime(df['datetime'])
df.set_index('datetime', inplace=True)
df['EMA7'] = ta.EMA(df['close'], timeperiod=7)
df['EMA21'] = ta.EMA(df['close'],timeperiod=21)
df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=14)
AllowedDrawDown = 0.4

# variables d
inmarket = 0
# inmarket = 0 means out of market and inmarket = 1 means in the market
CurrentAmount = []
tolerance = 5
# the stopless is when the price come 5% low as compared to the current value
lot = 0
signal = []
CurrentMoney = 100
open_price = 0
CurrentAmount.append(CurrentMoney)
signal.append(0)
lots = []
lots.append(0)
ReturnOnTrade = []
ReturnOnTrade.append(0)
'''Return on trade only tells about the till then in the trade what is the %return 
this return is not overall'''
for i in range(1,len(df)-1):
    if inmarket == 0:
        if (df['EMA7'][i-1] > df['EMA7'][i]) and (df['EMA7'][i] < df['EMA7'][i+1]):
            slippage = df['open'][i]*(0.001)
            lot = CurrentMoney/(df['open'][i]+slippage)
            inmarket = 1
            signal.append(1)
            ReturnOnTrade.append(0)
            open_price = df['open'][i]+slippage
        else:
            signal.append(0)
            ReturnOnTrade.append(0)
    else:
        ddflag = 0
        '''iterate back in the data till when we had buyed the position and check whether the maxdrawdown
        is more than 4% if it then leave the position, it the additional condition apart from 
        the crossover condition'''
        '''FromLastTrade for the number of candles since trade started'''
        FromLastTrade = 0
        k= i
        for j in reversed(range(k)):
            if signal[j] == 1:
                break
            else:
                FromLastTrade += 1
        '''LastMax for finding the maximum of Amount in current trade to find drawdown'''
        LastMax = max(CurrentAmount[-FromLastTrade:])
        
        # check what should be used here i used current money (df[amount])
        drawdown = (LastMax-CurrentMoney)/LastMax
        if(drawdown>=AllowedDrawDown): 
            ddflag = 1
        if(df['EMA7'][i] >= df['EMA21'][i]) and (df['EMA7'][i+1]<df['EMA21'][i+1]) or ddflag ==1 :
            CurrentMoney = df['close'][i]*lot*1.001
            '''multiplying by 1.1 because of slippage as of 0.1% of , there is not much affect 
            due the reasong that when we have bigger profits the no. of lots increases'''
            signal.append(-1)
            ret = ((df['close'][i]*1.001 - open_price)/open_price)*100
            ReturnOnTrade.append(ret)
            inmarket = 0
        else:
            # in market but the condition of leaving is not coming
            CurrentMoney = df['close'][i]*lot
            signal.append(0)
            ret = ((df['close'][i] - open_price)/open_price)*100
            ReturnOnTrade.append(ret)
    CurrentAmount.append(CurrentMoney)
    lots.append(lot)
CurrentAmount.append(CurrentMoney)
ReturnOnTrade.append(0)
signal.append(0)
lots.append(0)
df['signal'] = signal
df['Amount'] = CurrentAmount
df['Lots'] = lots
df['ReturnOnTrade'] = ReturnOnTrade
TotalTrades = 0
TotalProfitableTrade = 0
for i in range(0,len(df)):
    if df['signal'][i]==1:
        TotalTrades += 1
        OpenPrice = df['Amount'][i]
    elif df['signal'][i] == -1:
        if df['Amount'][i] >= OpenPrice:
            TotalProfitableTrade += 1

# print("Total number of trades are {}".format(TotalTrades))
# print("Total Profitable trades are {}".format(TotalProfitableTrade))
# print("Percentage of successful trades is {}".format((TotalProfitableTrade/TotalTrades)*100))
df.to_csv("ResultsAfterSlippage19-20withReturn.csv")
# plt.plot(df['Amount'], label='Amount', color='green')
# plt.savefig("ema plot")
df['Close'] = df['close']
df['Open'] = df['open']
df['Low'] = df['low']
df['High'] = df['high']
df['Volume'] = df['volume']
df['Open'] /= 1e6
df['High'] /= 1e6
df['Low'] /= 1e6
df['Close'] /= 1e6
# plt.show()

from backtesting import Backtest, Strategy

class MyStrat(Strategy):
    def init(self):
        self.current_money = 500
        self.lots = 0

    def next(self):
        slippage = self.data['Open'][-1] * 0.001  # Assuming slippage is 0.1%
        
        if self.data['signal'] == 1:
            # print(self.lots, self.current_money, slippage, self.data['Open'][-1])
            self.lots = self.current_money / (self.data['Open'][-1] + slippage)
            self.buy(sl=self.data['Open'][-1] - slippage, tp=self.data['Open'][-1] + slippage, limit=self.data['Open'][-1])
            self.current_money -= self.data['Open'][-1] * self.lots * 1.001  # Adjust for slippage
        elif self.data['signal'] == -1:
            # Use self.sell() to exit the long position
            self.sell(size = 1)
            # print(self.data, self.data['Close'])
            self.current_money += self.data['Close'][-1] * self.lots * 0.999  # Adjust for slippage and assuming no commission


# Assuming df is your DataFrame with OHLCV data
bt = Backtest(df, MyStrat, cash=500, commission=0.00)
result = bt.run()
print(result)