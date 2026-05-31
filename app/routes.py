from flask import render_template, request, redirect, url_for, jsonify, session, current_app
from flask_login import login_user, logout_user, login_required, current_user
from app import db, login_manager, limiter
from app.models import User, LoginAttempt, Metric
from app.logger import log_attempt
from app.defenses import (
    is_ip_blocked, is_account_locked, handle_failed_attempt,
    reset_failed_attempts, check_anomaly, trigger_alert,
    needs_captcha, generate_captcha, verify_captcha, check_pwned_password
)
from app.runtime_config import get_config, set_config, get_all_config, persist_to_file
import config

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def get_client_ip():
    """Get client IP, respecting X-Forwarded-For for distributed attack simulation"""
    return request.headers.get('X-Forwarded-For', request.remote_addr)

@current_app.route('/')
def index():
    return redirect(url_for('login'))

@current_app.route('/login', methods=['GET', 'POST'])
@limiter.limit(
    f"{config.RATE_LIMIT_REQUESTS} per minute",
    exempt_when=lambda: not get_config('RATE_LIMIT_ENABLED')
)
def login():
    if request.method == 'GET':
        return render_template('login.html')

    # Get credentials
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    ip = get_client_ip()

    # Defense Layer 1: IP Blocking
    if is_ip_blocked(ip):
        log_attempt(ip, username, success=False, blocked=True)
        return jsonify({'error': 'Your IP has been blocked'}), 403

    # Defense Layer 2: Anomaly Detection
    if check_anomaly(ip):
        trigger_alert(ip, config.ANOMALY_THRESHOLD)
        log_attempt(ip, username, success=False, blocked=True)
        return jsonify({'error': 'Suspicious activity detected'}), 429

    # Defense Layer 3: Account Lockout
    if is_account_locked(username):
        log_attempt(ip, username, success=False, blocked=True)
        return jsonify({'error': 'Account temporarily locked'}), 429

    # Defense Layer 4: CAPTCHA
    if needs_captcha(username):
        captcha_answer = request.form.get('captcha_answer', '')
        correct_answer = session.get('captcha_answer', '')

        if not captcha_answer or not verify_captcha(captcha_answer, correct_answer):
            # Generate new CAPTCHA
            captcha = generate_captcha()
            session['captcha_answer'] = captcha['answer']
            return render_template('captcha.html',
                                 captcha_question=captcha['question'],
                                 username=username)

    # Defense Layer 5: Pwned password check
    if get_config('PWNED_CHECK_ENABLED'):
        hibp_result = check_pwned_password(password)
        if hibp_result['is_pwned']:
            log_attempt(ip, username, success=False, blocked=True)
            breach_count = hibp_result.get('breach_count')
            if breach_count:
                error_msg = f'This password was found in {breach_count} known breaches. Please use a different password.'
            else:
                error_msg = 'This password has been compromised. Please use a different password.'
            return jsonify({'error': error_msg}), 403

    # Credential verification (intentionally vulnerable - MD5)
    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        # Successful login
        log_attempt(ip, username, success=True, blocked=False)
        reset_failed_attempts(username)
        login_user(user)

        # Defense Layer 6: MFA (if enabled)
        if get_config('MFA_ENABLED'):
            session['pending_mfa_user'] = user.id
            return redirect(url_for('mfa_verify'))

        return redirect(url_for('dashboard'))
    else:
        # Failed login
        log_attempt(ip, username, success=False, blocked=False)
        handle_failed_attempt(ip, username)
        return jsonify({'error': 'Invalid credentials'}), 401

@current_app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration endpoint"""
    if request.method == 'GET':
        return render_template('register.html')

    # Get form data
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    confirm_password = request.form.get('confirm_password', '')

    # Validation
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400

    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400

    # Defense: Password Strength Check
    if get_config('PASSWORD_STRENGTH'):
        from app.defenses import check_password_strength
        is_strong, strength_error = check_password_strength(password)
        if not is_strong:
            return jsonify({'error': strength_error}), 400

    # Defense: Pwned Password Check
    if get_config('PWNED_CHECK_ENABLED'):
        hibp_result = check_pwned_password(password)
        if hibp_result['is_pwned']:
            breach_count = hibp_result.get('breach_count')
            if breach_count:
                error_msg = f'This password was found in {breach_count:,} known breaches. Please choose a different password.'
            else:
                error_msg = 'This password has been compromised. Please choose a different password.'
            return jsonify({'error': error_msg}), 400

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'error': 'Username already exists'}), 400

    # Create new user with MD5 hash (intentionally weak for testbed)
    import hashlib
    password_hash = hashlib.md5(password.encode()).hexdigest()
    new_user = User(username=username, password_hash=password_hash)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Account created successfully! Redirecting to login...'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to create account. Please try again.'}), 500

@current_app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=current_user.username)

@current_app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@current_app.route('/mfa_verify', methods=['GET', 'POST'])
def mfa_verify():
    """Simulated MFA verification"""
    if 'pending_mfa_user' not in session:
        return redirect(url_for('login'))

    if request.method == 'GET':
        # In real system, OTP would be sent via email/SMS
        # For testing, we print it to console
        import pyotp
        totp = pyotp.TOTP('base32secret3232')
        otp = totp.now()
        print(f"[MFA] Your OTP code is: {otp}")
        return render_template('mfa.html')

    # Verify OTP
    user_otp = request.form.get('otp', '')
    # Simplified verification for testing
    if len(user_otp) == 6 and user_otp.isdigit():
        user_id = session.pop('pending_mfa_user')
        user = User.query.get(user_id)
        login_user(user)
        return redirect(url_for('dashboard'))
    else:
        return jsonify({'error': 'Invalid OTP'}), 401

# API Endpoints for Dashboard

@current_app.route('/api/logs')
def api_logs():
    """Return recent login attempts as JSON"""
    limit = request.args.get('limit', 100, type=int)
    logs = LoginAttempt.query.order_by(LoginAttempt.timestamp.desc()).limit(limit).all()
    return jsonify([log.to_dict() for log in logs])

@current_app.route('/api/metrics')
def api_metrics():
    """Return aggregated metrics"""
    total = LoginAttempt.query.count()
    blocked = LoginAttempt.query.filter_by(blocked=1).count()
    success = LoginAttempt.query.filter_by(success=1).count()
    failed = total - success - blocked

    return jsonify({
        'total': total,
        'blocked': blocked,
        'success': success,
        'failed': failed
    })

@current_app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """Get or update defense configuration"""
    if request.method == 'GET':
        # Return current defense configuration from runtime state
        runtime_config = get_all_config()
        return jsonify({
            'rate_limit': runtime_config['RATE_LIMIT_ENABLED'],
            'account_lockout': runtime_config['ACCOUNT_LOCKOUT'],
            'ip_blocking': runtime_config['IP_BLOCKING'],
            'captcha': runtime_config['CAPTCHA_ENABLED'],
            'anomaly_detection': runtime_config['ANOMALY_DETECTION'],
            'mfa': runtime_config['MFA_ENABLED'],
            'pwned_check': runtime_config['PWNED_CHECK_ENABLED'],
            'password_strength': runtime_config['PASSWORD_STRENGTH']
        })

    elif request.method == 'POST':
        # Update a defense configuration
        data = request.get_json()

        if not data or 'defense_name' not in data or 'value' not in data:
            return jsonify({'success': False, 'error': 'Missing defense_name or value'}), 400

        defense_name = data['defense_name']
        value = data['value']

        # Validate defense name
        valid_defenses = {
            'RATE_LIMIT_ENABLED', 'ACCOUNT_LOCKOUT', 'IP_BLOCKING',
            'CAPTCHA_ENABLED', 'ANOMALY_DETECTION', 'MFA_ENABLED',
            'PWNED_CHECK_ENABLED', 'PASSWORD_STRENGTH'
        }

        if defense_name not in valid_defenses:
            return jsonify({'success': False, 'error': f'Invalid defense name: {defense_name}'}), 400

        # Validate value is boolean
        if not isinstance(value, bool):
            return jsonify({'success': False, 'error': 'Value must be a boolean'}), 400

        # Update runtime config
        if not set_config(defense_name, value):
            return jsonify({'success': False, 'error': 'Failed to update runtime config'}), 500

        # Persist to config.py file
        persist_to_file(defense_name, value)

        return jsonify({
            'success': True,
            'defense_name': defense_name,
            'new_value': value
        })

@current_app.route('/api/stats')
def api_stats():
    """Return detailed statistics for dashboard"""
    from datetime import datetime, timedelta
    from sqlalchemy import func

    # Last hour activity
    one_hour_ago = datetime.utcnow() - timedelta(hours=1)
    recent_attempts = LoginAttempt.query.filter(
        LoginAttempt.timestamp >= one_hour_ago
    ).all()

    # Group by IP
    ip_stats = db.session.query(
        LoginAttempt.ip,
        func.count(LoginAttempt.id).label('count')
    ).group_by(LoginAttempt.ip).all()

    return jsonify({
        'recent_attempts': len(recent_attempts),
        'unique_ips': len(ip_stats),
        'top_ips': [{'ip': ip, 'count': count} for ip, count in ip_stats[:10]]
    })

# Register routes with app
def init_routes(app):
    """Initialize routes with the Flask app"""
    pass  # Routes are registered via decorators
