import os


def generate_label_pages(
    articles,
    gallery_labels,
    get_collection_default_view,
    get_collection_default_sort,
    make_slug,
    get_article_image_path,
    build_article_filename,
    output_dir="labels",
    asset_prefix="..",
    article_prefix="../articles",
    language="zh-cn",
):

    if language == "zh-tw":
        TEXT = {
            "home": "首頁",
            "mode": "模式",
            "standard": "標準",
            "eye": "護眼",
            "night": "夜間",
            "classic": "古籍",
            "font": "字級",
            "sort": "排序",
            "ascending": "由舊到新",
            "descending": "由新到舊",
            "asc_button": "正序",
            "desc_button": "倒序",
            "list": "列表",
            "gallery": "圖鑑",
            "read": "已閱讀",
        }
        html_lang = "zh-TW"

    else:
        TEXT = {
            "home": "首页",
            "mode": "模式",
            "standard": "标准",
            "eye": "护眼",
            "night": "夜间",
            "classic": "古籍",
            "font": "字号",
            "sort": "排序",
            "ascending": "升序",
            "descending": "降序",
            "asc_button": "正序",
            "desc_button": "倒序",
            "list": "列表",
            "gallery": "图鉴",
            "read": "已阅读",
        }
        html_lang = "zh-CN"

    os.makedirs(output_dir, exist_ok=True)
    gallery_label_slugs = {
        make_slug(gallery_label): gallery_label for gallery_label in gallery_labels
    }
    label_articles = {}
    for article in articles:
        for label in article["labels"]:
            if label not in label_articles:
                label_articles[label] = []
            label_articles[label].append(article)
    for label, articles_list in label_articles.items():
        collection_label = label
        label_slug = make_slug(label)

        if label not in gallery_labels and label_slug in gallery_label_slugs:
            collection_label = gallery_label_slugs[label_slug]

        has_gallery = collection_label in gallery_labels
        default_view = get_collection_default_view(collection_label)
        default_sort = get_collection_default_sort(collection_label)

        filename = f"{make_slug(label)}.html"
        filepath = os.path.join(output_dir, filename)

        if language == "zh-tw":
            language_switcher = f"""
<div class="language-switcher">
    <a href="../../labels/{filename}">简体中文</a>
    ｜
    <span class="current-language">繁體中文</span>
</div>
"""
            alternate_links = f"""
    <link rel="alternate" hreflang="zh-CN" href="../../labels/{filename}">
    <link rel="alternate" hreflang="zh-TW" href="{filename}">
"""

        else:
            language_switcher = f"""
<div class="language-switcher">
    <span class="current-language">简体中文</span>
    ｜
    <a href="../tc/labels/{filename}">繁體中文</a>
</div>
"""
            alternate_links = f"""
    <link rel="alternate" hreflang="zh-CN" href="{filename}">
    <link rel="alternate" hreflang="zh-TW" href="../tc/labels/{filename}">
"""

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"""<!DOCTYPE html>
<html lang="{html_lang}">
<head>
    <meta charset="utf-8">
    <meta name="viewport"
          content="width=device-width, initial-scale=1">
    <title>{label}</title>

{alternate_links}

    <link
    rel="stylesheet"
    href="{asset_prefix}/assets/css/theme.css">

<link
    rel="stylesheet"
    href="{asset_prefix}/assets/css/article.css">

    <style>

    #gallery-view {{

        display: grid;

        grid-template-columns:

            repeat(

                auto-fill,

                minmax(

                    220px,

                    1fr

                )

            );

        gap: 16px;

    }}

    .gallery-card {{

        border: 1px solid #ddd;

        border-radius: 8px;

        overflow: hidden;

    }}

    .gallery-card img {{

        width: 100%;

        display: block;

    }}

    .gallery-card p {{

        padding: 10px;

        font-weight: bold;

    }}

    </style>
</head>
<body
    data-default-view="{default_view}"
    data-default-sort="{default_sort}"
>
{language_switcher}
""")

            parent_label = ""

            for article in articles_list:
                if article["labels"] and article["labels"][0] != label:
                    parent_label = article["labels"][0]

                    break

            if parent_label:
                f.write(
                    f"<p>"
                    f'<a href="../index.html">'
                    f"{TEXT['home']}"
                    f"</a> / "
                    f'<a href="{make_slug(parent_label)}.html">'
                    f"{parent_label}"
                    f"</a> / "
                    f"{label}"
                    f"</p>"
                )

            else:
                f.write(
                    f'<p><a href="../index.html">{TEXT["home"]}</a> / {label}</p>'
                )

            f.write(f"<h1>{label}</h1>")

            f.write("""
<div id="reading-progress">
</div>

<div id="next-reading">
</div>
""")
            if has_gallery:
                f.write(f"""
<p>
<button onclick="sortAsc()">{TEXT["ascending"]}</button>
<button onclick="sortDesc()">{TEXT["descending"]}</button>
</p>

<p>
<button onclick="showListMode()">📄 {TEXT["list"]}</button>
<button onclick="showGalleryMode()">🖼 {TEXT["gallery"]}</button>
</p>
""")

            else:
                f.write(f"""
<p>
<button onclick="sortAsc()">{TEXT["asc_button"]}</button>
<button onclick="sortDesc()">{TEXT["desc_button"]}</button>
</p>
""")

            f.write("""
<ul
    id="article-list"
    class="article-list">
""")

            for index, article in enumerate(articles_list):
                f.write(
                    f'''
        <li
            data-index="{index}"
            data-title="{article["title"]}"
            data-image="{get_article_image_path(article, 1, prefix=asset_prefix)}"
        >
            <span class="read-mark">○</span>

            <a href="{article_prefix}/{build_article_filename(article)}">
                {article["title"]}
            </a>

        </li>
        '''
                )
            f.write("""
    </ul>

""")

            if has_gallery:
                f.write("""

<div
    id="gallery-view"
    style="display:none;"
>
</div>

""")

            f.write(
                """             
                                                            
<script>                                       

function showListMode() {

    document.getElementById(
        "article-list"
    ).style.display = "block";

    document.getElementById(
        "gallery-view"
    ).style.display = "none";

    localStorage.setItem(
        "viewMode",
        "list"
    );

}

function rebuildGallery() {

    const gallery =
        document.getElementById(
            "gallery-view"
        );

    gallery.innerHTML = "";

    const galleryItems =
        document.querySelectorAll(
            "#article-list li"
        );

    galleryItems.forEach(item => {

        const image =
            item.dataset.image;

        const title =
            item.dataset.title;

        const link =
            item.querySelector(
                "a"
            ).href;

        gallery.innerHTML += `

<div class="gallery-card">

    <a href="${link}">

        <img
            src="${image}"
            alt="${title}"
        >

        <p>
            ${title}
        </p>

    </a>

</div>

`;

    });

}
                                        
function showGalleryMode() {

    document.getElementById(
        "article-list"
    ).style.display = "none";

    const gallery =
        document.getElementById(
            "gallery-view"
        );

    gallery.style.display =
        "grid";

    rebuildGallery();

    localStorage.setItem(
        "viewMode",
        "gallery"
    );

}
                    
function sortAsc() {

    const list =
        document.getElementById(
            "article-list"
        );

    const items =
        Array.from(
            list.children
        );

    items.sort(
        (a, b) =>
        Number(b.dataset.index)
        -
        Number(a.dataset.index)
    );

    list.innerHTML = "";

    items.forEach(item => {

        list.appendChild(item);

    });

    localStorage.setItem(
        "sortOrder",
        "asc"
    );

    if (
        document.getElementById(
            "gallery-view"
        ).style.display !== "none"
    ) {

        rebuildGallery();

    }

}                    

function sortDesc() {

    const list =
        document.getElementById(
            "article-list"
        );

    const items =
        Array.from(
            list.children
        );

    items.sort(
        (a, b) =>
        Number(a.dataset.index)
        -
        Number(b.dataset.index)
    );

    list.innerHTML = "";

    items.forEach(item => {

        list.appendChild(item);

    });

    localStorage.setItem(
        "sortOrder",
        "desc"
    );
    if (
    document.getElementById(
        "gallery-view"
    ).style.display !== "none"
    ) {

    rebuildGallery();

    }                

}

function initializeReadingHistory() {

    const history = JSON.parse(

        localStorage.getItem(

            "readingHistory"

        ) || "[]"

    );

    const readTitles = history.map(

        item => item.title

    );

    document

        .querySelectorAll(

            "li[data-title]"

        )

        .forEach(li => {

            const title =

                li.dataset.title;

            if (

                readTitles.includes(title)

            ) {

                li.querySelector(

                    ".read-mark"

                ).textContent = "✓";

            }

        });

    const totalArticles = document

        .querySelectorAll(

            "li[data-title]"

        ).length;

    const readCount = document

        .querySelectorAll(

            ".read-mark"

        );

    let finished = 0;

    readCount.forEach(mark => {

        if (

            mark.textContent === "✓"

        ) {

            finished++;

        }

    });

    const percent = Math.round(

        finished * 100 / totalArticles

    );

    document.getElementById(

    "reading-progress"

).innerHTML = `

    <p>

        __READ_TEXT__

        ${finished}

        /

        ${totalArticles}

        (${percent}%)

    </p>

    <div class="reading-options">

        <div class="reading-options-group">

            <span class="reading-label">

                __MODE_TEXT__

            </span>

            <div class="reading-buttons">

                <button class="theme-button" data-theme="default">

                    __STANDARD_TEXT__

                </button>

                <button class="theme-button" data-theme="eye">

                    __EYE_TEXT__

                </button>

                <button class="theme-button" data-theme="dark">

                    __NIGHT_TEXT__

                </button>

                <button class="theme-button" data-theme="classic">

                    __CLASSIC_TEXT__

                </button>

            </div>

        </div>

        <div class="reading-options-group">

            <span class="reading-label">

                __FONT_TEXT__

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

`;
                    
document

    .querySelectorAll(".theme-button")

    .forEach(button => {

        button.addEventListener(

            "click",

            () => {

                setTheme(

                    button.dataset.theme

                );

            }

        );

    });

const smaller = document.getElementById("font-smaller");

const larger = document.getElementById("font-larger");

if (smaller) {

    smaller.onclick = () => {

        let size = parseInt(

            localStorage.getItem("fontSize")

        ) || DEFAULT_FONT_SIZE;

        if (size > MIN_FONT_SIZE) {

            applyFontSize(size - 1);

        }

    };

}

if (larger) {

    larger.onclick = () => {

        let size = parseInt(

            localStorage.getItem("fontSize")

        ) || DEFAULT_FONT_SIZE;

        if (size < MAX_FONT_SIZE) {

            applyFontSize(size + 1);

        }

    };

}                  

}

function initializeSort() {

    const savedOrder =

        localStorage.getItem(
            "sortOrder"
        );

    if (
        savedOrder === "asc"
    ) {

        sortAsc();

        return;

    }

    if (
        savedOrder === "desc"
    ) {

        sortDesc();

        return;

    }

    const defaultSort =

        document.body.dataset.defaultSort;

    if (
        defaultSort === "desc"
    ) {

        sortDesc();

    } else {

        sortAsc();

    }

}
                    
                    function initializeView() {

    const savedView =

        localStorage.getItem(
            "viewMode"
        );

    if (
        savedView === "gallery"
    ) {

        showGalleryMode();

        return;

    }

    if (
        savedView === "list"
    ) {

        showListMode();

        return;

    }

    const defaultView =

        document.body.dataset.defaultView;

    if (
        defaultView === "gallery"
    ) {

        showGalleryMode();

    } else {

        showListMode();

    }

}

function initializePage() {

    initializeReadingHistory();

    initializeTheme();

    initializeFontSize();

    initializeSort();

    initializeView();

}
                                                                                                  
</script>
                    
<script src="__ASSET_PREFIX__/assets/js/theme.js"></script>

<script src="__ASSET_PREFIX__/assets/js/article.js"></script>

<script>

initializePage();

</script>

</body>
</html>
""".replace("__ASSET_PREFIX__", asset_prefix)
                .replace("__READ_TEXT__", TEXT["read"])
                .replace("__MODE_TEXT__", TEXT["mode"])
                .replace("__STANDARD_TEXT__", TEXT["standard"])
                .replace("__EYE_TEXT__", TEXT["eye"])
                .replace("__NIGHT_TEXT__", TEXT["night"])
                .replace("__CLASSIC_TEXT__", TEXT["classic"])
                .replace("__FONT_TEXT__", TEXT["font"])
            )
