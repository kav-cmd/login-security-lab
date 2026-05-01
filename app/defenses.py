from datetime import datetime, timedelta
from app import db
from app.models import User, LoginAttempt, BlockedIP
import config
import random
import hashlib
import requests

def is_ip_blocked(ip):
    """Check if IP is permanently blocked"""
    if not config.IP_BLOCKING:
        return False

    blocked = BlockedIP.query.filter_by(ip=ip).first()
    return blocked is not None

def block_ip(ip, reason):
    """Add IP to permanent block list"""
    if BlockedIP.query.filter_by(ip=ip).first():
        return  # Already blocked

    blocked_ip = BlockedIP(ip=ip, reason=reason)
    db.session.add(blocked_ip)
    db.session.commit()

def is_account_locked(username):
    """Check if account is temporarily locked"""
    if not config.ACCOUNT_LOCKOUT:
        return False

    user = User.query.filter_by(username=username).first()
    if user and user.locked_until and user.locked_until > datetime.utcnow():
        return True
    return False

def handle_failed_attempt(ip, username):
    """Handle failed login attempt - update counters and apply locks"""
    # Account lockout logic
    if config.ACCOUNT_LOCKOUT:
        user = User.query.filter_by(username=username).first()
        if user:
            user.failed_attempts += 1
            if user.failed_attempts >= config.LOCKOUT_THRESHOLD:
                user.locked_until = datetime.utcnow() + timedelta(minutes=config.LOCKOUT_DURATION_MIN)
            db.session.commit()

    # IP blocking logic
    if config.IP_BLOCKING:
        sixty_days_ago = datetime.utcnow() - timedelta(days=60)
        failed_count = LoginAttempt.query.filter(
            LoginAttempt.ip == ip,
            LoginAttempt.success == 0,
            LoginAttempt.timestamp >= sixty_days_ago
        ).count()

        if failed_count >= config.IP_BLOCK_THRESHOLD:
            block_ip(ip, f"Exceeded {config.IP_BLOCK_THRESHOLD} failed attempts")

def reset_failed_attempts(username):
    """Reset failed attempt counter on successful login"""
    user = User.query.filter_by(username=username).first()
    if user:
        user.failed_attempts = 0
        user.locked_until = None
        db.session.commit()

def check_anomaly(ip):
    """Rule-based anomaly detection - check for suspicious activity"""
    if not config.ANOMALY_DETECTION:
        return False

    sixty_seconds_ago = datetime.utcnow() - timedelta(seconds=60)
    recent_attempts = LoginAttempt.query.filter(
        LoginAttempt.ip == ip,
        LoginAttempt.timestamp >= sixty_seconds_ago
    ).count()

    if recent_attempts >= config.ANOMALY_THRESHOLD:
        return True
    return False

def trigger_alert(ip, attempt_count):
    """Trigger anomaly alert (in real system would send notification)"""
    print(f"[ANOMALY ALERT] IP {ip} made {attempt_count} attempts in 60 seconds")

def needs_captcha(username):
    """Check if user needs to solve CAPTCHA"""
    if not config.CAPTCHA_ENABLED:
        return False

    user = User.query.filter_by(username=username).first()
    if user and user.failed_attempts >= config.CAPTCHA_TRIGGER:
        return True
    return False

def generate_captcha():
    """Generate simple math CAPTCHA"""
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    return {
        'question': f"What is {a} + {b}?",
        'answer': str(a + b)
    }

def verify_captcha(user_answer, correct_answer):
    """Verify CAPTCHA answer"""
    return user_answer.strip() == correct_answer.strip()

def check_pwned_password(password):
    """
    Check if password exists in HaveIBeenPwned database using k-anonymity.

    Uses the Pwned Passwords API (https://haveibeenpwned.com/API/v3#SearchingPwnedPasswordsByRange)
    which implements k-anonymity: we send first 5 chars of SHA-1 hash to the API,
    and it returns all matching hashes. We then search locally for the remainder.

    Returns:
        dict: {'is_pwned': bool, 'breach_count': int or None}
        - is_pwned: True if password found in breach databases
        - breach_count: Number of times this password appeared in breaches (if found)
    """
    if not config.PWNED_CHECK_ENABLED:
        return {'is_pwned': False, 'breach_count': None}

    try:
        # SHA-1 hash of password
        password_hash = hashlib.sha1(password.encode()).hexdigest().upper()

        # K-anonymity: send first 5 characters
        hash_prefix = password_hash[:5]
        hash_suffix = password_hash[5:]

        # Query HIBP API with timeout
        response = requests.get(
            f"{config.HIBP_API_URL}/{hash_prefix}",
            timeout=config.HIBP_API_TIMEOUT,
            headers={'User-Agent': 'LoginSecurityTestbed/1.0'}  # Required by HIBP API
        )

        # Non-200 responses indicate API issue
        if response.status_code == 404:
            # Not found in any breach database
            log_hibp_check(password, False, None)
            return {'is_pwned': False, 'breach_count': None}

        if response.status_code != 200:
            # API error - log and allow login (fail open)
            print(f"[HIBP API] HTTP {response.status_code}: {response.reason}")
            return {'is_pwned': False, 'breach_count': None}

        # Parse response: each line is "HASH_SUFFIX:COUNT"
        for line in response.text.splitlines():
            returned_suffix, count = line.split(':')

            if returned_suffix == hash_suffix:
                breach_count = int(count)
                log_hibp_check(password, True, breach_count)
                print(f"[HIBP] Password detected in {breach_count} breaches")
                return {'is_pwned': True, 'breach_count': breach_count}

        # Hash suffix not found - password is safe
        log_hibp_check(password, False, None)
        return {'is_pwned': False, 'breach_count': None}

    except requests.exceptions.Timeout:
        # API timeout - fail open (allow login)
        print(f"[HIBP API] Timeout after {config.HIBP_API_TIMEOUT}s - allowing login")
        return {'is_pwned': False, 'breach_count': None}

    except requests.exceptions.RequestException as e:
        # Network error, DNS issue, etc. - fail open
        print(f"[HIBP API] Error: {type(e).__name__}: {str(e)}")
        return {'is_pwned': False, 'breach_count': None}

    except Exception as e:
        # Unexpected error - log and fail open
        print(f"[HIBP] Unexpected error: {type(e).__name__}: {str(e)}")
        return {'is_pwned': False, 'breach_count': None}


def log_hibp_check(password, is_pwned, breach_count):
    """
    Log HIBP password check results.

    Only logs if password is found (is_pwned=True) for security/privacy.
    Does not log the actual password.
    """
    if is_pwned:
        print(f"[SECURITY] Pwned password detected: found in {breach_count} breaches")
        # Could integrate with logging system here if needed

def check_password_strength(password):
    """Check password strength"""
    if not config.PASSWORD_STRENGTH:
        return True, ""

    if len(password) < 8:
        return False, "Password must be at least 8 characters"

    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)

    if not (has_upper and has_lower and has_digit):
        return False, "Password must contain uppercase, lowercase, and numbers"

    return True, ""
