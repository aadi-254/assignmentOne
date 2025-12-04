-- Event Management System - MySQL Database Schema
-- Database: event_management_db

-- Create database (you can change the name if needed)
CREATE DATABASE IF NOT EXISTS event_management_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE event_management_db;

-- Note: Django will create these tables automatically when you run migrations
-- This SQL file shows the expected schema structure for reference

-- User table (Django's built-in auth_user)
-- This table is created by Django automatically

-- UserProfile table
-- Extends Django User model with additional fields
CREATE TABLE IF NOT EXISTS api_userprofile (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    bio TEXT NULL,
    location VARCHAR(255) NULL,
    profile_picture VARCHAR(100) NULL,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    user_id INT NOT NULL UNIQUE,
    CONSTRAINT fk_userprofile_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    INDEX idx_userprofile_user (user_id),
    INDEX idx_userprofile_location (location),
    INDEX idx_userprofile_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Event table
CREATE TABLE IF NOT EXISTS api_event (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255) NOT NULL,
    start_time DATETIME(6) NOT NULL,
    end_time DATETIME(6) NOT NULL,
    is_public TINYINT(1) NOT NULL DEFAULT 1,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    organizer_id INT NOT NULL,
    CONSTRAINT fk_event_organizer FOREIGN KEY (organizer_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    INDEX idx_event_organizer (organizer_id),
    INDEX idx_event_start_time (start_time),
    INDEX idx_event_location (location),
    INDEX idx_event_is_public (is_public),
    INDEX idx_event_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Event invited users (Many-to-Many relationship)
CREATE TABLE IF NOT EXISTS api_event_invited_users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    event_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_event_invited_event FOREIGN KEY (event_id) REFERENCES api_event(id) ON DELETE CASCADE,
    CONSTRAINT fk_event_invited_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_event_user (event_id, user_id),
    INDEX idx_invited_event (event_id),
    INDEX idx_invited_user (user_id)
) 

-- RSVP table
CREATE TABLE IF NOT EXISTS api_rsvp (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    status VARCHAR(20) NOT NULL DEFAULT 'going',
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    event_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_rsvp_event FOREIGN KEY (event_id) REFERENCES api_event(id) ON DELETE CASCADE,
    CONSTRAINT fk_rsvp_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_rsvp (event_id, user_id),
    INDEX idx_rsvp_event (event_id),
    INDEX idx_rsvp_user (user_id),
    INDEX idx_rsvp_status (status),
    INDEX idx_rsvp_created (created_at),
    CHECK (status IN ('going', 'maybe', 'not_going'))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Review table
CREATE TABLE IF NOT EXISTS api_review (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    rating INT NOT NULL,
    comment TEXT NOT NULL,
    created_at DATETIME(6) NOT NULL,
    updated_at DATETIME(6) NOT NULL,
    event_id BIGINT NOT NULL,
    user_id INT NOT NULL,
    CONSTRAINT fk_review_event FOREIGN KEY (event_id) REFERENCES api_event(id) ON DELETE CASCADE,
    CONSTRAINT fk_review_user FOREIGN KEY (user_id) REFERENCES auth_user(id) ON DELETE CASCADE,
    UNIQUE KEY unique_review (event_id, user_id),
    INDEX idx_review_event (event_id),
    INDEX idx_review_user (user_id),
    INDEX idx_review_rating (rating),
    INDEX idx_review_created (created_at),
    CHECK (rating >= 1 AND rating <= 5)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Create a user for the application (OPTIONAL - Update with your credentials)
-- CREATE USER IF NOT EXISTS 'event_app_user'@'localhost' IDENTIFIED BY 'your_secure_password';
-- GRANT ALL PRIVILEGES ON event_management_db.* TO 'event_app_user'@'localhost';
-- FLUSH PRIVILEGES;

-- Sample indexes for performance optimization
CREATE INDEX idx_event_public_start ON api_event(is_public, start_time);
CREATE INDEX idx_rsvp_event_status ON api_rsvp(event_id, status);
CREATE INDEX idx_review_event_rating ON api_review(event_id, rating);

-- End of schema   