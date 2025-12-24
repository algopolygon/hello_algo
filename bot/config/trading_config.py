"""
Технические параметры торговли
"""

TRADING_CONFIG = {
    'ticker': 'GAZP',
    'quantity': 700,
    'trading_start_time': '07:05:00',
    'trading_end_time': '23:40:00',
    'history_days': 3,
    'fetch_interval': 60,
    'timeframe': 10,
}

ARENA_CONFIG = {
    'url': 'https://arenago.ru',
    'token': '054078..........ee8b51',
    'bot': 'baseline_bot'
}

MOEX_API_BASE = 'https://iss.moex.com/iss/engines/stock/markets/shares/boards/tqbr/securities'
