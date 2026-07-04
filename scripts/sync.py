import re

from urllib.parse import quote

from pypinyin import lazy_pinyin

import json

from config import (
    DIGITAL_EXHIBITION,
    GALLERY_LABELS,
    get_collection_default_sort,
    get_collection_default_view,
)
from feed import fetch_feed
from generators.article import generate_html_files
from generators.label import generate_label_pages
from converters.opencc_converter import to_traditional

import os
import shutil
from urllib.request import urlretrieve

BUILD_DIR = "build"
OUTPUT_FILE = os.path.join(BUILD_DIR, "data", "articles.json")
SOURCE_OUTPUT_FILE = "data/articles.json"


def build_path(*parts):
    """Return a path inside the build output directory."""
    return os.path.join(BUILD_DIR, *parts)


def prepare_build_dir():
    """Create a fresh build directory with static site assets."""
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    os.makedirs(BUILD_DIR, exist_ok=True)

    shutil.copy2("index.html", build_path("index.html"))

    if os.path.exists("tc/index.html"):
        os.makedirs(build_path("tc"), exist_ok=True)
        shutil.copy2("tc/index.html", build_path("tc", "index.html"))

    if os.path.exists("assets"):
        shutil.copytree("assets", build_path("assets"))

    if os.path.exists("data"):
        shutil.copytree("data", build_path("data"))


prepare_build_dir()

print("开始同步 Blogger 档案...")

print("图鉴专题:", GALLERY_LABELS)

print("数字展厅:", DIGITAL_EXHIBITION)


def get_first_image(html):

    match = re.search(r'<img[^>]+src="([^"]+)"', html)

    if match:
        return match.group(1)

    return ""


import copy


def convert_articles(
    articles,
    converter,
):
    """
    复制文章数据，并转换指定字段。
    """

    articles_new = copy.deepcopy(articles)

    for article in articles_new:
        article["title"] = converter(article["title"])

        article["content"] = converter(article["content"])

        article["labels"] = [converter(label) for label in article["labels"]]

    return articles_new


def get_article_image_filename(article, index):
    """Return the local filename for an article image."""
    return f"{article['id']}-{index}.jpg"


def get_article_image_path(article, index, prefix=".."):
    """Return the local web path for an article image."""
    return f"{prefix}/assets/images/{get_article_image_filename(article, index)}"


def get_article_data_image_path(article, index):
    """Return the site-root-relative image path stored in JSON data."""
    return f"assets/images/{get_article_image_filename(article, index)}"


def make_slug(text):

    text = re.sub(r"[《》【】（）()：:、，。！？\s\-]", "", text)

    return "".join(lazy_pinyin(text))


def build_article_filename(article):

    if article["labels"]:
        label = article["labels"][-1]

    else:
        label = "archive"

    slug = make_slug(label)

    return f"{article['published']}-{slug}-{article['id']}.html"


def download_images(articles):

    os.makedirs(build_path("assets", "images"), exist_ok=True)

    total = 0

    for article in articles:
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', article["content"])

        for index, img_url in enumerate(imgs, start=1):
            original_url = img_url

            img_url = re.sub(r"/s\d+/", "/s0/", img_url)

            img_url = re.sub(r"/w\d+-h\d+/", "/s0/", img_url)

            img_url = re.sub(r"=w\d+-h\d+$", "=s0", img_url)

            if (
                original_url == img_url
                and "/s0/" not in img_url
                and "=s0" not in img_url
                and "/img/a/" not in img_url
            ):
                print("未处理图片格式:", img_url)

            filename = get_article_image_filename(article, index)

            filepath = build_path("assets", "images", filename)

            if os.path.exists(filepath):
                continue

            try:
                if "307230326693859030" in filename:
                    print()
                    print("===== 实际下载URL =====")
                    print(img_url)
                    print()

                urlretrieve(img_url, filepath)

                total += 1

                if "25-1.jpg" in img_url:
                    print()
                    print("===== 外星人图片 =====")
                    print(img_url)
                    print()

                print("下载:", filename)

            except Exception as e:
                print("失败:", img_url)

                print(e)

    print()
    print("新增图片:", total)


feed_articles = fetch_feed()


# =========================
# 读取现有档案
# =========================

existing_articles = []

existing_output_file = OUTPUT_FILE

if not os.path.exists(existing_output_file):
    existing_output_file = SOURCE_OUTPUT_FILE

if os.path.exists(existing_output_file):
    try:
        with open(existing_output_file, "r", encoding="utf-8") as f:
            existing_articles = json.load(f)

    except:
        existing_articles = []


# =========================
# 合并
# =========================

articles_by_id = {}

for article in existing_articles:
    articles_by_id[article["id"]] = article

for article in feed_articles:
    articles_by_id[article["id"]] = article


articles = list(articles_by_id.values())

articles_tc = convert_articles(articles, to_traditional)


# =========================
# 排序
# =========================

articles.sort(key=lambda x: x["published"], reverse=True)

articles_tc.sort(key=lambda x: x["published"], reverse=True)

for article in articles_tc:
    imgs = re.findall(r'<img[^>]+src="([^"]+)"', article["content"])

    if imgs:
        article["image"] = get_article_data_image_path(article, 1)
    else:
        article["image"] = ""

for article in articles:
    article["filename"] = build_article_filename(article)

    imgs = re.findall(r'<img[^>]+src="([^"]+)"', article["content"])

    if imgs:
        article["image"] = get_article_data_image_path(article, 1)
    else:
        article["image"] = ""

    # generate label slugs for each article
    article["label_slugs"] = []

    for label in article.get("labels", []):
        article["label_slugs"].append(make_slug(label))

for article in articles_tc:
    article["filename"] = build_article_filename(article)

    article["label_slugs"] = []

    for label in article.get("labels", []):
        article["label_slugs"].append(make_slug(label))

# =========================
# 保存
# =========================

os.makedirs(build_path("data"), exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=2)

with open(build_path("data", "articles_tc.json"), "w", encoding="utf-8") as f:
    json.dump(
        articles_tc,
        f,
        ensure_ascii=False,
        indent=2,
    )


print()
print("同步完成")
print("Feed读取数量:", len(feed_articles))
print("档案馆总数量:", len(articles))
print("输出文件:", OUTPUT_FILE)
print()

print(build_article_filename(articles[0]))
print()
print(make_slug("《心经》佛界之解1"))

print(make_slug("难经心神难篇"))
print()
print("===== 难经人间难篇排序 =====")

test_articles = []

for a in articles:
    if "难经人间难篇" in a["labels"]:
        test_articles.append(a)

test_articles.sort(key=lambda x: x["published"])

for a in test_articles:
    print(a["published"], a["title"])

# 简体
generate_html_files(
    articles,
    make_slug,
    build_article_filename,
    get_article_image_path,
    output_dir=build_path("articles"),
    asset_prefix="..",
)

# 繁体
generate_html_files(
    articles_tc,
    make_slug,
    build_article_filename,
    get_article_image_path,
    output_dir=build_path("tc", "articles"),
    asset_prefix="../..",
    language="zh-tw",
)
generate_label_pages(
    articles,
    GALLERY_LABELS,
    get_collection_default_view,
    get_collection_default_sort,
    make_slug,
    get_article_image_path,
    build_article_filename,
    output_dir=build_path("labels"),
    asset_prefix="..",
)

generate_label_pages(
    articles_tc,
    GALLERY_LABELS,
    get_collection_default_view,
    get_collection_default_sort,
    make_slug,
    get_article_image_path,
    build_article_filename,
    output_dir=build_path("tc", "labels"),
    asset_prefix="../..",
    article_prefix="../articles",
    language="zh-tw",
)

download_images(articles)
print()
print("静态HTML数量:", len(articles))
