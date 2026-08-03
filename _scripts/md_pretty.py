#!/usr/bin/env python3
import sys, argparse, datetime
from rich.console import Console
from rich.markdown import Markdown

def main():
    parser = argparse.ArgumentParser(description="Render terminal output with Claude Code CLI Native visual layout")
    parser.add_argument("--gateway", default="9Router (:20128)", help="Gateway label")
    parser.add_argument("--model", default="SONNET 4.6", help="Model label")
    parser.add_argument("--elapsed", default="1.2s", help="Elapsed execution time")
    args = parser.parse_args()

    console = Console()
    orange_color = "rgb(217,119,6)"
    cyan_color = "rgb(56,189,248)"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Clean short labels
    gw = args.gateway.replace(" - Terminal Siêu Tốc < 1ms", "").replace(" - Nén Token & Auto-Fallback Active", "").replace(" - Multi-Provider Engine", "")
    model = args.model.replace("COMBO: ", "")

    # Live animated spinner while reading input
    with console.status(f"[{orange_color}]⏳ Đang suy luận & kết nối {gw}...[/{orange_color}]", spinner="dots"):
        raw_text = sys.stdin.read()

    if not raw_text.strip():
        return

    # 1. Claude CLI Native Top Status Line (Header Row)
    console.print(f"[dim]{now_str}[/dim] [dim]│[/dim] [{cyan_color}]🔀 {gw}[/{cyan_color}] [dim]│[/dim] [bold green]🧠 {model}[/bold green] [dim]│[/dim] [yellow]📦 Cache Active[/yellow] [dim]│[/dim] [{orange_color}]⏱️ {args.elapsed}[/{orange_color}] [dim]│[/dim] [bold cyan]⚡ Max Speed[/bold cyan]")
    console.print(f"[{orange_color}]" + "─" * min(console.width, 88) + f"[/{orange_color}]")

    # 2. Main Markdown Content (Unbordered Body with Native Tables)
    try:
        md = Markdown(raw_text)
        console.print(md)
    except Exception:
        sys.stdout.write(raw_text)

    # 3. Claude CLI Native Bottom Status Line (Footer Row)
    console.print(f"[{orange_color}]" + "─" * min(console.width, 88) + f"[/{orange_color}]")
    console.print(f"[dim]⏱️ {args.elapsed}  │  ➔ Auto-Token Nén  │  📦 Cache Active  │  ⚡ Max Speed  │[/dim] [bold green]🟢 Session Active[/bold green]")

if __name__ == "__main__":
    main()
