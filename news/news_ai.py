import requests
import xml.etree.ElementTree as ET


class NewsAI:

    def analyze(self, code, name):

        try:
            url = "https://news.google.com/rss?hl=ja&gl=JP&ceid=JP:ja"

            res = requests.get(url, timeout=5)
            root = ET.fromstring(res.content)

            score = 0

            for item in root.findall(".//item")[:10]:
                title = item.find("title").text

                if name in title:
                    score += 20

                if "増益" in title or "成長" in title:
                    score += 30

                if "赤字" in title:
                    score -= 40

            return {"score": score}

        except:
            return {"score": 0}
