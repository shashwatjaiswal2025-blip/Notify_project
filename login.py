import psycopg2

DB_HOST = "localhost"
DB_NAME = "notifly_db"
DB_USER = "postgres"
DB_PASSWORD = "pass"
DB_PORT = "5432"

def check_login(login_id, password):
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute("SELECT 1 FROM users WHERE username = %s AND password = %s;", (username, password))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result is not None
    except Exception as e:
        print("Error:", e)
        return False

if __name__ == "__main__":
    while True:
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        if check_login(username, password):
            print("Authorised")
            break
        else:
            print("Invalid username or password. Please try again.")