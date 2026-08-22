-- ================================================================
-- Adaptive AI Placement Readiness System - Supabase Schema
-- Run this entire script in: Supabase Dashboard > SQL Editor
-- ================================================================

-- 1. Users / Students
CREATE TABLE IF NOT EXISTS users (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    target_role TEXT NOT NULL DEFAULT 'java_developer',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Assessment Sessions
CREATE TABLE IF NOT EXISTS assessment_sessions (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_type TEXT NOT NULL,
    target_role TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'in_progress',
    total_questions INTEGER DEFAULT 0,
    correct_count INTEGER DEFAULT 0,
    accuracy REAL DEFAULT 0.0,
    readiness_score REAL DEFAULT 0.0,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ DEFAULT NULL
);

-- 3. Response Logs
CREATE TABLE IF NOT EXISTS response_logs (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES assessment_sessions(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    question_id TEXT NOT NULL,
    selected_index INTEGER NOT NULL,
    is_correct INTEGER NOT NULL,
    response_time_sec REAL NOT NULL,
    subtopic TEXT NOT NULL,
    topic TEXT NOT NULL,
    skill TEXT NOT NULL,
    difficulty INTEGER NOT NULL,
    timestamp TIMESTAMPTZ DEFAULT NOW()
);

-- 4. Skill Mastery
CREATE TABLE IF NOT EXISTS skill_mastery (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    skill TEXT NOT NULL,
    topic TEXT NOT NULL,
    subtopic TEXT NOT NULL,
    mastery_score REAL NOT NULL DEFAULT 50.0,
    attempts_count INTEGER DEFAULT 0,
    correct_count INTEGER DEFAULT 0,
    avg_response_time REAL DEFAULT 0.0,
    last_updated TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, subtopic)
);

-- 5. Learning Roadmaps
CREATE TABLE IF NOT EXISTS learning_roadmaps (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    target_role TEXT NOT NULL,
    generated_at TIMESTAMPTZ DEFAULT NOW(),
    is_active INTEGER DEFAULT 1
);

-- 6. Roadmap Steps
CREATE TABLE IF NOT EXISTS roadmap_steps (
    id TEXT PRIMARY KEY,
    roadmap_id TEXT NOT NULL REFERENCES learning_roadmaps(id) ON DELETE CASCADE,
    day_number INTEGER NOT NULL,
    skill TEXT NOT NULL,
    topic TEXT NOT NULL,
    subtopic TEXT NOT NULL,
    action_title TEXT NOT NULL,
    explanation_summary TEXT NOT NULL,
    target_questions_count INTEGER DEFAULT 5,
    is_completed INTEGER DEFAULT 0,
    score_achieved REAL DEFAULT NULL
);

-- 7. Research Cohorts
CREATE TABLE IF NOT EXISTS experiment_cohorts (
    id TEXT PRIMARY KEY,
    cohort_name TEXT NOT NULL,
    group_type TEXT NOT NULL,
    student_id TEXT NOT NULL,
    pre_test_score REAL NOT NULL,
    post_test_score REAL NOT NULL,
    questions_attempted INTEGER NOT NULL,
    time_spent_mins REAL NOT NULL,
    weak_topics_improved INTEGER NOT NULL,
    readiness_gain REAL NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Disable RLS for all tables (service key bypasses, but good for dev)
ALTER TABLE users DISABLE ROW LEVEL SECURITY;
ALTER TABLE assessment_sessions DISABLE ROW LEVEL SECURITY;
ALTER TABLE response_logs DISABLE ROW LEVEL SECURITY;
ALTER TABLE skill_mastery DISABLE ROW LEVEL SECURITY;
ALTER TABLE learning_roadmaps DISABLE ROW LEVEL SECURITY;
ALTER TABLE roadmap_steps DISABLE ROW LEVEL SECURITY;
ALTER TABLE experiment_cohorts DISABLE ROW LEVEL SECURITY;
