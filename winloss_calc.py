#!/usr/bin/env python3

import pandas as pd

# Global win/loss value.
win = 0.0
loss = 0.0

def sell(sell_size, sell_price, orders):
    global win, loss
    # Read the last buy order from the FIFO list.
    last = orders[-1]
    
    # Last BUY is bigger than SELL. Keep and edit the position.
    if last['size'] > sell_size:
        loss += last['size'] * last['price']
        win += sell_size * sell_price
        # Edit the position.
        last['size'] -= sell_size
    # SELL size is bigger or equal than last BUY.
    # Eat up the last position and proceed with next.
    else:
        # Calculate size to take from the next position.
        loss += last['size'] * last['price']
        win += last['size'] * sell_price
        # Recurse to eat from the next BUY order
        sell(sell_size - last['size'], sell_price, orders[:-1])


def main():
    # Read CSV with pandas.
    df = pd.read_csv('fills.csv')

    # Buy positions to work with.
    positions = []

    # Iterate CSV line by line.
    for index, row in df.iterrows():
        
        size = float(row['size'])
        price = float(row['price'])

        if row['side'] == 'BUY':
            positions.append({
                'size' : size,
                'price' : price
            })
        else:
            sell(size, price, positions)

    print('Win = ' + str(win))
    print('Loss = ' + str(loss))
    print('Total = ' + str(win - loss))
   
main()
        