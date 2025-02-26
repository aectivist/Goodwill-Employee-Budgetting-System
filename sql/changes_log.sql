-- Create table for tracking changes made by users
CREATE TABLE IF NOT EXISTS change_logs (
    log_id SERIAL PRIMARY KEY,                    -- Unique identifier for each log entry
    username VARCHAR(50) NOT NULL,                -- Username who made the change
    action_type VARCHAR(10) NOT NULL,             -- Type of action (ADD, EDIT, DELETE)
    affected_table VARCHAR(50) NOT NULL,          -- Name of the table that was modified
    record_id VARCHAR(50) NOT NULL,               -- ID of the record that was modified
    changes TEXT NOT NULL,                        -- JSON string containing the changes
    timestamp TIMESTAMP WITH TIME ZONE            -- When the change occurred
        DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_changes_username ON change_logs(username);
CREATE INDEX IF NOT EXISTS idx_changes_timestamp ON change_logs(timestamp);
CREATE INDEX IF NOT EXISTS idx_changes_action_type ON change_logs(action_type);
CREATE INDEX IF NOT EXISTS idx_changes_table ON change_logs(affected_table);

-- Add comments for documentation
COMMENT ON TABLE change_logs IS 'Tracks all changes made to important tables';
COMMENT ON COLUMN change_logs.log_id IS 'Unique identifier for each log entry';
COMMENT ON COLUMN change_logs.username IS 'Username who made the change';
COMMENT ON COLUMN change_logs.action_type IS 'Type of action (ADD, EDIT, DELETE)';
COMMENT ON COLUMN change_logs.affected_table IS 'Name of the table that was modified';
COMMENT ON COLUMN change_logs.record_id IS 'ID of the record that was modified';
COMMENT ON COLUMN change_logs.changes IS 'JSON string containing the before/after values for the change';
COMMENT ON COLUMN change_logs.timestamp IS 'When the change occurred';

-- Grant appropriate permissions
GRANT INSERT, SELECT ON change_logs TO postgres;
GRANT USAGE ON SEQUENCE change_logs_log_id_seq TO postgres;
