"""
Flask Application Entry Point
Run this file to start the login application
"""
import os

from app import create_app

app = create_app()

if __name__ == '__main__':
    print("=" * 60)
    print("  LOGIN SECURITY TESTBED")
    print("  Flask Application Starting...")
    print("=" * 60)
    print()
    print("  URL: http://localhost:5000")
    print("  Dashboard: http://localhost:8501 (run separately)")
    print()
    print("  Press CTRL+C to stop")
    print("=" * 60)
    print()

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True,
        use_reloader=not bool(os.environ.get('DISABLE_RELOADER'))
    )
