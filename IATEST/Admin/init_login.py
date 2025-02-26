import psycopg2
from psycopg2 import Error

def init_login_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="12345",
            port=5432
        )
        conn.autocommit = True
        cur = conn.cursor()

        # First drop the table if it exists
        cur.execute("DROP TABLE IF EXISTS loginpaswd CASCADE")

        # Verify current tables
        cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'""")
        tables = cur.fetchall()
        print("Existing tables:", [table[0] for table in tables])
        
        # Check employeeTable structure
        cur.execute("""SELECT column_name, data_type FROM information_schema.columns
                      WHERE table_name = 'employeetable'""")
        employee_cols = cur.fetchall()
        print("\nEmployeeTable columns:", employee_cols)
        
        # Check admin user
        cur.execute("""SELECT * FROM employeetable WHERE employeeid = 'ADMIN1'""")
        admin = cur.fetchone()
        print("\nAdmin user:", admin)
        
        # Start transaction
        cur.execute("BEGIN")
        
        try:
            # Create loginpaswd table with foreign key
            cur.execute("""
            CREATE TABLE IF NOT EXISTS loginpaswd (
                employeeid VARCHAR(255) PRIMARY KEY,
                password VARCHAR(255) NOT NULL,
                FOREIGN KEY(employeeid) REFERENCES employeeTable(employeeid) ON DELETE CASCADE
            )
            """)

            # Insert default admin user - matching employeeTable's ADMIN1
            cur.execute("""
            INSERT INTO loginpaswd (employeeid, password)
            VALUES ('ADMIN1', '12345')
            ON CONFLICT (employeeid) DO NOTHING
            """)

            # Verify loginpaswd table
            cur.execute("SELECT * FROM loginpaswd WHERE employeeid = 'ADMIN1'")
            admin_login = cur.fetchone()
            print("\nAdmin login:", admin_login)
            
            cur.execute("COMMIT")
            print("\nLogin table created and initialized successfully!")
            
        except Exception as e:
            cur.execute("ROLLBACK")
            print(f"\nError initializing login table: {str(e)}")
            raise

    except Error as e:
        print(f"Database error occurred: {e}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    init_login_db()