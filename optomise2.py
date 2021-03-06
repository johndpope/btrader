import backtrader as bt
from datetime import datetime


class firstStrategy(bt.Strategy):
    params = (
        ("period", 21),
        ("rsi_low", 41),
        ("rsi_high", 66),
    )

    def __init__(self):
        self.startcash = self.broker.getvalue()
        self.rsi = bt.indicators.RSI_SMA(self.data.close, period=self.params.period)

    def next(self):
        if not self.position:
            if self.rsi < self.params.rsi_low:
                self.buy(size=100)
        else:
            if self.rsi > self.params.rsi_high:
                self.sell(size=100)

# INPUT DATA TO FEED INTO CEREBRO IS ADDED HERE
if __name__ == '__main__':
    # Variable for our starting cash
    startcash = 10000
    # Create an instance of cerebro
    cerebro = bt.Cerebro(optreturn=False)

    # Add our strategy
    cerebro.optstrategy(firstStrategy, period=range(10, 11), rsi_low=range(30, 40), rsi_high=range(55, 75))

    # Get Apple data from Yahoo Finance.
    data = bt.feeds.YahooFinanceData(
        dataname='MSFT',
        fromdate=datetime(2016, 1, 1),
        todate=datetime(2018, 1, 1),
        buffered=True
    )

    # Add the data to Cerebro
    cerebro.adddata(data)

    # Set our desired cash start
    cerebro.broker.setcash(startcash)

    # RUN STRATEGY THROUGH CEREBRO USING INPUT DATA
    opt_runs = cerebro.run()

    # CREATE A LIST VARIABLE THAT CONTAINS RESULTS
    final_results_list = []
    for run in opt_runs:
        for strategy in run:
            value = round(strategy.broker.get_value(), 2)
            PnL = round(value - startcash, 2)
            period = strategy.params.period
            rsi_low = strategy.params.rsi_low
            rsi_high = strategy.params.rsi_high
            final_results_list.append([period, rsi_low, rsi_high, PnL])

    # Sort Results List
    by_period = sorted(final_results_list, key=lambda x: x[0])
    by_PnL = sorted(final_results_list, key=lambda x: x[3], reverse=True)

    # Print results
    #print('Results: Ordered by period:')
    #for result in by_period:
        #print('Period: {}, rsi_low: {}, rsi_high: {}, PnL: {}'.format(result[0], result[1], result[3], result[4]))
    print('Results: Ordered by Profit:')
    for result in by_PnL:
        print('Period: {}, rsi_low: {}, rsi_high: {}, PnL: {}'.format(result[0], result[1], result[2], result[3]))
