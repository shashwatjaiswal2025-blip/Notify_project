import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="notifly_db",
    user="postgres",
    password="pass"
)

# Create cursor
cur = conn.cursor()

# Execute query
cur.execute("SELECT id, new_subject, new_body, priority,  FROM responses")

# Get all results
rows = cur.fetchall()

# Print results
for row in rows:
    print(f"ID: {row[0]}")
    print(f"Subject: {row[1]}")
    print(f"Body: {row[2]}")
    print(f"Priority: {row[3]}")
    print("---")

# Close connections
cur.close()
conn.close()