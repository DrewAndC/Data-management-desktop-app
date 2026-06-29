# RoastWorks Analytics Dashboard
This project is a Python-based analytics dashboard designed for RoastWorks Coffee Group. It automates the inputs, processsing, visualisation, and forecasting of sales data across three files:
- Commercial
- Domestic
- Cafe

The application replaces a manual Excel workflow with an automated system that generates key performance metrics and forecasts future performance. 

# Project Structure

The project is organised into the following main components:

Backend: Handles data loading, cleaning, aggregation, and forecasting

Frontend (PyQt6 GUI): Provides an interactive interface for file selection and dashboard visualisation

Data Processing: Combines and standardises multiple CSV inputs

Forecasting: Implements three forecasting models to predict future performance metrics

# Requirements 
- `matplotlib==3.10.8`
- `numpy==2.4.4`
- `pandas==3.0.2`
- `PyQt6==6.7.1`
- `statsmodels`

Install dependencies:

`pip install -r requirements.txt`

# How to Run

Run the application with a single command:

`python ./backend/main_window.py`

The GUI will allow you to:

Select the three CSV files:
- Data_Commercial.csv
- Data_Domestic.csv
- Data_Cafe.csv
  
View dashboards and forecasts

# AI Declaration 
We used generative AI (ChatGPT) to support aspects of this project, including debugging assistance, refining code structure, and improving clarity in documentation. AI was also used to help explore approaches for data processing and forecasting implementation.

All AI-generated suggestions were critically evaluated, tested, and modified where necessary, thus we take full responsibility for the accuracy, integrity, and completeness of the submitted work.
