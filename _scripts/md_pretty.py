#!/usr/bin/env python3
import sys, argparse
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

def main():
    parser = argparse.ArgumentParser(description="Render terminal Markdown output with Claude CLI native styling")
    parser.add_argument("--gateway", default="Auto-Detect", help="Gateway label")
    parser.add_argument("--model", default="Auto-Model", help="Model label")
    parser.add_argument("--elapsed", default="", help="Elapsed execution time")
    args = parser.parse_args()

    console = Console()
    
    # Read content from stdin
    with console.status("[bold cyan]⏳ Đang suy luận & xử lý câu hỏi...[/bold cyan]", spinner="dots"):
        raw_text = sys.stdin.read()

    if not raw_text.strip():
        return

    # Render Header Panel
    header_text = f"[bold cyan]🔀 Gateway:[/] [bold yellow]{args.gateway}[/]  │  [bold cyan]🧠 Model:[/] [bold green]{args.model}[/]  │  [bold green]🟢 Session Active[/]"
    console.print(Panel(header_text, border_style="bright_blue", title="[bold white]🤖 PuluSmartFlow v3.5[/]", expand=False))

    # Render Main Content
    try:
        md = Markdown(raw_text)
        console.print(md)
    except Exception:
        sys.stdout.write(raw_text)

    # Render Footer Panel
    elapsed_str = f"⏱️ {args.elapsed}s" if args.elapsed else "⏱️ Completed"
    footer_text = f"[bold dim]{elapsed_str} │ ➔ Auto-Token Nén │ 📦 Cache Active │ ⚡ Max Speed │ 🟢 Context Preserved[/]"
    console.print(Panel(footer_text, border_style="dim", expand=False))

if __name__ == "__main__":
    main()
