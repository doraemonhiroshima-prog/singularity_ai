import pandas as pd
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "model.pkl"
DATA_PATH = "data/training_data.csv"


def train_model():

    print("学習開始...")

    df = pd.read_csv(DATA_PATH)

    features = ["return", "vol_change", "ma5", "ma25"]

    X = df[features]
    y = df["target"]

    # =========================
    # 🔥 クリーニング（最重要）
    # =========================

    # 無限をNaNに
    X = X.replace([np.inf, -np.inf], np.nan)

    # NaN削除
    mask = X.notnull().all(axis=1)
    X = X[mask]
    y = y[mask]

    # 異常値カット（強い）
    X = X.clip(-10, 10)

    print("学習データ数:", len(X))

    if len(X) < 1000:
        print("データ不足")
        return

    # =========================
    # 学習
    # =========================
    model = RandomForestClassifier(
        n_estimators=10,
        max_depth=6,
        random_state=42
    )

    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)

    print("モデル完成")
