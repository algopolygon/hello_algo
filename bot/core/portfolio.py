"""
Управление позицией и историей сделок
"""

from datetime import datetime


class Portfolio:
    """Управление позицией и сделками"""

    def __init__(self):
        self.position = 0  # -1, 0, 1
        self.trade_history = []

    def get_position(self):
        """Получить текущую позицию"""
        return self.position

    def update_position(self, new_position, action, quantity, price):
        """Обновить позицию"""
        self.position = new_position

        self.trade_history.append({
            'time': datetime.now(),
            'action': action,
            'quantity': quantity,
            'price': price,
            'position': new_position
        })

    def close_position(self, action, quantity, price):
        """Закрыть позицию"""
        prev_position = self.position
        self.position = 0

        self.trade_history.append({
            'time': datetime.now(),
            'action': action,
            'quantity': quantity,
            'price': price,
            'prev_position': prev_position,
            'position': 0
        })

    def get_trade_count(self):
        """Количество сделок"""
        return len(self.trade_history)

    def get_trade_history(self):
        """История сделок"""
        return self.trade_history

    def print_summary(self):
        """Печать итоговой статистики"""
        print("\n" + "="*70)
        print("📊 TRADING SESSION SUMMARY")
        print("="*70)
        print(f"Total trades: {len(self.trade_history)}")
        print("\nTrade log:")
        for i, trade in enumerate(self.trade_history, 1):
            print(f"  {i}. {trade['time'].strftime('%H:%M:%S')} | "
                  f"{trade['action']:15s} | "
                  f"{trade['quantity']} @ {trade['price']:.2f}")
        print("="*70)