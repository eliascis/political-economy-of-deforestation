#!/usr/bin/env python3
import bibtexparser

# Load the bibliography
with open('data/polecon-def.bib', encoding='utf-8') as bibfile:
    bib_database = bibtexparser.load(bibfile)

# Build the Markdown table with Year as second column
lines = [
    "| Author(s) | Year | Title | Journal |",
    "|-----------|------|-------|---------|"
]
for entry in bib_database.entries:
    author  = entry.get('author', '').replace('\n', ' ')
    year    = entry.get('year', '')
    title   = entry.get('title', '').replace('\n', ' ').strip('{}')
    journal = entry.get('journal', '').replace('\n', ' ')
    lines.append(f"| {author} | {year} | *{title}* | {journal} |")

table_md = "\n".join(lines)

# Inject into README.md between the two <!-- BIB_TABLE --> markers
with open('README.md', encoding='utf-8') as f:
    content = f.read()

parts = content.split("<!-- BIB_TABLE -->")
if len(parts) != 3:
    raise RuntimeError("README.md must contain exactly two <!-- BIB_TABLE --> markers")

new_readme = (
    parts[0]
    + "<!-- BIB_TABLE -->\n"
    + table_md
    + "\n<!-- BIB_TABLE -->"
    + parts[2]
)

with open('README.md', 'w', encoding='utf-8') as f:
    f.write(new_readme)
