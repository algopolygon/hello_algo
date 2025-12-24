"""
Точка входа для запуска торгового бота
"""

import sys
from core.trading_engine import TradingEngine
from strategies.sma_strategy import SMACrossoverStrategy
from config.algo_params import SMA_CROSSOVER_PARAMS
from config.trading_config import TRADING_CONFIG


def main():
    """Главная функция"""

    try:
        print("\n✓ Выбрана стратегия: SMA Crossover")
        print(f"Параметры: Fast SMA = {SMA_CROSSOVER_PARAMS['sma_fast']}, "
              f"Slow SMA = {SMA_CROSSOVER_PARAMS['sma_slow']}")

        strategy = SMACrossoverStrategy(SMA_CROSSOVER_PARAMS)

        # Подтверждение запуска
        print("\n" + "="*70)
        print("📋 Конфигурация торговли:")
        print(f"  Тикер: {TRADING_CONFIG['ticker']}")
        print(f"  Размер позиции: {TRADING_CONFIG['quantity']}")
        print(f"  Таймфрейм: {TRADING_CONFIG['timeframe']} минут")
        print(f"  Торговое время: {TRADING_CONFIG['trading_start_time']} - {TRADING_CONFIG['trading_end_time']}")
        print(f"  Интервал обновления: {TRADING_CONFIG['fetch_interval']} сек")
        print("="*70)

        # Создание и запуск торгового движка
        engine = TradingEngine(strategy, TRADING_CONFIG)

        print("\n🚀 Запуск торгового бота...")
        print("Для остановки нажмите Ctrl+C\n")

        engine.run()

    except KeyboardInterrupt:
        print("\n\n⚠️  Программа остановлена пользователем")
        sys.exit(0)

    except Exception as e:
        print(f"\n❌ Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()