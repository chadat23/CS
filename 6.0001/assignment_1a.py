portion_down_payment = 0.25
current_savings = 0
r = 0.04

annual_salary = float(input('What is your annual salary? '))
portion_saved = float(input('What percent of your income will you save each month? '))
total_cost = float(input('How much do you expect to spend?'))

monthly_contribution = annual_salary / 12 * portion_saved
required_down_payment = total_cost * portion_down_payment


def new_balance(savings, contribution):
    return savings + savings * r / 12 + contribution


n_months = 0
while (current_savings <= required_down_payment):
    current_savings = new_balance(current_savings, monthly_contribution)
    n_months += 1

print('It will take', n_months, 'months to save the down payment.')
