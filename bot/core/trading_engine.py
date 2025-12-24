"""
Основной торговый движок
"""

import time
import pandas as pd
from datetime import datetime
from data.moex_client import MOEXClient
from execution.order_manager import OrderManager
from core.portfolio import Portfolio
from utils.time_utils import is_trading_time
from config.trading_config import TRADING_CONFIG


class TradingEngine:
    """Торговый движок"""

    def __init__(self, strategy, config=TRADING_CONFIG):
        self.strategy = strategy
        self.config = config
        self.moex_client = MOEXClient()
        self.order_manager = OrderManager()
        self.portfolio = Portfolio()
        self.market_data = pd.DataFrame()

    def initialize(self):
        """Инициализация - загрузка исторических данных"""
        print(f"🚀 Starting Trading Algorithm: {self.strategy.name}")
        print(f"Ticker: {self.config['ticker']}")
        print(f"Timeframe: {self.config['timeframe']} minutes")
        print(f"Position size: {self.config['quantity']}")
        print("="*70)

        print(f"\n📊 Loading {self.config['history_days']} days of historical data...")
        self.market_data = self.moex_client.load_historical_data(
            self.config['ticker'],
            self.config['history_days'],
            self.config['timeframe']
        )

        if self.market_data.empty:
            raise Exception("Failed to load historical data")

        self.market_data = self.strategy.calculate_indicators(self.market_data)
        print("✓ Ready to trade!\n")

    def update_market_data(self):
        """Обновить рыночные данные"""
        today_data = self.moex_client.fetch_today_data(
            self.config['ticker'],
            self.config['timeframe']
        )

        if not today_data.empty:
            self.market_data = pd.concat([self.market_data, today_data], ignore_index=True)
            self.market_data = self.market_data.drop_duplicates(subset=['begin']).sort_values('begin')
            self.market_data = self.market_data.reset_index(drop=True)
            self.market_data = self.strategy.calculate_indicators(self.market_data)
            return True
        return False

    def execute_signal(self, signal):
        """Исполнить торговый сигнал"""
        ticker = self.config['ticker']
        quantity = self.config['quantity']
        current_position = self.portfolio.get_position()
        current_price = self.market_data.iloc[-1]['close']

        if signal == 'BUY':
            # Закрыть short если есть
            if current_position < 0:
                if self.order_manager.submit_order('B', ticker, quantity):
                    self.portfolio.close_position('CLOSE SHORT', quantity, current_price)
                    time.sleep(0.5)

            # Открыть long
            if self.portfolio.get_position() == 0:
                if self.order_manager.submit_order('B', ticker, quantity):
                    self.portfolio.update_position(1, 'OPEN LONG', quantity, current_price)

        elif signal == 'SELL':
            # Закрыть long если есть
            if current_position > 0:
                if self.order_manager.submit_order('S', ticker, quantity):
                    self.portfolio.close_position('CLOSE LONG', quantity, current_price)
                    time.sleep(0.5)

            # Открыть short
            if self.portfolio.get_position() == 0:
                if self.order_manager.submit_order('S', ticker, quantity):
                    self.portfolio.update_position(-1, 'OPEN SHORT', quantity, current_price)

        elif signal == 'CLOSE':
            if current_position > 0:
                if self.order_manager.submit_order('S', ticker, quantity):
                    self.portfolio.close_position('CLOSE LONG', quantity, current_price)
            elif current_position < 0:
                if self.order_manager.submit_order('B', ticker, quantity):
                    self.portfolio.close_position('CLOSE SHORT', quantity, current_price)

    def print_status(self):
        """Вывод текущего статуса"""
        if len(self.market_data) == 0:
            return

        last = self.market_data.iloc[-1]
        position = self.portfolio.get_position()
        position_str = {-1: "SHORT", 0: "FLAT", 1: "LONG"}[position]

        print(f"\n{'='*70}")
        print(f"🕐 Time: {last['begin']} | Position: {position_str}")
        print(f"💰 Close: {last['close']:.2f}")

        # Вывод индикаторов в зависимости от стратегии
        if 'sma_fast' in last and 'sma_slow' in last:
            print(f"📊 SMA Fast: {last['sma_fast']:.2f} | SMA Slow: {last['sma_slow']:.2f}")

        if 'rsi' in last:
            print(f"📊 RSI: {last['rsi']:.1f}")

        if 'bb_upper' in last:
            print(f"📊 BB: [{last['bb_lower']:.2f}, {last['bb_middle']:.2f}, {last['bb_upper']:.2f}]")

        print(f"🔢 Trades today: {self.portfolio.get_trade_count()}")
        print(f"{'='*70}")

    def close_all_positions(self):
        """Закрыть все позиции в конце дня"""
        position = self.portfolio.get_position()
        ticker = self.config['ticker']
        quantity = self.config['quantity']

        if position != 0:
            direction = 'S' if position > 0 else 'B'
            action = 'EOD CLOSE LONG' if position > 0 else 'EOD CLOSE SHORT'

            print(f"📕 Closing position (end of day)...")
            if self.order_manager.submit_order(direction, ticker, quantity):
                price = self.market_data.iloc[-1]['close']
                self.portfolio.close_position(action, quantity, price)

    def run(self):
        """Основной торговый цикл"""
        self.initialize()

        iteration = 0

        while True:
            try:
                iteration += 1
                now = datetime.now()
                current_time = now.strftime('%H:%M:%S')

                # Проверка времени торговли
                if not is_trading_time(self.config):
                    if current_time > self.config['trading_end_time']:
                        print("\n⏰ Trading session ended.")
                        self.close_all_positions()
                        break

                    print(f"⏸ Outside trading hours. Waiting... ({current_time})")
                    time.sleep(60)
                    continue

                # Обновление данных
                print(f"\n[Iteration {iteration}] ⟳ Fetching new data... ({current_time})")

                if self.update_market_data():
                    # Генерация сигнала
                    signal = self.strategy.generate_signal(
                        self.market_data,
                        len(self.market_data) - 1,
                        self.portfolio.get_position()
                    )

                    print(f"🎯 Signal: {signal}")

                    # Исполнение
                    if signal in ['BUY', 'SELL', 'CLOSE']:
                        self.execute_signal(signal)

                    # Статус
                    self.print_status()
                else:
                    print("⚠ No new data received")

                # Ожидание
                time.sleep(self.config['fetch_interval'])

            except KeyboardInterrupt:
                print("\n\n⚠ Algorithm stopped by user")
                self.close_all_positions()
                break

            except Exception as e:
                print(f"✗ Error in main loop: {e}")
                import traceback
                traceback.print_exc()
                time.sleep(10)

        # Итоги
        self.portfolio.print_summary()