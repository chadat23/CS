portion_down_payment = 0.25
current_savings = 0
r = 0.04

annual_salary = float(input('What is your annual salary? '))
portion_saved = float(input('What percent of your income will you save each month? '))
total_cost = float(input('How much do you expect to spend? '))
semi_annual_raise = float(input('What do you expect your semi-annual raise to be? '))

required_down_payment = total_cost * portion_down_payment

n_months = 0
while (current_savings <= required_down_payment):
    monthly_contribution = annual_salary / 12 * portion_saved
    current_savings += current_savings * r / 12 + monthly_contribution
    n_months += 1
    if n_months > 0 and n_months % 6 == 0:
        annual_salary *= 1 + semi_annual_raise

print('It will take', n_months, 'months to save the down payment.')
