Configuration Design（配置设计）

1. Configuration Philosophy（配置理念）

archive.config.json 是腾空世界观数字档案馆的配置中心（Configuration Center）。

它用于保存整个档案馆的长期配置，以及由管理员决定的运行规则。

程序（sync.py）负责读取配置，根据配置自动生成最终网站。

配置不保存任何可以自动计算的数据。

⸻

2. Configuration Principle（配置原则）

配置用于表达管理员的意图（Intent）。

程序负责根据配置生成最终结果（Result）。

因此：

* 配置保存 What（希望网站是什么样）
* 程序负责 How（如何实现）

例如：

配置：

"view": "gallery"

表示：

希望该系列使用图鉴模式。

至于图鉴如何排列、响应式布局、图片大小等，由程序负责实现，而不是配置负责。

⸻

3. Configuration Boundary（配置边界）

应该写入 archive.config.json

属于管理员长期决定的内容，例如：

* 网站标题
* 网站语言
* 首页推荐
* 数字展厅
* Collection 展示方式
* 图标
* 封面
* 默认视图
* 首页布局

不应该写入 archive.config.json

属于程序自动计算的数据，例如：

* 文章数量
* 阅读数量
* 图片数量
* 更新时间
* 搜索索引
* 标签统计
* 阅读进度

这些内容由 sync.py 自动生成。

⸻

4. Core Objects（核心对象）

整个档案馆由三个核心对象组成：

Archive
    │
    └── Collection
              │
              └── Article

Archive

整个腾空世界观数字档案馆。

系统中只有一个 Archive。

⸻

Collection

Collection 是档案馆中的一个内容系列。

例如：

* 《难经》
* 《道德经》佛界版
* 《心经》佛界之解
* 腾空看到的外星人

Collection 保存整个系列的展示规则，例如：

* view
* homepage
* show_in_exhibition
* icon（未来）
* cover（未来）
* template（未来）

⸻

Article

Article 是 Collection 中的单篇内容。

例如：

* 第一百二十四难
* 外星人25
* 《道德经》第一章

Article 保存：

* 标题
* 正文
* 发布日期
* 图片
* Blogger 标签

⸻

5. Configuration Schema（配置结构）

当前配置结构如下：

archive.config.json
├── site
│
├── collections
│
├── homepage
│
├── search（预留）
│
├── reading（预留）
│
└── theme（预留）

每个节点负责一个独立模块。

后续新增功能时，应优先扩展配置，而不是修改程序结构。

⸻

6. Extension Rules（扩展规则）

新增功能时，请先回答两个问题：

Rule 1

这是管理员决定的吗？

如果是：

→ 写入 archive.config.json

如果不是：

→ 由 sync.py 自动计算。

⸻

Rule 2

这是 Collection 的属性吗？

如果是：

→ 写入 collections

如果不是：

→ 判断是否属于 Article。

⸻

7. Design Goal（设计目标）

整个配置系统遵循以下目标：

* 内容（Content）与配置（Configuration）完全分离。
* 配置（Configuration）与程序（Engine）完全分离。
* 页面全部自动生成。
* 新增功能优先扩展配置，而不是修改核心程序。
* 配置保持长期稳定，程序可以持续迭代。

最终目标：

通过修改 archive.config.json，即可控制整个档案馆的展示方式，而无需修改 HTML 页面或核心程序。

## Collection Fields

| Field | Description |
|--------|-------------|
| title | Display name |
| default_view | Initial page view |
| default_sort | Initial article order |
| show_in_homepage | Homepage recommendation |
| show_in_exhibition | Digital exhibition |
Configuration defines the default behavior of the archive. User preferences override configuration at runtime and are stored locally.