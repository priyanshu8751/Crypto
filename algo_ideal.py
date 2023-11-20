import pandas as pd

def ideal(filename, amount):
    
    df = pd.read_csv(filename)
    flag_purchased = False
    units = 0
    max_amount = amount
    for i in range(len(df) - 1):

        if df['open'][i] > df['open'][i+1]:
            if flag_purchased:
                amount = units * df['open'][i]
                units = 0
                flag_purchased = False

        else:
            if not flag_purchased:
                units = amount / df['open'][i]
                amount = 0
                flag_purchased = True

        max_amount = max(max_amount, units * df['open'][i])

    print("INVESTMENT:", amount)
    print("UNITS:", units)
    print("MAX VAL:", max_amount)

def main():
    ideal("btcusdt_3m.csv", 1)

if __name__ == "__main__":
    main()