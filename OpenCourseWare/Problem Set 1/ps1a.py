r = 0.04
portion_down_payment = 0.25

annual_salary = float(input("Enter your annual salary: "))
monthly_salary = annual_salary / 12

portion_saved = float(input("Enter the percent of your salary to save, as a decimal: "))

total_cost = float(input("Enter the cost of your dream home: "))
down_payment = total_cost * portion_down_payment

current_savings = 0
number_of_months = 0
while down_payment > current_savings:
    current_savings += current_savings * r / 12
    current_savings += portion_saved * monthly_salary
    number_of_months += 1

print("Number of months:", number_of_months)
