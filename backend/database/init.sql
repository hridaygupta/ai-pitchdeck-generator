-- Initialize the AI Pitch Deck Generator database
-- This script runs when the PostgreSQL container starts for the first time

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Create the database if it doesn't exist
-- (This is handled by the POSTGRES_DB environment variable)

-- Grant permissions
GRANT ALL PRIVILEGES ON DATABASE pitchdeck TO pitchdeck_user;

-- Create additional schemas if needed
CREATE SCHEMA IF NOT EXISTS analytics;
CREATE SCHEMA IF NOT EXISTS ai_models;

-- Set search path
SET search_path TO public, analytics, ai_models;

-- Create initial admin user (password: admin123)
-- This will be handled by the application's init_db function 