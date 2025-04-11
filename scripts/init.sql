-- Create messages table if not exists
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    subject VARCHAR(255) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on subject for faster lookups
CREATE INDEX IF NOT EXISTS idx_messages_subject ON messages(subject);
