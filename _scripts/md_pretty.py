#!/usr/bin/env python3
import sys, argparse, datetime
from rich.console import Console
from rich.markdown import Markdown

def main():
    parser = argparse.ArgumentParser(description="Render terminal output with ultra-clean Claude CLI Native visual styling")
    parser.add_argument("--gateway", default="9Router", help="Gateway label")
    parser.add_argument("--model", default="SONNET 4.6", help="Model label")
    parser.add_argument("--elapsed", default="", help="Elapsed execution time")
    args = parser.parse_args()

    console = Console()
    orange_color = "rgb(217,119,6)"
    dim_orange = "dim rgb(217,119,6)"
    cyan_color = "rgb(56,189,248)"
    start_time = datetime.datetime.now()
    now_str = start_time.strftime("%H:%M:%S")

    # Clean short labels for compact single-line rendering
    gw = args.gateway.replace(" - Terminal Siêu Tốc < 1ms", "").replace(" - Nén Token & Auto-Fallback Active", "").replace(" - Multi-Provider Engine", "").replace(" (:20128)", "").replace(" (:20130)", "")
    model = args.model.replace("COMBO: ", "").replace(" (Max Coding)", "")

    # Live animated spinner displayed IMMEDIATELY while reading piped stream
    with console.status(f"[{orange_color}]⏳ Đang suy luận & kết nối {gw}...[/{orange_color}]", spinner="dots"):
        raw_text = sys.stdin.read()

    end_time = datetime.datetime.now()
    elapsed_seconds = round((end_time - start_time).total_seconds(), 2)
    elapsed_str = f"{elapsed_seconds}s"

    if not raw_text.strip():
        return

    # Filter out duplicate banner or system header lines
    lines = raw_text.splitlines()
    filtered_lines = []
    seen = set()
    for line in lines:
        if "🚀 PuluSmartFlow" in line or "Auto Model & Auto Gateway Enabled" in line:
            continue
        # Remove consecutive duplicate blank lines
        if line.strip() == "" and filtered_lines and filtered_lines[-1].strip() == "":
            continue
        filtered_lines.append(line)

    clean_text = "\n".join(filtered_lines).strip()
    if not clean_text:
        return

    width = min(console.width, 80)

    # 1. Compact Header Row (Guaranteed No Line Wrapping)
    console.print(f"[dim]{now_str}[/dim] [dim]│[/dim] [{cyan_color}]{gw}[/{cyan_color}] [dim]│[/dim] [bold green]{model}[/bold green] [dim]│[/dim] [{orange_color}]{elapsed_str}[/{orange_color}] [dim]│[/dim] [bold cyan]Max Speed[/bold cyan]")
    console.print(f"[{orange_color}]" + "─" * width + f"[/{orange_color}]")

    # 2. Main Response Body (Markdown Rendered)
    try:
        md = Markdown(clean_text)
        console.print(md)
    except Exception:
        sys.stdout.write(clean_text + "\n")

    # 3. Dimmed Bottom Divider Line & Clean Compact Footer Row
    console.print(f"[{dim_orange}]" + "─" * width + f"[/{dim_orange}]")
    console.print(f"[dim]Time: {elapsed_str}  │  Tokens: Compressed  │  Cache: Active  │[/dim] [dim green]Session: Active[/dim green]")

if __name__ == "__main__":
    main()
