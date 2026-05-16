# core/news/news_collector.py

import requests


class NewsCollector:

    def __init__(self):

        self.headers = {
            "User-Agent": "Mozilla/5.0"
        }

    # =========================
    # Google News
    # =========================
    def google(self, keyword):

        try:

            url = (
                "https://news.google.com/rss/search?"
                f"q={keyword}&hl=ja&gl=JP&ceid=JP:ja"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=5
            )

            return res.text

        except:

            return ""

    # =========================
    # Yahoo Finance
    # =========================
    def yahoo(self, code):

        try:

            url = (
                f"https://finance.yahoo.co.jp/quote/"
                f"{code}/news"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=5
            )

            return res.text

        except:

            return ""

    # =========================
    # Kabutan
    # =========================
    def kabutan(self, code):

        try:

            code_num = code.replace(".T", "")

            url = (
                f"https://kabutan.jp/stock/news?"
                f"code={code_num}"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=5
            )

            return res.text

        except:

            return ""

    # =========================
    # Minkabu
    # =========================
    def minkabu(self, code):

        try:

            code_num = code.replace(".T", "")

            url = (
                f"https://minkabu.jp/stock/"
                f"{code_num}/news"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=5
            )

            return res.text

        except:

            return ""

    # =========================
    # TDNET
    # =========================
    def tdnet(self):

        try:

            url = (
                "https://www.release.tdnet.info/"
                "inbs/I_main_00.html"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=5
            )

            return res.text

        except:

            return ""

    # =========================
    # ALL
    # =========================
    def fetch_all(self, code, name):

        text = ""

        text += self.google(name)

        text += self.yahoo(code)

        text += self.kabutan(code)

        text += self.minkabu(code)

        text += self.tdnet()

        return text