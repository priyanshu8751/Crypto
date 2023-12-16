import pandas as pd
import talib as ta
import matplotlib.pyplot as plt
import os

from backtesting import Backtest, Strategy
import pandas as pd
from datetime import datetime, timedelta
import warnings
# warnings.warn('Error: A warning just appeared')
warnings.filterwarnings('ignore')
df = pd.DataFrame()

class crypto():
    def strategy(df):
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        df['EMA7'] = ta.EMA(df['close'], timeperiod=7)
        df['EMA14'] = ta.EMA(df['close'], timeperiod=14)
        df['EMA21'] = ta.EMA(df['close'],timeperiod=21)
        df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=14)
        df['macd'], df['macdsignal'],df['histogram'] = ta.MACD(df['close'],12,26,9)
        df.dropna(inplace = True)
        df['signal'] = 0
        inmarket = 0
        buy = 0
        open_price = -1
        # df['amount'] = 0
        df['sl'] = 0
        buy_sl = 0
        short_sl = 0
        c = 2
        for i in range(1,len(df)-1):
            if inmarket == 0:
                flag = 0
                # if(df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]+5 ) or (df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1] ) :
                #     flag = 1
                if(df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]+5 and df['histogram'][i]>=0) or (df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1] and df['histogram'][i]>=0) :
                    flag = 1
                # if(df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1]):
                #     flag = 1
                # if(df['EMA21'][i-1]<df['EMA21'][i] and df['EMA21'][i+1]+5 < df['EMA21'][i] ) or (df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1] ):
                #     flag = 2
                elif(df['EMA21'][i-1]<df['EMA21'][i] and df['EMA21'][i+1]+5 < df['EMA21'][i] and df['histogram'][i]<0) or (df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1] and df['histogram'][i]<0):
                    flag = 2
                # if(df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1]):
                #     flag = 2 
                if flag == 1:
                    buy = 1 
                    inmarket = 1 
                    df['signal'][i] = 1
                    buy_sl = df['close'][i] - c*df['ATR'][i]
                    df['sl'][i] = buy_sl
                    # open_price = df['open'][i]
                elif flag == 2:
                    buy = 0
                    inmarket = 1 
                    df['signal'][i] = -1 
                    short_sl = df['close'][i] + c*df['ATR'][i]
                    df['sl'][i] = short_sl
                    # open_price = df['open'][i]
            elif inmarket == 1:
                if buy == 1:
                    # if df['close'][i]<= buy_sl:
                    if (df['close'][i] <= df['sl'][i-1]) or (df['EMA14'][i-1]<df['EMA14'][i] and df['EMA14'][i+1] < df['EMA14'][i]) or (df['EMA7'][i-1]>df['EMA14'][i-1] and df['EMA7'][i+1]<df['EMA14'][i+1]):
                        inmarket = 0
                        df['signal'][i] = -1
                        df['sl'][i] = 0
                        buy_sl = 0
                    else:
                        temp_sl_buy = df['close'][i]-c*df['ATR'][i]
                        buy_sl = max(df['sl'][i-1],temp_sl_buy)
                        # df['sl'][i] = 0
                        df['sl'][i] = buy_sl
                        # buy_sl = 0
                elif buy == 0:
                    if (df['close'][i] >= df['sl'][i-1]) or (df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]) or (df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1]):
                        inmarket = 0
                        df['signal'][i] = 1
                        df['sl'][i] = 0
                        short_sl = 0
                    else:
                        temp_sl_short = df['close'][i]+c*df['ATR'][i]
                        short_sl = min(df['sl'][i-1], temp_sl_short)
                        # df['sl'][i] = 0
                        df['sl'][i] = short_sl

        df['sum'] = 0
        for i in range(1,len(df)):
            df['sum'][i] = df['sum'][i-1]+df['signal'][i-1]
        df.to_csv("Result_ATR_daily.csv")
        return df

    def strategy2(df):
        # df = pd.read_csv("DailyData_18-22.csv")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        df['EMA7'] = ta.EMA(df['close'], timeperiod=7)
        df['EMA14'] = ta.EMA(df['close'], timeperiod=14)
        df['EMA21'] = ta.EMA(df['close'],timeperiod=21)
        df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=14)
        df['macd'], df['macdsignal'],df['histogram'] = ta.MACD(df['close'],12,26,9)
        df.dropna(inplace = True)
        df['signal'] = 0
        inmarket = 0
        buy = 0
        open_price = -1
        # df['amount'] = 0
        df['sl'] = 0
        buy_sl = 0
        short_sl = 0
        c = 2
        for i in range(1,len(df)-1):
            if inmarket == 0:
                flag = 0
                # if(df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]+5 ) or (df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1] ) :
                #     flag = 1
                if(df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]+5 and df['histogram'][i]>=0) or (df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1] and df['histogram'][i]>=0) :
                    flag = 1
                # if(df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1]):
                #     flag = 1
                # if(df['EMA21'][i-1]<df['EMA21'][i] and df['EMA21'][i+1]+5 < df['EMA21'][i] ) or (df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1] ):
                #     flag = 2
                elif(df['EMA21'][i-1]<df['EMA21'][i] and df['EMA21'][i+1]+5 < df['EMA21'][i] and df['histogram'][i]<0) or (df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1] and df['histogram'][i]<0):
                    flag = 2
                # if(df['EMA7'][i-1]>df['EMA21'][i-1] and df['EMA7'][i+1]<df['EMA21'][i+1]):
                #     flag = 2 
                if flag == 1:
                    buy = 1 
                    inmarket = 1 
                    df['signal'][i] = 1
                    buy_sl = df['close'][i] - c*df['ATR'][i]
                    df['sl'][i] = buy_sl
                    # open_price = df['open'][i]
                elif flag == 2:
                    buy = 0
                    inmarket = 1 
                    df['signal'][i] = -1 
                    short_sl = df['close'][i] + c*df['ATR'][i]
                    df['sl'][i] = short_sl
                    # open_price = df['open'][i]
            elif inmarket == 1:
                if buy == 1:
                    # if df['close'][i]<= buy_sl:
                    if (df['close'][i] <= df['sl'][i-1]) or (df['EMA14'][i-1]<df['EMA14'][i] and df['EMA14'][i+1] < df['EMA14'][i]) or (df['EMA7'][i-1]>df['EMA14'][i-1] and df['EMA7'][i+1]<df['EMA14'][i+1]):
                        inmarket = 0
                        df['signal'][i] = -1
                        df['sl'][i] = 0
                        buy_sl = 0
                    else:
                        temp_sl_buy = df['close'][i]-c*df['ATR'][i]
                        buy_sl = max(df['sl'][i-1],temp_sl_buy)
                        # df['sl'][i] = 0
                        df['sl'][i] = buy_sl
                        # buy_sl = 0
                elif buy == 0:
                    if (df['close'][i] >= df['sl'][i-1]) or (df['EMA7'][i-1]>df['EMA7'][i] and df['EMA7'][i+1] > df['EMA7'][i]) or (df['EMA7'][i-1]<df['EMA21'][i-1] and df['EMA7'][i+1]>df['EMA21'][i+1]):
                        inmarket = 0
                        df['signal'][i] = 1
                        df['sl'][i] = 0
                        short_sl = 0
                    else:
                        temp_sl_short = df['close'][i]+c*df['ATR'][i]
                        short_sl = min(df['sl'][i-1], temp_sl_short)
                        # df['sl'][i] = 0
                        df['sl'][i] = short_sl

        df['sum'] = 0
        for i in range(1,len(df)):
            df['sum'][i] = df['sum'][i-1]+df['signal'][i-1]
        df.to_csv("Result_ATR_daily.csv")
        return df
    # -*- coding: utf-8 -*-

    def count(df):
        # df = pd.DataFrame()
        # df = pd.read_csv("Result_ATR_daily.csv")
        df['datetime'] = pd.to_datetime(df['datetime'])
        df.set_index('datetime', inplace=True)
        cnt = 0
        for i in range(len(df)):
            if df['signal'][i]==1:
                cnt += 1
        print(cnt)
        return cnt
    # df['pnl'] = 0
    # for i in range(len(df)):
        
    def modify_df(df):
        df['Close'] = df['close']
        df['Open'] = df['open']
        df['Low'] = df['low']
        df['High'] = df['high']
        df['Volume'] = df['volume']
        df['Open'] /= 1e6
        df['High'] /= 1e6
        df['Low'] /= 1e6
        df['Close'] /= 1e6
        return df

class MyStrat(Strategy):
    def init(self):
        pass
        # self.current_money = 500
        # self.lots = 0
        # self.TradeOpen = 'N'

    def next(self):
        if self.data['sum'] == 0:
            if self.data['signal'] == 1:
                self.buy()
            elif self.data['signal'] == -1:
                self.sell()
        else:
            if self.data['signal'] == -1 or self.data['signal']== 1:
                self.position.close()


def backtest(df):
    bt = Backtest(df, MyStrat, cash=1000, commission=0.001,trade_on_close=True)
    result = bt.run()
    bt.plot(superimpose=False)
    return bt
    # bt.plot()

def handwritten_backtest(df):
    df['pnl'] = 0
    df['days'] = 0
    d = 0
    entry_price = 0
    pos_pnl = 0
    neg_pnl = 0
    total_pnl = 0
    NoWinningTrade = 0
    NoLossingTrade = 0
    for i in range(len(df)-1):
        if df['sum'][i] == 0:
            d = 0
            if df['signal'][i] == 1:
                entry_price = df['open'][i+1]
            elif df['signal'][i] == -1:
                entry_price = df['open'][i+1]
        else:
            if df['signal'][i] == 1:
                df['pnl'][i] = (entry_price - df['close'][i])*(1000/entry_price)
                df['days'][i] = d+2
            elif df['signal'][i] == -1:
                df['pnl'][i] = (df['close'][i]-entry_price)*(1000/entry_price)
                df['days'][i] = d+2
            else:
                d += 1
    import sys
    max_int = sys.maxsize
    MaxLossingTrade = max_int
    min_int = -sys.maxsize - 1
    MaxWinningTrade = min_int
    for i in range(len(df)):
        if df['pnl'][i] >0:
            pos_pnl += df['pnl'][i]
            NoWinningTrade += 1
            MaxWinningTrade = max(MaxWinningTrade,df['pnl'][i])
        elif df['pnl'][i]<0:
            neg_pnl += df['pnl'][i]
            NoLossingTrade += 1
            MaxLossingTrade = min(MaxLossingTrade,df['pnl'][i])

    print("Positive PnL is",pos_pnl)
    print("negative PnL is",neg_pnl)
    print("total PnL(Gross Profit) is", pos_pnl+neg_pnl)
    print("Win[%] is", NoWinningTrade/(NoWinningTrade+NoLossingTrade)*100)
    print("Largest Winning Trade is",MaxWinningTrade)
    print("Largest Lossing Trade is",MaxLossingTrade)
    print("Avg. winning trade is",pos_pnl/NoWinningTrade)
    print("Avg. Lossing trade is",neg_pnl/NoLossingTrade)
    df.to_csv("ResultWithPnLUpdated.csv")

def main():
    df = pd.read_csv("")
    df = crypto.strategy(df)
    df = crypto.modify_df(df)
    # backtest(df)
    # handwritten_backtest(df)

if __name__ == "__main__":
    main()