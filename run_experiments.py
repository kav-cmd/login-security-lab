"""
Experiment runner for Milestone 7.
Runs all scenarios, records consolidated CSV, and generates comparison charts.
"""
from __future__ import annotations

import csv
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import plotly.express as px
import requests

ROOT = Path(__file__).resolve().parent
CONFIG_PATH = ROOT / "config.py"
DB_PATH = ROOT / "database.db"
RESULTS_DIR = ROOT / "results"
GRAPHS_DIR = RESULTS_DIR / "graphs"
RESULTS_CSV = RESULTS_DIR / "experiment_results.csv"
ATTACK_RESULT_RE = re.compile(r"Results saved to:\s*(.+\.json)")

TOGGLE_KEYS = (
    "RATE_LIMIT_ENABLED",
    "ACCOUNT_LOCKOUT",
    "IP_BLOCKING",
    "CAPTCHA_ENABLED",
    "ANOMALY_DETECTION",
    "MFA_ENABLED",
    "PWNED_CHECK_ENABLED",
    "PASSWORD_STRENGTH",
)

SCENARIOS = [
    {
        "name": "No Defense",
        "config": {
            "RATE_LIMIT_ENABLED": False,
            "ACCOUNT_LOCKOUT": False,
            "IP_BLOCKING": False,
            "CAPTCHA_ENABLED": False,
            "ANOMALY_DETECTION": False,
        },
        "attacks": [
            ["attacks/attack_bruteforce.py", "-u", "admin", "-w", "wordlists/passwords.txt", "--save"],
            ["attacks/attack_credential_stuffing.py", "-c", "wordlists/credentials.txt", "--save"],
            ["attacks/attack_distributed.py", "-u", "admin", "-w", "wordlists/passwords.txt", "-p", "50", "--save"],
        ],
    },
    {
        "name": "Rate Limit Only",
        "config": {
            "RATE_LIMIT_ENABLED": True,
            "ACCOUNT_LOCKOUT": False,
            "IP_BLOCKING": False,
            "CAPTCHA_ENABLED": False,
            "ANOMALY_DETECTION": False,
        },
        "attacks": [
            ["attacks/attack_bruteforce.py", "-u", "admin", "-w", "wordlists/passwords.txt", "--save"],
            ["attacks/attack_credential_stuffing.py", "-c", "wordlists/credentials.txt", "--save"],
            ["attacks/attack_distributed.py", "-u", "admin", "-w", "wordlists/passwords.txt", "-p", "50", "--save"],
        ],
    },
    {
        "name": "Account Lockout Only",
        "config": {
            "RATE_LIMIT_ENABLED": False,
            "ACCOUNT_LOCKOUT": True,
            "IP_BLOCKING": False,
            "CAPTCHA_ENABLED": False,
            "ANOMALY_DETECTION": False,
        },
        "attacks": [
            ["attacks/attack_bruteforce.py", "-u", "admin", "-w", "wordlists/passwords.txt", "--save"],
            ["attacks/attack_credential_stuffing.py", "-c", "wordlists/credentials.txt", "--save"],
            ["attacks/attack_distributed.py", "-u", "admin", "-w", "wordlists/passwords.txt", "-p", "50", "--save"],
        ],
    },
    {
        "name": "IP Blocking Only",
        "config": {
            "RATE_LIMIT_ENABLED": False,
            "ACCOUNT_LOCKOUT": False,
            "IP_BLOCKING": True,
            "CAPTCHA_ENABLED": False,
            "ANOMALY_DETECTION": False,
        },
        "attacks": [
            ["attacks/attack_bruteforce.py", "-u", "admin", "-w", "wordlists/passwords.txt", "--save"],
            ["attacks/attack_credential_stuffing.py", "-c", "wordlists/credentials.txt", "--save"],
            ["attacks/attack_distributed.py", "-u", "admin", "-w", "wordlists/passwords.txt", "-p", "50", "--save"],
        ],
    },
    {
        "name": "CAPTCHA Only",
        "config": {
            "RATE_LIMIT_ENABLED": False,
            "ACCOUNT_LOCKOUT": False,
            "IP_BLOCKING": False,
            "CAPTCHA_ENABLED": True,
            "ANOMALY_DETECTION": False,
        },
        "attacks": [
            ["attacks/attack_bruteforce.py", "-u", "admin", "-w", "wordlists/passwords.txt", "--save"],
            ["attacks/attack_credential_stuffing.py", "-c", "wordlists/credentials.txt", "--save"],
            ["attacks/attack_distributed.py", "-u", "admin", "-w", "wordlists/passwords.txt", "-p", "50", "--save"],
        ],
    },
    {
        "name": "All Defenses",
        "config": {
            "RATE_LIMIT_ENABLED": True,
            "ACCOUNT_LOCKOUT": True,
            "IP_BLOCKING": True,
            "CAPTCHA_ENABLED": True,
            "ANOMALY_DETECTION": True,
        },
        "attacks": [
            ["attacks/attack_bruteforce.py", "-u", "admin", "-w", "wordlists/passwords.txt", "--save"],
            ["attacks/attack_credential_stuffing.py", "-c", "wordlists/credentials.txt", "--save"],
            ["attacks/attack_distributed.py", "-u", "admin", "-w", "wordlists/passwords.txt", "-p", "50", "--save"],
        ],
    },
    {
        "name": "Distributed vs All Defenses",
        "config": {
            "RATE_LIMIT_ENABLED": True,
            "ACCOUNT_LOCKOUT": True,
            "IP_BLOCKING": True,
            "CAPTCHA_ENABLED": True,
            "ANOMALY_DETECTION": True,
        },
        "attacks": [
            ["attacks/attack_distributed.py", "-u", "admin", "-w", "wordlists/passwords.txt", "-p", "100", "--save"],
        ],
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.write_text(content, encoding="utf-8")


def set_config_toggles(config_values: dict[str, bool]) -> None:
    content = read_text(CONFIG_PATH)
    for key in TOGGLE_KEYS:
        value = config_values.get(key, False)
        content = re.sub(rf"^{key}\s*=.*$", f"{key} = {value}", content, flags=re.MULTILINE)
    write_text(CONFIG_PATH, content)


def clear_database() -> None:
    if DB_PATH.exists():
        start = time.time()
        timeout = 10
        while True:
            try:
                DB_PATH.unlink()
                return
            except PermissionError:
                if time.time() - start > timeout:
                    raise RuntimeError(
                        f"Could not delete database {DB_PATH!s}: file is locked by another process."
                        " Stop any running Flask/Streamlit instances and try again."
                    )
                time.sleep(1)


def wait_for_server(timeout_sec: int = 45) -> None:
    start = time.time()
    last_error = None

    while time.time() - start < timeout_sec:
        try:
            response = requests.get("http://127.0.0.1:5000/login", timeout=2)
            if response.status_code in (200, 405):
                return
        except requests.RequestException as exc:
            last_error = exc
        time.sleep(1)

    raise RuntimeError(f"Flask server did not become ready in {timeout_sec}s. Last error: {last_error}")


def start_flask_server() -> subprocess.Popen[str]:
    env = os.environ.copy()
    env["DISABLE_RELOADER"] = "1"
    process = subprocess.Popen(
        [sys.executable, "run.py"],
        cwd=ROOT,
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True,
    )
    wait_for_server()
    return process


def stop_flask_server(process: subprocess.Popen[str]) -> None:
    if os.name == "nt":
        subprocess.run(
            ["taskkill", "/PID", str(process.pid), "/T", "/F"],
            cwd=ROOT,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            pass
    else:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait(timeout=5)


def parse_attack_output(stdout: str) -> Path:
    match = ATTACK_RESULT_RE.search(stdout)
    if not match:
        raise RuntimeError("Attack script did not output a result JSON path.")
    output_path = Path(match.group(1).strip())
    if not output_path.is_absolute():
        output_path = ROOT / output_path
    if not output_path.exists():
        raise FileNotFoundError(f"Attack output not found: {output_path}")
    return output_path


def run_attack(attack_cmd: list[str]) -> dict[str, Any]:
    command = [sys.executable] + attack_cmd
    result = subprocess.run(
        command,
        cwd=ROOT,
        input="yes\n",
        capture_output=True,
        text=True,
        timeout=600,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"Attack command failed ({result.returncode}): {' '.join(command)}\n{result.stdout}\n{result.stderr}"
        )

    result_file = parse_attack_output(result.stdout)
    with result_file.open("r", encoding="utf-8") as file_obj:
        return json.load(file_obj)


def to_result_row(scenario_name: str, payload: dict[str, Any]) -> dict[str, Any]:
    attempts = int(payload.get("attempts", 0))
    successes = int(payload.get("success", 0))
    blocked = int(payload.get("blocked", 0))
    duration_sec = float(payload.get("duration_sec", 0.0))
    success_rate = (successes / attempts * 100.0) if attempts else 0.0
    block_rate = (blocked / attempts * 100.0) if attempts else 0.0

    return {
        "scenario": scenario_name,
        "attack_type": payload.get("attack_type", "unknown"),
        "total_attempts": attempts,
        "successes": successes,
        "blocked": blocked,
        "duration_sec": round(duration_sec, 3),
        "success_rate": round(success_rate, 2),
        "block_rate": round(block_rate, 2),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def write_results_csv(rows: list[dict[str, Any]]) -> None:
    fieldnames = [
        "scenario",
        "attack_type",
        "total_attempts",
        "successes",
        "blocked",
        "duration_sec",
        "success_rate",
        "block_rate",
        "timestamp",
    ]
    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generate_graphs(csv_path: Path) -> list[Path]:
    df = pd.read_csv(csv_path)
    generated: list[Path] = []

    fig_success = px.bar(
        df,
        x="scenario",
        y="success_rate",
        color="attack_type",
        barmode="group",
        title="Attack Success Rate by Scenario",
    )
    success_path = GRAPHS_DIR / "success_rate_comparison.html"
    fig_success.write_html(success_path)
    generated.append(success_path)

    fig_block = px.bar(
        df,
        x="scenario",
        y="block_rate",
        color="attack_type",
        barmode="group",
        title="Block Rate by Scenario",
    )
    block_path = GRAPHS_DIR / "block_rate_comparison.html"
    fig_block.write_html(block_path)
    generated.append(block_path)

    fig_duration = px.line(
        df,
        x="scenario",
        y="duration_sec",
        color="attack_type",
        markers=True,
        title="Attack Duration by Scenario",
    )
    duration_path = GRAPHS_DIR / "duration_comparison.html"
    fig_duration.write_html(duration_path)
    generated.append(duration_path)

    return generated


def main() -> None:
    print("=" * 70)
    print("  AUTOMATED EXPERIMENT RUNNER")
    print("=" * 70)
    print("This will:")
    print("  1. Run all 7 experiment scenarios")
    print("  2. Start/stop Flask app automatically per run")
    print("  3. Save consolidated CSV and comparison graphs")
    print()

    confirm = input("Continue? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("Cancelled.")
        return

    RESULTS_DIR.mkdir(exist_ok=True)
    GRAPHS_DIR.mkdir(parents=True, exist_ok=True)

    original_config = read_text(CONFIG_PATH)
    rows: list[dict[str, Any]] = []

    total_runs = sum(len(scenario["attacks"]) for scenario in SCENARIOS)
    current_run = 0

    try:
        for scenario in SCENARIOS:
            set_config_toggles(scenario["config"])
            print(f"\n[SCENARIO] {scenario['name']}")

            for attack_cmd in scenario["attacks"]:
                current_run += 1
                print(f"  [{current_run}/{total_runs}] Running: {' '.join(attack_cmd)}")
                clear_database()
                flask_process = start_flask_server()
                try:
                    payload = run_attack(attack_cmd)
                    rows.append(to_result_row(scenario["name"], payload))
                finally:
                    stop_flask_server(flask_process)

        write_results_csv(rows)
        graph_files = generate_graphs(RESULTS_CSV)

        print("\n" + "=" * 70)
        print("EXPERIMENTS COMPLETED")
        print(f"Results CSV: {RESULTS_CSV}")
        for graph_file in graph_files:
            print(f"Graph: {graph_file}")
        print("=" * 70)
    finally:
        write_text(CONFIG_PATH, original_config)


if __name__ == "__main__":
    main()
