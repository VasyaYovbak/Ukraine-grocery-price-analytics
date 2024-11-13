import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX


def initialize_sarimax_model(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12)):
    return SARIMAX(data['price'],
                   order=order,
                   seasonal_order=seasonal_order,
                   enforce_stationarity=False,
                   enforce_invertibility=False)


def fit_sarimax_model(model: SARIMAX, maxiter=50):
    return model.fit(disp=False, maxiter=maxiter)


def get_trained_sarimax_predictions(data, model, range=None):
    if range is None:
        range = (data['date'].min(), data['date'].max())
    results = fit_sarimax_model(model)
    prediced_mean_values = results.get_prediction().predicted_mean.values
    prediced_range_values = results.get_prediction().conf_int()

    df = pd.DataFrame({
        'date': data['date'],
        'mean': prediced_mean_values,
        'lower': prediced_range_values.iloc[:, 0],
        'upper': prediced_range_values.iloc[:, 1]
    })

    return df[(df['date'] >= range[0]) & (df['date'] <= range[1])]


def get_future_sarimax_predicitons(data, model, steps=12, range=None):
    if range is None:
        range = (data['date'].max(), pd.date_range(
            start=data['date'].max(), periods=steps, freq='ME').max())

    results = fit_sarimax_model(model)
    forecast = results.get_forecast(steps=steps)
    forecasted_mean_values = forecast.predicted_mean.values
    forecasted_range_values = forecast.conf_int()

    df = pd.DataFrame({
        'date': pd.date_range(start=data['date'].max(), periods=steps, freq='ME'),
        'mean': forecasted_mean_values,
        'lower': forecasted_range_values.iloc[:, 0],
        'upper': forecasted_range_values.iloc[:, 1]
    })

    return df[(df['date'] >= range[0]) & (df['date'] <= range[1])]
