"""
Feature 2: Runtime Configuration System
Shared state for defense configuration that can be updated without restarting the app
"""
import config
import threading

# Thread-safe shared state for runtime configuration
_config_lock = threading.Lock()
_runtime_config = {
    'RATE_LIMIT_ENABLED': config.RATE_LIMIT_ENABLED,
    'ACCOUNT_LOCKOUT': config.ACCOUNT_LOCKOUT,
    'IP_BLOCKING': config.IP_BLOCKING,
    'CAPTCHA_ENABLED': config.CAPTCHA_ENABLED,
    'ANOMALY_DETECTION': config.ANOMALY_DETECTION,
    'MFA_ENABLED': config.MFA_ENABLED,
    'PWNED_CHECK_ENABLED': config.PWNED_CHECK_ENABLED,
    'PASSWORD_STRENGTH': config.PASSWORD_STRENGTH,
}

def get_config(key):
    """Get a configuration value from runtime state"""
    with _config_lock:
        return _runtime_config.get(key)

def set_config(key, value):
    """Set a configuration value in runtime state"""
    with _config_lock:
        if key in _runtime_config:
            _runtime_config[key] = value
            return True
        return False

def get_all_config():
    """Get all configuration values"""
    with _config_lock:
        return _runtime_config.copy()

def persist_to_file(key, value):
    """
    Persist a configuration change to config.py file
    Updates only the specific line for the given key
    """
    import os
    config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'config.py')

    try:
        with open(config_path, 'r') as f:
            lines = f.readlines()

        # Find and update the line
        updated = False
        for i, line in enumerate(lines):
            if line.strip().startswith(f'{key} ='):
                lines[i] = f'{key} = {value}\n'
                updated = True
                break

        if updated:
            with open(config_path, 'w') as f:
                f.writelines(lines)
            return True
        return False
    except Exception as e:
        print(f"[CONFIG] Failed to persist {key} to file: {e}")
        return False
