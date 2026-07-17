#!/usr/bin/env python3
import subprocess
import shutil
import sys
import os

def run_cmd(cmd):
    base_cmd = cmd.split()[0]

    if shutil.which(base_cmd) is None:
        return "[ERROR] Command '%s' not found." % base_cmd
    else:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "[FAIL] Exit %d: %s" % (result.returncode, result.stderr.strip())

def print_header(title):
    print("\n" + "-" * 60)
    print("[ %s ]" % title)
    print("-" * 60)

def main():
    print("\n" + " " * 20 + "REMOTE SYSTEM HEALTH REPORT")
    print(" " * 20 + "-" * 30)
    print("   Hostname    : %s" % run_cmd('hostname'))
    print("   User        : %s" % run_cmd('whoami'))
    print("   Timestamp   : %s" % run_cmd('date'))
    print(" " * 20 + "-" * 30)

    print_header("1. KERNEL & OS")
    print(run_cmd("uname -a"))

    print_header("2. MEMORY USAGE (free -h)")
    print(run_cmd("free -h"))

    print_header("3. DISK SPACE (df -h /)")
    print(run_cmd("df -h /"))

    print_header("4. LOAD AVERAGE & UPTIME")
    print(run_cmd("uptime"))

    print_header("5. TOP 5 CPU PROCESSES")
    print(run_cmd("ps aux | sort -k3 -nr | head -6")) 

    print_header("6. TOP 5 MEMORY PROCESSES")
    print(run_cmd("ps aux | sort -k4 -nr | head -6"))

    print("\n" + "-" * 60)
    print("[OK] Report complete.")
    print("-" * 60)

if __name__ == "__main__":
    main()
