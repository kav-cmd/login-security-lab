"""
Defense Configuration System
All defenses are OFF by default - toggle to True to enable
"""

import os

# Defense toggles
RATE_LIMIT_ENABLED = False
ACCOUNT_LOCKOUT = False
IP_BLOCKING = False
CAPTCHA_ENABLED = False
ANOMALY_DETECTION = False
MFA_ENABLED = True
PWNED_CHECK_ENABLED = True
PASSWORD_STRENGTH = True

# Thresholds and limits
RATE_LIMIT_REQUESTS = 8       # requests per minute per IP
LOCKOUT_THRESHOLD = 5          # failed attempts before lockout
LOCKOUT_DURATION_MIN = 15      # lockout duration in minutes
IP_BLOCK_THRESHOLD = 50        # failed attempts before IP ban
ANOMALY_THRESHOLD = 20         # attempts per 60s to trigger alert
CAPTCHA_TRIGGER = 3            # failed attempts before CAPTCHA

# Database
DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.db')

# HaveIBeenPwned API
HIBP_API_TIMEOUT = 2  # seconds - API call timeout
HIBP_API_URL = 'https://api.pwnedpasswords.com/range'  # k-anonymity API endpoint

# Flask settings
SECRET_KEY = 'dev-secret-key-change-in-production'
DEBUG = True


