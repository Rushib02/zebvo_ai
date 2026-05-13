import sys
import os

# ── ANSI colours ──────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
MAGENTA= "\033[95m"
DIM    = "\033[2m"

def info(msg:  str): print(f"{CYAN}{BOLD}[INFO]{RESET}  {msg}")
def ok(msg:    str): print(f"{GREEN}{BOLD}[OK]{RESET}    {msg}")
def warn(msg:  str): print(f"{YELLOW}{BOLD}[WARN]{RESET}  {msg}")
def error(msg: str): print(f"{RED}{BOLD}[ERROR]{RESET} {msg}")
def stage(msg: str): print(f"\n{MAGENTA}{BOLD}▶  {msg}{RESET}")
def dim(msg:   str): print(f"{DIM}{msg}{RESET}")

def section(title: str):
    width = 50
    print(f"\n{CYAN}{'═'*width}{RESET}")
    print(f"{BOLD}{CYAN}  {title}{RESET}")
    print(f"{CYAN}{'═'*width}{RESET}")
