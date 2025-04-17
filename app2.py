# App Compound Interest Calculator
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

# Configurazione della pagina
st.set_page_config(page_title="Advanced Investment Simulator", page_icon="📊", layout="wide")

st.markdown("""
    <p style="font-size: 12px; text-align: center;">
        Created by: <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank">Luca Girlando</a>
    </p>
""", unsafe_allow_html=True)

# Premium scientific CSS styling
st.markdown("""
<style>
:root {
    --primary-dark: #1a2639;
    --primary-medium: #3e4a61;
    --primary-light: #d9dad7;
    --accent-blue: #4a6fa5;
    --accent-teal: #166088;
    --call-green: #4CAF50;
    --highlight: #f0f4f8;
    --chart-blue: #4285F4;
    --chart-green: #34A853;
    --chart-red: #EA4335;
    --chart-purple: #9C27B0;
}

* {
    font-family: 'Lato', 'Segoe UI', Roboto, sans-serif;
}

h1, h2, h3, h4 {
    color: var(--primary-dark);
    font-weight: 700;
    letter-spacing: -0.015em;
    margin-bottom: 0.5rem !important;
}

body {
    background-color: #f8f9fa;
}

.stNumberInput, .stSlider {
    margin-bottom: 1.2rem;
}

/* Premium metric cards */
.metric-container {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 1.5rem;
    border-radius: 12px;
    background: white;
    box-shadow: 0 6px 20px rgba(0,0,0,0.08);
    margin-bottom: 1.5rem;
    text-align: center;
    transition: all 0.3s cubic-bezier(.25,.8,.25,1);
    border: 1px solid rgba(0,0,0,0.05);
}

.metric-value {
    font-size: 2.1rem;
    font-weight: 800;
    font-family: 'Roboto Mono', monospace;
    margin: 0.7rem 0;
    color: var(--primary-dark);
    letter-spacing: -0.03em;
}

.metric-label {
    font-size: 1.05rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: var(--primary-medium);
    margin-bottom: 0.5rem;
}

/* Enhanced tables */
.stDataFrame {
    border-radius: 10px !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
    border: 1px solid rgba(0,0,0,0.03) !important;
}

/* Custom cards */
.custom-card {
    background: white;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.03);
}

.card-title {
    color: var(--accent-teal);
    font-weight: 600;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
}

/* Custom divider */
.section-divider {
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0,0,0,0.1), transparent);
    margin: 2rem 0;
}

/* Input styling */
.stSelectbox, .stNumberInput, .stSlider {
    border-radius: 8px !important;
}

/* Footer */
.footer {
    font-size: 0.78rem;
    text-align: center;
    margin-top: 3rem;
    color: #6c757d;
    padding: 1.2rem;
    border-top: 1px solid #e9ecef;
    letter-spacing: 0.03em;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: white !important;
    border-radius: 8px !important;
    padding: 10px 20px !important;
    transition: all 0.3s ease !important;
}

.stTabs [aria-selected="true"] {
    background: var(--accent-teal) !important;
    color: white !important;
    font-weight: 600 !important;
}
</style>
""", unsafe_allow_html=True)

# Function to calculate the investment values
def calculate_investment(initial_investment, periods_data, inflation_rate, years_to_calculate):
    months_in_year = 12

    # Lists to store results
    amounts = []  # Total value of the investment
    amounts_with_inflation = []  # Real value (adjusted for inflation)
    total_invested = []  # Total invested (initial capital + contributions)
    non_invested_capital = []  # Non-invested capital adjusted for inflation

    # Initialize variables
    current_value = initial_investment
    total_months = 0
    total_contributions = 0

    # Calculation for each year
    for year in years_to_calculate:
        # Determine which period parameters to use
        period_index = min(year // 10, len(periods_data) - 1)
        monthly_contribution = periods_data[period_index]['monthly_contribution']
        annual_return_rate = periods_data[period_index]['annual_return_rate']
        
        # Calculate months for this year
        if year == years_to_calculate[0]:
            months = year * months_in_year
        else:
            prev_year = years_to_calculate[years_to_calculate.index(year)-1]
            months = (year - prev_year) * months_in_year
        
        total_months += months
        
        # Calculate the future value with compound interest
        future_value = current_value * (1 + annual_return_rate / months_in_year) ** months
        for month in range(1, months + 1):
            future_value += monthly_contribution * (1 + annual_return_rate / months_in_year) ** (months - month)
            total_contributions += monthly_contribution
        
        current_value = future_value
        
        # Total invested up to this year
        invested = initial_investment + total_contributions
        total_invested.append(invested)

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
        'Real Value (€)': amounts_with_inflation,
        'Total Invested (€)': total_invested,
        'Non-Invested Capital (€)': non_invested_capital
    })

    # Format the numbers with a dot as a thousand separator
    for col in df.columns[1:]:
        df[col] = df[col].apply(lambda x: f"{x:,.0f}".replace(",", "."))

    return df, amounts, amounts_with_inflation, non_invested_capital, total_invested

# Streamlit UI
st.title("📈 Advanced Investment Simulator")
st.markdown("""
    <p style="font-size: 0.9rem; color: var(--primary-medium);">
        Simulate long-term investment growth with customizable periods, inflation adjustment, and detailed analytics
    </p>
""", unsafe_allow_html=True)

# User inputs in columns
col1, col2 = st.columns([1, 1])
with col1:
    st.markdown("### 🏦 Initial Parameters")
    with st.container():
        initial_investment = st.number_input("**Initial Investment (€)**", min_value=0, value=10000, step=100)
        inflation_rate = st.slider("**Annual Inflation Rate (%)**", min_value=0.0, max_value=10.0, value=2.0, step=0.1) / 100

with col2:
    st.markdown("### ⏳ Time Horizon")
    with st.container():
        years_to_calculate = st.select_slider(
            "**Investment Duration (years)**",
            options=[1, 5, 10, 20, 30, 40, 50],
            value=20
        )

# Calculate how many 10-year periods we need
num_periods = (years_to_calculate // 10) + (1 if years_to_calculate % 10 != 0 else 0)
if num_periods == 0:
    num_periods = 1

# Custom period configuration
st.markdown("### ⚙️ Period Configuration")
st.markdown("""
<div class="custom-card">
    <div class="card-title">📌 Investment Strategy Guidance</div>
    <p>Typically, investment strategies evolve over time based on risk tolerance:</p>
    <ul>
        <li><strong>Growth Phase (Years 1-10):</strong> Higher risk (80-100% stocks), 7-10% expected return</li>
        <li><strong>Consolidation Phase (Years 11-20):</strong> Balanced (60-80% stocks), 5-7% expected return</li>
        <li><strong>Preservation Phase (Years 21+):</strong> Conservative (20-40% stocks), 3-5% expected return</li>
    </ul>
    <p>Monthly contributions often increase with career progression.</p>
</div>
""", unsafe_allow_html=True)

# Create input fields for each period with default values
periods_data = []
tab_labels = [f"Period {i*10 + 1}-{min((i+1)*10, years_to_calculate)} years" for i in range(num_periods)]
tabs = st.tabs(tab_labels)

for i, tab in enumerate(tabs):
    with tab:
        cols = st.columns(2)
        with cols[0]:
            monthly_contribution = st.number_input(
                f"**Monthly Contribution (€)**",
                min_value=0,
                value=200 + i*100,  # Increasing default contributions
                step=50,
                key=f"monthly_{i}"
            )
        with cols[1]:
            annual_return_rate = st.slider(
                f"**Expected Annual Return (%)**",
                min_value=0.0,
                max_value=20.0,
                value=7.0 - i*1.5,  # Decreasing default returns
                step=0.1,
                key=f"return_{i}"
            ) / 100
        periods_data.append({
            'monthly_contribution': monthly_contribution,
            'annual_return_rate': annual_return_rate
        })

# List of years to calculate (including previous years up to the selected value)
years_to_calculate_list = [1, 5, 10, 20, 30, 40, 50]
years_to_calculate_selected = years_to_calculate_list[:years_to_calculate_list.index(years_to_calculate) + 1]

# Calculate the values
df, amounts, amounts_with_inflation, non_invested_capital, total_invested = calculate_investment(
    initial_investment, periods_data, inflation_rate, years_to_calculate_selected
)

# Display key metrics
st.markdown("### 📊 Investment Summary")
metric_cols = st.columns(4)
with metric_cols[0]:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Final Value</div>
        <div class="metric-value">€{amounts[-1]:,.0f}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)
with metric_cols[1]:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Real Value</div>
        <div class="metric-value">€{amounts_with_inflation[-1]:,.0f}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)
with metric_cols[2]:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Total Invested</div>
        <div class="metric-value">€{total_invested[-1]:,.0f}</div>
    </div>
    """.replace(",", "."), unsafe_allow_html=True)
with metric_cols[3]:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-label">Growth Multiple</div>
        <div class="metric-value">{amounts[-1]/total_invested[-1]:.1f}x</div>
    </div>
    """, unsafe_allow_html=True)

# Display the results table
st.markdown("### 📋 Detailed Projections")
st.dataframe(df)

# Plot the graph
st.markdown("### 📈 Growth Visualization")
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(years_to_calculate_selected, amounts, marker='o', color='#4285F4', label='Final Amount (€)', linewidth=2.5)
ax.plot(years_to_calculate_selected, amounts_with_inflation, marker='o', color='#34A853', label='Real Value (€)', linewidth=2.5)
ax.plot(years_to_calculate_selected, non_invested_capital, marker='o', color='#EA4335', label='Non-Invested Capital (€)', linewidth=2.5)
ax.plot(years_to_calculate_selected, total_invested, marker='o', color='#9C27B0', label='Total Invested (€)', linewidth=2.5)

ax.set_xlabel('Years', fontsize=12, labelpad=10)
ax.set_ylabel('Amount (€)', fontsize=12, labelpad=10)
ax.set_title('Investment Growth Projection', fontsize=14, pad=20)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend(fontsize=10, framealpha=1)
ax.set_facecolor('#f8f9fa')

# Format y-axis
formatter = FuncFormatter(lambda x, p: f"{int(x):,}".replace(",", "."))
ax.yaxis.set_major_formatter(formatter)

# Remove spines
for spine in ['top', 'right']:
    ax.spines[spine].set_visible(False)

st.pyplot(fig)

# Explanation section
st.subheader("📚 Investment Concepts Explained")

st.markdown("#### Compound Interest")
st.markdown("The exponential growth that occurs when earnings are reinvested to generate additional earnings over time. Calculated monthly in this model for both initial investment and contributions.")

st.markdown("#### Real vs Nominal Value")
st.markdown("**Final Amount** shows the nominal value, while **Real Value** adjusts for inflation to reveal actual purchasing power.")

st.markdown("#### Growth Multiple")
st.markdown("Shows how much your money multiplied compared to what you invested (Final Amount / Total Invested). A 3x multiple means each euro became three.")

# Footer
st.markdown("""
<div class="footer">
    <p>Created by <a href="https://www.linkedin.com/in/luca-girlando-775463302/" target="_blank">Luca Girlando</a> | 
    Investment projections are hypothetical and don't guarantee future performance</p>
</div>
""", unsafe_allow_html=True)
