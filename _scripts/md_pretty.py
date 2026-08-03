#!/usr/bin/env python3
"""
PuluSmartFlow Terminal Renderer — Claude CLI Native stream-json format parser.
Hiển thị từng bước suy luận, tool calls, và nội dung phản hồi real-time.
"""
import sys, json, datetime, re
from rich.console import Console
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text
from rich.panel import Panel
from rich.box import ROUNDED

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--gateway", default="9Router")
    parser.add_argument("--model", default="SONNET 4.6")
    args = parser.parse_args()

    console = Console(highlight=False)
    orange = "rgb(217,119,6)"
    dim_orange = "dim rgb(217,119,6)"
    cyan = "rgb(56,189,248)"
    width = min(console.width, 80)

    gw = args.gateway.replace(" - Terminal Siêu Tốc < 1ms", "").replace(" - Nén Token & Auto-Fallback Active", "").replace(" - Multi-Provider Engine", "").replace(" (:20128)", "").replace(" (:20130)", "")
    model = args.model.replace("COMBO: ", "").replace(" (Max Coding)", "")

    # Phase 1: Spinner while waiting for first data
    first_line = None
    with Live(Spinner("dots", text=f"[{orange}]⏳ Đang suy luận & kết nối {gw}...[/{orange}]"), console=console, transient=True, refresh_per_second=12):
        first_line = sys.stdin.readline()

    if not first_line:
        return

    # Phase 2: Header
    now_str = datetime.datetime.now().strftime("%H:%M:%S")
    start_ts = datetime.datetime.now()
    console.print(f"[dim]{now_str}[/dim] [dim]│[/dim] [{cyan}]{gw}[/{cyan}] [dim]│[/dim] [bold green]{model}[/bold green] [dim]│[/dim] [bold cyan]Max Speed[/bold cyan]")
    console.print(f"[{orange}]" + "─" * width + f"[/{orange}]")

    # State tracking
    tool_calls = {}     # tool_use_id -> name
    thinking_open = False
    text_buffer = ""

    def flush_text():
        nonlocal text_buffer
        if text_buffer.strip():
            console.print(text_buffer.rstrip())
        text_buffer = ""

    def handle_event(obj):
        nonlocal thinking_open, text_buffer
        etype = obj.get("type", "")

        # ─── assistant message (contains content blocks) ───────────────
        if etype == "assistant":
            msg = obj.get("message", {})
            for block in msg.get("content", []):
                btype = block.get("type", "")

                if btype == "thinking":
                    flush_text()
                    thinking_text = block.get("thinking", "").strip()
                    if thinking_text:
                        # Show thinking panel
                        console.print(f"[dim italic]💭 Suy luận:[/dim italic]")
                        for tline in thinking_text.splitlines():
                            if tline.strip():
                                console.print(f"  [dim italic]{tline}[/dim italic]")
                    console.print(f"[dim]{'─' * 40}[/dim]")

                elif btype == "text":
                    text = block.get("text", "")
                    if text:
                        console.print(text.rstrip())

                elif btype == "tool_use":
                    flush_text()
                    tool_name = block.get("name", "?")
                    tool_input = block.get("input", {})
                    tool_calls[block.get("id", "")] = tool_name
                    # Show tool call in Claude CLI native style
                    inp_str = ""
                    if "command" in tool_input:
                        inp_str = tool_input["command"][:80]
                    elif "path" in tool_input:
                        inp_str = tool_input["path"]
                    elif "query" in tool_input:
                        inp_str = tool_input["query"][:80]
                    elif "url" in tool_input:
                        inp_str = tool_input["url"][:80]
                    console.print(f"[{orange}]● {tool_name}[/{orange}] [dim]{inp_str}[/dim]")

        # ─── tool result ────────────────────────────────────────────────
        elif etype == "tool_result":
            tool_id = obj.get("tool_use_id", "")
            tool_name = tool_calls.get(tool_id, "Tool")
            content = obj.get("content", "")
            if isinstance(content, list):
                content = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
            if content:
                preview = content.strip()[:120].replace("\n", " ")
                console.print(f"  [dim]└─ {preview}{'...' if len(content) > 120 else ''}[/dim]")

        # ─── system init ─────────────────────────────────────────────────
        elif etype == "system":
            subtype = obj.get("subtype", "")
            if subtype == "init":
                tools_list = obj.get("tools", [])
                if tools_list:
                    console.print(f"[dim]⚙ Tools: {', '.join(t for t in tools_list[:5])}{'...' if len(tools_list)>5 else ''}[/dim]")

        # ─── result (final) ───────────────────────────────────────────────
        elif etype == "result":
            flush_text()
            usage = obj.get("usage", {})
            in_tok = usage.get("input_tokens", 0)
            out_tok = usage.get("output_tokens", 0)
            cache_r = usage.get("cache_read_input_tokens", 0)
            cache_c = usage.get("cache_creation_input_tokens", 0)
            dur_api = obj.get("duration_api_ms", 0)
            cost = obj.get("total_cost_usd", 0)

            elapsed = round((datetime.datetime.now() - start_ts).total_seconds(), 2)
            console.print(f"[{dim_orange}]" + "─" * width + f"[/{dim_orange}]")
            console.print(
                f"[dim]Time: {elapsed}s  │  "
                f"In: {in_tok:,}  │  "
                f"Out: {out_tok:,}  │  "
                f"Cache↑: {cache_c:,}  Cache↓: {cache_r:,}  │  "
                f"API: {dur_api:,}ms  │[/dim]"
                + (f" [dim yellow]Cost: ${cost:.4f}[/dim yellow]" if cost else "")
                + " [dim green]Session: Active[/dim green]"
            )

    # Process first line
    try:
        obj = json.loads(first_line.strip())
        handle_event(obj)
    except json.JSONDecodeError:
        # Not JSON — plain text mode
        console.print(first_line.rstrip())
        for line in sys.stdin:
            console.print(line.rstrip())
        elapsed = round((datetime.datetime.now() - start_ts).total_seconds(), 2)
        console.print(f"[{dim_orange}]" + "─" * width + f"[/{dim_orange}]")
        console.print(f"[dim]Time: {elapsed}s  │  Session: Active[/dim] [dim green]●[/dim green]")
        return

    # Stream remaining events
    for raw_line in sys.stdin:
        raw_line = raw_line.strip()
        if not raw_line:
            continue
        try:
            obj = json.loads(raw_line)
            handle_event(obj)
        except json.JSONDecodeError:
            console.print(raw_line)

if __name__ == "__main__":
    main()
