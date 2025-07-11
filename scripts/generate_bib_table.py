import bibtexparser

# Load the bib file
with open('data/polecon-def.bib') as bibfile:
    bib_database = bibtexparser.load(bibfile)

# Build a Markdown table
lines = [
    "| Key | Author(s) | Title | Year |",
    "|-----|------------|-------|------|"
]
for entry in bib_database.entries:
    key    = entry.get('ID', '')
    author = entry.get('author', '').replace('\n', ' ')
    title  = entry.get('title', '').replace('\n', ' ').strip('{}')
    year   = entry.get('year', '')
    lines.append(f"| {key} | {author} | *{title}* | {year} |")

table_md = "\n".join(lines)

# Inject table into README.md
with open('README.md', 'r') as f:
    content = f.read()

parts = content.split("<!-- BIB_TABLE -->")
if len(parts) != 3:
    raise ValueError("README.md must contain exactly two <!-- BIB_TABLE --> markers")

new_readme = parts[0] + "<!-- BIB_TABLE -->\n" + table_md + "\n<!-- BIB_TABLE -->" + parts[2]

with open('README.md', 'w') as f:
    f.write(new_readme)
