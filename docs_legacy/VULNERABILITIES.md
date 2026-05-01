# Intentional Vulnerabilities Documentation

> **This document catalogs security weaknesses intentionally built into the testbed for educational purposes.**

## ⚠️ Purpose

This login system contains deliberate vulnerabilities to demonstrate common authentication security flaws. These weaknesses are **NEVER** acceptable in production systems.

---

## 🔓 Vulnerability Catalog

### 1. Weak Password Hashing (CRITICAL)

**Location:** `app/models.py` - `User.check_password()`

**Vulnerability:**
- Passwords are hashed using MD5 algorithm
- MD5 is cryptographically broken and unsuitable for password storage
- No salt is used, making rainbow table attacks trivial
- Hash computation is extremely fast, enabling rapid brute-force attempts

**Code:**
```python
def check_password(self, password):
    md5_hash = hashlib.md5(password.encode()).hexdigest()
    return self.password_hash == md5_hash
```

**Impact:**
- Attackers can crack passwords at millions of attempts per second
- Pre-computed rainbow tables can instantly reverse common passwords
- Database breach exposes all passwords immediately

**Real-World Fix:**
- Use bcrypt, Argon2, or PBKDF2 with high iteration counts
- Always use unique salts per password
- Example: `bcrypt.hashpw(password.encode(), bcrypt.gensalt())`

---

### 2. No Rate Limiting (By Default)

**Location:** `app/routes.py` - `@app.route('/login')`

**Vulnerability:**
- Rate limiting is disabled by default (`RATE_LIMIT_ENABLED = False`)
- Attackers can send unlimited login attempts
- No throttling or delay between failed attempts

**Impact:**
- Brute-force attacks can try thousands of passwords per minute
- No protection against automated attack tools
- Server resources can be exhausted

**Real-World Fix:**
- Enable rate limiting by default
- Implement progressive delays after failed attempts
- Use CAPTCHA after N failed attempts
- Consider IP-based and account-based rate limits

---

### 3. No Account Lockout (By Default)

**Location:** `config.py` - `ACCOUNT_LOCKOUT = False`

**Vulnerability:**
- Accounts are never locked regardless of failed attempts
- Attackers can indefinitely attempt to guess passwords
- No temporary suspension mechanism

**Impact:**
- Single account can be targeted with unlimited attempts
- No deterrent for persistent attackers
- Legitimate users not notified of attack attempts

**Real-World Fix:**
- Lock accounts after 3-5 failed attempts
- Implement time-based lockout (15-30 minutes)
- Send email notification to account owner
- Provide secure account recovery mechanism

---

### 4. Generic Error Messages (Partial Mitigation)

**Location:** `app/routes.py` - Login error responses

**Current State:**
- Returns generic "Invalid credentials" message
- **However**, timing differences may still leak information
- Response time differs for valid vs. invalid usernames

**Vulnerability:**
- Timing attacks can enumerate valid usernames
- Database query time differs based on username existence
- Network timing analysis can reveal account validity

**Impact:**
- Attackers can build list of valid usernames
- Reduces attack surface from N×M to N (known usernames)
- Enables targeted attacks

**Real-World Fix:**
- Constant-time comparison for all authentication checks
- Add random delay to normalize response times
- Use same code path for valid and invalid usernames

---

### 5. No CAPTCHA (By Default)

**Location:** `config.py` - `CAPTCHA_ENABLED = False`

**Vulnerability:**
- No bot detection mechanism
- Automated scripts can run unimpeded
- No human verification challenge

**Impact:**
- Bots can perform attacks at machine speed
- No distinction between human and automated attempts
- Easy to script mass attacks

**Real-World Fix:**
- Implement CAPTCHA after 2-3 failed attempts
- Use reCAPTCHA v3 for invisible bot detection
- Consider alternative challenges (image selection, puzzles)

---

### 6. No Multi-Factor Authentication (By Default)

**Location:** `config.py` - `MFA_ENABLED = False`

**Vulnerability:**
- Single-factor authentication only (password)
- No second verification step
- Compromised password = full account access

**Impact:**
- Password breach leads to immediate account compromise
- No additional security layer
- Phishing attacks are highly effective

**Real-World Fix:**
- Implement TOTP-based 2FA (Google Authenticator, Authy)
- Support SMS or email OTP as backup
- Offer hardware security keys (FIDO2/WebAuthn)
- Make MFA mandatory for privileged accounts

---

### 7. No IP Blocking (By Default)

**Location:** `config.py` - `IP_BLOCKING = False`

**Vulnerability:**
- Malicious IPs are never blocked
- Same IP can attack indefinitely
- No persistent ban mechanism

**Impact:**
- Attackers can retry from same IP without consequence
- No cumulative penalty for repeated attacks
- Easy to automate attacks from single source

**Real-World Fix:**
- Block IPs after threshold of failed attempts
- Implement temporary and permanent bans
- Use IP reputation services
- Consider geolocation-based restrictions

---

### 8. Weak Session Management

**Location:** `app/__init__.py` - Flask session configuration

**Vulnerability:**
- Default Flask session settings
- Session cookies may not have all security flags
- No session timeout configuration visible

**Potential Issues:**
- Session fixation attacks possible
- XSS could steal session cookies
- Sessions may persist too long

**Real-World Fix:**
```python
app.config['SESSION_COOKIE_SECURE'] = True      # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True    # No JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = 1800 # 30 min timeout
```

---

### 9. No Breach Detection

**Location:** `config.py` - `PWNED_CHECK_ENABLED = False`

**Vulnerability:**
- Passwords not checked against known breaches
- Users can set commonly compromised passwords
- No integration with HaveIBeenPwned API

**Impact:**
- Users may unknowingly use leaked passwords
- Credential stuffing attacks more likely to succeed
- No proactive security warnings

**Real-World Fix:**
- Check passwords against HaveIBeenPwned on registration
- Warn users if their password appears in breaches
- Force password change for compromised credentials

---

### 10. Insufficient Logging

**Location:** `app/logger.py`

**Vulnerability:**
- Basic logging only (IP, username, timestamp)
- No user agent logging
- No geolocation tracking
- No anomaly scoring

**Impact:**
- Difficult to detect sophisticated attacks
- Limited forensic information
- No behavioral analysis possible

**Real-World Fix:**
- Log user agent, referrer, geolocation
- Implement anomaly scoring system
- Send alerts for suspicious patterns
- Integrate with SIEM systems

---

## 🎓 Educational Takeaways

### Key Lessons

1. **Defense in Depth**: No single defense is sufficient. Layer multiple mechanisms.
2. **Secure by Default**: Security features should be ON by default, not opt-in.
3. **Assume Breach**: Design systems assuming attackers will get through some defenses.
4. **Monitor Everything**: Comprehensive logging is essential for detection and response.
5. **Update Regularly**: Security is not a one-time implementation but ongoing process.

### Attack Surface Summary

| Attack Vector | Baseline Vulnerability | With All Defenses |
|---------------|------------------------|-------------------|
| Brute Force | ✅ Trivial | ❌ Blocked |
| Credential Stuffing | ✅ Effective | ⚠️ Partially Mitigated |
| Distributed Attack | ✅ Undetected | ⚠️ Slowed Down |
| Username Enumeration | ⚠️ Timing Leak | ⚠️ Still Possible |

---

## 🔒 Production Security Checklist

When building real authentication systems:

- [ ] Use bcrypt/Argon2 for password hashing
- [ ] Implement rate limiting (enabled by default)
- [ ] Add account lockout after failed attempts
- [ ] Require strong passwords (length, complexity)
- [ ] Check passwords against breach databases
- [ ] Implement CAPTCHA for bot detection
- [ ] Offer multi-factor authentication
- [ ] Use secure session management
- [ ] Log all authentication events
- [ ] Monitor for anomalies and attacks
- [ ] Implement IP reputation checking
- [ ] Use HTTPS exclusively
- [ ] Set secure cookie flags
- [ ] Implement CSRF protection
- [ ] Regular security audits and penetration testing

---

**Remember: These vulnerabilities exist for learning. Never deploy systems with these weaknesses to production.**
