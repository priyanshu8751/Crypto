import pandas as pd

def final_bal(file_name, column, amount, fraction_change):
    df = pd.read_csv(file_name)
    column_array = df[column].values
    column_array = [0] + column_array
    flag_purchased = 0
    tolerance = 0
    units = 0
    for i in range(1, len(column_array) - 1):
        if (flag_purchased == 0) and (column_array[i] < column_array[i-1]) and (column_array[i] < column_array[i+1]):
            units = amount / column_array[i]
            # amount = 0
            flag_purchased = 1
            tolerance = column_array[i] * 0.8
        if (flag_purchased == 1) and (column_array[i] <= tolerance):
            amount = units * column_array[i]
            # units = 0
            flag_purchased = 0
        if (flag_purchased == 1) and ((column_array[i + 1] - column_array[i]) / column_array[i] >= fraction_change):
            amount = units * column_array[i]
            # units = 0
            flag_purchased = 0
    print("Units we have", units)
    print("Investment we have", amount)

def main():
    final_bal("btcusdt_15m.csv", "open", 100, 10 / 360)

if __name__ == "__main__":
    main()