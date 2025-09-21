import sqlite3
from datetime import datetime

def add_sample_submissions():
    conn = sqlite3.connect('notifly.db')
    cursor = conn.cursor()
    
    sample_submissions = [
        {
            'title': 'Tech Conference 2025',
            'category': 'EVENT',
            'organization': 'TechCorp',
            'description': 'Join us for the biggest tech conference of the year featuring keynotes from industry leaders.',
            'event_date': '2025-10-15',
            'event_time': '09:00',
            'location': 'Convention Center',
            'contact_email': 'info@techcorp.com',
            'contact_name': 'John Smith',
            'contact_phone': '555-0123'
        },
        {
            'title': 'Community Art Exhibition',
            'category': 'CLUB',
            'organization': 'Local Art Club',
            'description': 'Showcasing local artists and their work. Free admission for all community members.',
            'event_date': '2025-09-30',
            'location': 'Community Gallery',
            'contact_email': 'art@community.org',
            'contact_name': 'Sarah Johnson'
        },
        {
            'title': 'Charity Fundraiser',
            'category': 'EVENT',
            'organization': 'Help Foundation',
            'description': 'Annual charity event to raise funds for local homeless shelter. Dinner and auction included.',
            'event_date': '2025-11-20',
            'location': 'Grand Hotel Ballroom',
            'contact_email': 'events@helpfoundation.org',
            'contact_name': 'Mike Wilson'
        }
    ]
    
    for submission in sample_submissions:
        cursor.execute('''
            INSERT INTO submissions 
            (title, category, organization, description, event_date, event_time, 
             location, contact_email, contact_phone, contact_name, submitted_at, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            submission['title'],
            submission['category'],
            submission['organization'],
            submission['description'],
            submission.get('event_date', ''),
            submission.get('event_time', ''),
            submission.get('location', ''),
            submission.get('contact_email', ''),
            submission.get('contact_phone', ''),
            submission.get('contact_name', ''),
            datetime.now().isoformat(),
            'pending'
        ))
    
    conn.commit()
    conn.close()
    print(f"Added {len(sample_submissions)} sample submissions to the database")

if __name__ == '__main__':
    add_sample_submissions()