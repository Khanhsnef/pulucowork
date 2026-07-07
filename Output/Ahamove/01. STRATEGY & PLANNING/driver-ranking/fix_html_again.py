import re

with open("2026-05-driver-ranking-params.md", "r", encoding="utf-8") as f:
    md_content = f.read()

# Instead of relying on string replacement of old values (which fail if the old value was already changed or doesn't match exactly),
# let's just re-convert the MD to HTML using our rebuild_html script, and THEN apply the dark theme wrapper.

import subprocess
subprocess.run(["python3", "rebuild_html.py"])
subprocess.run(["python3", "rewrite_dark_theme.py"])

