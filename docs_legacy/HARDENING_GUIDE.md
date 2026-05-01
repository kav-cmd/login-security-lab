# Security Hardening Guide

> **Practical recommendations for securing authentication systems in production**

## 🎯 Purpose

This guide provides actionable security recommendations based on lessons learned from this testbed. These practices should be implemented in all production authentication systems.

---

## 🔐 Top 5 Critical Recommendations

### 1. Use Strong Password Hashing

**Problem:** Weak hashing algorithms (MD5, SHA1) can be cracked in seconds.

**Solution:**
```python
import bcrypt

# Hashing a password
password = "user_password"
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))

# Verifying a password
if bcrypt.checkpw(password.encode(), hashed):
    print("Password correct")
```

**Best Practices:**
- Use bcrypt, Argon2, or PBKDF2
- Set high work factors (bcrypt rounds=12+, Argon2 memory=64MB+)
- Never implement your own crypto
- Unique salt per password (handled automatically by bcrypt)

**Why it matters:** A database breach shouldn't expose passwords. Strong hashing makes cracking computationally infeasible.

---

### 2. Implement Multi-Layered Rate Limiting

**Problem:** Unlimited login attempts enable brute-force attacks.

**Solution:**
```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # Login logic
    pass
```

**Layered Approach:**
1. **IP-based rate limiting** - 10 attempts per minute per IP
2. **Account-based rate limiting** - 5 attempts per hour per account
3. **Global rate limiting** - Protect against distributed attacks
4. **Progressive delays** - Exponential backoff after failures

**Why it matters:** Makes automated attacks impractical by drastically reducing attempt rate.

---

### 3. Mandatory Multi-Factor Authentication

**Problem:** Passwords alone are insufficient. Phishing and breaches are common.

**Solution:**
```python
import pyotp

# Generate secret for user (store in database)
secret = pyotp.random_base32()

# Generate QR code for user to scan
totp = pyotp.TOTP(secret)
qr_uri = totp.provisioning_uri(
    name=user.email,
    issuer_name="YourApp"
)

# Verify OTP during login
if totp.verify(user_provided_otp):
    # Grant access
    pass
```

**Implementation Strategy:**
- Make MFA mandatory for admin accounts
- Offer multiple options: TOTP apps, SMS, email, hardware keys
- Provide backup codes for account recovery
- Support FIDO2/WebAuthn for passwordless authentication

**Why it matters:** Even if password is compromised, attacker cannot access account without second factor.

---

### 4. Comprehensive Security Monitoring

**Problem:** Attacks go undetected without proper logging and alerting.

**Solution:**
```python
import logging
from datetime import datetime

def log_security_event(event_type, user, ip, details):
    logger.info({
        'timestamp': datetime.utcnow().isoformat(),
        'event': event_type,
        'user': user,
        'ip': ip,
        'user_agent': request.headers.get('User-Agent'),
        'details': details
    })

# Log all authentication events
log_security_event('login_failed', username, ip, {
    'reason': 'invalid_password',
    'attempt_count': user.failed_attempts
})
```

**What to Log:**
- All login attempts (success and failure)
- Account lockouts and unlocks
- Password changes and resets
- MFA enrollment and verification
- Suspicious patterns (velocity, geolocation changes)
- Administrative actions

**Alerting Rules:**
- 10+ failed attempts in 5 minutes → Alert
- Login from new country → Notify user
- Multiple accounts from same IP → Investigate
- Successful login after many failures → Verify

**Why it matters:** Early detection enables rapid response before significant damage occurs.

---

### 5. Secure Session Management

**Problem:** Weak session handling enables session hijacking and fixation attacks.

**Solution:**
```python
from flask import Flask
from datetime import timedelta

app = Flask(__name__)

# Secure session configuration
app.config.update(
    SECRET_KEY='generate-strong-random-key-here',
    SESSION_COOKIE_SECURE=True,      # HTTPS only
    SESSION_COOKIE_HTTPONLY=True,    # No JavaScript access
    SESSION_COOKIE_SAMESITE='Lax',   # CSRF protection
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=30),
    SESSION_REFRESH_EACH_REQUEST=True
)

# Regenerate session ID on login
from flask import session
@app.route('/login', methods=['POST'])
def login():
    # ... verify credentials ...
    session.clear()  # Clear old session
    session.regenerate()  # New session ID
    session['user_id'] = user.id
    session.permanent = True
```

**Best Practices:**
- Use cryptographically random session IDs
- Regenerate session ID on privilege change
- Implement absolute and idle timeouts
- Invalidate sessions on logout
- Store sessions server-side, not in cookies
- Implement concurrent session limits

**Why it matters:** Prevents session hijacking, fixation, and unauthorized access.

---

## 🛡️ Additional Security Controls

### Account Lockout Policy

```python
def handle_failed_login(user):
    user.failed_attempts += 1
    
    if user.failed_attempts >= 5:
        user.locked_until = datetime.utcnow() + timedelta(minutes=15)
        send_email_alert(user.email, "Account locked due to failed login attempts")
        
    db.session.commit()
```

**Configuration:**
- Lock after 3-5 failed attempts
- 15-30 minute lockout duration
- Email notification to account owner
- Admin override capability
- Automatic unlock after timeout

---

### Password Policy

```python
import re

def validate_password(password):
    if len(password) < 12:
        return False, "Password must be at least 12 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain number"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain special character"
    
    # Check against breach database
    if check_pwned_password(password):
        return False, "Password found in data breach database"
    
    return True, "Password is strong"
```

**Requirements:**
- Minimum 12 characters (16+ recommended)
- Mix of uppercase, lowercase, numbers, symbols
- Not in breach databases (HaveIBeenPwned API)
- Not similar to username or email
- Password history (prevent reuse of last 5)

---

### CAPTCHA Implementation

```python
from flask import session
import random

def generate_captcha():
    a = random.randint(1, 10)
    b = random.randint(1, 10)
    session['captcha_answer'] = str(a + b)
    return f"What is {a} + {b}?"

@app.route('/login', methods=['POST'])
def login():
    if user.failed_attempts >= 3:
        if not verify_captcha(request.form.get('captcha')):
            return jsonify({'error': 'Invalid CAPTCHA'}), 400
```

**Better Alternative - reCAPTCHA v3:**
```python
import requests

def verify_recaptcha(token):
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': RECAPTCHA_SECRET_KEY,
            'response': token
        }
    )
    result = response.json()
    return result.get('success') and result.get('score', 0) > 0.5
```

---

### IP Reputation & Geolocation

```python
def check_ip_reputation(ip):
    # Check against known malicious IP databases
    # Use services like AbuseIPDB, IPQualityScore
    
    response = requests.get(
        f'https://api.abuseipdb.com/api/v2/check',
        headers={'Key': API_KEY},
        params={'ipAddress': ip}
    )
    
    data = response.json()
    abuse_score = data.get('data', {}).get('abuseConfidenceScore', 0)
    
    return abuse_score < 50  # Block if score > 50

def check_geolocation_anomaly(user, ip):
    current_country = get_country_from_ip(ip)
    last_country = user.last_login_country
    
    if current_country != last_country:
        send_email_alert(user.email, 
            f"Login from new location: {current_country}")
        require_additional_verification()
```

---

## 🔍 Security Testing Checklist

### Before Deployment

- [ ] All passwords hashed with bcrypt/Argon2
- [ ] Rate limiting enabled and tested
- [ ] MFA available and encouraged
- [ ] Session security flags set correctly
- [ ] HTTPS enforced (no HTTP)
- [ ] Security headers configured (CSP, HSTS, X-Frame-Options)
- [ ] Input validation on all fields
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (output encoding)
- [ ] CSRF protection enabled
- [ ] Comprehensive logging implemented
- [ ] Monitoring and alerting configured
- [ ] Incident response plan documented
- [ ] Regular security audits scheduled

### Ongoing Maintenance

- [ ] Monitor failed login attempts daily
- [ ] Review security logs weekly
- [ ] Update dependencies monthly
- [ ] Conduct penetration testing quarterly
- [ ] Review and update security policies annually
- [ ] Train team on security best practices
- [ ] Maintain breach response procedures

---

## 📊 Metrics to Track

### Security KPIs

1. **Failed Login Rate** - % of failed vs. total attempts
2. **Account Lockout Rate** - Accounts locked per day
3. **MFA Adoption Rate** - % of users with MFA enabled
4. **Password Strength Score** - Average entropy of passwords
5. **Time to Detect** - Time from attack start to detection
6. **Time to Respond** - Time from detection to mitigation
7. **False Positive Rate** - Legitimate users blocked

### Alerting Thresholds

- Failed login rate > 10% → Investigate
- Account lockouts > 50/day → Review patterns
- MFA adoption < 80% → Increase awareness
- Detection time > 5 minutes → Improve monitoring
- False positive rate > 1% → Tune defenses

---

## 🚨 Incident Response

### When Attack Detected

1. **Immediate Actions**
   - Enable all defense mechanisms
   - Block attacking IPs
   - Notify security team
   - Preserve logs for forensics

2. **Investigation**
   - Identify attack vector
   - Determine scope and impact
   - Check for successful breaches
   - Review affected accounts

3. **Remediation**
   - Force password reset for affected accounts
   - Invalidate all sessions
   - Patch vulnerabilities
   - Update defense rules

4. **Post-Incident**
   - Document lessons learned
   - Update security procedures
   - Improve detection capabilities
   - Communicate with stakeholders

---

## 🎓 Key Takeaways

1. **Security is a Process** - Not a one-time implementation
2. **Defense in Depth** - Multiple layers of protection
3. **Assume Breach** - Plan for when (not if) attacks succeed
4. **Monitor Everything** - You can't protect what you can't see
5. **User Education** - Security is everyone's responsibility
6. **Regular Updates** - Threats evolve, defenses must too
7. **Test Regularly** - Verify defenses work as expected

---

## 📚 Additional Resources

- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)
- [HaveIBeenPwned API](https://haveibeenpwned.com/API/v3)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

**Remember: Security is not about being perfect, it's about making attacks so difficult and expensive that attackers move on to easier targets.**
