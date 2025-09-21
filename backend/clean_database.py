import sqlite3
import json
from datetime import datetime

def clean_database():
    """Clean up database by removing duplicates and adding fresh test data"""
    
    # Connect to database
    conn = sqlite3.connect('notifly.db')
    cursor = conn.cursor()
    
    print("Current submissions before cleanup:")
    cursor.execute('SELECT id, title, status FROM submissions ORDER BY id')
    results = cursor.fetchall()
    for row in results:
        print(f"ID: {row[0]}, Title: {row[1]}, Status: {row[2]}")
    
    # Clear all data
    print("\nClearing all submissions...")
    cursor.execute('DELETE FROM submissions')
    cursor.execute('DELETE FROM approved_newsletters')
    
    # Reset auto-increment
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="submissions"')
    cursor.execute('DELETE FROM sqlite_sequence WHERE name="approved_newsletters"')
    
    # Add fresh, unique test data
    print("Adding fresh test data...")
    
    test_submissions = [
        {
            'title': 'Tech Conference 2025',
            'category': 'Technology',
            'organization': 'TechCorp',
            'description': 'Join us for the biggest tech conference of the year featuring keynotes from industry leaders.',
            'event_date': '2025-10-15',
            'event_time': '09:00',
            'location': 'Convention Center',
            'contact_email': 'info@techcorp.com',
            'contact_name': 'John Smith',
            'contact_phone': '+1-555-0123',
            'submitted_at': '2025-09-21T10:00:00'
        },
        {
            'title': 'Community Art Exhibition',
            'category': 'Arts',
            'organization': 'Local Art Club',
            'description': 'Showcasing local artists and their work. Free admission for all community members.',
            'event_date': '2025-09-30',
            'event_time': '14:00',
            'location': 'Community Gallery',
            'contact_email': 'art@community.org',
            'contact_name': 'Sarah Johnson',
            'contact_phone': '+1-555-0456',
            'submitted_at': '2025-09-21T11:00:00'
        },
        {
            'title': 'Charity Fundraiser Event',
            'category': 'Community',
            'organization': 'Help Foundation',
            'description': 'Annual charity event to raise funds for local homeless shelter. Dinner and auction included.',
            'event_date': '2025-11-20',
            'event_time': '18:00',
            'location': 'Grand Hotel Ballroom',
            'contact_email': 'events@helpfoundation.org',
            'contact_name': 'Mike Wilson',
            'contact_phone': '+1-555-0789',
            'submitted_at': '2025-09-21T12:00:00'
        },
        {
            'title': 'University Job Fair',
            'category': 'Education',
            'organization': 'State University',
            'description': 'Career opportunities for students and recent graduates. Over 50 companies participating.',
            'event_date': '2025-10-05',
            'event_time': '10:00',
            'location': 'University Sports Center',
            'contact_email': 'careers@university.edu',
            'contact_name': 'Dr. Emily Chen',
            'contact_phone': '+1-555-0321',
            'submitted_at': '2025-09-21T13:00:00'
        },
        {
            'title': 'Environmental Cleanup Drive',
            'category': 'Environment',
            'organization': 'Green Earth Initiative',
            'description': 'Monthly community cleanup to keep our parks and waterways clean. Volunteers needed.',
            'event_date': '2025-09-28',
            'event_time': '08:00',
            'location': 'Central Park',
            'contact_email': 'volunteer@greenearth.org',
            'contact_name': 'Alex Rodriguez',
            'contact_phone': '+1-555-0654',
            'submitted_at': '2025-09-21T14:00:00'
        }
    ]
    
    # Insert fresh test data
    for submission in test_submissions:
        cursor.execute('''
            INSERT INTO submissions 
            (title, category, organization, description, event_date, event_time, 
             location, contact_email, contact_phone, contact_name, submitted_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'pending')
        ''', (
            submission['title'],
            submission['category'],
            submission['organization'],
            submission['description'],
            submission['event_date'],
            submission['event_time'],
            submission['location'],
            submission['contact_email'],
            submission['contact_phone'],
            submission['contact_name'],
            submission['submitted_at']
        ))
    
    conn.commit()
    
    # Show final results
    print("\nFinal submissions after cleanup:")
    cursor.execute('SELECT id, title, status FROM submissions ORDER BY id')
    results = cursor.fetchall()
    for row in results:
        print(f"ID: {row[0]}, Title: {row[1]}, Status: {row[2]}")
    
    conn.close()
    print(f"\nDatabase cleaned! Added {len(test_submissions)} fresh submissions.")
    print("All submissions are in 'pending' status and ready for testing approve/decline functionality.")

if __name__ == '__main__':
    clean_database()