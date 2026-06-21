# core/news/news_collector.py

import requests
import feedparser

from bs4 import BeautifulSoup


class NewsCollector:

    def __init__(self):

        self.headers = {
            "User-Agent":
            "Mozilla/5.0"
        }

        # TDNETキャッシュ
        self._tdnet_cache = None

    # =========================
    # Google News RSS
    # =========================
    def google(self, keyword):

        results = []

        try:

            url = (
                "https://news.google.com/rss/search?"
                f"q={keyword}"
                "&hl=ja&gl=JP&ceid=JP:ja"
            )

            feed = feedparser.parse(url)

            for entry in feed.entries[:20]:

                title = (
                    entry.title
                    .replace("\n", " ")
                    .strip()
                )

                if title:
                    results.append(title)

        except Exception:
            pass

        return results

    # =========================
    # Yahoo Finance
    # =========================
    def yahoo(self, code):

        results = []

        try:

            url = (
                f"https://finance.yahoo.co.jp/quote/"
                f"{code}/news"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=3
            )

            soup = BeautifulSoup(
                res.text,
                "html.parser"
            )

            texts = soup.get_text(
                "\n",
                strip=True
            )

            for line in texts.split("\n"):

                line = line.strip()

                if len(line) < 15:
                    continue

                results.append(line)

        except Exception:
            pass

        return results[:30]

    # =========================
    # Kabutan
    # =========================
    def kabutan(self, code):

        results = []

        try:

            code_num = (
                code.replace(".T", "")
            )

            url = (
                "https://kabutan.jp/stock/news?"
                f"code={code_num}"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=3
            )

            soup = BeautifulSoup(
                res.text,
                "html.parser"
            )

            texts = soup.get_text(
                "\n",
                strip=True
            )

            for line in texts.split("\n"):

                line = line.strip()

                if len(line) < 15:
                    continue

                results.append(line)

        except Exception:
            pass

        return results[:30]

    # =========================
    # Minkabu
    # =========================
    def minkabu(self, code):

        results = []

        try:

            code_num = (
                code.replace(".T", "")
            )

            url = (
                f"https://minkabu.jp/stock/"
                f"{code_num}/news"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=3
            )

            soup = BeautifulSoup(
                res.text,
                "html.parser"
            )

            texts = soup.get_text(
                "\n",
                strip=True
            )

            for line in texts.split("\n"):

                line = line.strip()

                if len(line) < 15:
                    continue

                results.append(line)

        except Exception:
            pass

        return results[:30]

    # =========================
    # TDNET
    # =========================
    def tdnet(self):

        # キャッシュ利用
        if self._tdnet_cache is not None:
            return self._tdnet_cache

        results = []

        try:

            url = (
                "https://www.release.tdnet.info/"
                "inbs/I_main_00.html"
            )

            res = requests.get(
                url,
                headers=self.headers,
                timeout=3
            )

            soup = BeautifulSoup(
                res.text,
                "html.parser"
            )

            texts = soup.get_text(
                "\n",
                strip=True
            )

            for line in texts.split("\n"):

                line = line.strip()

                if len(line) < 15:
                    continue

                results.append(line)

        except Exception:
            pass

        self._tdnet_cache = results[:50]

        return self._tdnet_cache

    # =========================
    # 重複除去
    # =========================
    def _deduplicate(
        self,
        items
    ):

        seen = set()

        result = []

        for item in items:

            key = item.strip()

            if key in seen:
                continue

            seen.add(key)

            result.append(item)

        return result

    # =========================
    # ALL NEWS
    # =========================
    def fetch_all(
        self,
        code,
        name
    ):

        news = []

        news.extend(
            self.google(name)
        )

        news.extend(
            self.yahoo(code)
        )

        news.extend(
            self.kabutan(code)
        )

        news.extend(
            self.minkabu(code)
        )

        news.extend(
            self.tdnet()
        )

        news = self._deduplicate(
            news
        )

        return news