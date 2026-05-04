import random
import json
import subprocess
import copy
import multiprocessing as mp

# =========================
# パラメータ生成
# =========================
def generate():
    return {
        "score_threshold": random.randint(160, 180),
        "take_profit": random.uniform(1.04, 1.1),
        "stop_loss": random.uniform(0.9, 0.95),
        "trailing_stop": random.uniform(0.02, 0.05),
        "future_weight": random.randint(1200, 1600),
        "max_positions": random.randint(3, 5),
        "risk_per_trade": random.uniform(0.03, 0.08)
    }

# =========================
# 変異
# =========================
def mutate(p):
    new = copy.deepcopy(p)
    k = random.choice(list(new.keys()))

    if isinstance(new[k], int):
        new[k] += random.randint(-3, 3)

    if isinstance(new[k], float):
        new[k] *= random.uniform(0.95, 1.05)

    return new

# =========================
# バックテスト実行
# =========================
def run_bt(args):
    p, start, end = args

    with open("config.json", "w") as f:
        json.dump(p, f)

    r = subprocess.run(
        ["python", "-m", "backtest.run_backtest", str(start), str(end)],
        capture_output=True,
        text=True
    )

    # 🔥 エラー確認
    if r.returncode != 0:
        print("❌ ERROR:", r.stderr)
        return 0

    # 🔥 ログ表示（重要）
    print(r.stdout)

    # 🔥 SCORE取得
    for line in r.stdout.split("\n"):
        if "SCORE" in line:
            try:
                return float(line.split(":")[1].strip())
            except:
                return 0

    return 0

# =========================
# 評価（並列）
# =========================
def evaluate(p):

    periods = [
        (2010, 2015),
        (2015, 2020),
        (2020, 2026)
    ]

    with mp.Pool(2) as pool:
        scores = pool.map(run_bt, [(p, s, e) for s, e in periods])

    return sum(scores) / len(scores)

# =========================
# メイン
# =========================
if __name__ == "__main__":

    population = [generate() for _ in range(6)]

    best_score = 0
    best = None

    for gen in range(5):

        print(f"\n🔥 GEN {gen}")

        results = []

        for p in population:
            score = evaluate(p)
            results.append((score, p))
            print("SCORE:", score)

        results.sort(reverse=True, key=lambda x: x[0])
        top = results[:2]

        # 🔥 BEST保存
        if top[0][0] > best_score:
            best_score = top[0][0]
            best = top[0][1]

            with open("best.json", "w") as f:
                json.dump(best, f, indent=2)

            print("🔥 BEST更新:", best_score)

        # 次世代生成
        new_pop = []

        for _, p in top:
            new_pop.append(p)
            for _ in range(2):
                new_pop.append(mutate(p))

        population = new_pop[:6]

    print("\n=== BEST ===")
    print(best)
    print("BEST SCORE:", best_score)
