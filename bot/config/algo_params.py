"""
Гиперпараметры стратегий
"""

# Hello World SMA Crossover
SMA_CROSSOVER_PARAMS = {
    'sma_fast': 5,
    'sma_slow': 15,
}

# Mean Reversion with Bollinger Bands
MEAN_REVERSION_PARAMS = {
    'bb_period': 20,
    'bb_std': 2.0,
    'rsi_period': 14,
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'ema_fast': 9,
    'ema_slow': 21,
    'volume_ma_period': 20,
    'volume_threshold': 1.2,
    'cooldown_candles': 3,
}