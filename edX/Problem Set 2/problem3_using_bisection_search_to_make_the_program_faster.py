EPSILON = 0.01


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


monthly_payment_lower_bound = balance / 12
monthly_payment_upper_bound = (balance * (1 + monthly_interest_rate) ** 12) / 12.0

initial_balance = balance

while abs(balance) > EPSILON:
    balance = initial_balance
    monthly_payment = (monthly_payment_lower_bound + monthly_payment_upper_bound) / 2
    balance = calculate_balance_after_payment(balance, monthly_interest_rate, monthly_payment, target_months=12)
    if balance > 0:
        monthly_payment_lower_bound = monthly_payment + 0.01
    else:
        monthly_payment_upper_bound = monthly_payment - 0.01


print(f"Lowest Payment: {monthly_payment:.2f}")
