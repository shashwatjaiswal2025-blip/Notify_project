import psycopg2

# Database credentials (update as needed)
DB_HOST = "localhost"
DB_NAME = "notifly_db"
DB_USER = "postgres"
DB_PASSWORD = "pass"
DB_HOST = "localhost"
DB_PORT = "5432"
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(255) UNIQUE NOT NULL,
                password VARCHAR(255) NOT NULL
            );
        """)
        conn.commit()

def username_exists(conn, username):
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM users WHERE username = %s;", (username,))
        return cur.fetchone() is not None

def add_user(conn, username, password):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s);",
            (username, password)
        )
        conn.commit()

def main():
    try:
        conn = psycopg2.connect(
            host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS
        )
        create_users_table(conn)
        while True:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            if username_exists(conn, username):
                print("Username already exists. Please choose a different username.")
            else:
                add_user(conn, username, password)
                print("Account created successfully.")
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()