"""
Клиент для работы с API Московской биржи
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from config.venue_config import MOEX_DATA_API


class MOEXClient:
    """Клиент для получения данных с MOEX"""

    def __init__(self, base_url=MOEX_DATA_API):
        self.base_url = base_url

    def fetch_candles(self, ticker, from_date, till_date, interval=10, start=0):
        """Получить свечи с MOEX"""
        url = f"{self.base_url}/{ticker}/candles.json"
        params = {
            'from': from_date,
            'till': till_date,
            'interval': interval,
            'start': start
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                candles = data['candles']['data']
                columns = data['candles']['columns']
                df = pd.DataFrame(candles, columns=columns)
                if not df.empty:
                    df['begin'] = pd.to_datetime(df['begin'])
                    df['close'] = pd.to_numeric(df['close'], errors='coerce')
                    df['open'] = pd.to_numeric(df['open'], errors='coerce')
                    df['high'] = pd.to_numeric(df['high'], errors='coerce')
                    df['low'] = pd.to_numeric(df['low'], errors='coerce')
                    df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
                return df
            else:
                print(f"MOEX API error: {response.status_code}")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error fetching candles: {e}")
            return pd.DataFrame()

    def load_historical_data(self, ticker, days=3, interval=10):
        """Загрузить исторические данные за несколько дней"""
        all_data = []

        for i in range(days, 0, -1):
            date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')

            df = self.fetch_candles(ticker, date, date, interval=interval, start=0)
            if not df.empty:
                all_data.append(df)

            time.sleep(0.3)

        if all_data:
            combined = pd.concat(all_data, ignore_index=True)
            combined = combined.sort_values('begin').drop_duplicates(subset=['begin'])
            combined = combined.reset_index(drop=True)
            print(f"✓ Загружено {len(combined)} исторических свечей ({interval}-min)")
            return combined

        return pd.DataFrame()

    def fetch_today_data(self, ticker, interval=10):
        """Получить данные за сегодня"""
        today = datetime.now().strftime('%Y-%m-%d')
        df = self.fetch_candles(ticker, today, today, interval=interval, start=0)

        if not df.empty:
            df = df.sort_values('begin').drop_duplicates(subset=['begin'])

        return df