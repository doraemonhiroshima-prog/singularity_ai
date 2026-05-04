import pandas as pd
import requests
import os


def create_stock_list():

    try:
        print("Downloading JPX stock list...")

        url = "https://www.jpx.co.jp/markets/statistics-equities/misc/tvdivq0000001vg2-att/data_j.xls"

        res = requests.get(url)

        os.makedirs("data", exist_ok=True)

        with open("data/jpx.xls", "wb") as f:
            f.write(res.content)

        # ★ engine削除（自動判定）
        df = pd.read_excel("data/jpx.xls")

        # =========================
        # RENAME
        # =========================
        df = df.rename(columns={
            df.columns[1]: "Code",
            df.columns[2]: "Name",
            df.columns[3]: "Market"
        })

        # =========================
        # CODE CLEAN
        # =========================
        df["Code"] = df["Code"].astype(str).str.extract(r"(\d+)")
        df = df.dropna(subset=["Code"])
        df["Code"] = df["Code"].astype(int).astype(str).str.zfill(4)

        # =========================
        # 除外（ETFなど）
        # =========================
        exclude_keywords = [
            "ETF", "ETN", "REIT", "投資法人",
            "インフラ", "ファンド", "指数", "連動"
        ]

        pattern = "|".join(exclude_keywords)

        df = df[~df["Name"].astype(str).str.contains(pattern, na=False)]

        # =========================
        # 市場フィルター
        # =========================
        df = df[
            df["Market"].astype(str).str.contains(
                "プライム|スタンダード|グロース|Prime|Standard|Growth",
                na=False
            )
        ]

        # =========================
        # コード制限
        # =========================
        df = df[df["Code"].str.match(r"^[1-9][0-9]{3}$")]

        # =========================
        # FINAL
        # =========================
        df = df[["Code", "Name"]]
        df.columns = ["code", "name"]

        df["code"] = df["code"] + ".T"

        # ★ 保存先修正（ここ重要）
        df.to_csv("data/stock_list.csv", index=False, encoding="utf-8-sig")

        print(f"✅ 完了: {len(df)} 銘柄")

    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    create_stock_list()
