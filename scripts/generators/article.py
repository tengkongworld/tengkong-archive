import os
import re


def generate_html_files(
    articles,
    make_slug,
    build_article_filename,
    get_article_image_path,
    output_dir="articles",
    asset_prefix="..",
    label_prefix="../labels",
    language="zh-cn",
):

    if language == "zh-tw":
        TEXT = {
            "home": "首頁",
            "published": "發布日期",
            "mode": "模式",
            "standard": "標準",
            "eye": "護眼",
            "night": "夜間",
            "classic": "古籍",
            "font": "字級",
            "read": "已閱讀",
            "previous_next": "上一篇 / 下一篇",
            "archive_id": "檔案編號",
            "source": "來源",
            "archive_name": "騰空世界觀檔案館",
        }

    else:
        TEXT = {
            "home": "首页",
            "published": "发布日期",
            "mode": "模式",
            "standard": "标准",
            "eye": "护眼",
            "night": "夜间",
            "classic": "古籍",
            "font": "字号",
            "read": "已阅读",
            "previous_next": "上一篇 / 下一篇",
            "archive_id": "档案编号",
            "source": "来源",
            "archive_name": "腾空世界观档案馆",
        }

    os.makedirs(output_dir, exist_ok=True)

    for article in articles:
        current_label = ""

        if article["labels"]:
            current_label = article["labels"][-1]

        same_label_articles = []

        for a in articles:
            if current_label in a["labels"]:
                same_label_articles.append(a)

        same_label_articles.sort(key=lambda x: x["published"])

        current_index = same_label_articles.index(article)

        previous_article = None
        next_article = None

        if current_index > 0:
            previous_article = same_label_articles[current_index - 1]

        if current_index < (len(same_label_articles) - 1):
            next_article = same_label_articles[current_index + 1]

        filename = build_article_filename(article)

        filepath = os.path.join(output_dir, filename)

        label_links = []

        for label in article["labels"]:
            label_slug = make_slug(label)

            label_links.append(
                f'<a href="{asset_prefix}/labels/{label_slug}.html">{label}</a>'
            )

        labels_html = " / ".join(label_links)

        breadcrumb_links = [f'<a href="../index.html">{TEXT["home"]}</a>']

        for label in article["labels"]:
            label_slug = make_slug(label)

            breadcrumb_links.append(
                f'<a href="{label_prefix}/{label_slug}.html">{label}</a>'
            )

        back_to_label = f"""
<p>
{" / ".join(breadcrumb_links)}
</p>
"""

        content = article["content"]

        # 删除 Blogger / Word 导出的字号样式，
        # 统一由 article.css 和 article.js 控制字体大小。

        content = re.sub(
            r"font-size\s*:\s*[^;\"']+;?",
            "",
            content,
            flags=re.IGNORECASE,
        )

        imgs = re.findall(r'<img[^>]+src="([^"]+)"', content)

        local_images = {}

        for index, img_url in enumerate(imgs, start=1):
            local_image = get_article_image_path(article, index, prefix=asset_prefix)

            local_images[img_url] = local_image

            content = content.replace(img_url, local_image)

        blogger_image_links = re.findall(
            r'<a\b[^>]*href="(https://blogger\.googleusercontent\.com/[^"]+)"',
            content,
        )

        for index, href in enumerate(blogger_image_links, start=1):
            local_image = local_images.get(href)

            if local_image is None and index <= len(imgs):
                local_image = get_article_image_path(
                    article, index, prefix=asset_prefix
                )

            if local_image:
                content = content.replace(f'href="{href}"', f'href="{local_image}"')

        navigation_html = ""

        if previous_article:
            navigation_html += (
                f"<p>← "
                f'<a href="{build_article_filename(previous_article)}">'
                f"{previous_article['title']}"
                f"</a></p>"
            )

        if next_article:
            navigation_html += (
                f"<p>"
                f'<a href="{build_article_filename(next_article)}">'
                f"{next_article['title']}"
                f"</a> →</p>"
            )

        if language == "zh-tw":
            html_lang = "zh-TW"
            language_switcher = f"""
<div class="language-switcher">
    <a href="../../articles/{filename}">简体中文</a>
    ｜
    <span class="current-language">繁體中文</span>
</div>
"""
            alternate_links = f"""
<link rel="alternate" hreflang="zh-CN" href="../../articles/{filename}">
<link rel="alternate" hreflang="zh-TW" href="{filename}">
"""
        else:
            html_lang = "zh-CN"
            language_switcher = f"""
<div class="language-switcher">
    <span class="current-language">简体中文</span>
    ｜
    <a href="../tc/articles/{filename}">繁體中文</a>
</div>
"""
            alternate_links = f"""
<link rel="alternate" hreflang="zh-CN" href="{filename}">
<link rel="alternate" hreflang="zh-TW" href="../tc/articles/{filename}">
"""

        html = f"""<!DOCTYPE html>
        <html lang="{html_lang}">

<head>

<meta charset="utf-8">

<meta name="viewport"
content="width=device-width, initial-scale=1">

<title>{article["title"]}</title>

{alternate_links}

<link rel="stylesheet"
href="{asset_prefix}/assets/css/theme.css">

<link
    rel="stylesheet"
    href="{asset_prefix}/assets/css/article.css">

</head>

<body>

{language_switcher}

{back_to_label}

<h1>
{article["title"]}
</h1>

<p>
{TEXT["published"]}：
{article["published"]}
</p>

<div class="reading-options">

    <div class="reading-options-group">

        <span class="reading-label">
            {TEXT["mode"]}
        </span>

        <div class="reading-buttons">

            <button class="theme-button" data-theme="default">
                {TEXT["standard"]}
            </button>

            <button class="theme-button" data-theme="eye">
                {TEXT["eye"]}
            </button>

            <button class="theme-button" data-theme="dark">
                {TEXT["night"]}
            </button>

            <button class="theme-button" data-theme="classic">
                {TEXT["classic"]}
            </button>

        </div>

    </div>

    <div class="reading-options-group">

        <span class="reading-label">
            {TEXT["font"]}
        </span>

        <div class="font-buttons">

            <button id="font-smaller">
                A－
            </button>

            <span id="font-size">
                18
            </span>

            <button id="font-larger">
                A＋
            </button>

        </div>

    </div>

</div>

<hr>

<div class="article-content">

{content}

</div>

<hr>

<h3>{TEXT["previous_next"]}</h3>

{navigation_html}

<hr>

<p>
{TEXT["archive_id"]}：
{article["id"]}
</p>

<p>
{TEXT["source"]}：
{TEXT["archive_name"]}
</p>

<script>

window.currentArticle = {{
            title: "{article["title"]}",

    url: window.location.pathname,

    time: Date.now()

}};

</script>

<script src="{asset_prefix}/assets/js/theme.js"></script>

<script src="{asset_prefix}/assets/js/article.js"></script>

</body>

</html>
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(html)
