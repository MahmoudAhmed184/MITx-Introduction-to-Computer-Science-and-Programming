def calculate_balance_after_payment(
    balance: float,
    monthly_interest_rate: float,
    monthly_payment: float,
    target_months: int,
):
    while target_months:
        monthly_unpaid_balance = balance - monthly_payment
        interest = monthly_interest_rate * monthly_unpaid_balance
        balance = monthly_unpaid_balance + interest
        target_months -= 1

    return balance


balance = float(input("Enter the outstanding balance on the credit card: "))
annual_interest_rate = float(input("Enter the annual interest rate as a decimal: "))
monthly_interest_rate = annual_interest_rate / 12.0


initial_balance = balance
monthly_payment = 0

while balance > 0:
    balance = initial_balance
    monthly_payment += 10
    balance = calculate_balance_after_payment(
        balance, monthly_interest_rate, monthly_payment, target_months=12
    )


print(f"Lowest Payment: {monthly_payment}")
