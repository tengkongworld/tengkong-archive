Repository Architecture
1. 项目目标（Project Goal）

先写清楚为什么要拆分仓库。

例如：

将源码（Source）与发布网站（Deployment）彻底分离，使开发、自动构建与网站发布各自独立，避免 Git 冲突，提高长期维护性。

这一段以后任何人看到都知道为什么采用这种架构。

2. 仓库职责
tengkong-archive（Source Repository）

负责：

Python
Generator
Workflow
配置
文档
自动化
未来功能开发

永远不直接对外提供网站。

tengkongworld.github.io（Deployment Repository）

负责：

HTML
JSON
图片
CSS
JS
robots.txt
sitemap.xml

永远不开发，只发布。

3. CI/CD 流程

我建议画成流程图。

Blogger
    │
    ▼
tengkong-archive
    │
GitHub Actions
    │
python sync.py
    │
Build Website
    │
Push
    │
▼
tengkongworld.github.io
    │
▼
GitHub Pages

以后所有开发都围绕这个流程。

4. build 目录

这一部分我觉得非常重要。

建议以后所有 Generator：

全部输出：

build/

例如：

build/

index.html

tc/

articles/

labels/

assets/

data/

以后：

Generator 绝不能直接生成到仓库根目录。

5. GitHub Actions

建议明确规定：

以后：

GitHub Actions：

运行位置：

tengkong-archive

负责：

同步 Blogger

↓

生成 build

↓

推送到：

tengkongworld.github.io

而不是：

修改自己。

6. 发布流程

例如：

开发

↓

git push archive

↓

GitHub Actions

↓

Build

↓

Publish

↓

GitHub Pages

以后整个项目都遵循这一套流程。

7. 目录规范

例如：

scripts/
generators/
config/
docs/
workflow/
source/

build/

以后任何 Generator：

都不能直接写：

articles/

应该写：

build/articles/
8. Git 规范

这一节我觉得以后会特别有用。

例如：

Source Repository

允许：

Version 4

Version 4.1

Feature

Bug Fix

禁止：

Auto update archive
Deployment Repository

允许：

Auto publish

Auto sync Blogger

Build Website

禁止：

人工修改 HTML

以后整个团队（哪怕只有你一个人）都会很清楚。

9. 回滚策略

例如：

如果发布失败：

tengkongworld.github.io

↓

恢复到：

Tag

源码：

完全不受影响。

这是 Source Repository 最大的价值。

10. Version 4 迁移计划

最后我建议增加一个 Checklist。

例如：

□ 建立 build/

□ Generator 输出 build/

□ 修改 sync.py

□ 修改 Workflow

□ Push Deployment Repository

□ GitHub Pages 改为 Deployment Repository

□ 删除旧自动 Commit

□ 测试自动发布

□ 完成迁移

以后我们就按这个 Checklist 一项一项完成。

架构原则（Architecture Principles）

例如：

源码与生成结果必须分离。
所有开发只发生在 tengkong-archive。
发布仓库不允许手工修改。
所有网站内容必须由 Generator 自动生成。
GitHub Actions 负责构建与发布，不负责功能开发。

Build 目录属于临时构建结果，不参与人工编辑。