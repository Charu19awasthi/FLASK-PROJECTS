from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Initial coffee machine resources
water = 1000
milk = 500
coffee_beans = 200
money = 0

menu = {
    "espresso": {"water": 50, "milk": 0, "coffee_beans": 18, "cost": 3},
    "latte": {"water": 200, "milk": 150, "coffee_beans": 24, "cost": 5},
    "cappuccino": {"water": 250, "milk": 100, "coffee_beans": 24, "cost": 6},
}

# Function to check if resources are sufficient
def check_resources(drink):
    global water, milk, coffee_beans
    coffee = menu[drink]
    if water < coffee["water"]:
        return False, "Not enough water!"
    if milk < coffee["milk"]:
        return False, "Not enough milk!"
    if coffee_beans < coffee["coffee_beans"]:
        return False, "Not enough coffee beans!"
    return True, ""

# Route for the home page
@app.route('/')
def index():
    return render_template('index.html', water=water, milk=milk, coffee_beans=coffee_beans, money=money)

# Route to handle making coffee
@app.route('/make_coffee/<drink>', methods=['POST'])
def make_coffee(drink):
    global water, milk, coffee_beans, money
    success, message = check_resources(drink)
    if success:
        coffee = menu[drink]
        water -= coffee["water"]
        milk -= coffee["milk"]
        coffee_beans -= coffee["coffee_beans"]
        money += coffee["cost"]
        return jsonify(status="success", message=f"Here is your {drink}. Enjoy!", water=water, milk=milk, coffee_beans=coffee_beans, money=money)
    else:
        return jsonify(status="error", message=message, water=water, milk=milk, coffee_beans=coffee_beans, money=money)

# Route to refill the machine
@app.route('/refill', methods=['POST'])
def refill():
    global water, milk, coffee_beans
    water = 1000
    milk = 500
    coffee_beans = 200
    return jsonify(status="success", message="Machine refilled!", water=water, milk=milk, coffee_beans=coffee_beans, money=money)

if __name__ == '__main__':
    app.run(debug=True)
