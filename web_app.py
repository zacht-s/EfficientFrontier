from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def home():
    if request.method == 'POST':
        print(f'Stocks: {request.form.getlist("universe")}')
        print(f'Start Date: {request.form["StartDate"]}')
        print(f'Lookback: {request.form["lookback"]}')
        return render_template('input.html')

    else:
        return render_template('input.html')


if __name__ == '__main__':
    app.run()


