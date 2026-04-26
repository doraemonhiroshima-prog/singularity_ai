import pandas as pd


class TechnicalAI:

    def process(self, market_data):

        results = []

        for r in market_data:

            try:
                df = r["df"].copy()

                # =========================
                # データ前処理
                # =========================
                df = df.dropna()

                if len(df) < 80:
                    continue

                close = pd.to_numeric(df["Close"], errors="coerce")
                volume = pd.to_numeric(df["Volume"], errors="coerce")

                price = float(close.iloc[-1])

                ma5 = close.rolling(5).mean()
                ma25 = close.rolling(25).mean()
                ma75 = close.rolling(75).mean()

                score = 0

                # =========================
                # トレンド（強化）
                # =========================
                if price > ma25.iloc[-1]:
                    score += 20

                if price > ma75.iloc[-1]:
                    score += 30

                if ma25.iloc[-1] > ma75.iloc[-1]:
                    score += 20  # 上昇トレンド確定

                # =========================
                # モメンタム（強化）
                # =========================
                ret5 = close.pct_change(5).iloc[-1]
                ret20 = close.pct_change(20).iloc[-1]

                if ret5 > 0.03:
                    score += 15

                if ret20 > 0.10:
                    score += 25

                # =========================
                # ブレイクアウト
                # =========================
                high20 = close.shift(1).rolling(20).max().iloc[-1]

                if price > high20:
                    score += 40

                # =========================
                # 🔥 出来高初動（最重要）
                # =========================
                v_now = volume.iloc[-1]
                v_avg = volume.rolling(20).mean().iloc[-1]

                if v_avg > 0:
                    ratio = v_now / v_avg

                    if ratio > 3:
                        score += 100
                    elif ratio > 2:
                        score += 60
                    elif ratio > 1.5:
                        score += 30

                # =========================
                # フィルタ（重要）
                # =========================
                if score < 40:
                    continue

                # =========================
                # 出力
                # =========================
                results.append({
                    "code": r["code"],
                    "name": r.get("name", ""),
                    "df": df,
                    "market_score": r.get("market_score", 0),
                    "technical_score": int(score),
                    "market_cap": r.get("market_cap", 0),
                    "price": price
                })

            except Exception as e:
                print(f"TECH ERROR: {r.get('code', 'UNKNOWN')} {e}")
                continue

        # =========================
        # スコア順にソート
        # =========================
        results = sorted(results, key=lambda x: x["technical_score"], reverse=True)

        return results
