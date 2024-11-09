MONTHS_PER_YEAR = 12
MONTHS_PER_SEMI_ANNUAL_PERIOD = 6
TARGET_MONTHS = 36
HOUSE_COST = 1_000_000
PORTION_DOWN_PAYMENT = 0.25
DOWN_PAYMENT = HOUSE_COST * PORTION_DOWN_PAYMENT
BISECTION_TOLERANCE = 100
SAVINGS_RATE_PRECISION_SCALE = 10_000
DEFAULT_ANNUAL_INVESTMENT_RETURN_RATE = 0.04
DEFAULT_SEMI_ANNUAL_RAISE = 0.07


def calculate_total_savings(
    saving_rate: float,
    annual_salary: float,
    number_of_months: int,
    semi_annual_raise: float,
    annual_investment_return_rate: float,
) -> float:
    
    monthly_salary = annual_salary / MONTHS_PER_YEAR
    current_savings = 0

    while number_of_months:
        current_savings += current_savings * annual_investment_return_rate / MONTHS_PER_YEAR
        current_savings += saving_rate * monthly_salary
        number_of_months -= 1

        if number_of_months % MONTHS_PER_SEMI_ANNUAL_PERIOD == 0:
            annual_salary += semi_annual_raise * annual_salary
            monthly_salary = annual_salary / MONTHS_PER_YEAR
    
    return current_savings


def calculate_saving_rate(
    target_amount: float,
    annual_salary: float,
    number_of_months: int = TARGET_MONTHS,
    semi_annual_raise: float = DEFAULT_SEMI_ANNUAL_RAISE,
    annual_investment_return_rate: float = DEFAULT_ANNUAL_INVESTMENT_RETURN_RATE,
) -> tuple[float, int]:
    
    number_of_steps = 0
    left = 1
    right = SAVINGS_RATE_PRECISION_SCALE
    
    while left <= right:
        number_of_steps += 1
        mid = (left + right) // 2
        saving_rate = mid / SAVINGS_RATE_PRECISION_SCALE
        
        total_savings = calculate_total_savings(
            saving_rate,
            annual_salary,
            number_of_months,
            semi_annual_raise,
            annual_investment_return_rate,
        )

        if abs(total_savings - target_amount) <= BISECTION_TOLERANCE:
            return saving_rate, number_of_steps
        elif total_savings < target_amount:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1, number_of_steps


annual_salary = float(input("Enter the starting salary: "))

savings_rate, number_of_steps = calculate_saving_rate(DOWN_PAYMENT, annual_salary)

if savings_rate == -1:
    print("It is not possible to pay the down payment in three years.")
else:
    print("Best savings rate:", savings_rate)
    print("Steps in bisection search:", number_of_steps)
