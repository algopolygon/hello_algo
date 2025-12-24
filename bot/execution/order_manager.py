"""
Управление ордерами и их исполнение
"""

import requests
from datetime import datetime
from config.trading_config import ARENA_CONFIG


class OrderManager:
    """Менеджер для отправки ордеров"""

    def __init__(self, config=ARENA_CONFIG):
        self.config = config
        self.url = config['url']
        self.token = config['token']
        self.bot = config['bot']

    def submit_order(self, direction, secid, quantity):
        """Отправить ордер в Arena GO"""
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"{self.token}"
        }

        params = {
            "direction": direction,
            "secid": secid,
            "quantity": quantity,
            "bot": self.bot
        }

        try:
            response = requests.post(
                f"{self.url}/api/submit_order",
                headers=headers,
                json=params,
                timeout=10
            )

            if response.status_code == 200:
                print(f"✓ Order executed: {direction} {quantity} {secid}")
                return True
            else:
                print(f"✗ Order failed: {response.status_code}, {response.text}")
                return False

        except Exception as e:
            print(f"✗ Order error: {e}")
            return False