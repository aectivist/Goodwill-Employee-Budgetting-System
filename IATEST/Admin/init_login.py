import psycopg2

def init_login_db():
    conn = psycopg2.connect(
        host="localhost",
        dbname="postgres",
        user="postgres",
        password="12345",
        port=5432
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Create loginpaswd table if it doesn't exist
    cur.execute("""
    CREATE TABLE IF NOT EXISTS loginpaswd (
        loginid VARCHAR(50) PRIMARY KEY,
        password VARCHAR(50) NOT NULL
    )
    """)

    # Check if admin user exists
    cur.execute("SELECT * FROM loginpaswd WHERE loginid = 'Admin'")
    if not cur.fetchone():
        # Insert admin user if not exists
        cur.execute(
            "INSERT INTO loginpaswd (loginid, password) VALUES (%s, %s)",
            ('Admin', 'budget!2System')
        )

    cur.close()
    conn.close()

if __name__ == "__main__":
    init_login_db()
    print("Login database initialized successfully!")