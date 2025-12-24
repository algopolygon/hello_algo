"""
Стратегия пересечения скользящих средних (Hello World)
"""

import pandas as pd
from strategies.base_strategy import BaseStrategy
from indicators.technical import calculate_sma


class SMACrossoverStrategy(BaseStrategy):
    """Стратегия пересечения SMA"""

    def __init__(self, params):
        super().__init__(params)
        self.sma_fast = params['sma_fast']
        self.sma_slow = params['sma_slow']

    def calculate_indicators(self, df):
        """Рассчитать индикаторы"""
        if len(df) < self.sma_slow:
            return df

        df['sma_fast'] = calculate_sma(df['close'], self.sma_fast)
        df['sma_slow'] = calculate_sma(df['close'], self.sma_slow)

        return df

    def generate_signal(self, df, current_idx, current_position):
        """Генерация сигнала на основе пересечения SMA"""

        if current_idx < self.sma_slow:
            return 'HOLD'

        current = df.iloc[current_idx]
        previous = df.iloc[current_idx - 1]

        sma_fast_now = current['sma_fast']
        sma_slow_now = current['sma_slow']
        sma_fast_prev = previous['sma_fast']
        sma_slow_prev = previous['sma_slow']

        if pd.isna([sma_fast_now, sma_slow_now, sma_fast_prev, sma_slow_prev]).any():
            return 'HOLD'

        # Golden Cross
        if (sma_fast_prev <= sma_slow_prev) and (sma_fast_now > sma_slow_now):
            if current_position <= 0:
                return 'BUY'

        # Death Cross
        if (sma_fast_prev >= sma_slow_prev) and (sma_fast_now < sma_slow_now):
            if current_position >= 0:
                return 'SELL'

        return 'HOLD'

    def get_required_history_length(self):
        return self.sma_slow