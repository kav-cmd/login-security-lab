from datetime import datetime, timedelta
from app import db
from app.models import LoginAttempt, BlockedIP, User

def log_attempt(ip, username, success, blocked, attack_type=None):
    """Log every login attempt to database"""
    attempt = LoginAttempt(
        ip=ip,
        username=username,
        success=int(success),
        blocked=int(blocked),
        attack_type=attack_type,
        timestamp=datetime.utcnow()
    )
    db.session.add(attempt)
    db.session.commit()

def log_experiment_result(attack_type, defense_config, total_attempts, successful, blocked, duration_sec):
    """Save experiment results to metrics table"""
    from app.models import Metric
    metric = Metric(
        attack_type=attack_type,
        defense_config=defense_config,
        total_attempts=total_attempts,
        successful=successful,
        blocked=blocked,
        duration_sec=duration_sec
    )
    db.session.add(metric)
    db.session.commit()
