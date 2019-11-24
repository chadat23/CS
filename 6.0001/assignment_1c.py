portion_down_payment = 0.25
current_savings = 0
semi_annual_raise = 0.07
total_cost = 1000000
r = 0.04

annual_salary = float(input('What is your annual salary? '))

required_down_payment = total_cost * portion_down_payment

min = 0
max = 1
tries = 0
this_current_savings = 0

while (abs(this_current_savings - required_down_payment) > 100):
    this_current_savings = current_savings
    this_annual_salary = annual_salary
    for month in range(36):
        portion_saved = (max + min) / 2
        monthly_contribution = this_annual_salary / 12 * portion_saved
        this_current_savings += this_current_savings * r / 12 + monthly_contribution
        if month > 0 and month % 6 == 0:
            this_annual_salary *= 1 + semi_annual_raise
    if this_current_savings < required_down_payment:
        min = portion_saved
    else:
        max = portion_saved
    if min > 0.9999:
        print("Can't be done.")
        break
    tries += 1

if abs(this_current_savings - required_down_payment) < 100:
    print('Best savings rate: ', portion_saved)
    print('Steps in bisection search', tries)
