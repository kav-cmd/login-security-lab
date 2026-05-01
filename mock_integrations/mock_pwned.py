"""
Mock HaveIBeenPwned API
Simulates checking passwords against breach databases
"""

# Common passwords that would be flagged as "pwned"
PWNED_PASSWORDS = {
    'password', '123456', '12345678', 'qwerty', 'abc123',
    'monkey', 'letmein', 'trustno1', 'dragon', 'baseball',
    'iloveyou', 'master', 'sunshine', 'ashley', 'bailey',
    'passw0rd', 'shadow', 'superman', 'qazwsx', 'michael',
    'football', 'welcome', 'jesus', 'ninja', 'mustang',
    'password1', 'password123', '123456789', '12345',
    '1234567', 'password1', '12345678', '123456789',
    'admin', 'root', 'toor', 'pass', 'test', 'guest',
    'admin123', 'root123', 'administrator', 'user',
    'demo', 'changeme', 'welcome1', 'hello', 'login'
}

def check_password(password):
    """
    Check if password appears in breach database

    Args:
        password: Password to check

    Returns:
        tuple: (is_pwned, breach_count)
    """
    password_lower = password.lower()

    if password_lower in PWNED_PASSWORDS:
        # Simulate breach count (higher for more common passwords)
        breach_count = len(password_lower) * 100000
        return True, breach_count

    return False, 0

def get_breach_info(password):
    """
    Get detailed breach information for a password

    Args:
        password: Password to check

    Returns:
        dict: Breach information
    """
    is_pwned, count = check_password(password)

    return {
        'is_pwned': is_pwned,
        'breach_count': count,
        'severity': 'HIGH' if count > 100000 else 'MEDIUM' if count > 10000 else 'LOW',
        'recommendation': 'Change immediately' if is_pwned else 'Password appears safe'
    }

if __name__ == '__main__':
    # Test the mock API
    test_passwords = [
        'password',
        'MySecureP@ssw0rd2024!',
        '123456',
        'correct-horse-battery-staple'
    ]

    print("Mock HaveIBeenPwned API Test")
    print("=" * 60)

    for pwd in test_passwords:
        info = get_breach_info(pwd)
        print(f"\nPassword: {pwd}")
        print(f"  Pwned: {info['is_pwned']}")
        print(f"  Breach Count: {info['breach_count']:,}")
        print(f"  Severity: {info['severity']}")
        print(f"  Recommendation: {info['recommendation']}")
