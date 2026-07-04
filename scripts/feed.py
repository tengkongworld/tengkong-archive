import json

from urllib.request import urlopen

PAGE_SIZE = 150


def fetch_feed():
    feed_articles = []

    start_index = 1

    while True:
        feed_url = (
            "https://tengkongworld.blogspot.com/"
            f"feeds/posts/default?alt=json"
            f"&max-results={PAGE_SIZE}"
            f"&start-index={start_index}"
        )

        print(f"读取第 {start_index} 篇开始的数据...")

        with urlopen(feed_url) as response:
            data = json.load(response)

        entries = data["feed"].get("entry", [])

        if not entries:
            break

        print(f"本页读取 {len(entries)} 篇")

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
                "content": content,
            })

        start_index += PAGE_SIZE

    return feed_articles
