class Strategy:

    def decide(self, signal_data, price):

        signal = signal_data["signal"]

        # =========================
        # エントリー
        # =========================
        if signal == "STRONG_BUY":
            return {
                "action": "BUY",
                "size": 1.0,   # フル
                "stop_loss": price * 0.93,
                "take_profit": price * 1.15
            }

        elif signal == "BUY":
            return {
                "action": "BUY",
                "size": 0.5,
                "stop_loss": price * 0.95,
                "take_profit": price * 1.10
            }

        # =========================
        # ホールド
        # =========================
        elif signal == "HOLD":
            return {
                "action": "HOLD"
            }

        # =========================
        # 売り
        # =========================
        else:
            return {
                "action": "SELL"
            }
