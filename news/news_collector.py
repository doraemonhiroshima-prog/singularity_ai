import requests


class NewsCollector:

    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0"}

    # =========================
    # Google News
    # =========================
    def google(self, keyword):
        try:
            url = f"https://news.google.com/rss/search?q={keyword}&hl=ja&gl=JP&ceid=JP:ja"
            return requests.get(url, headers=self.headers, timeout=3).text
        except:
            return ""

    # =========================
    # Yahoo Finance
    # =========================
    def yahoo(self, code):
        try:
            url = f"https://finance.yahoo.co.jp/quote/{code}/news"
            return requests.get(url, headers=self.headers, timeout=3).text
        except:
            return ""

    # =========================
    # 株探
    # =========================
    def kabutan(self, code):
        try:
            code_num = code.replace(".T", "")
            url = f"https://kabutan.jp/stock/news?code={code_num}"
            return requests.get(url, headers=self.headers, timeout=3).text
        except:
            return ""

    # =========================
    # みんかぶ
    # =========================
    def minkabu(self, code):
        try:
            code_num = code.replace(".T", "")
            url = f"https://minkabu.jp/stock/{code_num}/news"
            return requests.get(url, headers=self.headers, timeout=3).text
        except:
            return ""

    # =========================
    # TDnet
    # =========================
    def tdnet(self):
        try:
            url = "https://www.release.tdnet.info/inbs/I_main_00.html"
            return requests.get(url, headers=self.headers, timeout=3).text
        except:
            return ""

    # =========================
    # Twitter（簡易：将来API）
    # =========================
    def twitter(self, keyword):
        # API無しなので簡易
        return ""

    # =========================
    # 全取得
    # =========================
    def fetch_all(self, code, name):

        text = ""

        text += self.google(name)
        text += self.yahoo(code)
        text += self.kabutan(code)
        text += self.minkabu(code)
        text += self.tdnet()
        text += self.twitter(name)

        return text
