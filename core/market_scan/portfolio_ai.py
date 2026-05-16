class PortfolioAI:

    def __init__(self, config):
        self.config = config

    def decide_buy(self, candidates, portfolio, market_regime="BULL"):

        decisions = []

        if market_regime == "BEAR":
            return decisions

        candidates = sorted(candidates, key=lambda x: x["score"], reverse=True)

        for c in candidates[:self.config.TOP_N]:

            code = c["code"]
            price = c["price"]
            score = c["score"]

            if score < self.config.MIN_SCORE:
                continue

            if code in portfolio.positions:
                continue

            if len(portfolio.positions) >= self.config.MAX_POSITIONS:
                break

            # ★ スコア連動資金配分
            weight = min(score / 100, 1.0)
            amount = portfolio.cash * 0.2 * weight

            decisions.append({
                "action": "BUY",
                "code": code,
                "price": price,
                "amount": amount
            })

        return decisions

    def decide_sell(self, portfolio, data_map, sell_func):

        decisions = []

        for code, pos in portfolio.positions.items():

            if code not in data_map:
                continue

            df = data_map[code]

            signal = sell_func(
                df,
                pos["buy_price"],
                pos.get("peak")
            )

            if signal == "TAKE_PROFIT":
                decisions.append({"action": "SELL_HALF", "code": code})

            elif signal in ["STOP_LOSS", "TRAILING_STOP", "TREND_BREAK"]:
                decisions.append({"action": "SELL_ALL", "code": code})

        return decisions