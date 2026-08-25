# core/news/news_collector.py

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import feedparser
from bs4 import BeautifulSoup


class NewsCollector:
    """
    Ω SINGULARITY AI News Collector V1

    役割:
      - ニュース取得
      - 整形
      - 重複除去
      - キャッシュ
      - 並列取得

    分析は行わない。
    SentimentEngine / ThemeDetector / NewsAI が利用する
    list[str] 形式を返す。
    """

    def __init__(self, cache_ttl=600, timeout=5):
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            )
        }

        self.cache_ttl = cache_ttl
        self.timeout = timeout

        self._cache = {}
        self._lock = threading.Lock()

    # =========================
    # CACHE
    # =========================
    def _get_cache(self, key):
        with self._lock:
            if key not in self._cache:
                return None

            timestamp, data = self._cache[key]

            if time.time() - timestamp < self.cache_ttl:
                return data

            del self._cache[key]
            return None

    def _set_cache(self, key, data):
        with self._lock:
            self._cache[key] = (time.time(), data)

    # =========================
    # HTTP GET
    # =========================
    def _safe_get(self, url, timeout=None):
        timeout = timeout or self.timeout

        for _ in range(2):
            try:
                res = requests.get(
                    url,
                    headers=self.headers,
                    timeout=timeout
                )

                if res.status_code == 200:
                    return res

            except Exception:
                continue

        return None

    # =========================
    # CLEAN TEXT
    # =========================
    def _clean_text(self, text):
        text = str(text).replace("\n", " ").replace("\r", " ").strip()

        if len(text) < 15:
            return ""

        noise_words = [
            "ログイン",
            "会員登録",
            "広告",
            "PR",
            "続きを読む",
            "おすすめ",
            "ランキング"
        ]

        if any(word in text for word in noise_words):
            return ""

        return text

    # =========================
    # GOOGLE RSS
    # =========================
    def google(self, keyword):
        cache_key = f"google:{keyword}"
        cached = self._get_cache(cache_key)

        if cached is not None:
            return cached

        results = []

        try:
            url = (
                "https://news.google.com/rss/search?"
                f"q={keyword}"
                "&hl=ja&gl=JP&ceid=JP:ja"
            )

            feed = feedparser.parse(url)

            for entry in feed.entries[:20]:
                title = self._clean_text(entry.title)

                if title:
                    results.append(title)

        except Exception:
            pass

        self._set_cache(cache_key, results)
        return results

    # =========================
    # YAHOO FINANCE
    # =========================
    def yahoo(self, code):
        cache_key = f"yahoo:{code}"
        cached = self._get_cache(cache_key)

        if cached is not None:
            return cached

        results = []

        try:
            url = f"https://finance.yahoo.co.jp/quote/{code}/news"

            res = self._safe_get(url)

            if res is not None:
                soup = BeautifulSoup(res.text, "html.parser")

                texts = soup.get_text("\n", strip=True)

                for line in texts.split("\n"):
                    line = self._clean_text(line)

                    if line:
                        results.append(line)

        except Exception:
            pass

        results = results[:30]
        self._set_cache(cache_key, results)
        return results

    # =========================
    # KABUTAN
    # =========================
    def kabutan(self, code):
        cache_key = f"kabutan:{code}"
        cached = self._get_cache(cache_key)

        if cached is not None:
            return cached

        results = []

        try:
            code_num = code.replace(".T", "")

            url = f"https://kabutan.jp/stock/news?code={code_num}"

            res = self._safe_get(url)

            if res is not None:
                soup = BeautifulSoup(res.text, "html.parser")

                texts = soup.get_text("\n", strip=True)

                for line in texts.split("\n"):
                    line = self._clean_text(line)

                    if line:
                        results.append(line)

        except Exception:
            pass

        results = results[:30]
        self._set_cache(cache_key, results)
        return results

    # =========================
    # MINKABU
    # =========================
    def minkabu(self, code):
        cache_key = f"minkabu:{code}"
        cached = self._get_cache(cache_key)

        if cached is not None:
            return cached

        results = []

        try:
            code_num = code.replace(".T", "")

            url = f"https://minkabu.jp/stock/{code_num}/news"

            res = self._safe_get(url)

            if res is not None:
                soup = BeautifulSoup(res.text, "html.parser")

                texts = soup.get_text("\n", strip=True)

                for line in texts.split("\n"):
                    line = self._clean_text(line)

                    if line:
                        results.append(line)

        except Exception:
            pass

        results = results[:30]
        self._set_cache(cache_key, results)
        return results

    # =========================
    # TDNET
    # =========================
    def tdnet(self):
        cache_key = "tdnet"
        cached = self._get_cache(cache_key)

        if cached is not None:
            return cached

        results = []

        try:
            url = "https://www.release.tdnet.info/inbs/I_main_00.html"

            res = self._safe_get(url)

            if res is not None:
                soup = BeautifulSoup(res.text, "html.parser")

                texts = soup.get_text("\n", strip=True)

                for line in texts.split("\n"):
                    line = self._clean_text(line)

                    if line:
                        results.append(line)

        except Exception:
            pass

        results = results[:50]
        self._set_cache(cache_key, results)
        return results

    # =========================
    # DEDUPLICATE
    # =========================
    def _deduplicate(self, items):
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
# FETCH ALL
# =========================
    def fetch_all(self, code, name):
        news = []

        tasks = {
            "google": lambda: self.google(name),
            "yahoo": lambda: self.yahoo(code),
            "kabutan": lambda: self.kabutan(code),
            "minkabu": lambda: self.minkabu(code),
            "tdnet": self.tdnet
        }

        with ThreadPoolExecutor(max_workers=5) as executor:

            future_map = {
                executor.submit(func): key
                for key, func in tasks.items()
            }

            for future in as_completed(future_map):

                source = future_map[future]

                try:
                    result = future.result()

                    if result:
                        news.extend(result)

                except Exception as e:
                    print(f"[{source}] ERROR : {e}")

        news = self._deduplicate(news)

        return news