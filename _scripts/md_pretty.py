#!/usr/bin/env python3
import sys
from rich.console import Console
from rich.markdown import Markdown

def format_output():
    console = Console()
    with console.status("[bold cyan]⏳ Đang suy luận & kết nối Gateway...[/bold cyan]", spinner="dots"):
        raw_text = sys.stdin.read()
        
    if not raw_text.strip():
        return
    
    try:
        md = Markdown(raw_text)
        console.print(md)
    except Exception:
        sys.stdout.write(raw_text)

if __name__ == "__main__":
    format_output()
