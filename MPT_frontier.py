import pandas as pd
import numpy as np
import yfinance as yf
from matplotlib import pyplot as plt
from datetime import datetime, timedelta
from scipy.optimize import minimize, Bounds, LinearConstraint


def risk(weights, cov_matrix):
    return np.matmul(np.matmul(weights, cov_matrix), weights)


def efficient_frontier(mark_port, tgt_ret_vec=np.arange(2, 50, 3)/100, show=False):
    ret_vec, risk_vec, lev_vec = [], [], []

    for ret in tgt_ret_vec:
        mark_port.tgt_ret = ret
        mark_port.solve()

        ret_vec.append(ret)
        risk_vec.append(mark_port.volatility)
        lev_vec.append(mark_port.leverage)

    #print(ret_vec)
    #print(risk_vec)
    #print(lev_vec)
    """
    plt.scatter(risk_vec, ret_vec)
    plt.xlabel('Risk')
    plt.ylabel('Return')
    plt.title('Efficient Frontier')
    plt.show()

    plt.scatter(risk_vec, lev_vec)
    plt.xlabel('Risk')
    plt.ylabel('Leverage')
    plt.title('Leverage Ratio vs Risk for Frontier')
    plt.show()
    """

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, sharex=True)
    ax1.set_title('Efficient Frontier')
    ax1.set_ylabel('Return')
    ax1.scatter(risk_vec, ret_vec)

    ax2.set_title('Leverage Ratio vs Risk for Frontier')
    ax2.set_xlabel('Risk')
    ax2.set_ylabel('Leverage Ratio')
    ax2.scatter(risk_vec, lev_vec)

    if show:
        plt.show()

    return fig, (ax1, ax2)


class Markowitz:
    def __init__(self, tickers, trade_start, lookback=60,
                 max_holding=0.5, long_only=False, tgt_ret=0.08):
        """
        :param tickers: List of stock tickers (strings) for universe considered
        :param trade_start: datetime date for first day buy portflio
        :param lookback: Integer, number of days before trade_start to use in getting asset returns
                            and Covariance matrix
        :param max_holding: Floating between 0 and 1. Represents max weight assigned to any one stock
        :param long_only: Boolean, True if short selling not allowed
        :param tgt_ret: Floating number for the annualized target return of the portfolio
        """
        self.tickers = tickers
        self.trade_start = trade_start
        self.lookback = lookback
        self.max_holding = max_holding
        self.long_only = long_only
        self.tgt_ret = tgt_ret

        # Get return data for stock universe from Yahoo Finance
        start = trade_start - timedelta(days=lookback + 1)
        end = trade_start - timedelta(days=1)
        prices = yf.download(tickers=tickers, start=start, end=end)['Adj Close']
        returns = np.log(prices) - np.log(prices).shift(1)
        returns = returns.dropna()
        print('')

        self.avg_ret = returns.mean()
        self.cov = returns.cov()
        self.holdings = None
        self.volatility = None
        self.leverage = None

    def __repr__(self):
        desc = '\n'.join([
            'This is a Markowitz Portfolio Object with...',
            f'Target Return: {self.tgt_ret} and Max Individual Asset weight: {self.max_holding}',
            f'The first day to buy this portfolio: {self.trade_start}',
            f'Asset returns and risk data were estimated from a {self.lookback} day leading window',
            ''
        ])
        return desc

    def solve(self):
        w0 = np.ones(len(self.tickers))/len(self.tickers)
        daily_tgt = self.tgt_ret / 252

        if self.long_only:
            bound = Bounds(lb=np.zeros(len(self.tickers)), ub=np.zeros(len(self.tickers))+self.max_holding)
        else:
            bound = Bounds(lb=np.zeros(len(self.tickers))-self.max_holding,
                           ub=np.zeros(len(self.tickers))+self.max_holding)

        def exp_return(weights):
            return np.matmul(self.avg_ret.to_numpy(), weights) - daily_tgt

        def fully_invested(weights):
            return weights.sum() - 1

        cons = [{'type': 'eq', 'fun': exp_return},
                {'type': 'eq', 'fun': fully_invested}]

        result = minimize(risk, w0, method='trust-constr',
                          constraints=cons, bounds=bound,
                          args=(self.cov.to_numpy()), options={'verbose': 0})

        self.holdings = pd.DataFrame(result.x, index=self.cov.index)[0]
        self.volatility = risk(result.x, cov_matrix=self.cov.to_numpy()) ** (1/2) * 252 ** (1/2)
        self.leverage = abs(self.holdings).sum()


        #print('Solution Suceeded')
        #print(f'Expected Annual Return: {(np.matmul(result.x, self.avg_ret.to_numpy()) +1)**252-1}')
        #print(f'Annual Volatility: {self.volatility}')
        #print(f'Check Weight Sum {self.holdings.sum()}')
        #print(f'Leverage Ratio: {self.leverage}')
        #print('')


if __name__ == '__main__':
    universe = ['UNH', 'MSFT', 'GS', 'HD', 'MCD',
               'CAT', 'AMGN', 'V', 'BA', 'CRM',
               'HON', 'AAPL', 'TRV', 'AXP', 'JNJ',
               'CVX', 'WMT', 'PG', 'JPM', 'IBM',
               'NKE', 'MRK', 'MMM', 'DIS', 'KO',
               'DOW', 'CSCO', 'VZ', 'INTC', 'WBA']


    Mark1 = Markowitz(tickers=universe, trade_start=datetime(2023, 5, 1), lookback=365,
                      max_holding=0.5, long_only=False, tgt_ret=0.05)
    #Mark1.solve()

    fig, axes = efficient_frontier(Mark1, show=True)

    fig.savefig('frontier_plot.png')





