#!/usr/bin/env python3
import bibtexparser

# Load the bibliography
with open('data/polecon-def.bib', encoding='utf-8') as bibfile:
    bib_database = bibtexparser.load(bibfile)

# Build the Markdown table with Link column
lines = [
    "| Author(s) | Year | Title | Journal | Link |",
    "|-----------|------|-------|---------|:----:|"
]
for entry in bib_database.entries:
    # Extract last names only
    raw_authors = entry.get('author', '').replace('\n', ' ')
    parts       = [a.strip() for a in raw_authors.split(' and ')]
    last_names  = []
    for name in parts:
        if ',' in name:
            last = name.split(',', 1)[0].strip()
        else:
            tokens = name.split()
            last = tokens[-1] if tokens else ''
        last_names.append(last)
    author = ', '.join(last_names)

    year    = entry.get('year', '')
    title   = entry.get('title', '').replace('\n', ' ').strip('{}')
    journal = entry.get('journal', '').replace('\n', ' ')

    # Determine link: prefer DOI, else URL
    doi = entry.get('doi', '').strip()
    url = entry.get('url', '').strip()
    if doi:
        link_target = f"https://doi.org/{doi}"
    elif url:
        link_target = url
    else:
        link_target = ''

    link_md = f"[🔗]({link_target})" if link_target else ""

    lines.append(f"| {author} | {year} | *{title}* | {journal} | {link_md} |")

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
