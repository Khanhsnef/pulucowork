#!/usr/bin/env python3
import sys
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

def format_output():
    raw_text = sys.stdin.read()
    if not raw_text.strip():
        return
    
    console = Console()
    try:
        md = Markdown(raw_text)
        console.print(md)
    except Exception:
        sys.stdout.write(raw_text)

if __name__ == "__main__":
    format_output()
