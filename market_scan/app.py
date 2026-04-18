from flask import Flask, render_template_string
import pandas as pd
from market_scan.market_scan_ai import MarketScanAI
from technical.technical_runner import TechnicalAI

app = Flask(__name__)

# =========================
# AI初期化
# =========================
market_ai = MarketScanAI()
tech_ai = TechnicalAI()

# =========================
# HTML
# =========================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Stock AI Dashboard</title>
</head>
<body>
    <h1>Ω SINGULARITY AI</h1>

    <form method="get">
        <button type="submit">Run Scan</button>
    </form>

    <hr>

    {% for row in data %}
        <h3>{{ row.code }} {{ row.name }}</h3>

        <p>
        Score: {{ row.score }} |
        Signal: {{ row.signal }} |
        Confidence: {{ row.confidence }}<br>
        Price: {{ row.price }}
        </p>

        <hr>
    {% endfor %}
</body>
</html>
"""

# =========================
# メイン処理
# =========================
def run_pipeline():

    scan_results = market_ai.process()

    final = []

    for r in scan_results:

        code = r["code"]

        try:
            from market_scan.data_fetcher import fetch_data
            data = fetch_data([code])

            if code not in data:
                continue

            df = data[code]

            tech = tech_ai.process(df)

            final.append({
                "code": code,
                "name": r["name"],
                "score": r["score"],
                "price": r["price"],
                "signal": tech["signal"],
                "confidence": tech["confidence"]
            })

        except:
            continue

    return final[:20]

# =========================
# ルート
# =========================
@app.route("/")
def index():
    data = run_pipeline()
    return render_template_string(HTML, data=data)

# =========================
# 実行
# =========================
if __name__ == "__main__":
    app.run(debug=True)
