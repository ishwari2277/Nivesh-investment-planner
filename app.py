from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Define realistic CAGR values for Stocks & Gold (based on historical data)
CAGR_STOCKS = 0.12  # 12% yearly return
CAGR_GOLD = 0.08    # 8% yearly return
TIME_YEARS = 5  # Assume a 5-year investment horizon

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        investment = float(request.form['investment'])
        risk_tolerance = request.form['risk_tolerance']

        # Define stock & gold allocation based on risk tolerance
        if risk_tolerance == "aggressive":
            stock_ratio = 0.8
            gold_ratio = 0.2
        elif risk_tolerance == "balanced":
            stock_ratio = 0.6
            gold_ratio = 0.4
        else:  # Conservative
            stock_ratio = 0.4
            gold_ratio = 0.6

        # Allocate funds
        stock_investment = investment * stock_ratio
        gold_investment = investment * gold_ratio

        # Calculate future values using CAGR formula
        stock_future_value = stock_investment * ((1 + CAGR_STOCKS) ** TIME_YEARS)
        gold_future_value = gold_investment * ((1 + CAGR_GOLD) ** TIME_YEARS)

        total_future_value = stock_future_value + gold_future_value

        return jsonify({
            "investment_type": risk_tolerance.capitalize(),
            "initial_investment": round(investment, 2),
            "stock_investment": round(stock_investment, 2),
            "gold_investment": round(gold_investment, 2),
            "expected_stock_value": round(stock_future_value, 2),
            "expected_gold_value": round(gold_future_value, 2),
            "expected_total_value": round(total_future_value, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
