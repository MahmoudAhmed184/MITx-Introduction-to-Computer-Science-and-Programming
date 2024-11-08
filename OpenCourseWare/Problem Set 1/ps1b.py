MONTHS_IN_YEAR = 12

r = 0.04
portion_down_payment = 0.25

annual_salary = float(input("Enter your annual salary: "))
monthly_salary = annual_salary / MONTHS_IN_YEAR

portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))

total_cost = float(input("Enter the cost of your dream home: "))
down_payment = total_cost * portion_down_payment

semi_annual_raise = float(input("Enter the semi annual raise, as a decimal: "))

current_savings = 0
number_of_months = 0

while down_payment > current_savings:
    current_savings += current_savings * r / MONTHS_IN_YEAR
    current_savings += portion_saved * monthly_salary
    number_of_months += 1

    if number_of_months % 6 == 0:
        annual_salary += semi_annual_raise * annual_salary
        monthly_salary = annual_salary / MONTHS_IN_YEAR


print("Number of months:", number_of_months)
