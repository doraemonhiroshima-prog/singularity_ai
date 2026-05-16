class LearningAnalyzer:

    def analyze(self, portfolio_ai):

        print("\n=== LEARNING ANALYSIS ===")

        stats = portfolio_ai.stock_stats
        signals = portfolio_ai.signal_stats
        memory = portfolio_ai.memory_score

        # =========================
        # ① 銘柄学習状況
        # =========================
        print("\n[TOP WINNING STOCKS]")

        top = sorted(
            stats.items(),
            key=lambda x: x[1]["pnl_sum"],
            reverse=True
        )[:10]

        for code, s in top:
            win_rate = s["wins"] / max(1, s["wins"] + s["losses"])
            avg = s["pnl_sum"] / max(1, s["wins"] + s["losses"])

            print(code, "WR:", round(win_rate, 2), "AVG:", round(avg, 4))

        # =========================
        # ② 負け銘柄
        # =========================
        print("\n[TOP LOSING STOCKS]")

        worst = sorted(
            stats.items(),
            key=lambda x: x[1]["pnl_sum"]
        )[:10]

        for code, s in worst:
            win_rate = s["wins"] / max(1, s["wins"] + s["losses"])
            avg = s["pnl_sum"] / max(1, s["wins"] + s["losses"])

            print(code, "WR:", round(win_rate, 2), "AVG:", round(avg, 4))

        # =========================
        # ③ SIGNAL学習
        # =========================
        print("\n[SIGNAL PERFORMANCE]")

        for sig, s in signals.items():
            total = s["wins"] + s["losses"]
            if total == 0:
                continue

            wr = s["wins"] / total

            print(sig, "WR:", round(wr, 2), "COUNT:", total)

        # =========================
        # ④ 学習進度判定
        # =========================
        total_trades = sum(
            s["wins"] + s["losses"]
            for s in stats.values()
        )

        print("\n[LEARNING PROGRESS]")

        if total_trades < 50:
            print("STATUS: NOISE (まだ学習前)")
        elif total_trades < 200:
            print("STATUS: EARLY LEARNING")
        elif total_trades < 500:
            print("STATUS: STRUCTURE FORMING")
        else:
            print("STATUS: INSTITUTION LEVEL SIGNAL")