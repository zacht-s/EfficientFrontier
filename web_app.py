from flask import Flask, render_template, request

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
        print(f'Stocks: {request.form.getlist("universe")}')
        print(f'Start Date: {request.form["StartDate"]}')
        print(f'Lookback: {request.form["lookback"]}')
        return render_template('input.html', stocks=dow_stocks)

    else:
        return render_template('input.html', stocks=dow_stocks)


if __name__ == '__main__':
    #print(dow_stocks)
    app.run()


