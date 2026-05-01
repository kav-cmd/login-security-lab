"""
Project Verification Script
Checks that all components are properly installed and configured
"""
import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"[OK] {description}")
        return True
    else:
        print(f"[MISSING] {description}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if os.path.isdir(dirpath):
        print(f"[OK] {description}")
        return True
    else:
        print(f"[MISSING] {description}")
        return False

def check_python_version():
    """Check Python version"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(f"[OK] Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"[FAIL] Python version {version.major}.{version.minor} (requires 3.10+)")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'flask', 'flask_login', 'flask_limiter', 'flask_sqlalchemy',
        'requests', 'streamlit', 'plotly', 'pyotp', 'bcrypt', 'dotenv'
    ]

    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"[OK] {package}")
        except ImportError:
            print(f"[MISSING] {package}")
            missing.append(package)

    return len(missing) == 0

def main():
    print("=" * 70)
    print("  LOGIN SECURITY TESTBED - PROJECT VERIFICATION")
    print("=" * 70)
    print()

    all_checks = []

    # Python version
    print("1. Python Version")
    all_checks.append(check_python_version())
    print()

    # Core files
    print("2. Core Application Files")
    all_checks.append(check_file("config.py", "Configuration file"))
    all_checks.append(check_file("run.py", "Flask launcher"))
    all_checks.append(check_file("requirements.txt", "Dependencies list"))
    all_checks.append(check_file("db_utils.py", "Database utilities"))
    print()

    # App directory
    print("3. Flask Application")
    all_checks.append(check_directory("app", "App directory"))
    all_checks.append(check_file("app/__init__.py", "App factory"))
    all_checks.append(check_file("app/models.py", "Database models"))
    all_checks.append(check_file("app/routes.py", "Routes"))
    all_checks.append(check_file("app/defenses.py", "Defense mechanisms"))
    all_checks.append(check_file("app/logger.py", "Logger"))
    print()

    # Templates
    print("4. HTML Templates")
    all_checks.append(check_directory("app/templates", "Templates directory"))
    all_checks.append(check_file("app/templates/login.html", "Login page"))
    all_checks.append(check_file("app/templates/dashboard.html", "Dashboard page"))
    all_checks.append(check_file("app/templates/captcha.html", "CAPTCHA page"))
    all_checks.append(check_file("app/templates/mfa.html", "MFA page"))
    print()

    # Attack scripts
    print("5. Attack Simulation Scripts")
    all_checks.append(check_directory("attacks", "Attacks directory"))
    all_checks.append(check_file("attacks/attack_bruteforce.py", "Brute force"))
    all_checks.append(check_file("attacks/attack_credential_stuffing.py", "Credential stuffing"))
    all_checks.append(check_file("attacks/attack_distributed.py", "Distributed attack"))
    all_checks.append(check_file("attacks/attack_username_enum.py", "Username enumeration"))
    print()

    # Wordlists
    print("6. Wordlists")
    all_checks.append(check_directory("wordlists", "Wordlists directory"))
    all_checks.append(check_file("wordlists/passwords.txt", "Passwords"))
    all_checks.append(check_file("wordlists/credentials.txt", "Credentials"))
    all_checks.append(check_file("wordlists/usernames.txt", "Usernames"))
    print()

    # Dashboard
    print("7. Monitoring Dashboard")
    all_checks.append(check_directory("dashboard", "Dashboard directory"))
    all_checks.append(check_file("dashboard/app.py", "Streamlit dashboard"))
    print()

    # Documentation
    print("8. Documentation")
    all_checks.append(check_file("README.md", "README"))
    all_checks.append(check_file("VULNERABILITIES.md", "Vulnerabilities doc"))
    all_checks.append(check_file("HARDENING_GUIDE.md", "Hardening guide"))
    all_checks.append(check_file("QUICK_START.md", "Quick start guide"))
    all_checks.append(check_file("PROJECT_SUMMARY.md", "Project summary"))
    print()

    # Other directories
    print("9. Supporting Directories")
    all_checks.append(check_directory("results", "Results directory"))
    all_checks.append(check_directory("mock_integrations", "Mock integrations"))
    print()

    # Dependencies
    print("10. Python Dependencies")
    deps_ok = check_dependencies()
    all_checks.append(deps_ok)
    print()

    # Summary
    print("=" * 70)
    passed = sum(all_checks)
    total = len(all_checks)

    if passed == total:
        print(f"SUCCESS: ALL CHECKS PASSED ({passed}/{total})")
        print()
        print("Your project is ready to use!")
        print()
        print("Next steps:")
        print("  1. Run: python run.py")
        print("  2. Run: streamlit run dashboard/app.py")
        print("  3. Run: python attacks/attack_bruteforce.py -u admin -w wordlists/passwords.txt -v")
    else:
        print(f"WARNING: SOME CHECKS FAILED ({passed}/{total} passed)")
        print()
        if not deps_ok:
            print("Install dependencies: pip install -r requirements.txt")

    print("=" * 70)

if __name__ == "__main__":
    main()
