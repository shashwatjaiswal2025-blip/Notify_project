#!/usr/bin/env python3
"""
View Submissions Script
Shows all submissions stored in the Notifly database
"""

import sqlite3
import json
from datetime import datetime

def view_submissions():
    try:
        # Connect to database
        conn = sqlite3.connect('notifly.db')
        cursor = conn.cursor()
        
        # Get all submissions
        cursor.execute('SELECT * FROM submissions ORDER BY submitted_at DESC')
        rows = cursor.fetchall()
        
        print("=" * 80)
        print("NOTIFLY SUBMISSIONS DATABASE")
        print("=" * 80)
        print(f"Total submissions: {len(rows)}")
        print("-" * 80)
        
        if not rows:
            print("No submissions found.")
            print("\nTo test the system:")
            print("1. Go to http://localhost:8000/templates/submit.html")
            print("2. Fill out and submit the form")
            print("3. Run this script again to see the data")
        else:
            for i, row in enumerate(rows, 1):
                print(f"\n--- SUBMISSION #{i} ---")
                print(f"ID: {row[0]}")
                print(f"Title: {row[1]}")
                print(f"Category: {row[2]}")
                print(f"Organization: {row[3] or 'Not specified'}")
                print(f"Description: {row[4][:100]}{'...' if len(row[4]) > 100 else ''}")
                print(f"Event Date: {row[5] or 'Not specified'}")
                print(f"Event Time: {row[6] or 'Not specified'}")
                print(f"Location: {row[7] or 'Not specified'}")
                print(f"Contact Name: {row[8] or 'Not specified'}")
                print(f"Contact Email: {row[9]}")
                print(f"Contact Phone: {row[10] or 'Not specified'}")
                print(f"Submitted At: {row[11]}")
                print(f"Status: {row[12]}")
                
                # Show attachments if any
                if row[13]:  # attachments column
                    attachments = json.loads(row[13])
                    print(f"Attachments: {', '.join(attachments)}")
                else:
                    print("Attachments: None")
        
        print("\n" + "=" * 80)
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    view_submissions()