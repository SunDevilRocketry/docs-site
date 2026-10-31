#!/usr/bin/env python3
"""Generate navigable index pages for static-hosted directories."""

from __future__ import annotations

import argparse
import html
import os
from pathlib import Path
from urllib.parse import quote
from datetime import date


EXCLUDED_DIRECTORIES = {".git", ".github", "__pycache__", "resources", "scripts"}
EXCLUDED_FILES = {".gitignore", ".gitmodules", "README.md"}


def listing_items(
    directory: Path, listing_root: Path, indexed_directories: set[Path]
) -> str:
    entries: list[str] = []
    for entry in sorted(directory.iterdir(), key=lambda item: (not item.is_dir(), item.name.casefold())):
        if (
            entry.name in EXCLUDED_DIRECTORIES
            or entry.name in EXCLUDED_FILES
            or entry.name == "index.html"
        ):
            continue

        escaped_name = html.escape(entry.name)
        href = quote(entry.relative_to(listing_root).as_posix(), safe="/")
        if entry.is_dir():
            has_index = entry in indexed_directories
            icon = "🌐" if has_index else "📁"
            display_name = escaped_name if has_index else f"{escaped_name}/"
            target = f"{href}/index.html" if has_index else f"{href}/"
            folder_link = (
                f'<span aria-hidden="true">{icon}</span> <a href="{target}">'
                f"{display_name}</a>"
            )
            if has_index:
                entries.append(f'<li class="directory">{folder_link}</li>')
            else:
                children = listing_items(entry, listing_root, indexed_directories)
                nested_items = (
                    f"\n<ul>{children}</ul>" if children else "<p>This directory is empty.</p>"
                )
                entries.append(
                    f'<li class="directory"><details><summary>{folder_link}</summary>'
                    f"{nested_items}</details></li>"
                )
        elif entry.is_file():
            entries.append(
                f'<li><a href="{href}"><span aria-hidden="true">📄</span> {escaped_name}</a></li>'
            )

    return "\n".join(entries)


def directory_listing(
    directory: Path, root: Path, indexed_directories: set[Path]
) -> str:
    relative_directory = directory.relative_to(root)
    depth = len(relative_directory.parts)
    home_href = "../" * depth or "./"
    site_title = "Sun Devil Rocketry Documentation Server"
    title = "Docs" if not relative_directory.parts else relative_directory.as_posix()
    logo_href = f"{home_href}resources/icon.png"
    top_link = (
        f'<a class="top-link" href="{home_href}">Back to top</a>' if relative_directory.parts else ""
    )

    contents = (
        listing_items(directory, directory, indexed_directories)
        or "<li>This directory is empty.</li>"
    )
    return f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{html.escape(title)} | Sun Devil Rocketry</title>
    <style>
      :root {{
        color-scheme: light dark;
        font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
        --background: #f7f7f7;
        --surface: #ffffff;
        --text: #242424;
        --muted: #666666;
        --border: #d9d9d9;
        --link: #8c1d40;
        --hover: #f6edf0;
      }}
      @media (prefers-color-scheme: dark) {{
        :root {{
          --background: #161616;
          --surface: #202020;
          --text: #f4f4f4;
          --muted: #b8b8b8;
          --border: #404040;
          --link: #ffb1c8;
          --hover: #35252a;
        }}
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        color: var(--text);
        background: var(--background);
        line-height: 1.5;
      }}
      a {{ color: var(--link); }}
      .site-header {{
        border-bottom: 1px solid var(--border);
        background: var(--surface);
      }}
      .header-content, main {{ width: min(100% - 2rem, 68rem); margin: 0 auto; }}
      .header-content {{ display: flex; align-items: center; justify-content: space-between; gap: 1rem; min-height: 4.5rem; }}
      .brand {{ display: inline-flex; align-items: center; gap: 0.75rem; color: var(--text); font-weight: 700; text-decoration: none; }}
      .brand-logo {{ width: 2.25rem; height: 2.25rem; object-fit: contain; }}
      .top-link {{ font-size: 0.9rem; }}
      main {{ padding: 3rem 0; }}
      .library {{ padding: clamp(1.25rem, 4vw, 2.5rem); border: 1px solid var(--border); background: var(--surface); }}
      h1 {{ margin: 0; font-size: clamp(1.75rem, 4vw, 2.75rem); line-height: 1.15; }}
      .intro {{ margin: 0.75rem 0 1.75rem; color: var(--muted); }}
      .legend {{ display: flex; flex-wrap: wrap; gap: 0.5rem 1.25rem; margin-bottom: 1.25rem; color: var(--muted); font-size: 0.9rem; }}
      .legend span {{ display: inline-flex; align-items: center; gap: 0.35rem; }}
      .directory-tree, .directory-tree ul {{ margin: 0; padding-left: 1.25rem; list-style: none; }}
      .directory-tree {{ padding: 0; }}
      .directory-tree ul {{ margin: 0.2rem 0; border-left: 1px solid var(--border); }}
      li {{ margin: 0.1rem 0; }}
      li > a, summary, .directory > span {{
        display: inline-flex;
        align-items: center;
        gap: 0.38rem;
        min-height: 2rem;
        padding: 0.15rem 0.35rem;
        border-radius: 0.2rem;
      }}
      li > a:hover, summary:hover, .directory > span:hover {{ background: var(--hover); }}
      .directory {{ font-weight: 650; }}
      details > summary {{ cursor: pointer; list-style: none; }}
      details > summary::-webkit-details-marker {{ display: none; }}
      details > summary::before {{ width: 0.75rem; color: var(--muted); content: "›"; font-size: 1.1rem; }}
      details[open] > summary::before {{ content: "⌄"; }}
      .directory p {{ margin: 0.3rem 0 0.3rem 1.25rem; color: var(--muted); font-size: 0.9rem; font-weight: 400; }}
      .site-information {{ margin-top: 2rem; border-top: 1px solid var(--border); padding-top: 1.5rem; }}
      .information-grid {{ display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1.5rem 2.5rem; }}
      .information-section h2 {{ margin: 0 0 0.5rem; font-size: 1rem; }}
      .information-section p {{ margin: 0; color: var(--muted); }}
      .contact-list {{ margin: 0; }}
      .contact-list div {{ display: grid; grid-template-columns: 9rem 1fr; gap: 0.5rem; padding: 0.3rem 0; border-bottom: 1px; }}
      .contact-list dt {{ color: var(--muted); }}
      .contact-list dd {{ margin: 0; }}
      .license {{ grid-column: 1 / -1; }}
      .license ol {{ margin: 0.75rem 0; padding-left: 1.3rem; color: var(--muted); }}
      .license li {{ margin: 0.45rem 0; }}
      .license-disclaimer {{ font-size: 0.9rem; }}
      @media (max-width: 38rem) {{
        main {{ padding: 1.5rem 0; }}
        .brand {{ font-size: 0.9rem; }}
        .information-grid {{ grid-template-columns: 1fr; }}
        .license {{ grid-column: auto; }}
        .contact-list div {{ grid-template-columns: 1fr; gap: 0.1rem; }}
      }}
    </style>
  </head>
  <body>
    <header class="site-header">
      <div class="header-content">
        <a class="brand" href="{home_href}"><img class="brand-logo" src="{logo_href}" alt=""><span>{site_title}</span></a>
        {top_link}
      </div>
    </header>
    <main>
      <section class="library">
        <h1>{html.escape(title)}</h1>
        <p class="intro">Browse technical resources and project records.</p>
        <div class="legend" aria-label="Directory key">
          <span><span aria-hidden="true">📁</span> Expandable folder</span>
          <span><span aria-hidden="true">🌐</span> Published document site</span>
          <span><span aria-hidden="true">📄</span> File</span>
        </div>
        <ul class="directory-tree">
        {contents}
        </ul>
        <footer class="site-information">
          <div class="information-grid">
            <section class="information-section">
                <h2>Contact</h2>
                <dl class="contact-list">
                <div>
                    <dt>Site contact</dt>
                    <dd><a href="mailto:contact@etsells.dev">Eli Sells</a></dd>
                </div>
                <div>
                    <dt>General inquiries</dt>
                    <dd><a href="mailto:rocketry.asu@gmail.com">Sun Devil Rocketry</a></dd>
                </div>
                </dl>
            </section>
            <section class="information-section license">
              <h2>BSD 3-Clause License</h2>
              <p>Copyright (c) {date.today().year}, Sun Devil Rocketry</p>
              <p>Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:</p>
              <ol>
                <li>Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.</li>
                <li>Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.</li>
                <li>Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.</li>
              </ol>
              <p class="license-disclaimer">THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.</p>
            </section>
          </div>
        </footer>
      </section>
    </main>
  </body>
</html>
"""


def generate_indexes(root: Path) -> None:
    indexed_directories = {
        path.parent
        for path in root.rglob("index.html")
        if not any(excluded in path.parts for excluded in EXCLUDED_DIRECTORIES)
    }

    for current_directory, directories, _ in os.walk(root, topdown=False):
        directories[:] = [name for name in directories if name not in EXCLUDED_DIRECTORIES]
        directory = Path(current_directory)
        if not (directory / "index.html").exists():
            (directory / "index.html").write_text(
                directory_listing(directory, root, indexed_directories), encoding="utf-8"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate index.html files for directories without one."
    )
    parser.add_argument("site_root", type=Path, help="directory to prepare for hosting")
    args = parser.parse_args()

    root = args.site_root.resolve()
    if not root.is_dir():
        parser.error(f"site root does not exist or is not a directory: {root}")

    generate_indexes(root)


if __name__ == "__main__":
    main()
