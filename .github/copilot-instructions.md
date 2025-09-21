# Copilot Instructions for Notify_project

## Project Overview
This project is a Python script (`Back_end.py`) that connects to Gmail via IMAP, fetches emails, and stores them in a PostgreSQL database. It is intended for automated email ingestion and archiving.

## Architecture & Data Flow
- **Email Fetching:** Uses `imaplib` to connect to Gmail and retrieve all emails from the inbox.
- **Email Parsing:** Uses the `email` library to decode subject, sender, and body. Handles both multipart and plain text emails.
- **Database Storage:** Uses `psycopg2` to connect to PostgreSQL. Emails are stored in an `emails` table (created if not exists) with columns: `id`, `subject`, `sender`, `body`.
- **Configuration:** Credentials for Gmail and PostgreSQL are hardcoded as variables at the top of `Back_end.py`. Consider using environment variables for production.

## Developer Workflows
- **Run Script:** Execute `Back_end.py` directly to fetch and store emails:  
  `python Back_end.py`
- **Database Setup:** The script auto-creates the `emails` table if it does not exist.
- **Dependencies:** Requires `psycopg2` for PostgreSQL and access to Gmail IMAP. Install with:  
  `pip install psycopg2`
- **Gmail App Password:** If Gmail 2FA is enabled, use an App Password for authentication.

## Project-Specific Patterns
- **Single File:** All logic is in `Back_end.py`. No modularization or separation of concerns yet.
- **Error Handling:** Minimal; add try/except blocks for production robustness.
- **Email Parsing:** Only stores plain text parts of emails. Attachments and HTML are ignored.
- **Table Creation:** Table is created on every run if missing; no migrations or schema management.

## Integration Points
- **Gmail IMAP:** External dependency for email fetching.
- **PostgreSQL:** External dependency for data storage. Ensure the database is running and accessible.

## Example Pattern
```python
if __name__ == "__main__":
    fetch_gmail()
```

## Key File Reference
- `Back_end.py`: Main script containing all logic.

---

**For AI agents:**
- Focus on improving modularity, error handling, and configuration management.
- When adding features, maintain the simple data flow: fetch → parse → store.
- Document any new dependencies or workflow changes in this file.

---

*If any section is unclear or missing, please provide feedback to iterate and improve these instructions.*
