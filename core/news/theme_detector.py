     # core/news/theme_detector.py

class ThemeDetector:

    def __init__(self):

        # 将来 evolution.py が学習で更新
        self.theme_weights = {

            "AI": 1.0,
            "半導体": 1.0,
            "EV": 1.0,
            "DX": 1.0,
            "バイオ": 1.0,
            "ロボット": 1.0,
            "量子": 1.0,
            "宇宙": 1.0,
            "防衛": 1.0,
            "再エネ": 1.0,
            "データセンター": 1.0,
            "サイバー": 1.0
        }

        self.themes = {

            "量子": [
                "量子",
                "量子コンピュータ",
                "量子技術"
            ],

            "宇宙": [
                "宇宙",
                "ロケット",
                "人工衛星",
                "SpaceX"
            ],

            "防衛": [
                "防衛",
                "防衛省",
                "軍需"
            ],

            "再エネ": [
                "再生可能",
                "太陽光",
                "風力",
                "水素"
            ],

            "データセンター": [
                "データセンター",
                
                "クラウド"
            ],

            "サイバー": [
                "サイバー",
                "セキュリティ",
                "SOC",
                "ゼロトラスト"
            ],

            "AI": [
                "AI",
                "人工知能",
                "生成AI",
                "LLM",
                "ChatGPT",
                "OpenAI",
                "Copilot",
                "Gemini"
            ],

            "EV": [
                "EV",
                "電気自動車",
                "蓄電池",
                "リチウム",
                "自動運転",
                "Tesla"
            ],

            "半導体": [
                "半導体",
                "TSMC",
                "NVIDIA",
                "GPU",
                "AMD",
                "ASML",
                "先端プロセス"
            ],

            "バイオ": [
                "バイオ",
                "創薬",
                "治験",
                "再生医療"
            ],

            "ロボット": [
                "ロボット",
                "自動化",
                "FA",
                "産業ロボット"
            ],

            "DX": [
                "DX",
                "クラウド",
                "SaaS",
                "デジタル"
            ]
        }

        self.combo_themes = [

            ("AI", "半導体"),
            ("AI", "データセンター"),
            ("EV", "半導体"),
            ("ロボット", "AI"),
            ("サイバー", "AI")
        ]

    # =========================
    # THEME ANALYSIS
    # =========================
    def analyze(self, texts):

        if isinstance(texts, str):
            texts = [texts]

        theme_hits = {}

        for theme in self.themes:
            theme_hits[theme] = 0

        # -------------------------
        # テーマ検出
        # -------------------------
        for text in texts:

            text = str(text)

            for theme, words in self.themes.items():

                for word in words:

                    if word in text:

                        

                        theme_hits[theme] += 1

        total_score = 0

        matched = []

        # -------------------------
        # 強度計算
        # -------------------------
        for theme, hits in theme_hits.items():

            if hits == 0:
                continue

            score = min(
                hits * 5,
                30
            )

            score *= self.theme_weights.get(
                theme,
                1.0
            )

            score = int(score)

            total_score += score

            matched.append(
                (
                    theme,
                    score
                )
            )

        # -------------------------
        # 複合テーマ
        # -------------------------
        detected = {

            theme
            for theme, _
            in matched

        }

        for t1, t2 in self.combo_themes:

            if t1 in detected and t2 in detected:

                total_score += 8

                matched.append(
                    (
                        f"{t1}+{t2}",
                        8
                    )
                )

        total_score = min(
            total_score,
            100
        )

        matched.sort(
            key=lambda x: x[1],
            reverse=True
        )

        return (
            total_score,
            matched
        )