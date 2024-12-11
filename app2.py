import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.markdown("""
    <p style="font-size: 12px; text-align: center;">
        Created by: <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank">Luca Girlando</a>
    </p>
""", unsafe_allow_html=True)

# Function to calculate the investment values
def calculate_investment(initial_investment, monthly_contribution, annual_return_rate, inflation_rate, years_to_calculate):
    months_in_year = 12

    # Lists to store results
    amounts = []  # Total value of the investment
    amounts_with_inflation = []  # Real value (adjusted for inflation)
    total_invested = []  # Total invested (initial capital + contributions)
    non_invested_capital = []  # Non-invested capital adjusted for inflation

    # Calculation for each year
    for year in years_to_calculate:
        months = year * months_in_year
        # Total invested up to this year
        invested = initial_investment + monthly_contribution * months
        total_invested.append(invested)

        # Calculate the future value with compound interest
        future_value = initial_investment * (1 + annual_return_rate / months_in_year) ** months
        for month in range(1, months + 1):
            future_value += monthly_contribution * (1 + annual_return_rate / months_in_year) ** (months - month)

        amounts.append(int(future_value))

        # Real value of the investment (adjusted for inflation)
        real_value = future_value / ((1 + inflation_rate) ** year)
        amounts_with_inflation.append(int(real_value))

        # Non-invested capital adjusted for inflation
        non_invested_value = invested / ((1 + inflation_rate) ** year)
        non_invested_capital.append(int(non_invested_value))

    # Create a DataFrame to display the results
    df = pd.DataFrame({
        'Year': years_to_calculate,
        'Final Amount (€)': amounts,
        'Real Invested Value (€)': amounts_with_inflation,
        'Total Invested (€)': total_invested,
        'Non-Invested Capital (€)': non_invested_capital
    })

    # Format the numbers with a dot as a thousand separator
    df['Final Amount (€)'] = df['Final Amount (€)'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df['Real Invested Value (€)'] = df['Real Invested Value (€)'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df['Total Invested (€)'] = df['Total Invested (€)'].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    df['Non-Invested Capital (€)'] = df['Non-Invested Capital (€)'].apply(lambda x: f"{x:,.0f}".replace(",", "."))

    return df, amounts, amounts_with_inflation, non_invested_capital, total_invested

# Streamlit UI
st.title("Investment Calculation with Compound Interest and Inflation Adjustment")

# User inputs
initial_investment = st.number_input("Initial Investment (€)", min_value=0, value=10000, step=100)
monthly_contribution = st.number_input("Monthly Contribution (€)", min_value=0, value=200, step=50)
annual_return_rate = st.slider("Annual Return (%)", min_value=0.0, max_value=20.0, value=7.0) / 100
inflation_rate = st.slider("Annual Inflation Rate (%)", min_value=0.0, max_value=10.0, value=2.0) / 100
years_to_calculate = st.select_slider(
    "Years to Calculate", options=[1, 5, 10, 20, 30, 40, 50, 60, 70], value=10
)

# List of years to calculate (including previous years up to the selected value)
years_to_calculate_list = [1, 5, 10, 20, 30, 40, 50, 60, 70]
years_to_calculate_selected = years_to_calculate_list[:years_to_calculate_list.index(years_to_calculate) + 1]

# Calculate the values
df, amounts, amounts_with_inflation, non_invested_capital, total_invested = calculate_investment(
    initial_investment, monthly_contribution, annual_return_rate, inflation_rate, years_to_calculate_selected
)

# Display the results table
st.write("### Investment Results")
st.dataframe(df)

# Explanation of the results
st.write("""
### Explanation of the Investment Metrics:
- **Final Amount (€)**: This is the total value of the investment after compounding interest over the selected number of years, including both the initial investment and monthly contributions.
- **Real Invested Value (€)**: This is the value of the investment adjusted for inflation, showing the "real" purchasing power of the amount after the inflationary effect.
- **Total Invested (€)**: This is the total amount you have contributed to the investment over time, which includes the initial investment plus all the monthly contributions.
- **Non-Invested Capital (€)**: This is the capital that has not been invested (i.e., just saved) and its value adjusted for inflation over the years.

### What is Compound Interest?
Compound interest is the process by which interest is calculated on the initial principal as well as on the accumulated interest from previous periods. This leads to exponential growth of the investment over time. In this model, we calculate compound interest monthly for both the initial investment and monthly contributions.

""")

# Plot the graph
plt.figure(figsize=(12, 8))
plt.plot(years_to_calculate_selected, amounts, marker='o', color='b', label='Final Amount (€)')
plt.plot(years_to_calculate_selected, amounts_with_inflation, marker='o', color='g', label='Real Invested Value (€)')
plt.plot(years_to_calculate_selected, non_invested_capital, marker='o', color='r', label='Non-Invested Capital (€)')
plt.plot(years_to_calculate_selected, total_invested, marker='o', color='purple', label='Total Invested (€)')
plt.xlabel('Years')
plt.ylabel('Amount (€)')
plt.title('Investment with Monthly Contributions and Inflation Impact')
plt.grid(True)
plt.legend()
plt.ticklabel_format(style='plain', axis='y')  # Disable scientific notation
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", ".")))
st.pyplot(plt)
