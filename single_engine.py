import pandas as pd
import numpy as np
import random

class SignalEngine:
    def __init__(self, assets):
        self.assets = assets

    def get_signal(self, asset):
        data = self._simulate_data()
        ema_fast = data['close'].ewm(span=9).mean()
        ema_slow = data['close'].ewm(span=21).mean()
        rsi = self._compute_rsi(data['close'], 14)
        atr = self._compute_atr(data)

        signal = None
        if ema_fast.iloc[-1] > ema_slow.iloc[-1] and rsi.iloc[-1] < 70:
            signal = 'BUY'
        elif ema_fast.iloc[-1] < ema_slow.iloc[-1] and rsi.iloc[-1] > 30:
            signal = 'SELL'

        if signal:
            entry = data['close'].iloc[-1]
            tp = entry + 1.5 * atr if signal == 'BUY' else entry - 1.5 * atr
            sl = entry - atr if signal == 'BUY' else entry + atr
            return {'signal': signal, 'entry': entry, 'tp': tp, 'sl': sl}
        return None

    def _simulate_data(self):
        prices = [100 + random.uniform(-1, 1) for _ in range(100)]
        return pd.DataFrame({'close': prices})

    def _compute_rsi(self, series, period):
        delta = series.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def _compute_atr(self, data, period=14):
        high = data['close'] + 0.5
        low = data['close'] - 0.5
        close = data['close']
        tr = pd.DataFrame({
            'h-l': high - low,
            'h-c': abs(high - close.shift()),
            'l-c': abs(low - close.shift())
        }).max(axis=1)
        atr = tr.rolling(window=period).mean()
        return atr.iloc[-1]