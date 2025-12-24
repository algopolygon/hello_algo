"""
Технические индикаторы
"""

import pandas as pd
import numpy as np


def calculate_sma(prices, period):
    """Простая скользящая средняя"""
    return prices.rolling(window=period).mean()


def calculate_ema(prices, period):
    """Экспоненциальная скользящая средняя"""
    return prices.ewm(span=period, adjust=False).mean()


def calculate_rsi(prices, period=14):
    """Индекс относительной силы (RSI)"""
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calculate_bollinger_bands(prices, period=20, std=2):
    """Bollinger Bands"""
    sma = prices.rolling(window=period).mean()
    rolling_std = prices.rolling(window=period).std()
    upper_band = sma + (rolling_std * std)
    lower_band = sma - (rolling_std * std)
    return upper_band, sma, lower_band


def calculate_volume_ma(volume, period=20):
    """Скользящая средняя объема"""
    return volume.rolling(window=period).mean()