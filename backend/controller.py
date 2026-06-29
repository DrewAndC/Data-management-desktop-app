from processing import load_data, clean_data, process_monthly
from forecast import (
    naive_forecast,
    moving_average_forecast,
    arima_forecast, 
    mae,
    mse
)
import pandas as pd

class Controller:
    def __init__(self):
        self.monthly_data = None
        self.segment_data = None

    def load_and_process(self, file_paths):
        df = load_data(file_paths)
        df = clean_data(df)

        monthly, monthly_segment = process_monthly(df)

        self.monthly_data = monthly
        self.segment_data = monthly_segment

    def forecast_metric(self, series, horizon):
        if len(series) <= horizon:
            raise ValueError("Not enough data for forecasting")
        
        train = series[:-horizon]
        test = series[-horizon:]

        results = {}

        # naive
        naive_pred = naive_forecast(train, horizon)
        results["naive"] = {
            "predictions": naive_pred.tolist(),
            "mae": float(mae(test, naive_pred)),
            "mse": float(mse(test, naive_pred))
        }

        # moving average
        ma_pred = moving_average_forecast(train, horizon)
        results["moving_average"] = {
            "predictions": ma_pred.tolist(),
            "mae": float(mae(test, ma_pred)),
            "mse": float(mse(test, ma_pred))
        }

        # ARIMA
        arima_pred = arima_forecast(train, horizon)
        results["arima"] = {
            "predictions": arima_pred.tolist(),
            "mae": float(mae(test, arima_pred)),
            "mse": float(mse(test, arima_pred))
        }

        # determine best model (lowest MAE)
        best_model = min(results, key=lambda m: results[m]["mae"])
        best_predictions = results[best_model]["predictions"]

        return {
            "actual": test.tolist(),
            "models": results,
            "best_model": best_model,
            "best_predictions": best_predictions
        }

    def forecast(self, horizon=3, train_window=None):
        if self.monthly_data is None:
            raise ValueError("Data not loaded. Call load_and_process first.")

        output = {}

        for metric in ["revenue", "cost", "margin"]:
            series = self.monthly_data[metric]

            if train_window is not None:
                train_window = max(train_window, horizon + 1)
                series = series[-train_window:]

            result = self.forecast_metric(series, horizon)
            output[metric] = result

        # future prediction month
        last_month = pd.to_datetime(self.monthly_data['month'].iloc[-1])

        future_months = [
            (last_month + pd.DateOffset(months=i)).strftime("%Y-%m")
            for i in range(1, horizon + 1)
        ]

        return {
            "months": future_months,
            "metrics": output
        }