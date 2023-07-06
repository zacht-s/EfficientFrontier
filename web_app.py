from flask import Flask, render_template, request, url_for
from MPT_frontier import Markowitz, efficient_frontier
from datetime import datetime

app = Flask(__name__)

dow_stocks = {'AAPL': 'Apple', 'AMGN': 'Amgen', 'AXP': 'American Express', 'BA': 'Boeing', 'CAT': 'Caterpillar',
              'CRM': 'Salesforce Inc', 'CSCO': 'Cisco', 'CVX': 'Chevron', 'DIS': 'Disney', 'DOW': 'Dow Chemical',
              'GS': 'Goldman Sachs', 'HD': 'Home Depot', 'HON': 'Honeywell', 'IBM': 'IBM', 'INTC': 'Intel',
              'JNJ': 'Johnson & Johnson', 'JPM': 'JP Morgan', 'KO': 'Coca Cola', 'MCD': 'McDonalds', 'MMM': '3M',
              'MRK': 'Merck & Co Inc', 'MSFT': 'Microsoft', 'PG': 'Proctor & Gamble', 'TRV': 'Travelers Companies Inc',
              'TSLA': 'Tesla', 'UNH': 'United Health', 'V': 'Visa', 'VZ': 'Verizon', 'WBA': 'Walgreens Boots Alliance',
              'WMT': 'Walmart'}


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':

        universe = request.form.getlist("universe")
        start_date = datetime.strptime(request.form["StartDate"], '%Y-%m-%d')
        lookback = int(request.form["lookback"])
        target_return = int(request.form["TgtReturn"])/100
        if request.form["LongOnly"] == "False":
            long_only = False
        else:
            long_only = True

        portfolio = Markowitz(tickers=universe, trade_start=start_date, lookback=lookback,
                              tgt_ret=int(target_return)/100, long_only=long_only)

        portfolio.solve()

        fig, axes = efficient_frontier(portfolio, show=False)

        fig.savefig(r'static\frontier_plot.png')

        return render_template('output.html', holdings=portfolio.holdings, stocks=dow_stocks)

    else:
        return render_template('input.html', stocks=dow_stocks)


if __name__ == '__main__':
    app.run()


