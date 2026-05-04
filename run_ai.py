import glob
import os
import pandas as pd

from ai.technical.technical_runner import TechnicalAI
from ai.institution.institution_ai import InstitutionAI
from ai.institution.flow_detector import FlowDetector
from ai.institution.order_estimator import OrderEstimator
from ai.institution.pressure_analyzer import PressureAnalyzer

from ai.Future_prediction.predict_ai import PredictAI
from news.news_ai import NewsAI

from core.signals.strategy.strategy import StrategyAI
from core.portfolio.portfolio_ai import PortfolioAI

from growth.evaluator import Evaluator
from growth.growth_ai import GrowthAI


tech_ai = TechnicalAI()
inst_ai = InstitutionAI()
flow = FlowDetector()
order = OrderEstimator()
pressure = PressureAnalyzer()

pred_ai = PredictAI()
news_ai = NewsAI()

strategy_ai = StrategyAI()
portfolio = PortfolioAI(3000000)

evaluator = Evaluator()
growth = GrowthAI()


def run():

    files = glob.glob("data/*.csv")
    signals = []

    for f in files:

        try:
            code = os.path.basename(f).replace(".csv", "")
            df = pd.read_csv(f)

            if len(df) < 50:
                continue

            if "Close" not in df.columns:
                df.columns = ["Date","Close","High","Low","Open","Volume"]

            df = df.dropna()

            close = df["Close"]
            volume = df["Volume"]

            price = float(close.iloc[-1])
            vol = float(volume.iloc[-1])
            change = float(close.pct_change().iloc[-1])

            tech = tech_ai.process([{
                "code": code,
                "name": code,
                "df": df,
                "market_score": 0
            }])

            tech_score = tech[0]["technical_score"] if tech else 0

            inst_score = inst_ai.analyze(df)
            flow_score = flow.analyze(df)
            order_score = order.analyze(df)
            pressure_score = pressure.analyze(df)

            news_score = news_ai.analyze(code)

            prob = pred_ai.predict(price, vol, change, news_score)

            signals.append({
                "code": code,
                "price": price,
                "tech": tech_score,
                "inst": inst_score,
                "flow": flow_score,
                "order": order_score,
                "pressure": pressure_score,
                "news": news_score,
                "prob": prob
            })

        except Exception as e:
            print("ERROR:", f, e)

    # =========================
    # 上位選定
    # =========================
    ranked = sorted(signals, key=lambda x: x["prob"], reverse=True)[:10]

    # =========================
    # 売買
    # =========================
    for s in ranked:

        if s["prob"] < 0.55:
            continue

        strategy = strategy_ai.build(s)
        portfolio.try_buy(s, strategy)

    portfolio.update()
    portfolio.status()

    # =========================
    # 評価＆進化
    # =========================
    results = sorted(signals, key=lambda x: x["prob"], reverse=True)

    metrics = evaluator.evaluate(results)
    growth.update(metrics)


if __name__ == "__main__":
    run()
