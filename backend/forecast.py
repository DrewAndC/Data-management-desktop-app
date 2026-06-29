import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# function to generate forecasts using naive model. 
def naive_forecast(train, horizon): # train = historical data, horizon = number of future points to predict. 
    if len(train) == 0: # checks that training data exists and prevents errors later. 
        raise ValueError("Training data is empty")

    # ensures all values are numeric. 
    # predicts that all future values = last ovserved value. 
    train = train.astype(float)
    return np.round(np.full(horizon, train.iloc[-1]), 2)


# function to generate forecasts using moving average. 
def moving_average_forecast(train, horizon, window=3): # window = number of past values used for averaging. 
    if len(train) == 0:
        raise ValueError("Training data is empty")

    # ensures numeric values. 
    # converts data to a python list. 
    train = train.astype(float)
    history = train.tolist()
    preds = [] # empty list to store predictions. 

    # loop runs once per prediction step. 
    for _ in range(horizon):
        w = min(window, len(history)) #  takes last w values from history and computes their average. 
        value = np.mean(history[-w:])
        preds.append(value) # stores predicted value. 
        history.append(value) # adds prediction to history which makes this forecasting recursive. 

    # comverts list to NumPy array. 
    # rounds to two decimal places. 
    return np.round(np.array(preds), 2)

# function to generate forecasts using arima.  
def arima_forecast(train, horizon, order=(1, 1, 1)):
    # ensures training data is not empty
    if len(train) == 0:
        raise ValueError("Training data is empty")
    
    train = train.astype(float)

    # more error handling just to be safe
    if len(train) < 6:
        return naive_forecast(train, horizon)
    
    try: 
        # fit arima model 
        model = ARIMA(train, order=order)
        model_fit = model.fit()

        # forecast future values
        forecast = model_fit.forecast(steps=horizon)

        return np.round(forecast.values, 2)
    
    except Exception:
        # fallback to naive if ARIMA fails 
        return np.round(np.full(horizon, train.iloc[-1]), 2)
    
# function to compute mean absolute error (mae)
def mae(actual, predicted):

    # converts inputs to numeric arrays.
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)

    # computes average absolute difference between actual and predicted values. 
    return np.mean(np.abs(actual - predicted))

# function to compute mean squared error. 
def mse(actual, predicted):

    # converts inputs to numeric arrays. 
    actual = np.array(actual, dtype=float)
    predicted = np.array(predicted, dtype=float)

    # squares errors before averaging. 
    return np.mean((actual - predicted) ** 2)
    
def compare_models(train, horizon=3):
    results = {}

    # generate forecasts
    naive_preds = naive_forecast(train, horizon)
    ma_preds = moving_average_forecast(train, horizon)
    arima_preds = arima_forecast(train, horizon)

    # use last actual values for comparison
    actual = train[-horizon:]

    # compute errors
    results["naive"] = mae(actual, naive_preds)
    results["moving_average"] = mae(actual, ma_preds)
    results["arima"] = mae(actual, arima_preds)

    # find best model (lowest error)
    best_model = min(results, key=results.get)

    return {
        "errors": results,
        "best_model": best_model,
        "forecasts": {
            "naive": naive_preds,
            "moving_average": ma_preds,
            "arima": arima_preds
        }
    }