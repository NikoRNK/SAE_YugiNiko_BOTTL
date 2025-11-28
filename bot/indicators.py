import math
import numpy as np
import pandas as pd


def compute_rsi(close: pd.Series, period: int = 14) -> pd.Series:
    delta = close.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss.replace(0, 1e-9)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def compute_macd(
    close: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame:
    ema_fast = close.ewm(span=fast, adjust=False).mean()
    ema_slow = close.ewm(span=slow, adjust=False).mean()
    macd = ema_fast - ema_slow
    signal_line = macd.ewm(span=signal, adjust=False).mean()
    return pd.DataFrame({"macd": macd, "signal": signal_line})


def compute_indicators(close: pd.Series) -> pd.DataFrame:
    rsi = compute_rsi(close)
    macd_df = compute_macd(close)
    df = pd.DataFrame({"close": close, "rsi": rsi})
    df["macd"] = macd_df["macd"]
    df["macd_signal"] = macd_df["signal"]
    return df


def compute_volatility(close: pd.Series) -> float:
    returns = np.log(close / close.shift(1)).dropna()
    return float(returns.std() * math.sqrt(365) * 100)
