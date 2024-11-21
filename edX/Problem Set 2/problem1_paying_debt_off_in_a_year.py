balance = float(input("Enter the outstanding balance on the credit card: "))
annual_interest_rate = float(input("Enter the annual interest rate as a decimal: "))
monthly_payment_rate = float(input("Enter the minimum monthly payment rate as a decimal: "))
monthly_interest_rate = annual_interest_rate / 12.0

target_months = 12

while target_months:
    minimum_monthly_payment = monthly_payment_rate * balance
    monthly_unpaid_balance = balance - minimum_monthly_payment
    interest = monthly_interest_rate * monthly_unpaid_balance
    balance = monthly_unpaid_balance + interest
    target_months -= 1

print(f"Remaining balance: {balance:.2f}")
