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
    exempt_when=lambda: not config.RATE_LIMIT_ENABLED
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
    if config.PWNED_CHECK_ENABLED:
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
        if config.MFA_ENABLED:
            session['pending_mfa_user'] = user.id
            return redirect(url_for('mfa_verify'))

        return redirect(url_for('dashboard'))
    else:
        # Failed login
        log_attempt(ip, username, success=False, blocked=False)
        handle_failed_attempt(ip, username)
        return jsonify({'error': 'Invalid credentials'}), 401

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

@current_app.route('/api/config')
def api_config():
    """Return current defense configuration"""
    return jsonify({
        'rate_limit': config.RATE_LIMIT_ENABLED,
        'account_lockout': config.ACCOUNT_LOCKOUT,
        'ip_blocking': config.IP_BLOCKING,
        'captcha': config.CAPTCHA_ENABLED,
        'anomaly_detection': config.ANOMALY_DETECTION,
        'mfa': config.MFA_ENABLED,
        'pwned_check': config.PWNED_CHECK_ENABLED,
        'password_strength': config.PASSWORD_STRENGTH
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
