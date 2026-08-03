#!/usr/bin/env python3
import sys, argparse
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.box import ROUNDED

def main():
    parser = argparse.ArgumentParser(description="Render terminal Markdown output with Claude CLI native styling")
    parser.add_argument("--gateway", default="Auto-Detect", help="Gateway label")
    parser.add_argument("--model", default="Auto-Model", help="Model label")
    parser.add_argument("--elapsed", default="", help="Elapsed execution time")
    args = parser.parse_args()

    console = Console()
    orange_style = "rgb(215,95,0)"
    
    # Read content from stdin
    with console.status("[bold rgb(215,95,0)]⏳ Đang suy luận & kết nối Gateway...[/bold rgb(215,95,0)]", spinner="dots"):
        raw_text = sys.stdin.read()

    if not raw_text.strip():
        return

    # Shorten labels if necessary to prevent wrapping
    gw = args.gateway.replace(" - Terminal Siêu Tốc < 1ms", "").replace(" - Nén Token & Auto-Fallback Active", "").replace(" - Multi-Provider Engine", "")
    model = args.model.replace("COMBO: ", "")

    # 1. Header Panel (Concise 1-Line Claude Orange Box)
    header_content = f"🔀 [bold yellow]{gw}[/]   │   🧠 [bold green]{model}[/]   │   [bold green]🟢 Active[/]"
    console.print(
        Panel(
            header_content,
            title="[bold white on rgb(215,95,0)] 🤖 PuluSmartFlow v3.5 [/bold white on rgb(215,95,0)]",
            border_style=orange_style,
            box=ROUNDED,
            expand=False
        )
    )

    # 2. Main Markdown Content
    try:
        md = Markdown(raw_text)
        console.print(md)
    except Exception:
        sys.stdout.write(raw_text)

    # 3. Footer Panel (Compact 1-Line Meter Panel)
    elapsed_str = f"⏱️ {args.elapsed}s" if args.elapsed else "⏱️ Completed"
    footer_content = f"[dim white]{elapsed_str}  │  ➔ Auto-Token Nén  │  📦 Cache Active  │  ⚡ Max Speed  │  🟢 Active[/]"
    console.print(
        Panel(
            footer_content,
            border_style=f"dim {orange_style}",
            box=ROUNDED,
            expand=False
        )
    )

if __name__ == "__main__":
    main()
