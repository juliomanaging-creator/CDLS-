# dashboard/app.py

from flask import Flask, render_template, jsonify
import psycopg2
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.getenv('DB_HOST'),
        dbname=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASS')
    )

@app.route('/')
def dashboard():
    """Main dashboard view"""
    return render_template('dashboard.html')

@app.route('/api/metrics/summary')
def metrics_summary():
    """Real-time summary metrics"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            COUNT(*) as total_today,
            COUNT(*) FILTER (WHERE integrity_score < 0.95) as flagged_today,
            AVG(integrity_score) as avg_integrity,
            COUNT(*) FILTER (WHERE reconciliation_status = 'exception') as critical_today
        FROM transaction_reconciliation
        WHERE created_at >= CURRENT_DATE
    """)
    
    data = cur.fetchone()
    
    cur.close()
    conn.close()
    
    return jsonify({
        'total_today': data[0],
        'flagged_today': data[1],
        'avg_integrity': float(data[2]) if data[2] else 0,
        'critical_today': data[3],
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/exceptions/live')
def live_exceptions():
    """Live exception feed"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            transaction_id,
            haul_timestamp,
            integrity_score,
            reconciliation_status,
            gps_variance_pct,
            energy_variance_pct,
            financial_variance_pct
        FROM institutional_audit_view
        ORDER BY haul_timestamp DESC
        LIMIT 50
    """)
    
    exceptions = []
    for row in cur.fetchall():
        exceptions.append({
            'transaction_id': str(row[0]),
            'timestamp': row[1].isoformat(),
            'integrity_score': float(row[2]),
            'status': row[3],
            'gps_variance': float(row[4]),
            'energy_variance': float(row[5]),
            'financial_variance': float(row[6])
        })
    
    cur.close()
    conn.close()
    
    return jsonify(exceptions)

@app.route('/api/regulatory/alerts')
def regulatory_alerts():
    """Recent regulatory alerts"""
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        SELECT 
            alert_type,
            severity,
            message,
            created_at
        FROM regulatory_alerts
        WHERE created_at >= NOW() - INTERVAL '24 hours'
        ORDER BY created_at DESC
        LIMIT 20
    """)
    
    alerts = []
    for row in cur.fetchall():
        alerts.append({
            'type': row[0],
            'severity': row[1],
            'message': row[2],
            'timestamp': row[3].isoformat()
        })
    
    cur.close()
    conn.close()
    
    return jsonify(alerts)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)