import re
import hashlib

from urllib.parse import quote, urlsplit, urlunsplit

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
from generators.homepage import generate_homepage
from generators.label import generate_label_pages
from converters.opencc_converter import to_traditional

import os
import shutil
from urllib.request import urlretrieve

BUILD_DIR = "build"
OUTPUT_FILE = os.path.join(BUILD_DIR, "data", "articles.json")


def build_path(*parts):
    """Return a path inside the build output directory."""
    return os.path.join(BUILD_DIR, *parts)


def prepare_build_dir():
    """Create a fresh build directory with static site assets."""
    cached_images = None
    cached_images_path = build_path("assets", "images")

    if os.path.exists(cached_images_path):
        cached_images = os.path.join("/tmp", "tengkong-archive-image-cache")

        if os.path.exists(cached_images):
            shutil.rmtree(cached_images)

        shutil.copytree(cached_images_path, cached_images)

    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)

    os.makedirs(BUILD_DIR, exist_ok=True)

    # 创建 data 目录（关键修复）
    os.makedirs(build_path("data"), exist_ok=True)

    homepage_source_files = (
        "homepage.json",
        "homepage_tc.json",
    )

    for filename in homepage_source_files:
        source_path = os.path.join("data", filename)
        destination_path = build_path("data", filename)

        if not os.path.exists(source_path):
            raise FileNotFoundError(f"缺少手动首页配置文件：{source_path}")

        # copy each homepage source into the build data directory
        shutil.copy2(source_path, destination_path)

    if os.path.exists("assets"):
        # copytree with dirs_exist_ok to avoid errors if target exists (Py3.8+)
        shutil.copytree("assets", build_path("assets"), dirs_exist_ok=True)

    if cached_images:
        os.makedirs(build_path("assets"), exist_ok=True)
        shutil.copytree(cached_images, cached_images_path)
        shutil.rmtree(cached_images)


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


def normalize_image_url(img_url):
    """Return a stable full-size URL for cache identity."""
    img_url = re.sub(r"/s\d+/", "/s0/", img_url)

    img_url = re.sub(r"/w\d+-h\d+/", "/s0/", img_url)

    img_url = re.sub(r"=w\d+-h\d+$", "=s0", img_url)

    parts = urlsplit(img_url)

    return urlunsplit((parts.scheme, parts.netloc, parts.path, parts.query, ""))


def get_image_extension(img_url):
    """Return a conservative image extension for a URL."""
    path = urlsplit(img_url).path.lower()

    match = re.search(r"\.(jpg|jpeg|png|gif|webp)$", path)

    if match:
        extension = match.group(1)

        if extension == "jpeg":
            return "jpg"

        return extension

    return "jpg"


def get_image_cache_filename(img_url):
    """Return a stable cache filename for a logical image URL."""
    normalized_url = normalize_image_url(img_url)

    digest = hashlib.sha1(normalized_url.encode("utf-8")).hexdigest()[:16]

    return f"{digest}.{get_image_extension(normalized_url)}"


def prepare_article_image_filenames(articles):
    """Attach stable image filenames used by render and download steps."""
    for article in articles:
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', article["content"])

        article["_image_filenames"] = [
            get_image_cache_filename(img_url) for img_url in imgs
        ]


def get_article_image_filename(article, index):
    """Return the local filename for an article image."""
    image_filenames = article.get("_image_filenames", [])

    if 0 < index <= len(image_filenames):
        return image_filenames[index - 1]

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

    image_dir = build_path("assets", "images")

    os.makedirs(image_dir, exist_ok=True)

    total = 0

    for article in articles:
        imgs = re.findall(r'<img[^>]+src="([^"]+)"', article["content"])

        for index, img_url in enumerate(imgs, start=1):
            original_url = img_url

            img_url = normalize_image_url(img_url)

            if (
                original_url == img_url
                and "/s0/" not in img_url
                and "=s0" not in img_url
                and "/img/a/" not in img_url
            ):
                print("未处理图片格式:", img_url)

            filename = get_article_image_filename(article, index)

            filepath = os.path.join(image_dir, filename)

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


def cleanup_unused_images(articles):
    """Remove generated image files that are no longer referenced."""
    image_dir = build_path("assets", "images")

    if not os.path.exists(image_dir):
        return

    used_filenames = set()

    for article in articles:
        used_filenames.update(article.get("_image_filenames", []))

    removed = 0

    for filename in os.listdir(image_dir):
        filepath = os.path.join(image_dir, filename)

        if not os.path.isfile(filepath):
            continue

        if filename in used_filenames:
            continue

        os.remove(filepath)
        removed += 1

    if removed:
        print("清理旧图片:", removed)


feed_articles = fetch_feed()


# =========================
# 读取现有档案
# =========================

existing_articles = []

existing_output_file = OUTPUT_FILE

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

prepare_article_image_filenames(articles)

prepare_article_image_filenames(articles_tc)

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

articles_json = [
    {key: value for key, value in article.items() if not key.startswith("_")}
    for article in articles
]

articles_tc_json = [
    {key: value for key, value in article.items() if not key.startswith("_")}
    for article in articles_tc
]

for article in articles_tc_json:
    if article.get("image"):
        article["image"] = "../" + article["image"]

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(articles_json, f, ensure_ascii=False, indent=2)

with open(build_path("data", "articles_tc.json"), "w", encoding="utf-8") as f:
    json.dump(
        articles_tc_json,
        f,
        ensure_ascii=False,
        indent=2,
    )

generate_homepage(
    "index.html",
    build_path("index.html"),
    "data/articles.json",
    "data/homepage.json",
)

generate_homepage(
    "index.html",
    build_path("tc", "index.html"),
    "../data/articles_tc.json",
    "../data/homepage_tc.json",
    asset_prefix="..",
    converter=to_traditional,
    language="zh-tw",
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
cleanup_unused_images(articles)
print()
print("静态HTML数量:", len(articles))
