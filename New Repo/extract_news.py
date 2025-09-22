import psycopg2

# Connect to database
conn = psycopg2.connect(
    host="localhost",
    database="notifly",
    user="postgres",
    password="your_password"
)

# Create cursor
cur = conn.cursor()

# Execute query
cur.execute("SELECT id, subjct, body FROM responce")

# Get all results
rows = cur.fetchall()

# Print results
for row in rows:
    print(f"ID: {row[0]}")
    print(f"Subject: {row[1]}")
    print(f"Body: {row[2]}")
    print("---")

# Close connections
cur.close()
conn.close()