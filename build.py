#!/usr/bin/env python3
"""Build log/*.html from log/*.md using a shared template.

Each log entry is a markdown file with YAML-ish frontmatter:

    ---
    day: 1
    title: Day 1: deployment
    date: May 20, 2026
    description: Day 1 of rebuilding Calenduel
    ---

    ## What I worked on
    ...

Run: python build.py
"""

import re
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.exit("Missing dependency. Install with: pip install markdown")

ROOT = Path(__file__).parent
LOG_DIR = ROOT / "log"

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>Day {day} - Log - Zach</title>

    <link rel="stylesheet" href="/style.css">

    <script>
        (function() {{
            const theme = localStorage.getItem('theme-preference');
            const isDark = theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches);
            if (isDark) document.documentElement.classList.add('dark-mode');
        }})();
    </script>
</head>
<body>
    <nav class="site-nav">
        <div class="nav-container">
            <a href="/" class="nav-home">galbs</a>
            <div class="nav-links">
                <a href="/about.html">About</a>
                <a href="/log/">Log</a>
                <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                    <span class="theme-icon"></span>
                </button>
            </div>
        </div>
    </nav>

    <main class="content">
        <article>
            <header class="page-header">
                <h1>{title}</h1>
                <p class="subtitle">{date}</p>
            </header>

{body}
        </article>
    </main>

    <footer class="site-footer"></footer>

    <script src="/dark-mode.js"></script>
</body>
</html>
"""

INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Daily notes from building things">
    <title>Log - Zach</title>

    <link rel="stylesheet" href="/style.css">

    <script>
        (function() {{
            const theme = localStorage.getItem('theme-preference');
            const isDark = theme === 'dark' || (!theme && window.matchMedia('(prefers-color-scheme: dark)').matches);
            if (isDark) document.documentElement.classList.add('dark-mode');
        }})();
    </script>
</head>
<body>
    <nav class="site-nav">
        <div class="nav-container">
            <a href="/" class="nav-home">galbs</a>
            <div class="nav-links">
                <a href="/about.html">About</a>
                <a href="/log/">Log</a>
                <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                    <span class="theme-icon"></span>
                </button>
            </div>
        </div>
    </nav>

    <main class="content">
        <article>
            <header class="page-header">
                <h1>Log</h1>
                <p class="subtitle">Daily notes from building Calenduel.</p>
            </header>

            <section class="section">
                <ul class="log-list">
{entries}
                </ul>
            </section>
        </article>
    </main>

    <footer class="site-footer"></footer>

    <script src="/dark-mode.js"></script>
</body>
</html>
"""


def parse_frontmatter(text, source):
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        sys.exit(f"{source}: missing frontmatter (file must start with --- block)")
    meta = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        meta[key.strip()] = value.strip()
    for required in ("day", "title", "date", "description"):
        if required not in meta:
            sys.exit(f"{source}: frontmatter missing required key '{required}'")
    return meta, match.group(2).strip()


def render_body(md_body):
    """Split body on level-2 headings, wrap each chunk in <section class='section'>."""
    chunks = [c.strip() for c in re.split(r"(?=^## )", md_body, flags=re.MULTILINE) if c.strip()]
    sections = []
    for chunk in chunks:
        html = markdown.markdown(chunk, extensions=['fenced_code'])
        html = html.replace("<ul>", '<ul class="log-list">')
        indented = "\n".join("                " + line for line in html.splitlines())
        sections.append(f'            <section class="section">\n{indented}\n            </section>')
    return "\n\n".join(sections)


def build_entry(md_path):
    meta, body = parse_frontmatter(md_path.read_text(), md_path.name)
    page = PAGE_TEMPLATE.format(
        title=meta["title"],
        date=meta["date"],
        description=meta["description"],
        day=meta["day"],
        body=render_body(body),
    )
    md_path.with_suffix(".html").write_text(page)
    return meta


def build_index(entries):
    lines = [
        f'                    <li><a href="/log/{slug}.html">Day {meta["day"]}: {meta["title"].split(":", 1)[-1].strip() if ":" in meta["title"] else meta["title"]}</a></li>'
        for slug, meta in entries
    ]
    (LOG_DIR / "index.html").write_text(INDEX_TEMPLATE.format(entries="\n".join(lines)))


def main():
    md_files = sorted(LOG_DIR.glob("*.md"), reverse=True)
    if not md_files:
        sys.exit(f"no markdown files found in {LOG_DIR}")
    entries = []
    for md_path in md_files:
        meta = build_entry(md_path)
        entries.append((md_path.stem, meta))
        print(f"built log/{md_path.stem}.html")
    build_index(entries)
    print(f"built log/index.html ({len(entries)} entries)")


if __name__ == "__main__":
    main()
