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
            # Drop all tables first to ensure clean creation
            cursor.execute("""
                DROP TABLE IF EXISTS user_login_logs CASCADE;
                DROP TABLE IF EXISTS change_logs CASCADE;
                DROP TABLE IF EXISTS loginpaswd CASCADE;
                DROP TABLE IF EXISTS employeeTable CASCADE;
                DROP TABLE IF EXISTS goodwillBranch CASCADE
            """)

            # Create goodwillbranch table first
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS goodwillBranch (
                    BranchId bigint not null,
                    branchName varchar (200) not null,
                    branchAddress varchar(200) not null,
                    branchPhoneNumber bigint,
                    PRIMARY KEY (branchId)
                )
            """)

            # Insert default branch if it doesn't exist
            try:
                cursor.execute("""
                    INSERT INTO goodwillBranch VALUES (0, 'n/a', 'n/a', 0)
                    ON CONFLICT (branchid) DO NOTHING
                """)
            except Exception as e:
                print(f"Warning: Could not insert default branch: {str(e)}")

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

            # Insert default admin user if it doesn't exist
            try:
                cursor.execute("""
                    INSERT INTO employeeTable VALUES
                    ('ADMIN1', 'Administrator', 'ADMIN', CURRENT_DATE, 'Information technology', 0)
                    ON CONFLICT (employeeid) DO NOTHING
                """)
            except Exception as e:
                print(f"Warning: Could not insert admin user: {str(e)}")

            # Create login password table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS loginpaswd (
                    employeeid VARCHAR(255) PRIMARY KEY NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    FOREIGN KEY(employeeid) REFERENCES employeeTable(employeeid) ON DELETE CASCADE
                )
            """)

            # Insert default admin login if it doesn't exist
            try:
                cursor.execute("""
                    INSERT INTO loginpaswd (employeeid, password)
                    VALUES ('ADMIN1', '12345')
                    ON CONFLICT (employeeid) DO NOTHING
                """)
            except Exception as e:
                print(f"Warning: Could not insert admin login: {str(e)}")

            # Create user login logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_login_logs (
                    log_id SERIAL PRIMARY KEY,
                    employeeid VARCHAR(255) NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    action_type VARCHAR(20) NOT NULL,
                    page_accessed VARCHAR(100),
                    action_details TEXT,
                    action_timestamp TIMESTAMP WITH TIME ZONE
                        DEFAULT CURRENT_TIMESTAMP,
                    ip_address VARCHAR(45),
                    user_agent TEXT
                )
            """)

            # Add foreign key after table creation
            cursor.execute("""
                ALTER TABLE user_login_logs
                ADD CONSTRAINT fk_login_logs_employee
                FOREIGN KEY (employeeid)
                REFERENCES employeeTable(employeeid)
                ON DELETE CASCADE
            """)

            # Create indexes for login logs
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_login_logs_employeeid ON user_login_logs(employeeid);
                CREATE INDEX IF NOT EXISTS idx_login_logs_username ON user_login_logs(username);
                CREATE INDEX IF NOT EXISTS idx_login_logs_timestamp ON user_login_logs(action_timestamp);
                CREATE INDEX IF NOT EXISTS idx_login_logs_action_type ON user_login_logs(action_type)
            """)

            # Create change logs table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS change_logs (
                    log_id SERIAL PRIMARY KEY,
                    employeeid VARCHAR(255) NOT NULL,
                    username VARCHAR(50) NOT NULL,
                    action_type VARCHAR(10) NOT NULL,
                    affected_table VARCHAR(50) NOT NULL,
                    record_id VARCHAR(50) NOT NULL,
                    changes TEXT NOT NULL,
                    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Add foreign key after table creation
            cursor.execute("""
                ALTER TABLE change_logs
                ADD CONSTRAINT fk_change_logs_employee
                FOREIGN KEY (employeeid)
                REFERENCES employeeTable(employeeid)
                ON DELETE CASCADE
            """)

            # Create indexes for change logs
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_changes_username ON change_logs(username);
                CREATE INDEX IF NOT EXISTS idx_changes_employeeid ON change_logs(employeeid);
                CREATE INDEX IF NOT EXISTS idx_changes_timestamp ON change_logs(timestamp);
                CREATE INDEX IF NOT EXISTS idx_changes_action_type ON change_logs(action_type);
                CREATE INDEX IF NOT EXISTS idx_changes_table ON change_logs(affected_table)
            """)

            # Grant permissions
            cursor.execute("""
                GRANT INSERT, SELECT ON change_logs TO postgres;
                GRANT USAGE ON SEQUENCE change_logs_log_id_seq TO postgres;
                GRANT INSERT, SELECT ON user_login_logs TO postgres;
                GRANT USAGE ON SEQUENCE user_login_logs_log_id_seq TO postgres
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