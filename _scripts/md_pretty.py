#!/usr/bin/env python3
"""
PuluSmartFlow Terminal Renderer v2.0
Visual hierarchy:
  - Tool calls:   ┌─ ● Bash  <command dim>
  - Tool output:  │  <text>   (indented)
  - Text/answer:  Rich Markdown (bold/italic/code/table rendered)
  - Dividers:     ─── sections
  - Footer:       token stats
"""
import sys, json, datetime, re, textwrap
from rich.console import Console
from rich.markdown import Markdown
from rich.live import Live
from rich.spinner import Spinner
from rich.text import Text

INDENT   = "  "          # 2-space base indent
BRANCH   = "  │  "       # continuation indent under tool call
ORANGE   = "rgb(217,119,6)"
DIM_ORG  = "dim rgb(217,119,6)"
CYAN     = "rgb(56,189,248)"
GREEN    = "rgb(134,239,172)"
GRAY     = "rgb(100,116,139)"
CODE_BG  = "rgb(30,30,30)"

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--gateway", default="9Router")
    parser.add_argument("--model",   default="SONNET 4.6")
    args = parser.parse_args()

    console = Console(highlight=False)
    width   = min(console.width, 80)

    gw    = re.sub(r'\s*\(:[0-9]+\)', '', args.gateway)
    gw    = re.sub(r'\s*-\s*(Terminal.*|Nén.*|Multi.*)', '', gw).strip()
    model = args.model.replace("COMBO: ", "").replace(" (Max Coding)", "")

    # ── Spinner until first byte ─────────────────────────────────────────
    first_line = None
    with Live(
        Spinner("dots", text=f"[{ORANGE}]Đang suy luận & kết nối {gw}…[/{ORANGE}]"),
        console=console, transient=True, refresh_per_second=14
    ):
        first_line = sys.stdin.readline()
    if not first_line:
        return

    # ── Header ───────────────────────────────────────────────────────────
    start_ts = datetime.datetime.now()
    now_str  = start_ts.strftime("%H:%M:%S")
    console.print(
        f"[{GRAY}]{now_str}[/{GRAY}]  "
        f"[{CYAN}]{gw}[/{CYAN}]  "
        f"[bold {GREEN}]{model}[/bold {GREEN}]  "
        f"[{GRAY}]Max Speed[/{GRAY}]"
    )
    console.print(f"[{ORANGE}]{'─' * width}[/{ORANGE}]")

    # ── State ─────────────────────────────────────────────────────────────
    tool_calls   = {}          # id → name
    init_shown   = False
    last_result  = None
    pending_text = []          # text blocks to render as Markdown
    last_tool_id = None        # for associating next tool result

    def flush_pending_text():
        """Render accumulated text as Markdown with proper indentation."""
        if not pending_text:
            return
        raw = "\n".join(pending_text).strip()
        pending_text.clear()
        if not raw:
            return
        # Render Markdown (bold/italic/code/table/lists)
        console.print(Markdown(raw, code_theme="monokai"))

    def render_tool_call(name, inp):
        """● ToolName  <command preview>"""
        flush_pending_text()
        # Build command preview
        cmd = ""
        if isinstance(inp, dict):
            cmd = (inp.get("command") or inp.get("path") or
                   inp.get("query") or inp.get("url") or
                   inp.get("description") or "")
        elif isinstance(inp, str):
            cmd = inp
        # Truncate long commands to first line
        cmd_first = cmd.split("\n")[0][:70] if cmd else ""
        remainder = cmd[len(cmd_first):].strip() if len(cmd) > len(cmd_first) else ""

        console.print(
            f"{INDENT}[bold {ORANGE}]●[/bold {ORANGE}] "
            f"[bold white]{name}[/bold white]  "
            f"[{GRAY}]{cmd_first}[/{GRAY}]"
        )
        # Extra lines of command (multiline bash)
        if remainder:
            for extra in remainder.split("\n")[:3]:
                if extra.strip():
                    console.print(f"{BRANCH}[{GRAY}]{extra.strip()}[/{GRAY}]")

    def render_tool_result(content):
        """  │  <result preview>"""
        text = ""
        if isinstance(content, list):
            text = " ".join(c.get("text", "") for c in content if c.get("type") == "text")
        elif isinstance(content, str):
            text = content
        text = text.strip()
        if not text:
            return
        # Show up to 3 lines of result
        lines = text.splitlines()
        shown = lines[:3]
        for ln in shown:
            if ln.strip():
                console.print(f"{BRANCH}[{GRAY}]{ln[:100]}[/{GRAY}]")
        if len(lines) > 3:
            console.print(f"{BRANCH}[{GRAY}]… ({len(lines)-3} dòng tiếp theo)[/{GRAY}]")

    def handle_event(obj):
        nonlocal init_shown, last_result, last_tool_id

        etype = obj.get("type", "")

        # ── assistant message ─────────────────────────────────────────────
        if etype == "assistant":
            for block in obj.get("message", {}).get("content", []):
                btype = block.get("type", "")

                if btype == "thinking":
                    flush_pending_text()
                    thought = block.get("thinking", "").strip()
                    if thought:
                        console.print(f"\n{INDENT}[dim italic]💭 Suy luận nội tâm:[/dim italic]")
                        for ln in thought.splitlines():
                            if ln.strip():
                                console.print(f"{BRANCH}[dim italic]{ln}[/dim italic]")
                        console.print(f"{INDENT}[{GRAY}]{'─'*40}[/{GRAY}]")

                elif btype == "text":
                    text = block.get("text", "")
                    if text.strip():
                        pending_text.append(text)

                elif btype == "tool_use":
                    tid   = block.get("id", "")
                    name  = block.get("name", "Tool")
                    inp   = block.get("input", {})
                    tool_calls[tid] = name
                    last_tool_id    = tid
                    render_tool_call(name, inp)

        # ── tool result ───────────────────────────────────────────────────
        elif etype == "tool_result":
            render_tool_result(obj.get("content", ""))

        # ── system init ───────────────────────────────────────────────────
        elif etype == "system":
            if obj.get("subtype") == "init" and not init_shown:
                init_shown = True
                tlist = obj.get("tools", [])
                if tlist:
                    console.print(
                        f"[{GRAY}]⚙  {', '.join(tlist[:6])}"
                        f"{'…' if len(tlist) > 6 else ''}[/{GRAY}]"
                    )

        # ── result (final) ────────────────────────────────────────────────
        elif etype == "result":
            out_tok = obj.get("usage", {}).get("output_tokens", 0)
            if out_tok > 0 or last_result is None:
                last_result = obj

    # ── Process events ───────────────────────────────────────────────────
    for raw in [first_line] + list(sys.stdin):
        raw = raw.strip()
        if not raw:
            continue
        try:
            handle_event(json.loads(raw))
        except json.JSONDecodeError:
            # Plain-text fallback (non-JSON stream)
            if raw and not raw.startswith("{"):
                pending_text.append(raw)

    # ── Flush remaining text & print footer ──────────────────────────────
    flush_pending_text()
    elapsed = round((datetime.datetime.now() - start_ts).total_seconds(), 2)
    console.print(f"\n[{DIM_ORG}]{'─' * width}[/{DIM_ORG}]")

    if last_result:
        u       = last_result.get("usage", {})
        in_tok  = u.get("input_tokens", 0)
        out_tok = u.get("output_tokens", 0)
        cache_r = u.get("cache_read_input_tokens", 0)
        cache_c = u.get("cache_creation_input_tokens", 0)
        dur_api = last_result.get("duration_api_ms", 0)
        cost    = last_result.get("total_cost_usd", 0)
        cost_str = f"  [yellow]${cost:.4f}[/yellow]" if cost else ""
        console.print(
            f"[{GRAY}]Time: {elapsed}s  │  "
            f"In: {in_tok:,}  │  Out: {out_tok:,}  │  "
            f"Cache↑: {cache_c:,}  Cache↓: {cache_r:,}  │  "
            f"API: {dur_api:,}ms[/{GRAY}]"
            f"{cost_str}  [{GREEN}]Session: Active[/{GREEN}]"
        )
    else:
        console.print(f"[{GRAY}]Time: {elapsed}s  │  Session: Active[/{GRAY}]")

if __name__ == "__main__":
    main()
