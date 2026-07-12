#!/usr/bin/env python3
"""
Demand Forecasting Module
Moving average and exponential smoothing for demand prediction.

Author: Mupo Mubita <mubitamupo@outlook.com>
"""

import numpy as np


def moving_average_forecast(demand_history, window=3):
    """
    Simple moving average forecast.

    Parameters:
        demand_history: List of historical demand values
        window: Number of periods to average

    Returns:
        Forecasted demand for next period
    """
    if len(demand_history) < window:
        return np.mean(demand_history)
    return np.mean(demand_history[-window:])


def exponential_smoothing(demand_history, alpha=0.3):
    """
    Exponential smoothing forecast.

    Parameters:
        demand_history: List of historical demand values
        alpha: Smoothing factor (0 < alpha < 1)

    Returns:
        Forecasted demand for next period
    """
    if not demand_history:
        return 0

    forecast = demand_history[0]
    for demand in demand_history[1:]:
        forecast = alpha * demand + (1 - alpha) * forecast
    return forecast


def forecast_accuracy(actual, predicted):
    """Calculate MAPE (Mean Absolute Percentage Error)."""
    errors = [abs(a - p) / max(a, 1) for a, p in zip(actual, predicted)]
    return np.mean(errors) * 100


if __name__ == "__main__":
    history = [120, 135, 128, 142, 155, 148, 160, 175, 168, 180]

    ma_forecast = moving_average_forecast(history, window=3)
    es_forecast = exponential_smoothing(history, alpha=0.3)

    print(f"Historical demand: {history}")
    print(f"Moving Average Forecast (next period): {ma_forecast:.1f}")
    print(f"Exponential Smoothing Forecast: {es_forecast:.1f}")
