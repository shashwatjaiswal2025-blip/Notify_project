from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import sqlite3
import os
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Database setup
def init_db():
    conn = sqlite3.connect('notifly.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS submissions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            organization TEXT,
            description TEXT NOT NULL,
            event_date TEXT,
            event_time TEXT,
            location TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            contact_name TEXT,
            submitted_at TEXT NOT NULL,
            status TEXT DEFAULT 'pending'
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS approved_newsletters (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            submission_id INTEGER,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            organization TEXT,
            description TEXT NOT NULL,
            event_date TEXT,
            event_time TEXT,
            location TEXT,
            contact_email TEXT,
            contact_phone TEXT,
            contact_name TEXT,
            submitted_at TEXT NOT NULL,
            approved_at TEXT NOT NULL,
            FOREIGN KEY (submission_id) REFERENCES submissions (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

@app.route('/')
def home():
    return '''
    <h1>Notifly Backend API</h1>
    <p>Backend server is running!</p>
    <ul>
        <li><a href="/api/test">Test API</a></li>
        <li><a href="/api/submissions">View Submissions</a></li>
        <li><a href="/test-submit.html">Test Form</a></li>
    </ul>
    '''

@app.route('/api/test')
def test_api():
    return jsonify({
        'status': 'success',
        'message': 'API is working!',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/submit-news', methods=['POST', 'OPTIONS'])
def submit_news():
    if request.method == 'OPTIONS':
        # Handle preflight request
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    try:
        # Get form data
        data = {}
        
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            # Form data
            data = {
                'title': request.form.get('title', ''),
                'category': request.form.get('category', ''),
                'organization': request.form.get('organization', ''),
                'description': request.form.get('description', ''),
                'event_date': request.form.get('event_date', ''),
                'event_time': request.form.get('event_time', ''),
                'location': request.form.get('location', ''),
                'contact_email': request.form.get('contact_email', ''),
                'contact_phone': request.form.get('contact_phone', ''),
                'contact_name': request.form.get('contact_name', ''),
                'submitted_at': request.form.get('submitted_at', datetime.now().isoformat())
            }
        
        # Validate required fields
        required_fields = ['title', 'category', 'description']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Insert into database
        conn = sqlite3.connect('notifly.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO submissions 
            (title, category, organization, description, event_date, event_time, 
             location, contact_email, contact_phone, contact_name, submitted_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['title'],
            data['category'],
            data.get('organization', ''),
            data['description'],
            data.get('event_date', ''),
            data.get('event_time', ''),
            data.get('location', ''),
            data.get('contact_email', ''),
            data.get('contact_phone', ''),
            data.get('contact_name', ''),
            data['submitted_at']
        ))
        
        submission_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Handle file uploads if present
        files_saved = []
        if 'attachments' in request.files:
            files = request.files.getlist('attachments')
            upload_dir = 'uploads'
            os.makedirs(upload_dir, exist_ok=True)
            
            for file in files:
                if file.filename:
                    filename = f"{submission_id}_{file.filename}"
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    files_saved.append(filename)
        
        return jsonify({
            'success': True,
            'message': 'News submitted successfully!',
            'id': submission_id,
            'files_saved': files_saved
        }), 200
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Server error: {str(e)}'
        }), 500

@app.route('/api/submissions')
def get_submissions():
    try:
        conn = sqlite3.connect('notifly.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM submissions ORDER BY submitted_at DESC')
        rows = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        submissions = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'submissions': submissions,
            'count': len(submissions)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving submissions: {str(e)}'
        }), 500

@app.route('/api/submissions/<int:submission_id>/approve', methods=['POST', 'OPTIONS'])
def approve_submission(submission_id):
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    try:
        conn = sqlite3.connect('notifly.db')
        cursor = conn.cursor()
        
        # Check if submission exists and is pending
        cursor.execute('SELECT * FROM submissions WHERE id = ? AND status = "pending"', (submission_id,))
        submission = cursor.fetchone()
        
        if not submission:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Submission not found or already processed'
            }), 404
        
        # Update status to approved
        cursor.execute('UPDATE submissions SET status = "approved" WHERE id = ?', (submission_id,))
        
        # Copy to approved_newsletters table
        cursor.execute('''
            INSERT INTO approved_newsletters 
            (submission_id, title, category, organization, description, event_date, event_time, 
             location, contact_email, contact_phone, contact_name, submitted_at, approved_at)
            SELECT id, title, category, organization, description, event_date, event_time, 
                   location, contact_email, contact_phone, contact_name, submitted_at, ?
            FROM submissions WHERE id = ?
        ''', (datetime.now().isoformat(), submission_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Submission approved successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error approving submission: {str(e)}'
        }), 500

@app.route('/api/submissions/<int:submission_id>/decline', methods=['POST', 'OPTIONS'])
def decline_submission(submission_id):
    if request.method == 'OPTIONS':
        response = jsonify({'status': 'ok'})
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Requested-With')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        return response
    
    try:
        conn = sqlite3.connect('notifly.db')
        cursor = conn.cursor()
        
        # Check if submission exists and is pending
        cursor.execute('SELECT * FROM submissions WHERE id = ? AND status = "pending"', (submission_id,))
        submission = cursor.fetchone()
        
        if not submission:
            conn.close()
            return jsonify({
                'success': False,
                'message': 'Submission not found or already processed'
            }), 404
        
        # Update status to rejected
        cursor.execute('UPDATE submissions SET status = "rejected" WHERE id = ?', (submission_id,))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Submission declined successfully'
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error declining submission: {str(e)}'
        }), 500

@app.route('/api/approved-newsletters')
def get_approved_newsletters():
    try:
        conn = sqlite3.connect('notifly.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM approved_newsletters ORDER BY approved_at DESC')
        rows = cursor.fetchall()
        
        columns = [description[0] for description in cursor.description]
        newsletters = [dict(zip(columns, row)) for row in rows]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'newsletters': newsletters,
            'count': len(newsletters)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error retrieving approved newsletters: {str(e)}'
        }), 500

@app.route('/submit', methods=['POST'])
def submit_fallback():
    """Fallback endpoint for simple form submissions"""
    return submit_news()

if __name__ == '__main__':
    print("Starting Notifly Backend...")
    print("Available endpoints:")
    print("- http://localhost:5000/")
    print("- http://localhost:5000/api/test")
    print("- http://localhost:5000/api/submit-news")
    print("- http://localhost:5000/api/submissions")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
