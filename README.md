# Investment-Calculator-Compound-Interest

A Streamlit-based web application for calculating investment growth with compound interest, monthly contributions, and inflation adjustments. The app allows users to forecast their investment's future value, including both nominal and real values adjusted for inflation.

## Overview

This project provides an interactive web application for investment calculations. The application calculates the future value of investments, considering factors like initial capital, monthly contributions, compound interest, and inflation over a customizable time horizon. It displays the results in an easy-to-read table and interactive graphs.

### Key Features:
- **Investment Calculation**: Calculates the future value of investments based on initial capital, monthly contributions, and compound interest.
- **Inflation Adjustment**: Adjusts the future value of the investment for inflation, providing the real value of the investment.
- **Multiple Investment Metrics**: Provides key investment metrics like total invested, real invested value, non-invested capital, and more.
- **Interactive Visualization**: View the investment growth over time with interactive graphs showing the nominal and real values.
- **Customizable Input**: Adjust the initial investment, monthly contribution, annual return, inflation rate, and the number of years for calculation.

### Usage:
Once the application is running, follow these steps to use it:
- **Enter Initial Investment**: In the sidebar, input your initial investment amount (e.g., 10,000€).
- **Enter Monthly Contribution**: Input the monthly amount you plan to contribute to the investment.
- **Select Annual Return Rate**: Use the slider to choose your expected annual return rate (e.g., 7%).
- **Select Inflation Rate**: Adjust the annual inflation rate that will be applied to the real value of your investment.
- **Choose Years to Calculate**: Select the number of years for which you want to calculate your investment's future value.
- **View Results**: The app will display a table with your investment's future value, adjusted for inflation, and generate an interactive chart showing the investment's growth over time.

## Requirements

To run the application, you'll need the following libraries:

- **Python 3.8+**
- **Streamlit**: For creating the interactive web app.
- **pandas**: For data manipulation and analysis.
- **matplotlib**: For data visualization (e.g., plotting investment growth).
  
