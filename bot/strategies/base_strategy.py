"""
Базовый класс для всех стратегий
"""

from abc import ABC, abstractmethod
import pandas as pd


class BaseStrategy(ABC):
    """Абстрактный базовый класс стратегии"""

    def __init__(self, params):
        self.params = params
        self.name = self.__class__.__name__

    @abstractmethod
    def calculate_indicators(self, df):
        """Рассчитать индикаторы на данных"""
        pass

    @abstractmethod
    def generate_signal(self, df, current_idx, current_position):
        """
        Генерировать торговый сигнал

        Returns: 'BUY', 'SELL', 'HOLD'
        """
        pass

    def get_required_history_length(self):
        """Минимальная длина истории для стратегии"""
        return 50  # По умолчанию