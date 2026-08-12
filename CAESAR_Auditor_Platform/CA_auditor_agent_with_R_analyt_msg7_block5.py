#!/bin/bash
# deploy_setup.sh - ENHANCED DEPLOYMENT

echo "========================================="
echo "CDLS AUDITOR AGENT - DEPLOYMENT SCRIPT"
echo "========================================="

# 1. Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is required but not installed."
    exit 1
fi

echo "✓ Python 3 detected"

# 2. Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt --quiet

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed"
else
    echo "ERROR: Failed to install dependencies"
    exit 1
fi

# 3. Verify .env file exists
if [ ! -f .env ]; then
    echo "ERROR: .env file not found. Please create it from .env.example"
    exit 1
fi

echo "✓ Configuration file found"

# 4. Secure permissions
chmod 600 .env
echo "✓ Secured .env permissions"

# 5. Create logs directory
mkdir -p logs
echo "✓ Logs directory created"

# 6. Test database connection
echo "Testing database connection..."
python3 -c "
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS'),
        connect_timeout=5
    )
    conn.close()
    print('✓ Database connection successful')
except Exception as e:
    print(f'✗ Database connection failed: {e}')
    exit(1)
"

if [ $? -ne 0 ]; then
    exit 1
fi

# 7. Schedule cron job
SCRIPT_PATH=$(pwd)/auditor_logic.py

# Remove existing cron job if present
crontab -l 2>/dev/null | grep -v "$SCRIPT_PATH" | crontab -

# Add new cron job (Every Friday at 4 PM)
(crontab -l 2>/dev/null; echo "0 16 * * 5 /usr/bin/python3 $SCRIPT_PATH >> $(pwd)/logs/cron.log 2>&1") | crontab -

echo "✓ Cron job scheduled (Fridays at 4 PM)"

# 8. Optional: Start dashboard
read -p "Start real-time dashboard? (y/n): " START_DASHBOARD

if [ "$START_DASHBOARD" = "y" ]; then
    echo "Starting Flask dashboard on port 5000..."
    cd dashboard
    nohup python3 app.py > ../logs/dashboard.log 2>&1 &
    echo "✓ Dashboard running at http://localhost:5000"
    echo "  (Check logs/dashboard.log for details)"
fi

# 9. Test run (optional)
read -p "Run test audit now? (y/n): " RUN_TEST

if [ "$RUN_TEST" = "y" ]; then
    echo ""
    echo "========================================="
    echo "EXECUTING TEST AUDIT RUN"
    echo "========================================="
    python3 auditor_logic.py
fi

echo ""
echo "========================================="
echo "DEPLOYMENT COMPLETE"
echo "========================================="
echo ""
echo "Next Steps:"
echo "1. Check your email for the first audit report"
echo "2. Access dashboard at http://localhost:5000 (if started)"
echo "3. Scheduled reports will run every Friday at 4 PM"
echo ""
echo "For support: engineering@californiadealerlogistics.com"