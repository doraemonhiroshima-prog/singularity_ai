import pandas as pd

from strategy.signals import SignalGenerator
from strategy.strategy import Strategy
from Future_prediction.predict_ai import PredictAI


signal_gen = SignalGenerator()
strategy = Strategy()
predict_ai = PredictAI()


def run():

    df = pd.read_csv("data_7203.csv", index_col=0)

    cash = 3_000_000
    position = 0
    entry_price = 0

    history = []

    last_trade_index = -100  # クールダウン用

    for i in range(50, len(df)):

        window = df.iloc[:i]

        price = float(df["Close"].iloc[i])
        volume = float(df["Volume"].iloc[i])
        change = float(df["Close"].pct_change(fill_method=None).iloc[i])

        # =========================
        # トレンドフィルター（重要）
        # =========================
        ma25 = window["Close"].rolling(25).mean().iloc[-1]
        ma75 = window["Close"].rolling(75).mean().iloc[-1]

        trend_ok = (price > ma25) and (ma25 > ma75)

        # =========================
        # AI
        # =========================
        try:
            prob = predict_ai.predict(price, volume, change, 0)
            future = prob * 100
        except:
            future = 50

        signal_data = {
            "T": 60,
            "I": 50,
            "N": 50,
            "F": future
        }

        sig = signal_gen.generate(signal_data)
        decision = strategy.decide(sig, price)

        action = decision.get("action", "HOLD")

        # =========================
        # クールダウン（過剰売買防止）
        # =========================
        if i - last_trade_index < 5:
            action = "HOLD"

        # =========================
        # BUY条件強化
        # =========================
        if action == "BUY" and position == 0 and trend_ok:

            size = 0.3  # ★ここ重要（30%だけ）
            invest = cash * size

            position = invest / price
            entry_price = price
            cash -= invest

            last_trade_index = i

        # =========================
        # SELL
        # =========================
        elif action == "SELL" and position > 0:

            cash += position * price
            position = 0
            entry_price = 0

            last_trade_index = i

        # =========================
        # 強制損切り・利確
        # =========================
        elif position > 0:

            stop_loss = entry_price * 0.95   # -5%
            take_profit = entry_price * 1.15 # +15%

            if price <= stop_loss or price >= take_profit:
                cash += position * price
                position = 0
                entry_price = 0

                last_trade_index = i

        total = cash + position * price
        history.append(total)

    # =========================
    # 結果
    # =========================
    result = pd.Series(history)

    final = result.iloc[-1]
    peak = result.cummax()
    dd = (result - peak) / peak
    max_dd = dd.min()

    print("\n===== SAFE RESULT =====")
    print(f"FINAL: {int(final):,}円")
    print(f"MAX DD: {max_dd:.2%}")


if __name__ == "__main__":
    run()
