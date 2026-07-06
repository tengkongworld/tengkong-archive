import os


def generate_homepage(
    template_path,
    output_path,
    articles_data_path,
    homepage_data_path,
    asset_prefix=".",
    converter=None,
    language="zh-cn",
):
    """Generate a homepage from the shared homepage template."""
    with open(template_path, "r", encoding="utf-8") as f:
        html = f.read()

    html = html.replace('href="assets/', f'href="{asset_prefix}/assets/')
    html = html.replace('src="assets/', f'src="{asset_prefix}/assets/')
    html = html.replace("fetch('data/articles.json')", f"fetch('{articles_data_path}')")
    html = html.replace("fetch('data/homepage.json')", f"fetch('{homepage_data_path}')")

    if converter:
        html = converter(html)

    if language == "zh-tw":
        html = replace_language_switcher(
            html,
            "簡體中文",
            "繁體中文",
            current_language="zh-tw",
        )
    else:
        html = replace_language_switcher(
            html,
            "简体中文",
            "繁體中文",
            current_language="zh-cn",
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)


def replace_language_switcher(
    html,
    simplified_text,
    traditional_text,
    current_language,
):
    """Render stable, clickable homepage language links."""
    simplified_class = ' class="current-language"' if current_language == "zh-cn" else ""
    traditional_class = ' class="current-language"' if current_language == "zh-tw" else ""

    language_switcher = f"""<div class="language-switcher">
        <a href="/"{simplified_class}>{simplified_text}</a>
        |
        <a href="/tc/"{traditional_class}>{traditional_text}</a>
    </div>"""

    start = html.find('<div class="language-switcher">')

    if start == -1:
        return html

    end = html.find("</div>", start)

    if end == -1:
        return html

    return html[:start] + language_switcher + html[end + len("</div>"):]
