"""
Real-Time Security Monitoring Dashboard
Displays live login attempts, attack metrics, and defense status
Feature 3: Added defense toggle controls with live API updates
"""
import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
from datetime import datetime, timedelta
import time
import sys
import os
import sqlite3
import requests

# Work around Plotly template issues that can cause recursion errors on some
# Plotly/Streamlit combinations by forcing a known-safe built-in template.
SAFE_PLOTLY_TEMPLATE = "plotly_white"
try:
    pio.templates.default = SAFE_PLOTLY_TEMPLATE
    px.defaults.template = SAFE_PLOTLY_TEMPLATE
except Exception:
    pass

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from db_utils import init_database

DB_PATH = config.DATABASE_PATH

st.set_page_config(
    page_title="Security Testbed Monitor",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_db_connection():
    """Create database connection"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def ensure_database_initialized():
    """Create the database schema if it does not exist yet."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='login_attempts'")
        if cursor.fetchone() is None:
            init_database()
    finally:
        conn.close()

def load_login_attempts(limit=500):
    """Load recent login attempts"""
    conn = get_db_connection()
    try:
        query = f"""
            SELECT * FROM login_attempts
            ORDER BY timestamp DESC
            LIMIT {limit}
        """
        df = pd.read_sql(query, conn)
    except (sqlite3.OperationalError, pd.errors.DatabaseError):
        df = pd.DataFrame()
    finally:
        conn.close()

    if not df.empty and 'timestamp' in df.columns:
        # Stored timestamps are UTC; parse as UTC and convert to local timezone for display
        df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
        local_tz = datetime.now().astimezone().tzinfo
        try:
            df['timestamp'] = df['timestamp'].dt.tz_convert(local_tz)
        except Exception:
            # If conversion fails, fall back to naive UTC timestamps
            df['timestamp'] = df['timestamp'].dt.tz_localize(None)

    return df

def load_metrics():
    """Load aggregated metrics"""
    conn = get_db_connection()

    try:
        total = pd.read_sql("SELECT COUNT(*) as count FROM login_attempts", conn).iloc[0]['count']
        blocked = pd.read_sql("SELECT COUNT(*) as count FROM login_attempts WHERE blocked = 1", conn).iloc[0]['count']
        success = pd.read_sql("SELECT COUNT(*) as count FROM login_attempts WHERE success = 1", conn).iloc[0]['count']
        failed = total - blocked - success
    except (sqlite3.OperationalError, pd.errors.DatabaseError):
        total = blocked = success = failed = 0
    finally:
        conn.close()

    return {
        'total': total,
        'blocked': blocked,
        'success': success,
        'failed': failed
    }

def load_defense_config():
    """Load current defense configuration from API"""
    try:
        response = requests.get('http://localhost:5000/api/config', timeout=2)
        if response.ok:
            api_config = response.json()
            return {
                'Rate Limiting': api_config.get('rate_limit', False),
                'Account Lockout': api_config.get('account_lockout', False),
                'IP Blocking': api_config.get('ip_blocking', False),
                'CAPTCHA': api_config.get('captcha', False),
                'Anomaly Detection': api_config.get('anomaly_detection', False),
                'MFA': api_config.get('mfa', False),
                'Pwned Check': api_config.get('pwned_check', False),
                'Password Strength': api_config.get('password_strength', False)
            }
    except Exception as e:
        print(f"Error loading config from API: {e}")

    # Fallback to config.py if API fails
    return {
        'Rate Limiting': config.RATE_LIMIT_ENABLED,
        'Account Lockout': config.ACCOUNT_LOCKOUT,
        'IP Blocking': config.IP_BLOCKING,
        'CAPTCHA': config.CAPTCHA_ENABLED,
        'Anomaly Detection': config.ANOMALY_DETECTION,
        'MFA': config.MFA_ENABLED,
        'Pwned Check': config.PWNED_CHECK_ENABLED,
        'Password Strength': config.PASSWORD_STRENGTH
    }

def main():
    ensure_database_initialized()

    # Header
    st.title("🔐 Login Security Testbed - Live Monitor")
    st.markdown("Real-time monitoring of authentication attacks and defenses")
    st.markdown("---")

    # Sidebar - Defense Configuration
    with st.sidebar:
        st.header("⚙️ Defense Configuration")
        st.markdown("Toggle defenses in real-time:")

        defenses = load_defense_config()

        # Defense name mapping
        defense_mapping = {
            'Rate Limiting': 'RATE_LIMIT_ENABLED',
            'Account Lockout': 'ACCOUNT_LOCKOUT',
            'IP Blocking': 'IP_BLOCKING',
            'CAPTCHA': 'CAPTCHA_ENABLED',
            'Anomaly Detection': 'ANOMALY_DETECTION',
            'MFA': 'MFA_ENABLED',
            'Pwned Check': 'PWNED_CHECK_ENABLED',
            'Password Strength': 'PASSWORD_STRENGTH'
        }

        # Create toggles for each defense
        for display_name, config_key in defense_mapping.items():
            current_value = defenses.get(display_name, False)
            new_value = st.toggle(display_name, value=current_value, key=config_key)

            # If value changed, update via API
            if new_value != current_value:
                try:
                    response = requests.post(
                        'http://localhost:5000/api/config',
                        json={'defense_name': config_key, 'value': new_value},
                        timeout=2
                    )
                    if response.ok:
                        # Don't show success message to avoid blur
                        # Just rerun to refresh the state
                        st.rerun()
                    else:
                        st.error(f"Failed to update {display_name}")
                except Exception as e:
                    st.error(f"Error: {str(e)}")

        st.markdown("---")
        st.markdown("### 📊 Thresholds")
        st.markdown(f"Rate Limit: {config.RATE_LIMIT_REQUESTS}/min")
        st.markdown(f"Lockout: {config.LOCKOUT_THRESHOLD} attempts")
        st.markdown(f"IP Block: {config.IP_BLOCK_THRESHOLD} attempts")
        st.markdown(f"CAPTCHA: {config.CAPTCHA_TRIGGER} attempts")
        st.markdown(f"Anomaly: {config.ANOMALY_THRESHOLD}/60s")

    # Auto-refresh toggle
    auto_refresh = st.checkbox("🔄 Auto-refresh (10s)", value=True)

    # Main metrics
    metrics = load_metrics()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Attempts", metrics['total'])
    with col2:
        st.metric("Blocked", metrics['blocked'],
                 delta=f"{(metrics['blocked']/metrics['total']*100) if metrics['total'] > 0 else 0:.1f}%")
    with col3:
        st.metric("Successful", metrics['success'],
                 delta=f"{(metrics['success']/metrics['total']*100) if metrics['total'] > 0 else 0:.1f}%")
    with col4:
        st.metric("Failed", metrics['failed'])

    st.markdown("---")

    # Load data
    df = load_login_attempts(500)

    if df.empty:
        st.warning("⚠️ No login attempts recorded yet. Start an attack simulation to see data.")
        if auto_refresh:
            time.sleep(2)
            st.rerun()
        return

    # Two column layout for charts
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Attempts Per Minute")

        # Group by minute
        df_time = df.copy()
        df_time['minute'] = df_time['timestamp'].dt.floor('min')
        df_grouped = df_time.groupby('minute').size().reset_index(name='count')

        fig_time = px.bar(
            df_grouped.tail(20),
            x='minute',
            y='count',
            labels={'minute': 'Time', 'count': 'Attempts'},
            color_discrete_sequence=['#667eea'],
            template=SAFE_PLOTLY_TEMPLATE
        )
        fig_time.update_layout(height=300, template=SAFE_PLOTLY_TEMPLATE)
        st.plotly_chart(fig_time, use_container_width=True)

    with col2:
        st.subheader("🥧 Attempt Status Distribution")

        status_counts = {
            'Blocked': metrics['blocked'],
            'Successful': metrics['success'],
            'Failed': metrics['failed']
        }

        fig_pie = go.Figure(data=[go.Pie(
            labels=list(status_counts.keys()),
            values=list(status_counts.values()),
            marker=dict(colors=['#e74c3c', '#2ecc71', '#f39c12'])
        )])
        fig_pie.update_layout(height=300, template=SAFE_PLOTLY_TEMPLATE)
        st.plotly_chart(fig_pie, use_container_width=True)

    # IP Activity Heatmap
    st.subheader("🌐 Top IP Addresses")

    ip_counts = df['ip'].value_counts().head(10).reset_index()
    ip_counts.columns = ['IP Address', 'Attempts']

    fig_ip = px.bar(
        ip_counts,
        x='IP Address',
        y='Attempts',
        color='Attempts',
        color_continuous_scale='Reds',
        labels={'Attempts': 'Number of Attempts'},
        template=SAFE_PLOTLY_TEMPLATE
    )
    fig_ip.update_layout(height=300, template=SAFE_PLOTLY_TEMPLATE)
    st.plotly_chart(fig_ip, use_container_width=True)

    # Recent attempts table
    st.subheader("📋 Recent Login Attempts")

    # Format the dataframe for display
    display_df = df[['timestamp', 'ip', 'username', 'success', 'blocked']].head(20).copy()
    # Format timestamp to readable local string
    try:
        display_df['timestamp'] = display_df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S %Z')
    except Exception:
        display_df['timestamp'] = display_df['timestamp'].astype(str)

    display_df['success'] = display_df['success'].map({1: '✅ Yes', 0: '❌ No'})
    display_df['blocked'] = display_df['blocked'].map({1: '🚫 Yes', 0: '✓ No'})
    display_df.columns = ['Timestamp', 'IP Address', 'Username', 'Success', 'Blocked']

    st.dataframe(display_df, use_container_width=True, height=400)

    # Attack type breakdown
    if 'attack_type' in df.columns and df['attack_type'].notna().any():
        st.subheader("🎯 Attack Type Breakdown")

        attack_counts = df[df['attack_type'].notna()]['attack_type'].value_counts()

        col1, col2 = st.columns([2, 1])

        with col1:
            fig_attack = px.bar(
                x=attack_counts.index,
                y=attack_counts.values,
                labels={'x': 'Attack Type', 'y': 'Count'},
                color_discrete_sequence=['#764ba2']
            )
            fig_attack.update_layout(height=300)
            st.plotly_chart(fig_attack, use_container_width=True)

        with col2:
            st.markdown("### Attack Statistics")
            for attack_type, count in attack_counts.items():
                st.markdown(f"**{attack_type}**: {count}")

    # Anomaly alerts
    if metrics['total'] > 0:
        # Use timezone-aware now() to match timestamp timezone in dataframe
        recent_time = datetime.now().astimezone() - timedelta(seconds=60)
        recent_df = df[df['timestamp'] > recent_time]

        if len(recent_df) >= config.ANOMALY_THRESHOLD:
            st.error(f"🚨 ANOMALY ALERT: {len(recent_df)} attempts in the last 60 seconds!")

    # Footer
    st.markdown("---")
    st.markdown(f"**Last updated:** {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S %Z')}")

    # Auto-refresh
    if auto_refresh:
        time.sleep(10)
        st.rerun()

if __name__ == "__main__":
    main()
