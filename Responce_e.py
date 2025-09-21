import psycopg2
import requests
import json
import time
from typing import Optional


url = "http://10.91.86.87:8081"

def ping_server(url, timeout=5):
    """
    Simple server ping using GET request
    """
    try:
        response = requests.get(url, timeout=timeout)
        print(f"Server responded with status code: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.RequestException as e:
        print(f"Error pinging server: {e}")
        return False

# Example usage

is_alive = ping_server(url)
print(f"Server is alive: {is_alive}")



# Database configuration
PG_HOST = "localhost"
PG_DB = "notifly_db"
PG_USER = "postgres"
PG_PASS = "pass"




def connect_to_database():
    """Establish connection to PostgreSQL database"""
    try:
        connection = psycopg2.connect(
            host=PG_HOST,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASS,
            port=5432  # Default PostgreSQL port
        )
        print("Successfully connected to PostgreSQL database")
        return connection
    except (Exception, psycopg2.Error) as error:
        print(f"Error connecting to PostgreSQL database: {error}")
        return None

def fetch_email_data(connection):
    """Fetch all email records from the database"""
    try:
        cursor = connection.cursor()
        
        # SQL query to fetch data from email table
        query = """
        SELECT id, subject, body, received_date 
        FROM emails 
        ORDER BY received_date DESC
        """
        
        cursor.execute(query)
        records = cursor.fetchall()
        
        print(f"Fetched {len(records)} email records from database")
        
        # Convert to list of dictionaries for easier handling
        email_data = []
        for record in records:
            email_data.append({
                'id': record[0],
                'subject': record[1],
                'body': record[2],
                'received_date': record[3]
            })
        
        cursor.close()
        return email_data
        
    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching data from database: {error}")
        return []

def make_post_request(email_record, url_endpoint):
    """Make POST request with email data"""
    print("url_endpoint=",url_endpoint)
    url_endpoint+='/process_email'
    try:
        # Prepare payload according to specified format
        payload = {
            'subject': email_record['subject'] if email_record['subject'] else "",
            'body': email_record['body'] if email_record['body'] else ""
        }
        
        # Set headers for JSON content
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        
        # Make POST request
        response = requests.post(
            url_endpoint, 
            json=payload,  # Using json parameter automatically sets Content-Type
            headers=headers,
            timeout=30  # 30 second timeout
        )
        
        # Check response status
        if response.status_code == 200 or response.status_code == 201:
            print(f"✅ Successfully posted email ID {email_record['id']} - Status: {response.status_code}")
            return True
        else:
            print(f"❌ Failed to post email ID {email_record['id']} - Status: {response.status_code}, Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error for email ID {email_record['id']}: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error for email ID {email_record['id']}: {e}")
        return False

def process_emails_with_rate_limit(email_data, url_endpoint, delay=1):
    """Process all emails with optional rate limiting"""
    success_count = 0
    failure_count = 0
    print(f"\n🚀 Starting to process {len(email_data)} emails...")
    
    for i, email in enumerate(email_data, 1):
        print(f"\n📧 Processing email {i}/{len(email_data)} (ID: {email['id']})")
        print(f"Subject: {email['subject'][:50]}..." if len(email['subject']) > 50 else f"Subject: {email['subject']}")
        
        success = make_post_request(email, url_endpoint)
        print(success)
        if success:
            success_count += 1
        else:
            failure_count += 1
        
        # Add delay between requests to avoid overwhelming the server
        if i < len(email_data):  # Don't delay after the last request
            time.sleep(delay)
    
    print(f"\n📊 Processing completed!")
    print(f"✅ Successful requests: {success_count}")
    print(f"❌ Failed requests: {failure_count}")
    print(f"📈 Success rate: {(success_count/(success_count+failure_count))*100:.1f}%")

def main():
    """Main execution function"""
    print("🔄 Starting email processing script...")
    
    # Connect to database
    connection = connect_to_database()
    if not connection:
        print("❌ Failed to connect to database. Exiting.")
        return
    
    try:
        # Fetch email data
        email_data = fetch_email_data(connection)
        
        if not email_data:
            print("📭 No email data found or error occurred while fetching data.")
            return
        
        # Process emails and make POST requests
        process_emails_with_rate_limit(email_data, url, delay=0.5)  # 0.5 second delay between requests
        
    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")
    
    finally:
        # Always close the database connection
        if connection:
            connection.close()
            print("🔐 Database connection closed.")

if __name__ == "__main__":
    main()
