# 腾空世界观数字档案馆架构设计（Architecture v1.0）

## 1. 项目定位（Project Overview）

腾空世界观数字档案馆（Tengkong Digital Archive System）

是一个用于长期保存、组织、检索、展示腾空世界观资料的数字档案系统（Digital Archive System）。

本项目不是：

- 博客（Blog）
- CMS 内容管理系统
- Wiki 百科系统
- 论坛（Forum）

本项目定位为：

- 数字档案馆（Digital Archive）
- 数字出版平台（Digital Publishing Platform）
- 长期知识库（Long-term Knowledge Base）

## 2. 四层架构（Four-layer Architecture）

整个系统由四层组成：

Content（内容层）

↓

Configuration（配置层）

↓

Engine（引擎层）

↓

Presentation（展示层）

设计目的：

- 内容与程序彻底分离。
- 配置与业务逻辑彻底分离。
- 展示页面全部自动生成。
- 长期维护无需修改 HTML。

## 3. 开发原则（Development Principles）

### 原则一

所有内容来自 Blogger。

禁止手工修改 articles。

---

### 原则二

所有规则来自 archive.config.json。

禁止把人工规则写入 Python。

---

### 原则三

sync.py 负责解释配置。

不负责保存配置。

---

### 原则四

HTML 页面全部自动生成。

不允许手工修改 labels 与 articles。

---

### 原则五

新增功能应优先通过配置扩展，而不是修改核心逻辑。

## 4. 核心对象（Core Objects）

整个档案馆由三个核心对象组成。

Collection

↓

Article

↓

Asset

archive.config.json
│
├── site
│      │
│      ├── title
│      ├── language
│      ├── description（未来）
│      ├── theme（未来）
│      └── version（未来）
│
├── collections
│      │
│      ├── 难经
│      │      │
│      │      ├── view
│      │      ├── homepage
│      │      ├── show_in_exhibition
│      │      ├── icon（未来）
│      │      ├── cover（未来）
│      │      ├── description（未来）
│      │      └── template（未来）
│      │
│      ├── 腾空看到的外星人
│      │
│      └── 山海经（未来）
│
├── homepage
│      │
│      ├── featured
│      ├── recommendations（未来）
│      ├── banner（未来）
│      └── layout（未来）
│
├── search（未来）
│
├── reading（未来）
│
└── theme（未来）

## 5. sync.py Current Structure（当前结构）

`scripts/sync.py` is currently a single-file engine script. It contains configuration loading, compatibility constants, helper functions, Blogger feed fetching, archive merging, static HTML generation, image downloading, and direct execution flow in one module.

Current module structure:

- Imports and configuration loading
- Version 2 collection helper functions
- Legacy compatibility constants
- General article and asset helper functions
- Article HTML generation
- Label page generation
- Image download logic
- Blogger feed fetch loop
- Existing archive load and merge
- Article metadata enrichment
- JSON archive save
- Final static generation calls

The script executes immediately when run. There is no `main()` wrapper yet, so importing the module would also run the synchronization process.

## 6. Main Function Responsibilities（主要函数职责）

`get_collection_default_view(name)`

Returns the configured default view for a collection, falling back to `list`.

`get_collection_default_sort(name)`

Returns the configured default sort order for a collection, falling back to `asc`.

`get_collection(name)`

Reads one collection config from `COLLECTIONS`. It returns `{}` when the collection is missing or malformed.

`get_collection_view(name)`

Returns the configured collection view, falling back to `list`.

`show_in_exhibition(name)`

Returns whether a collection should appear in exhibition-style views.

`is_homepage_collection(name)`

Returns whether a collection is marked for homepage use.

`get_first_image(html)`

Extracts the first `<img src="...">` URL from a content HTML string. It returns an empty string if no image exists.

`get_article_image_filename(article, index)`

Builds the local image filename for an article image using `{article_id}-{index}.jpg`.

`get_article_image_path(article, index, prefix="..")`

Builds the local web path for an article image, currently `../assets/images/{article_id}-{index}.jpg` for generated article and label pages.

`make_slug(text)`

Converts Chinese label text into a pinyin slug after removing punctuation and whitespace. This function is currently defined twice with the same implementation.

`build_article_filename(article)`

Builds the generated article filename from article date, last Blogger label slug, and Blogger article id.

`generate_html_files(articles)`

Generates one static HTML page per article under `articles/`. It also:

- Calculates previous and next article links within the same current label.
- Builds article label links and breadcrumbs.
- Rewrites article `<img src>` values to local image paths.
- Rewrites Blogger image anchor `href` values to local image paths.
- Embeds article-level reading history JavaScript.

`generate_label_pages(articles)`

Generates one static label page per Blogger label under `labels/`. It also:

- Groups articles by label.
- Detects whether the label should use gallery controls through `GALLERY_LABELS`.
- Builds list and optional gallery markup.
- Embeds label-page sorting, gallery, reading progress, and reading status JavaScript.

`download_images(articles)`

Downloads article images into `assets/images/`. It:

- Extracts image URLs from original Blogger content.
- Normalizes some Blogger image URLs to larger source variants.
- Saves images using the same article image filename convention used by generated HTML.
- Skips files that already exist locally.

## 7. Data Flow（数据流）

Current runtime data flow:

1. Load configuration from `config/archive.config.json`.
2. Fetch paginated Blogger JSON feed from `https://tengkongworld.blogspot.com/feeds/posts/default`.
3. Convert each feed entry into an article dictionary:

   - `id`
   - `title`
   - `published`
   - `labels`
   - `content`

4. Load existing archive data from `data/articles.json` if present.
5. Merge existing articles and fetched articles by `id`.
6. Sort merged articles by `published` descending.
7. Add generated fields:

   - `filename`
   - `label_slugs`

8. Save merged archive data back to `data/articles.json`.
9. Generate article HTML files under `articles/`.
10. Generate label HTML files under `labels/`.
11. Download missing images into `assets/images/`.

The source of truth for content remains Blogger. The local JSON file is an archive cache and merge target, not the original authoring source.

## 8. Configuration Flow（配置流）

Configuration is loaded once at startup:

`config/archive.config.json` → `CONFIG`

Version 2 collection configuration is read from:

`CONFIG["collections"]` → `COLLECTIONS`

Collection helper functions read from `COLLECTIONS` and provide safe defaults when configuration is missing.

Collection

is the primary organizational object
of the archive.

Articles belong to Collections.

Assets belong to Articles.

Configuration defines Collection behavior.

Legacy constants are still created for compatibility:

- `GALLERY_LABELS`
- `DIGITAL_EXHIBITION`
- `FEATURED_LABELS`
- `HOMEPAGE_RECOMMENDATIONS`

`GALLERY_LABELS` and `DIGITAL_EXHIBITION` can still read old V1 keys if present. When those keys are absent, they are derived from Version 2 collection settings.

Current active configuration effects:

- `collections.*.view = "gallery"` can feed `GALLERY_LABELS`.
- `collections.*.show_in_exhibition = true` can feed `DIGITAL_EXHIBITION`.
- Label page gallery mode still checks `label in GALLERY_LABELS`.

## 9. Legacy V1 Components（旧版组件）

The current script still contains several V1 label-based concepts:

- `GALLERY_LABELS`
- `DIGITAL_EXHIBITION`
- `FEATURED_LABELS`
- `HOMEPAGE_RECOMMENDATIONS`
- Label pages generated from every Blogger label.
- Article filenames based on the last Blogger label.
- Navigation based on shared Blogger labels.
- Gallery behavior based on label membership.

These components should remain until each downstream behavior has a Version 2 collection-based replacement.

## 10. Version 2 Components（Version 2 组件）

Version 2 components currently present in `sync.py`:

- `config/archive.config.json`
- `COLLECTIONS`
- `get_collection_default_view(name)`
- `get_collection_default_sort(name)`
- `get_collection(name)`
- `get_collection_view(name)`
- `show_in_exhibition(name)`
- `is_homepage_collection(name)`

Version 2 is currently an additive compatibility layer. It reads collection configuration and provides helper APIs, while most generated output still depends on legacy label-based logic.

## 11. Future Refactoring Opportunities（未来重构建议）

Suggested future refactoring opportunities:

- Add a `main()` function so importing helper functions does not run the sync process.
- Split the script into clear sections or modules:

  - configuration
  - Blogger client
  - article normalization
  - archive merge
  - asset handling
  - article page renderer
  - label or collection page renderer

- Remove the duplicated `make_slug()` definition.
- Move large inline HTML templates into template files or renderer functions.
- Replace label-based page generation with collection-based page generation gradually.
- Introduce a collection resolution layer that maps Blogger labels to archive collections.
- Keep one shared image mapping function for article HTML generation and image downloading.
- Separate data generation from file writing to make verification easier.
- Add a dry-run or local-cache mode for testing without requiring Blogger network access.
- Add validation for `archive.config.json` so configuration errors can be reported clearly.
- Remove V1 compatibility constants only after all generated behavior has moved to Version 2 collection APIs.

Configuration Layer

↓

Generation Layer

↓

Runtime Layer

↓

Presentation Layer

archive.config.json
          │
          ▼
   scripts/config.py
          │
          ▼
   scripts/sync.py
          │
          ▼
   scripts/feed.py
          │
          ▼
      Articles
          │
          ▼
      Generators
          │
          ▼
   HTML Pages
          │
          ▼
 JavaScript Runtime