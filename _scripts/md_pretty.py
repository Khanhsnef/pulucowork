#!/usr/bin/env python3
import sys, argparse, datetime
from rich.console import Console
from rich.markdown import Markdown

def main():
    parser = argparse.ArgumentParser(description="Render terminal output with ultra-clean Claude CLI Native visual styling")
    parser.add_argument("--gateway", default="9Router (:20128)", help="Gateway label")
    parser.add_argument("--model", default="SONNET 4.6", help="Model label")
    parser.add_argument("--elapsed", default="", help="Elapsed execution time")
    args = parser.parse_args()

    console = Console()
    orange_color = "rgb(217,119,6)"
    dim_orange = "dim rgb(217,119,6)"
    cyan_color = "rgb(56,189,248)"
    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Clean short labels (remove extraneous text)
    gw = args.gateway.replace(" - Terminal Siêu Tốc < 1ms", "").replace(" - Nén Token & Auto-Fallback Active", "").replace(" - Multi-Provider Engine", "")
    model = args.model.replace("COMBO: ", "")

    # Live animated spinner while waiting for input
    with console.status(f"[{orange_color}]⏳ Đang suy luận & kết nối {gw}...[/{orange_color}]", spinner="dots"):
        raw_text = sys.stdin.read()

    if not raw_text.strip():
        return

    width = min(console.width, 88)
    elapsed_str = f"{args.elapsed}s" if args.elapsed else "1.2s"

    # 1. Clean Header Row (No Icons, Pure Minimalist Text)
    console.print(f"[dim]{now_str}[/dim] [dim]│[/dim] [{cyan_color}]Gateway: {gw}[/{cyan_color}] [dim]│[/dim] [bold green]Model: {model}[/bold green] [dim]│[/dim] [yellow]Cache: Active[/yellow] [dim]│[/dim] [{orange_color}]Latency: {elapsed_str}[/{orange_color}] [dim]│[/dim] [bold cyan]Speed: Max[/bold cyan]")
    console.print(f"[{orange_color}]" + "─" * width + f"[/{orange_color}]")

    # 2. Main Response Body (Markdown Rendered)
    try:
        md = Markdown(raw_text)
        console.print(md)
    except Exception:
        sys.stdout.write(raw_text)

    # 3. Dimmed Bottom Divider Line & Clean Footer Row (No Icons, Dim Soft Tint)
    console.print(f"[{dim_orange}]" + "─" * width + f"[/{dim_orange}]")
    console.print(f"[dim]Time: {elapsed_str}  │  Tokens: Auto-Compressed  │  Cache: Active  │  Speed: Max  │[/dim] [dim green]Session: Active[/dim green]")

if __name__ == "__main__":
    main()
