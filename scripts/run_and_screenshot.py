#!/usr/bin/env python3
import sys
import subprocess
import os

RENDER_SCRIPT = os.path.expanduser("~/.gemini/config/skills/k8s-lab-pipeline/scripts/render_terminal_screenshot.py")

def run_and_capture(cmd, output_png, current_dir="Devops-Capstone-Project", min_height=260):
    print(f"==> Running: {cmd}")
    res = subprocess.run(cmd, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output_text = res.stdout
    print(output_text)

    # Compute appropriate auto-height based on line count
    lines = len(output_text.splitlines())
    auto_height = max(min_height, min(1200, 110 + lines * 22))

    subprocess.run([
        "python3", RENDER_SCRIPT,
        "--command", cmd,
        "--output-text", output_text,
        "--output", output_png,
        "--height", str(auto_height),
        "--dir", current_dir
    ], check=True)
    print(f"==> Saved screenshot to: {output_png}\n")
    return output_text

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 run_and_screenshot.py '<cmd>' '<output_png>' [dir] [min_height]")
        sys.exit(1)
    command = sys.argv[1]
    out_file = sys.argv[2]
    cwd_name = sys.argv[3] if len(sys.argv) > 3 else "Devops-Capstone-Project"
    h = int(sys.argv[4]) if len(sys.argv) > 4 else 260
    run_and_capture(command, out_file, cwd_name, h)
