from app import db
from flask_login import UserMixin
from datetime import datetime
import hashlib
import bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    failed_attempts = db.Column(db.Integer, default=0)
    locked_until = db.Column(db.DateTime, nullable=True)
    mfa_secret = db.Column(db.String(32), nullable=True)

    def check_password(self, password):
        # Intentionally weak MD5 for baseline vulnerability
        md5_hash = hashlib.md5(password.encode()).hexdigest()
        return self.password_hash == md5_hash

    def check_password_bcrypt(self, password):
        # Stronger bcrypt option
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())

class LoginAttempt(db.Model):
    __tablename__ = 'login_attempts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ip = db.Column(db.String(45))
    username = db.Column(db.String(80))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    success = db.Column(db.Integer, default=0)
    blocked = db.Column(db.Integer, default=0)
    attack_type = db.Column(db.String(50), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'ip': self.ip,
            'username': self.username,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'success': bool(self.success),
            'blocked': bool(self.blocked),
            'attack_type': self.attack_type
        }

class Metric(db.Model):
    __tablename__ = 'metrics'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attack_type = db.Column(db.String(50))
    defense_config = db.Column(db.String(200))
    total_attempts = db.Column(db.Integer)
    successful = db.Column(db.Integer)
    blocked = db.Column(db.Integer)
    duration_sec = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class BlockedIP(db.Model):
    __tablename__ = 'blocked_ips'

    ip = db.Column(db.String(45), primary_key=True)
    blocked_at = db.Column(db.DateTime, default=datetime.utcnow)
    reason = db.Column(db.String(200))

def populate_dummy_users():
    """Create 20 synthetic dummy user accounts"""
    import hashlib

    dummy_users = [
        ('admin', 'admin123'),
        ('user001', 'password123'),
        ('john_doe', 'qwerty'),
        ('alice_smith', 'letmein'),
        ('bob_jones', '123456'),
        ('charlie_brown', 'password'),
        ('david_wilson', 'welcome'),
        ('emma_davis', 'abc123'),
        ('frank_miller', 'monkey'),
        ('grace_taylor', '12345678'),
        ('henry_anderson', 'dragon'),
        ('isabel_thomas', 'iloveyou'),
        ('jack_jackson', 'trustno1'),
        ('kate_white', 'sunshine'),
        ('leo_harris', 'princess'),
        ('mary_martin', 'football'),
        ('nathan_lee', 'shadow'),
        ('olivia_walker', 'master'),
        ('peter_hall', 'hello'),
        ('quinn_allen', 'freedom')
    ]

    for username, password in dummy_users:
        # Using MD5 (intentionally weak)
        password_hash = hashlib.md5(password.encode()).hexdigest()
        user = User(username=username, password_hash=password_hash)
        db.session.add(user)

    db.session.commit()
    print(f"Created {len(dummy_users)} dummy users")
