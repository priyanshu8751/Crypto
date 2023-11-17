import pandas as pd
import talib as ta
import matplotlib.pyplot as plt

# what about after sell to current point
# check tolerance bruh

# ema : timestamp 7, 21 try
def final_bal(file_name, column, amount, fraction_change, time_period):

    df = pd.read_csv(file_name)
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    df['EMA'] = ta.EMA(df['close'], timeperiod=time_period)
    df['ATR'] = ta.ATR(df['high'], df['low'], df['close'], timeperiod=time_period)

    plt.plot(df['close'], label='Close Prices')
    plt.plot(df['EMA'], label=f'EMA {time_period} days', linestyle='--', color='red')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('EMA Plot')
    plt.legend()

    column_array = df[column].values
    column_array = [0] + column_array
    flag_purchased = 0
    tolerance = 0 # investment - 2atr
    units = 0
    current_price = []
    signal = []
    
    for i in range(0, len(column_array) - 1):

        if (flag_purchased == 0) and (column_array[i] < column_array[i-1]) and (column_array[i] < column_array[i+1]):
            units = amount / df['open'][i]
            amount = 0
            flag_purchased = 1
            tolerance = column_array[i] 
            signal.append(1)

        elif (flag_purchased == 1) and (column_array[i] <= tolerance):
            amount = units * df['close'][i]
            units = 0
            flag_purchased = 0
            signal.append(-1)

        elif (flag_purchased == 1) and ((column_array[i + 1] - column_array[i]) / column_array[i] >= fraction_change):
            amount = units * df['close'][i]
            units = 0
            flag_purchased = 0
            signal.append(-1)

        else:
            signal.append(0)

        if (flag_purchased == 0):
            current_price.append(amount)
        else:
            current_price.append(units * df['close'][i])

    if(units):
        amount = units * df['close'][len(df) - 1]
        signal.append(-1)
    else:
        signal.append(0)

    current_price.append(amount)

    df['signal'] = signal
    df['amount'] = current_price
    df.to_csv("btcusdt_15m_ema.csv")

    # print (df.loc[df['signal'] != 0])
    
    plt.plot(df['amount'], label='Amount', color='green')
    plt.savefig("ema plot")
    plt.show()
    
    print("Units we have", units)
    print("Investment we have", amount)

def main():
    final_bal("btcusdt_15m.csv", "EMA", 100, 7.9 / 360, 7)

if __name__ == "__main__":
    main()