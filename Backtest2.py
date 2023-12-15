import pandas as pd
from backtesting import Backtest, Strategy
import warnings
warnings.filterwarnings("ignore")

def ideal(df, amount):
    
    flag_purchased = False
    units = 0
    signal = [0]
    max_amount = amount
    for i in range(0, len(df) - 1):

        if df['open'][i] > df['open'][i+1]:
            if flag_purchased:
                amount = units * df['open'][i]
                units = 0
                flag_purchased = False
                signal.append(-1)
            else:
                signal.append(0)

        else:
            if not flag_purchased:
                units = amount / df['open'][i]
                amount = 0
                signal.append(1)
                flag_purchased = True
            else:
                signal.append(0)

        max_amount = max(max_amount, units * df['open'][i])

    # signal.append(0)
    df['signal'] = signal

    print("INVESTMENT:", amount)
    print("UNITS:", units)
    print("MAX VAL:", max_amount)
    return df

def backtest(df):
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

def main():
    df = pd.read_csv("btcusdt_15m.csv")
    ideal(df, 100)
    df = backtest(df)
    bt = Backtest(df, MyStrat, cash=500, commission=0.00)
    result = bt.run()
    print(result)

if __name__ == "__main__":
    main()