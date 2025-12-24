"""
Утилиты для работы со временем
"""

from datetime import datetime


def is_trading_time(config):
    """Проверка времени торговли"""
    now = datetime.now()

    # Проверка рабочего дня
    if now.weekday() >= 5:
        return False

    current_time = now.strftime('%H:%M:%S')
    return config['trading_start_time'] <= current_time <= config['trading_end_time']