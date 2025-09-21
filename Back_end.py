import imaplib
import email
from email.header import decode_header
import psycopg2

# --- Configuration (replace with your credentials) ---
GMAIL_USER = "shashwat.jaiswal2025@vitstudent.ac.in"
GMAIL_PASSWORD = "cp8QSsxbAR"
IMAP_SERVER = "imap.gmail.com"
POSTGRES_HOST = "localhost"
POSTGRES_DB = "notify_db"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgress"

def connect_postgres():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )
    return conn

def create_table(conn):
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id SERIAL PRIMARY KEY,
                subject TEXT,
                sender TEXT,
                body TEXT
            );
        """)
        conn.commit()

def parse_email(msg):
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8", errors="ignore")
    sender = msg.get("From")
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain" and not part.get('Content-Disposition'):
                charset = part.get_content_charset() or "utf-8"
                body += part.get_payload(decode=True).decode(charset, errors="ignore")
    else:
        charset = msg.get_content_charset() or "utf-8"
        body = msg.get_payload(decode=True).decode(charset, errors="ignore")
    return subject, sender, body

def save_email(conn, subject, sender, body):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO emails (subject, sender, body) VALUES (%s, %s, %s);",
            (subject, sender, body)
        )
        conn.commit()

def fetch_gmail():
    # Connect to Gmail IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(GMAIL_USER, GMAIL_PASSWORD)
    mail.select("inbox")
    typ, data = mail.search(None, "ALL")
    email_ids = data[0].split()

    conn = connect_postgres()
    create_table(conn)

    for eid in email_ids:
        typ, msg_data = mail.fetch(eid, "(RFC822)")
        for response_part in msg_data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                subject, sender, body = parse_email(msg)
                save_email(conn, subject, sender, body)

    conn.close()
    mail.logout()

if __name__ == "__main__":
    fetch_gmail()