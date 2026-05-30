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
COURSES_DIR = ROOT / "courses"

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
                <a href="/courses/">Courses</a>
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

COURSE_PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Notes from Module {module} of {course}.">
    <title>Module {module}: {title} — {course}</title>

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
                <a href="/courses/">Courses</a>
                <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                    <span class="theme-icon"></span>
                </button>
            </div>
        </div>
    </nav>

    <main class="content">
        <article>
            <header class="page-header">
                <h1>Module {module}: {title}</h1>
                <p class="subtitle">{course} — {provider}</p>
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
                <a href="/courses/">Courses</a>
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


COURSES_INDEX_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Notes from courses">
    <title>Courses - Zach</title>

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
                <a href="/courses/">Courses</a>
                <button class="theme-toggle" id="theme-toggle" aria-label="Toggle theme">
                    <span class="theme-icon"></span>
                </button>
            </div>
        </div>
    </nav>

    <main class="content">
        <article>
            <header class="page-header">
                <h1>Courses</h1>
                <p class="subtitle">Notes from courses I'm working through.</p>
            </header>

{sections}
        </article>
    </main>

    <footer class="site-footer"></footer>

    <script src="/dark-mode.js"></script>
</body>
</html>
"""


def parse_frontmatter(text, source, required=("day", "title", "date", "description")):
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        sys.exit(f"{source}: missing frontmatter (file must start with --- block)")
    meta = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        value = value.strip()
        # Strip surrounding quotes so YAML-quoted values don't leak into output
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
            value = value[1:-1]
        meta[key.strip()] = value
    for field in required:
        if field not in meta:
            sys.exit(f"{source}: frontmatter missing required key '{field}'")
    return meta, match.group(2).strip()


def render_body(md_body):
    """Split body on level-2 headings, wrap each chunk in <section class='section'>."""
    chunks = [c.strip() for c in re.split(r"(?=^## )", md_body, flags=re.MULTILINE) if c.strip()]
    sections = []
    for chunk in chunks:
        html = markdown.markdown(chunk, extensions=['fenced_code', 'smarty'])
        html = html.replace("<ul>", '<ul class="log-list">')
        sections.append(f'            <section class="section">\n{html}\n            </section>')
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


def build_course_entry(md_path):
    meta, body = parse_frontmatter(
        md_path.read_text(),
        md_path.name,
        required=("title", "course", "module", "provider"),
    )
    # Strip a leading h1 if present — the page template provides the h1.
    body = re.sub(r"^#\s+[^\n]+\n+", "", body, count=1)
    page = COURSE_PAGE_TEMPLATE.format(
        title=meta["title"],
        course=meta["course"],
        module=meta["module"],
        provider=meta["provider"],
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


def build_courses_index():
    """Build /courses/index.html listing all courses and their modules."""
    if not COURSES_DIR.exists():
        return
    sections = []
    for course_dir in sorted(COURSES_DIR.iterdir()):
        if not course_dir.is_dir():
            continue
        modules = []
        course_info = None
        for md_path in sorted(course_dir.glob("*.md")):
            meta, _ = parse_frontmatter(
                md_path.read_text(),
                md_path.name,
                required=("title", "course", "module", "provider"),
            )
            modules.append((int(meta["module"]), meta["title"], md_path.stem))
            course_info = (meta["course"], meta["provider"])
        if not course_info or not modules:
            continue
        modules.sort()
        course_name, provider = course_info
        items = "\n".join(
            f'                    <li><a href="/courses/{course_dir.name}/{slug}.html">Module {num}: {title}</a></li>'
            for num, title, slug in modules
        )
        sections.append(
            f'            <section class="section">\n'
            f'                <h2>{course_name}</h2>\n'
            f'                <p class="experiment-meta">{provider}</p>\n'
            f'                <ul class="log-list">\n'
            f'{items}\n'
            f'                </ul>\n'
            f'            </section>'
        )
    if not sections:
        return
    (COURSES_DIR / "index.html").write_text(
        COURSES_INDEX_TEMPLATE.format(sections="\n\n".join(sections))
    )
    print(f"built courses/index.html ({len(sections)} course(s))")


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

    if COURSES_DIR.exists():
        for md_path in sorted(COURSES_DIR.rglob("*.md")):
            build_course_entry(md_path)
            print(f"built {md_path.relative_to(ROOT).with_suffix('.html')}")
        build_courses_index()


if __name__ == "__main__":
    main()
