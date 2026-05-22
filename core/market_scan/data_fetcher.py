import yfinance as yf


def fetch_data(codes):

    data = {}

    try:

        # =========================
        # BATCH DOWNLOAD
        # =========================
        dfs = yf.download(
            codes,
            period="6mo",
            interval="1d",
            group_by="ticker",
            threads=True,
            progress=False
        )

        # =========================
        # SINGLE / MULTI 対応
        # =========================
        if len(codes) == 1:

            code = codes[0]

            if dfs is not None and not dfs.empty:
                data[code] = dfs

            return data

        # =========================
        # MULTI
        # =========================
        for code in codes:

            try:

                if code not in dfs:
                    continue

                df = dfs[code]

                if df is None or df.empty:
                    continue

                data[code] = df

            except Exception as e:

                print(
                    "PARSE ERROR:",
                    code,
                    e
                )

    except Exception as e:

        print(
            "BATCH DL ERROR:",
            e
        )

    return data