#!/usr/bin/env python3
import sys, argparse, datetime, re
from rich.console import Console
from rich.markdown import Markdown
from rich.text import Text
from rich.live import Live
from rich.spinner import Spinner
from rich.table import Column

def main():
    parser = argparse.ArgumentParser(description="Stream terminal output with Claude CLI Native visual styling")
    parser.add_argument("--gateway", default="9Router", help="Gateway label")
    parser.add_argument("--model", default="SONNET 4.6", help="Model label")
    args = parser.parse_args()

    console = Console(highlight=False)
    orange_color = "rgb(217,119,6)"
    dim_orange = "dim rgb(217,119,6)"
    cyan_color = "rgb(56,189,248)"
    width = min(console.width, 80)

    # Clean labels
    gw = args.gateway.replace(" - Terminal Siêu Tốc < 1ms", "").replace(" - Nén Token & Auto-Fallback Active", "").replace(" - Multi-Provider Engine", "").replace(" (:20128)", "").replace(" (:20130)", "")
    model = args.model.replace("COMBO: ", "").replace(" (Max Coding)", "")

    # Phase 1: Show spinner while waiting for first byte
    lines_buffer = []
    first_line = None

    with Live(Spinner("dots", text=f"[{orange_color}]⏳ Đang suy luận & kết nối {gw}...[/{orange_color}]"), console=console, transient=True, refresh_per_second=12):
        first_line = sys.stdin.readline()

    if not first_line:
        return

    # Phase 2: Header
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    start_ts = datetime.datetime.now()
    console.print(f"[dim]{now_str}[/dim] [dim]│[/dim] [{cyan_color}]{gw}[/{cyan_color}] [dim]│[/dim] [bold green]{model}[/bold green] [dim]│[/dim] [bold cyan]Max Speed[/bold cyan]")
    console.print(f"[{orange_color}]" + "─" * width + f"[/{orange_color}]")

    # Phase 3: Stream lines real-time (show reasoning/execution steps as they arrive)
    step_count = 0
    all_lines = [first_line.rstrip('\n')]

    # Tool call / reasoning step detection patterns
    TOOL_PATTERNS = [
        (r'^●\s+(\w+)', "tool"),         # ● Read (2)
        (r'^[│├└]', "tree"),              # Tree structure lines
        (r'^>\s+', "quote"),              # Quoted output
        (r'^\[thinking\]', "think"),      # Thinking block
        (r'^\s*(─{3,})', "divider"),      # Dividers from claude
    ]

    def render_line(line):
        stripped = line.strip()
        if not stripped or stripped in ("🚀 PuluSmartFlow v3.5 Auto-Detect Engine Loaded | Auto Model & Auto Gateway Enabled",):
            return  # Skip banner noise

        # Detect tool call / tree structure
        for pattern, kind in TOOL_PATTERNS:
            if re.match(pattern, stripped):
                if kind == "tool":
                    console.print(f"[{orange_color}]{stripped}[/{orange_color}]")
                elif kind == "tree":
                    console.print(f"  [dim cyan]{stripped}[/dim cyan]")
                elif kind == "divider":
                    pass  # Skip duplicate dividers
                else:
                    console.print(f"[dim]{stripped}[/dim]")
                return

        # Regular content — stream directly
        console.print(stripped if stripped else "")

    # Print first line
    render_line(first_line)

    # Stream the rest
    for raw_line in sys.stdin:
        line = raw_line.rstrip('\n')
        all_lines.append(line)
        render_line(line)

    # Phase 4: Footer
    elapsed = round((datetime.datetime.now() - start_ts).total_seconds(), 2)
    console.print(f"[{dim_orange}]" + "─" * width + f"[/{dim_orange}]")
    console.print(f"[dim]Time: {elapsed}s  │  Tokens: Compressed  │  Cache: Active  │[/dim] [dim green]Session: Active[/dim green]")

if __name__ == "__main__":
    main()
