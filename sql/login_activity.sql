-- Update login logs table to include more detailed information
DROP TABLE IF EXISTS user_login_logs;

CREATE TABLE user_login_logs (
    log_id SERIAL PRIMARY KEY,
    employeeid VARCHAR(50) NOT NULL,            -- Employee ID reference
    username VARCHAR(50) NOT NULL,              -- Username for display
    action_type VARCHAR(20) NOT NULL,           -- Type of action (LOGIN_SUCCESS, LOGIN_FAILED, PAGE_ACCESS)
    page_accessed VARCHAR(100),                 -- Which page/feature was accessed (for PAGE_ACCESS)
    action_details TEXT,                        -- Additional details about the action
    action_timestamp TIMESTAMP WITH TIME ZONE   -- When the action occurred
        DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),                    
    user_agent TEXT,
    FOREIGN KEY (employeeid) REFERENCES employeeTable(employeeid) ON DELETE CASCADE
);

-- Create indexes for faster searches
CREATE INDEX idx_login_logs_employeeid ON user_login_logs(employeeid);
CREATE INDEX idx_login_logs_username ON user_login_logs(username);
CREATE INDEX idx_login_logs_timestamp ON user_login_logs(action_timestamp);
CREATE INDEX idx_login_logs_action_type ON user_login_logs(action_type);

-- Add comments for documentation
COMMENT ON TABLE user_login_logs IS 'Tracks all user activity including logins and page access';
COMMENT ON COLUMN user_login_logs.employeeid IS 'Employee ID from employeeTable';
COMMENT ON COLUMN user_login_logs.username IS 'Username for display purposes';
COMMENT ON COLUMN user_login_logs.action_type IS 'Type of action (LOGIN_SUCCESS, LOGIN_FAILED, PAGE_ACCESS)';
COMMENT ON COLUMN user_login_logs.page_accessed IS 'Page or feature that was accessed';
COMMENT ON COLUMN user_login_logs.action_details IS 'Additional details about the action';
COMMENT ON COLUMN user_login_logs.action_timestamp IS 'When the action occurred';

-- Grant appropriate permissions
GRANT INSERT, SELECT ON user_login_logs TO postgres;
GRANT USAGE ON SEQUENCE user_login_logs_log_id_seq TO postgres;