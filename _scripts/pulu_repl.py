#!/usr/bin/env python3
import sys, os, subprocess

def main():
    danger = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] == "!" else ""
    
    print("\n┌── 🤖 PuluSmartFlow Interactive Auto-Detect Chat ─────────────────┐")
    if danger:
        print("│ ⚡ CHẾ ĐỘ CHAT!: TỰ ĐỘNG CẤP QUYỀN (--dangerously-skip-permissions) │")
    else:
        print("│ 🔒 CHẾ ĐỘ CHAT: XÁC THỰC QUYỀN MẶC ĐỊNH                            │")
    print("│ Nhập/dán câu hỏi (gõ 'exit' hoặc nhấn Ctrl+C để thoát)           │")
    print("└───────────────────────────────────────────────────────────────────┘\n")

    workspace = "/Users/ts-1148/Desktop/Pulu-workspace"

    while True:
        try:
            print("💬 Nhập câu hỏi: ", end="", flush=True)
            line = sys.stdin.readline()
            if not line: # EOF / Ctrl+D
                print("\n👋 Tạm biệt!")
                break
            
            prompt_str = line.strip()
            if not prompt_str:
                continue
            if prompt_str.lower() in ["exit", "quit", "bye", "thoát", "q"]:
                print("👋 Tạm biệt!")
                break
            
            # Execute processing via bash subshell safely
            danger_arg = "!" if danger else ""
            env = os.environ.copy()
            subprocess.run(
                ["zsh", "-c", f'source ~/.zshrc && _process_single_chat_prompt "{prompt_str}"'],
                cwd=workspace,
                env=env,
                check=False
            )
            print("")
        except (KeyboardInterrupt, EOFError):
            print("\n👋 Tạm biệt!")
            break

if __name__ == "__main__":
    main()
