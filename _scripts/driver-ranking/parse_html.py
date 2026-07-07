import re

with open("2026-05-driver-ranking-params.html", "r") as f:
    content = f.read()

sections = re.findall(r'(<section id="s\d+">.*?</section>)', content, re.DOTALL)
print(f"Found {len(sections)} sections")
for i, s in enumerate(sections):
    title_match = re.search(r'<h2>(.*?)</h2>', s)
    title = title_match.group(1) if title_match else "No title"
    print(f"S{i+1}: {title}")
