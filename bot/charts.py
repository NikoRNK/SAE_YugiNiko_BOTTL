from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from .indicators import compute_indicators


def build_price_chart_png(ohlc: list[list[float]], file_path: Path) -> None:
    timestamps = [row[0] for row in ohlc]
    closes = [row[4] for row in ohlc]

    plt.figure(figsize=(8, 4))
    plt.plot(timestamps, closes)
    plt.title("Prix en USD")
    plt.xlabel("Temps")
    plt.ylabel("Prix")
    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()


def build_indicators_chart_png(ohlc: list[list[float]], file_path: Path) -> None:
    closes = [row[4] for row in ohlc]
    close_series = pd.Series(closes)
    ind = compute_indicators(close_series)

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 8), sharex=True)

    ax1.plot(ind.index, ind["close"])
    ax1.set_title("Prix")

    ax2.plot(ind.index, ind["rsi"], label="RSI")
    ax2.axhline(30, color="red", linestyle="--", linewidth=0.8)
    ax2.axhline(70, color="red", linestyle="--", linewidth=0.8)
    ax2.set_title("RSI")
    ax2.legend()

    ax3.plot(ind.index, ind["macd"], label="MACD")
    ax3.plot(ind.index, ind["macd_signal"], label="Signal")
    ax3.set_title("MACD")
    ax3.legend()

    plt.tight_layout()
    plt.savefig(file_path)
    plt.close()
