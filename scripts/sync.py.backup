import json
import os
from urllib.request import urlopen

FEED_URL = "https://tengkongworld.blogspot.com/feeds/posts/default?alt=json&max-results=999"
OUTPUT_FILE = "data/articles.json"

print("正在读取 Blogger Feed...")

with urlopen(FEED_URL) as response:
    data = json.load(response)

entries = data["feed"].get("entry", [])

articles = []

for entry in entries:
    article_id = entry["id"]["$t"].split("-")[-1]

    title = entry.get("title", {}).get("$t", "")

    published = entry.get("published", {}).get("$t", "")[:10]

    labels = []
    for category in entry.get("category", []):
        labels.append(category.get("term", ""))

    content = entry.get("content", {}).get("$t", "")

    articles.append({
        "id": article_id,
        "title": title,
        "published": published,
        "labels": labels,
        "content": content
    })

os.makedirs("data", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

print("Feed统计总数:", data["feed"]["openSearch$totalResults"]["$t"])
print("实际读取数量:", len(articles))
print("已生成:", OUTPUT_FILE)