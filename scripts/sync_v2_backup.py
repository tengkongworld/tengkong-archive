import json
import os
from urllib.request import urlopen

FEED_URL = "https://tengkongworld.blogspot.com/feeds/posts/default?alt=json&max-results=999"

OUTPUT_FILE = "data/articles.json"

print("正在读取 Blogger Feed...")

# =========================
# 读取 Blogger Feed
# =========================

with urlopen(FEED_URL) as response:
    data = json.load(response)

entries = data["feed"].get("entry", [])

feed_articles = []

for entry in entries:

    article_id = entry["id"]["$t"].split("-")[-1]

    title = entry.get("title", {}).get("$t", "")

    published = entry.get("published", {}).get("$t", "")[:10]

    labels = []

    for category in entry.get("category", []):
        labels.append(category.get("term", ""))

    content = entry.get("content", {}).get("$t", "")

    feed_articles.append({
        "id": article_id,
        "title": title,
        "published": published,
        "labels": labels,
        "content": content
    })

# =========================
# 读取现有档案
# =========================

existing_articles = []

if os.path.exists(OUTPUT_FILE):

    with open(OUTPUT_FILE, "r", encoding="utf-8") as f:

        try:
            existing_articles = json.load(f)
        except:
            existing_articles = []

# =========================
# 合并档案
# =========================

articles_by_id = {}

# 先导入旧档案

for article in existing_articles:
    articles_by_id[article["id"]] = article

# 再导入 Feed（同ID自动覆盖）

for article in feed_articles:
    articles_by_id[article["id"]] = article

# =========================
# 转换回列表
# =========================

articles = list(articles_by_id.values())

# =========================
# 按发布日期排序（最新在前）
# =========================

articles.sort(
    key=lambda x: x["published"],
    reverse=True
)

# =========================
# 保存
# =========================

os.makedirs("data", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(
        articles,
        f,
        ensure_ascii=False,
        indent=2
    )

print("Feed统计总数:", data["feed"]["openSearch$totalResults"]["$t"])

print("本次读取数量:", len(feed_articles))

print("档案馆总数量:", len(articles))

print("已生成:", OUTPUT_FILE)
print("永久档案模式同步完成")