import os
import glob
import pandas as pd
import json
import sys

from core.strategy.strategy import StrategyAI
from core.portfolio.portfolio_ai import PortfolioAI
from core.signal.signals import SignalGenerator

from ai.technical.technical_runner import TechnicalRunner
from ai.institution.institution_ai import InstitutionAI

from data_pipeline.data_cleaner import clean_df


START_CASH = 3000000


def run_backtest(start_year=None, end_year=None):

    # =========================
    # config
    # =========================
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except:
        config = {}

    # =========================
    # AI初期化
    # =========================
    strategy_ai = StrategyAI()
    signal_ai = SignalGenerator()
    portfolio = PortfolioAI(START_CASH)

    tech_ai = TechnicalRunner()
    inst_ai = InstitutionAI()

    # =========================
    # データ読み込み
    # =========================
    files = glob.glob("data/*.csv")

    data_map = {}

    for f in files:
        try:
            code = os.path.basename(f).replace(".csv", "")
            df = pd.read_csv(f)
            df = clean_df(df)

            if "Date" in df.columns:
                df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

                if start_year:
                    df = df[df["Date"].dt.year >= start_year]
                if end_year:
                    df = df[df["Date"].dt.year <= end_year]

            if len(df) < 120:
                continue

            if "Close" not in df.columns:
                print("❌ 欠損列:", code)
                continue

            data_map[code] = df.reset_index(drop=True)

        except:
            continue

    print("銘柄数:", len(data_map))

    if len(data_map) == 0:
        print("❌ データ無し")
        return 0

    # =========================
    # バックテスト
    # =========================
    max_days = min([len(df) for df in data_map.values()])

    total_signals = 0
    total_trades = 0

    for day in range(100, max_days - 1):

        signals = []

        for code, df in data_map.items():

            if day >= len(df):
                continue

            past = df.iloc[:day]
            price = df.iloc[day]["Close"]

            # ===== AIスコア =====
            tech = tech_ai.analyze(past) if hasattr(tech_ai, "analyze") else 50
            inst = inst_ai.analyze(past) if hasattr(inst_ai, "analyze") else 50

            news = 50
            growth = 50

            # ===== future =====
            ma5 = past["Close"].rolling(5).mean().iloc[-1]
            ma20 = past["Close"].rolling(20).mean().iloc[-1]

            if ma20 == 0 or pd.isna(ma20):
                continue

            diff = (ma5 - ma20) / ma20

            fw = config.get("future_weight", 800)

            future = 50 + (diff * fw)
            future = max(0, min(100, future))

            data = {
                "tech": tech,
                "inst": inst,
                "news": news,
                "future": future,
                "growth": growth
            }

            sig = signal_ai.generate(data)

            # 🔥 強制デバッグ（シグナル確認）
            if sig["signal"] == "BUY":
                signals.append({
                    "code": code,
                    "price": price,
                    "confidence": sig["confidence"]
                })

        # 🔥 シグナル数確認
        print(f"DAY {day} SIGNALS:", len(signals))
        total_signals += len(signals)

        # =========================
        # 強制トレードON（デバッグ用）
        # =========================
        selected = signals[:5]  # ← strategy無効化

        # =========================
        # 売買
        # =========================
        for s in selected:
            portfolio.buy(s)
            total_trades += 1

        portfolio.update(data_map, day)

    print("総シグナル:", total_signals)
    print("総トレード:", total_trades)

    # =========================
    # 結果
    # =========================
    final = portfolio.total_value(data_map, day)

    total = len(portfolio.trade_log)
    profits = [t["pl"] for t in portfolio.trade_log]

    if total > 0:
        win = len([p for p in profits if p > 0]) / total
    else:
        win = 0

    # DD
    equity = [t["equity"] for t in portfolio.trade_log]

    peak = 0
    dd = 0

    for v in equity:
        if v > peak:
            peak = v
        if peak > 0:
            dd = max(dd, (peak - v) / peak)

    score = (final / START_CASH) + win - dd

    print("\n=== RESULT ===")
    print("開始:", START_CASH)
    print("終了:", int(final))
    print("倍率:", round(final / START_CASH, 4))
    print("勝率:", round(win, 3))
    print("DD:", round(dd, 3))
    print("SCORE:", round(score, 3))

    return score


# =========================
# CLI
# =========================
if __name__ == "__main__":

    if len(sys.argv) == 3:
        s = int(sys.argv[1])
        e = int(sys.argv[2])
        run_backtest(s, e)

    elif len(sys.argv) == 2:
        s = int(sys.argv[1])
        run_backtest(s, None)

    else:
        run_backtest()
