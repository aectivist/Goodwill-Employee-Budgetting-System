import psycopg2

def init_database():
    connection = None
    try:
        # Connect to database
        connection = psycopg2.connect(
            host="localhost",
            dbname="postgres",
            user="postgres",
            password="12345",
            port=5432
        )
        cursor = connection.cursor()

        # Create tables with transaction
        cursor.execute("BEGIN")
        try:
            # Create employee table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS employeeTable (
                    employeeid VARCHAR(255) PRIMARY KEY NOT NULL,
                    employeeName VARCHAR(400),
                    employeeNumber VARCHAR(30),
                    DateOfChange DATE,
                    OrganizationSector VARCHAR(255) CHECK (OrganizationSector IN (
                        'Health care',
                        'Precision manufacturing',
                        'Engineering',
                        'Finance/accounting',
                        'Information technology'
                    )),
                    BranchId bigint NOT NULL,
                    FOREIGN KEY(BranchId) REFERENCES goodwillbranch(BranchId)
                )
            """)

            # Create login password table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS loginpaswd (
                    id VARCHAR(255) PRIMARY KEY NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    FOREIGN KEY(id) REFERENCES employeeTable(employeeid) ON DELETE CASCADE
                )
            """)

            cursor.execute("COMMIT")
            print("Database tables created successfully!")

        except Exception as e:
            cursor.execute("ROLLBACK")
            print(f"Error creating tables: {str(e)}")
            raise e

    except Exception as e:
        print(f"Database connection error: {str(e)}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    init_database()