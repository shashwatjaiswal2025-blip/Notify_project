import imaplib
import email
from email.header import decode_header
import psycopg2
from email.utils import parsedate_to_datetime

# --- Configuration ---
GMAIL_USER = "shashwat.jaiswal2025@vitstudent.ac.in"
GMAIL_PASS = "rmnd jgml zija wsvm"
IMAP_SERVER = "imap.gmail.com"
PG_HOST = "localhost"
PG_DB = "notifly_db"
PG_USER = "postgres"
PG_PASS = "pass"

# --- Database Setup ---
def init_db():
    conn = psycopg2.connect(
        host=PG_HOST, dbname=PG_DB, user=PG_USER, password=PG_PASS
    )
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS emails (
            id SERIAL PRIMARY KEY,
            subject TEXT,
            sender TEXT,
            body TEXT,
            received_date TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    print("Database initialized and table ensured.")
    return conn

# --- Email Fetching ---
def fetch_gmail():
    print("Fetching started")
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(GMAIL_USER, GMAIL_PASS)
    mail.select("inbox")
    typ, data = mail.search(None, "ALL")
    email_ids = data[0].split()
    emails = []
    i=0
    print("For loop starts")
    for eid in email_ids:
        i+=1
        typ, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, encoding = decode_header(msg.get("Subject"))[0]
                if isinstance(subject, bytes):
                    subject = subject.decode(encoding or "utf-8", errors="ignore")
                sender = msg.get("From")
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain" and not part.get("Content-Disposition"):
                            charset = part.get_content_charset() or "utf-8"
                            body += part.get_payload(decode=True).decode(charset, errors="ignore")
                else:
                    charset = msg.get_content_charset() or "utf-8"
                    body = msg.get_payload(decode=True).decode(charset, errors="ignore")
                received_date_str = msg.get('Date')
                try:
                    received_date = parsedate_to_datetime(received_date_str) if received_date_str else None
                except Exception:
                    received_date = None
                emails.append((subject, sender, body, received_date))
        print(i)
        if i>=10:
            break

    mail.logout()
    print(f"Fetched {len(emails)} emails from Gmail.")
    return emails

# --- Store Emails ---
def store_emails(conn, emails):
    cur = conn.cursor()
    for subject, sender, body, received_date in emails:
        cur.execute(
            "SELECT id FROM emails WHERE subject=%s AND sender=%s AND received_date=%s",
            (subject, sender, received_date)
        )
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO emails (subject, sender, body, received_date) VALUES (%s, %s, %s, %s)",
                (subject, sender, body, received_date)
            )
    conn.commit()
    cur.close()
    print(f"Stored {len(emails)} emails in the database.")

def main():
    conn = init_db()
    emails = fetch_gmail()
    store_emails(conn, emails)
    conn.close()
main()