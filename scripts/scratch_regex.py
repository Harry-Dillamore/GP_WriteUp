import re

with open('Presentation.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace Markdown image links: ](filename.ext)
content = re.sub(
    r'\]\((?!http)([a-zA-Z0-9_\-\.]+\.(png|svg|jpg|jpeg))\)',
    r'](https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/\1)',
    content
)

# Replace HTML image links: src="filename.ext"
content = re.sub(
    r'src="(?!http)([a-zA-Z0-9_\-\.]+\.(png|svg|jpg|jpeg))"',
    r'src="https://pub-9c6c59cb1e3f474f938dca895e9f576d.r2.dev/GreedyPiggies/\1"',
    content
)

with open('Presentation.md', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done")
