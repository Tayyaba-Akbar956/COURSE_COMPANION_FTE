# SPEC-T-001-database-schema-v1.0

## Status
- [x] Draft
- [ ] Pending Approval
- [ ] Approved
- [ ] In Progress
- [ ] Completed
- [ ] Deprecated

## Metadata
- **Created:** 2026-03-29
- **Author:** Qwen Code (AI Builder)
- **Approved By:** [Pending User Approval]
- **Version:** 1.0.0

## 1. Overview

This spec defines the complete database schema for the Course Companion FTE application. All data is stored in PostgreSQL (Supabase) with proper indexing, relationships, and constraints to support the Phase 1 features.

## 2. Database Choice

**Technology:** PostgreSQL 15+ via Supabase  
**Rationale:**
- Relational data (users, chapters, progress, quizzes)
- Supabase provides auth + database in one platform
- Free tier generous (500MB, sufficient for MVP)
- Full SQL support with advanced features
- Row Level Security (RLS) for data privacy
- Automatic backups and point-in-time recovery

## 3. Entity Relationship Diagram

```
┌─────────────────┐       ┌─────────────────┐
│     users       │       │   subscriptions │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │───┬──▶│ id (PK)         │
│ email           │   │   │ user_id (FK)    │
│ created_at      │   │   │ tier            │
│ updated_at      │   │   │ status          │
└─────────────────┘   │   │ started_at      │
                      │   │ expires_at      │
                      │   └─────────────────┘
                      │
                      │   ┌─────────────────┐
                      │   │    chapters     │
                      │   ├─────────────────┤
                      │   │ id (PK)         │
                      │   │ chapter_number  │
                      │   │ module_id (FK)  │
                      │   │ title           │
                      │   │ content         │
                      │   │ is_free         │
                      │   └─────────────────┘
                      │
                      │   ┌─────────────────┐
                      │   │     modules     │
                      │   ├─────────────────┤
                      │   │ id (PK)         │
                      │   │ title           │
                      │   │ description     │
                      │   │ order           │
                      │   └─────────────────┘
                      │
                      │   ┌─────────────────┐
                      │   │   quiz_questions│
                      │   ├─────────────────┤
                      │   │ id (PK)         │
                      │   │ chapter_id (FK) │
                      │   │ question_text   │
                      │   │ options         │
                      │   │ correct_answer  │
                      │   └─────────────────┘
                      │
                      │   ┌─────────────────┐
                      │   │  chapter_progress│
                      │   ├─────────────────┤
                      │   │ id (PK)         │
                      │   │ user_id (FK)    │◀──┘
                      │   │ chapter_id (FK) │
                      │   │ completed       │
                      │   │ completed_at    │
                      │   └─────────────────┘
                      │
                      │   ┌─────────────────┐
                      │   │   quiz_attempts │
                      │   ├─────────────────┤
                      │   │ id (PK)         │
                      │   │ user_id (FK)    │◀──┘
                      │   │ chapter_id (FK) │
                      │   │ score           │
                      │   │ answers         │
                      │   └─────────────────┘
                      │
                      │   ┌─────────────────┐
                      │   │   achievements  │
                      │   ├─────────────────┤
                      │   │ id (PK)         │
                      │   │ name            │
                      │   │ description     │
                      │   │ icon            │
                      │   │ criteria        │
                      │   └─────────────────┘
                      │
                      │   ┌─────────────────┐
                      │   │user_achievements│
                      │   ├─────────────────┤
                      │   │ id (PK)         │
                      │   │ user_id (FK)    │◀──┘
                      │   │ achievement_id  │
                      │   │ unlocked_at     │
                      │   └─────────────────┘
```

## 4. Table Definitions

### 4.1 users

Stores user account information (managed by Supabase Auth, mirrored here)

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255),
    avatar_url VARCHAR(500),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_created_at ON users(created_at);

-- Triggers for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 4.2 modules

Stores course module information

```sql
CREATE TABLE modules (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    module_order INTEGER NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_modules_order ON modules(module_order);

-- Sample data (6 modules for Generative AI Fundamentals)
INSERT INTO modules (title, description, module_order) VALUES
('Introduction to Generative AI', 'Foundational concepts in generative AI', 1),
('Understanding Large Language Models', 'Deep dive into LLMs and transformers', 2),
('Prompt Engineering Fundamentals', 'Master the art of prompting', 3),
('Retrieval Augmented Generation', 'Build RAG systems', 4),
('Fine-tuning and Customization', 'Customize models for your needs', 5),
('Building Generative AI Applications', 'Deploy production AI apps', 6);
```

### 4.3 chapters

Stores course chapter content and metadata

```sql
CREATE TABLE chapters (
    id SERIAL PRIMARY KEY,
    chapter_number INTEGER NOT NULL,
    module_id INTEGER NOT NULL REFERENCES modules(id) ON DELETE CASCADE,
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    content_html TEXT,
    is_free BOOLEAN DEFAULT FALSE,
    estimated_minutes INTEGER DEFAULT 15,
    order_in_module INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(module_id, chapter_number),
    UNIQUE(module_id, order_in_module)
);

-- Indexes
CREATE INDEX idx_chapters_module_id ON chapters(module_id);
CREATE INDEX idx_chapters_number ON chapters(chapter_number);
CREATE INDEX idx_chapters_is_free ON chapters(is_free);
CREATE INDEX idx_chapters_full_text ON chapters USING GIN(to_tsvector('english', title || ' ' || content));

-- Triggers
CREATE TRIGGER update_chapters_updated_at
    BEFORE UPDATE ON chapters
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 4.4 subscriptions

Stores user subscription information

```sql
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    tier VARCHAR(50) NOT NULL DEFAULT 'free',
    status VARCHAR(50) NOT NULL DEFAULT 'free',
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE,
    auto_renew BOOLEAN DEFAULT FALSE,
    stripe_subscription_id VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_tier CHECK (tier IN ('free', 'premium', 'pro', 'team')),
    CONSTRAINT valid_status CHECK (status IN ('free', 'active', 'cancelled', 'expired', 'past_due'))
);

-- Indexes
CREATE INDEX idx_subscriptions_user_id ON subscriptions(user_id);
CREATE INDEX idx_subscriptions_tier ON subscriptions(tier);
CREATE INDEX idx_subscriptions_status ON subscriptions(status);
CREATE INDEX idx_subscriptions_expires_at ON subscriptions(expires_at);

-- Triggers
CREATE TRIGGER update_subscriptions_updated_at
    BEFORE UPDATE ON subscriptions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 4.5 chapter_progress

Tracks user progress on chapters

```sql
CREATE TABLE chapter_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMP WITH TIME ZONE,
    time_spent_seconds INTEGER DEFAULT 0,
    last_accessed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, chapter_id)
);

-- Indexes
CREATE INDEX idx_chapter_progress_user_id ON chapter_progress(user_id);
CREATE INDEX idx_chapter_progress_chapter_id ON chapter_progress(chapter_id);
CREATE INDEX idx_chapter_progress_completed ON chapter_progress(completed);
CREATE INDEX idx_chapter_progress_user_completed ON chapter_progress(user_id, completed);

-- Triggers
CREATE TRIGGER update_chapter_progress_updated_at
    BEFORE UPDATE ON chapter_progress
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 4.6 quiz_questions

Stores quiz questions for each chapter

```sql
CREATE TABLE quiz_questions (
    id SERIAL PRIMARY KEY,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    question_text TEXT NOT NULL,
    options JSONB NOT NULL, -- [{"id": "A", "text": "..."}, {"id": "B", "text": "..."}]
    correct_answer VARCHAR(10) NOT NULL,
    explanation TEXT,
    why_wrong TEXT,
    source_reference VARCHAR(500),
    difficulty VARCHAR(20) DEFAULT 'medium',
    order_in_chapter INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_difficulty CHECK (difficulty IN ('easy', 'medium', 'hard'))
);

-- Indexes
CREATE INDEX idx_quiz_questions_chapter_id ON quiz_questions(chapter_id);
CREATE INDEX idx_quiz_questions_difficulty ON quiz_questions(difficulty);
CREATE INDEX idx_quiz_questions_full_text ON quiz_questions USING GIN(to_tsvector('english', question_text));

-- Triggers
CREATE TRIGGER update_quiz_questions_updated_at
    BEFORE UPDATE ON quiz_questions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

### 4.7 quiz_attempts

Stores user quiz attempt history

```sql
CREATE TABLE quiz_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter_id INTEGER NOT NULL REFERENCES chapters(id) ON DELETE CASCADE,
    quiz_session_id VARCHAR(255) NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    correct_answers INTEGER NOT NULL,
    incorrect_answers INTEGER NOT NULL,
    passed BOOLEAN NOT NULL,
    passing_score INTEGER DEFAULT 80,
    answers JSONB NOT NULL, -- [{"question_id": 1, "answer": "A", "is_correct": true}]
    time_taken_seconds INTEGER,
    attempt_number INTEGER NOT NULL,
    submitted_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    CONSTRAINT valid_score CHECK (score >= 0 AND score <= 100)
);

-- Indexes
CREATE INDEX idx_quiz_attempts_user_id ON quiz_attempts(user_id);
CREATE INDEX idx_quiz_attempts_chapter_id ON quiz_attempts(chapter_id);
CREATE INDEX idx_quiz_attempts_submitted_at ON quiz_attempts(submitted_at);
CREATE INDEX idx_quiz_attempts_user_chapter ON quiz_attempts(user_id, chapter_id);
CREATE INDEX idx_quiz_attempts_passed ON quiz_attempts(passed);

-- Unique constraint for quiz session
CREATE UNIQUE INDEX idx_quiz_attempts_session_id ON quiz_attempts(quiz_session_id);
```

### 4.8 achievements

Stores achievement definitions

```sql
CREATE TABLE achievements (
    id VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    icon VARCHAR(50) NOT NULL,
    criteria JSONB NOT NULL, -- {"type": "chapter_completion", "count": 1}
    achievement_order INTEGER NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_achievements_order ON achievements(achievement_order);
CREATE INDEX idx_achievements_active ON achievements(is_active);

-- Sample data
INSERT INTO achievements (id, name, description, icon, criteria, achievement_order) VALUES
('first_chapter', 'First Steps', 'Complete your first chapter', '🏅', '{"type": "chapter_completion", "count": 1}', 1),
('quiz_perfect', 'Perfectionist', 'Get 100% on any quiz', '🎯', '{"type": "quiz_score", "score": 100}', 2),
('streak_5', 'Consistent Learner', '5-day learning streak', '🔥', '{"type": "streak", "days": 5}', 3),
('streak_10', 'Dedicated Scholar', '10-day learning streak', '⚡', '{"type": "streak", "days": 10}', 4),
('module_master', 'Module Master', 'Complete all chapters in a module', '🎓', '{"type": "module_completion", "count": 1}', 5),
('course_complete', 'Graduate', 'Complete the entire course', '🎉', '{"type": "chapter_completion", "count": 24}', 6);
```

### 4.9 user_achievements

Stores user-achievement mappings (unlocked achievements)

```sql
CREATE TABLE user_achievements (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    achievement_id VARCHAR(100) NOT NULL REFERENCES achievements(id) ON DELETE CASCADE,
    unlocked_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, achievement_id)
);

-- Indexes
CREATE INDEX idx_user_achievements_user_id ON user_achievements(user_id);
CREATE INDEX idx_user_achievements_achievement_id ON user_achievements(achievement_id);
CREATE INDEX idx_user_achievements_unlocked_at ON user_achievements(unlocked_at);
```

### 4.10 daily_streaks

Tracks daily activity for streak calculation

```sql
CREATE TABLE daily_streaks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    activity_date DATE NOT NULL,
    chapters_completed INTEGER DEFAULT 0,
    quizzes_taken INTEGER DEFAULT 0,
    minutes_spent INTEGER DEFAULT 0,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(user_id, activity_date)
);

-- Indexes
CREATE INDEX idx_daily_streaks_user_id ON daily_streaks(user_id);
CREATE INDEX idx_daily_streaks_activity_date ON daily_streaks(activity_date);
CREATE INDEX idx_daily_streaks_user_date ON daily_streaks(user_id, activity_date);

-- Triggers
CREATE TRIGGER update_daily_streaks_updated_at
    BEFORE UPDATE ON daily_streaks
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
```

## 5. Views

### 5.1 user_progress_summary

Materialized view for quick progress queries

```sql
CREATE MATERIALIZED VIEW user_progress_summary AS
SELECT 
    u.id AS user_id,
    COUNT(DISTINCT cp.chapter_id) FILTER (WHERE cp.completed = true) AS chapters_completed,
    COUNT(DISTINCT c.id) AS total_chapters,
    ROUND(COUNT(DISTINCT cp.chapter_id) FILTER (WHERE cp.completed = true) * 100.0 / NULLIF(COUNT(DISTINCT c.id), 0), 2) AS completion_percentage,
    COUNT(DISTINCT qa.id) AS total_quiz_attempts,
    AVG(qa.score) AS average_quiz_score,
    MAX(qa.score) AS best_quiz_score,
    SUM(cp.time_spent_seconds) / 60 AS total_minutes_spent,
    MAX(cp.last_accessed_at) AS last_activity
FROM users u
CROSS JOIN chapters c
LEFT JOIN chapter_progress cp ON u.id = cp.user_id AND c.id = cp.chapter_id
LEFT JOIN quiz_attempts qa ON u.id = qa.user_id
GROUP BY u.id;

-- Index on materialized view
CREATE UNIQUE INDEX idx_user_progress_summary_user_id ON user_progress_summary(user_id);

-- Refresh function
CREATE OR REPLACE FUNCTION refresh_user_progress_summary()
RETURNS void AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY user_progress_summary;
END;
$$ LANGUAGE plpgsql;
```

### 5.2 module_progress_view

View for module-level progress

```sql
CREATE VIEW module_progress_view AS
SELECT 
    m.id AS module_id,
    m.title AS module_title,
    m.module_order,
    u.id AS user_id,
    COUNT(c.id) AS total_chapters,
    COUNT(cp.chapter_id) FILTER (WHERE cp.completed = true) AS completed_chapters,
    ROUND(COUNT(cp.chapter_id) FILTER (WHERE cp.completed = true) * 100.0 / NULLIF(COUNT(c.id), 0), 2) AS completion_percentage,
    AVG(qa.score) AS average_quiz_score
FROM modules m
CROSS JOIN users u
LEFT JOIN chapters c ON m.id = c.module_id
LEFT JOIN chapter_progress cp ON u.id = cp.user_id AND c.id = cp.chapter_id AND cp.completed = true
LEFT JOIN quiz_attempts qa ON u.id = qa.user_id AND c.id = qa.chapter_id
GROUP BY m.id, m.title, m.module_order, u.id;
```

## 6. Row Level Security (RLS)

Enable RLS for data privacy:

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE subscriptions ENABLE ROW LEVEL SECURITY;
ALTER TABLE chapter_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE quiz_attempts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_achievements ENABLE ROW LEVEL SECURITY;
ALTER TABLE daily_streaks ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY users_select_own ON users
    FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY subscriptions_select_own ON subscriptions
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY chapter_progress_select_own ON chapter_progress
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY chapter_progress_insert_own ON chapter_progress
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY chapter_progress_update_own ON chapter_progress
    FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY quiz_attempts_select_own ON quiz_attempts
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY quiz_attempts_insert_own ON quiz_attempts
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY user_achievements_select_own ON user_achievements
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY daily_streaks_select_own ON daily_streaks
    FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY daily_streaks_insert_own ON daily_streaks
    FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY daily_streaks_update_own ON daily_streaks
    FOR UPDATE
    USING (auth.uid() = user_id);
```

## 7. Database Functions

### 7.1 Calculate Current Streak

```sql
CREATE OR REPLACE FUNCTION calculate_current_streak(user_uuid UUID)
RETURNS INTEGER AS $$
DECLARE
    streak_count INTEGER := 0;
    current_date_val DATE := CURRENT_DATE;
    activity_date_val DATE;
BEGIN
    -- Check if user has activity today or yesterday (streak still active)
    SELECT MAX(activity_date) INTO activity_date_val
    FROM daily_streaks
    WHERE user_id = user_uuid
    AND activity_date >= current_date_val - INTERVAL '1 day';
    
    IF activity_date_val IS NULL OR activity_date_val < current_date_val - INTERVAL '1 day' THEN
        RETURN 0;
    END IF;
    
    -- Count consecutive days
    SELECT COUNT(*) INTO streak_count
    FROM (
        SELECT activity_date,
               ROW_NUMBER() OVER (ORDER BY activity_date DESC) AS rn
        FROM daily_streaks
        WHERE user_id = user_uuid
        AND activity_date <= current_date_val
        ORDER BY activity_date DESC
    ) consecutive
    WHERE activity_date = current_date_val - (rn - 1);
    
    RETURN streak_count;
END;
$$ LANGUAGE plpgsql STABLE;
```

### 7.2 Check and Award Achievements

```sql
CREATE OR REPLACE FUNCTION check_and_award_achievements(user_uuid UUID)
RETURNS TABLE(achievement_id VARCHAR, achievement_name VARCHAR) AS $$
DECLARE
    ach RECORD;
    chapters_completed INTEGER;
    best_quiz_score INTEGER;
    current_streak INTEGER;
    modules_completed INTEGER;
BEGIN
    -- Get user stats
    SELECT COUNT(*) INTO chapters_completed
    FROM chapter_progress
    WHERE user_id = user_uuid AND completed = true;
    
    SELECT MAX(score) INTO best_quiz_score
    FROM quiz_attempts
    WHERE user_id = user_uuid;
    
    SELECT calculate_current_streak(user_uuid) INTO current_streak;
    
    SELECT COUNT(DISTINCT m.id) INTO modules_completed
    FROM modules m
    WHERE NOT EXISTS (
        SELECT 1 FROM chapters c
        LEFT JOIN chapter_progress cp ON c.id = cp.chapter_id AND cp.user_id = user_uuid
        WHERE c.module_id = m.id AND (cp.chapter_id IS NULL OR cp.completed = false)
    );
    
    -- Check each achievement
    FOR ach IN SELECT * FROM achievements WHERE is_active = true LOOP
        -- Check if already unlocked
        IF NOT EXISTS (SELECT 1 FROM user_achievements WHERE user_id = user_uuid AND achievement_id = ach.id) THEN
            -- Check criteria based on achievement type
            IF ach.criteria->>'type' = 'chapter_completion' AND chapters_completed >= (ach.criteria->>'count')::INTEGER THEN
                INSERT INTO user_achievements (user_id, achievement_id) VALUES (user_uuid, ach.id);
                RETURN NEXT;
            ELSIF ach.criteria->>'type' = 'quiz_score' AND best_quiz_score >= (ach.criteria->>'score')::INTEGER THEN
                INSERT INTO user_achievements (user_id, achievement_id) VALUES (user_uuid, ach.id);
                RETURN NEXT;
            ELSIF ach.criteria->>'type' = 'streak' AND current_streak >= (ach.criteria->>'days')::INTEGER THEN
                INSERT INTO user_achievements (user_id, achievement_id) VALUES (user_uuid, ach.id);
                RETURN NEXT;
            ELSIF ach.criteria->>'type' = 'module_completion' AND modules_completed >= (ach.criteria->>'count')::INTEGER THEN
                INSERT INTO user_achievements (user_id, achievement_id) VALUES (user_uuid, ach.id);
                RETURN NEXT;
            END IF;
        END IF;
    END LOOP;
    
    RETURN;
END;
$$ LANGUAGE plpgsql;
```

## 8. Migrations

Use Alembic for database migrations:

```bash
# Initialize Alembic
cd backend
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Initial schema creation"

# Apply migration
alembic upgrade head
```

## 9. Testing Requirements

### Test Scenarios

```python
def test_database_users_table_created():
    """Users table should exist with correct columns"""
    # Assert: Table exists, has id, email, created_at columns

def test_database_chapters_table_created():
    """Chapters table should exist with correct columns"""
    # Assert: Table exists, has id, chapter_number, module_id, title, content columns

def test_database_rls_enabled():
    """Row Level Security should be enabled on user tables"""
    # Assert: RLS policies exist for users, chapter_progress, quiz_attempts

def test_database_calculate_streak_function():
    """Streak calculation function should work correctly"""
    # Arrange: User with 5 consecutive days of activity
    # Act: SELECT calculate_current_streak(user_id)
    # Assert: Returns 5

def test_database_achievement_award_function():
    """Achievement award function should unlock achievements"""
    # Arrange: User completes first chapter
    # Act: SELECT check_and_award_achievements(user_id)
    # Assert: first_chapter achievement unlocked
```

## 10. Open Questions

1. **Content Storage:** Should chapter content be in database or Cloudflare R2? (Currently in DB for simplicity)
2. **Quiz Session Tracking:** Should quiz sessions be a separate table? (Currently just session_id in attempts)
3. **Materialized View Refresh:** How often to refresh user_progress_summary? (On every update, hourly, daily?)
4. **Soft Deletes:** Should we implement soft deletes for chapters/users? (Currently hard deletes only)

## 11. Revision History

| Version | Date | Changes | Author |
|---------|------|---------|--------|
| 1.0 | 2026-03-29 | Initial draft | Qwen Code |

---

## 📋 APPROVAL REQUEST

**What:** Database Schema Spec (SPEC-T-001-database-schema-v1.0)  
**Why:** Defines complete database structure for all Phase 1 features  
**Files Affected:** 
- `docs/specs/technical/SPEC-T-001-database-schema-v1.0.md`

**Key Decisions:**
- PostgreSQL via Supabase (free tier, auth included)
- 10 tables: users, modules, chapters, subscriptions, chapter_progress, quiz_questions, quiz_attempts, achievements, user_achievements, daily_streaks
- Row Level Security for data privacy
- Materialized views for performance
- Database functions for streak calculation and achievement awards
- Alembic for migrations

**Do you approve this spec?** (Yes/No/Modify)

---

**Progress Update:**
- ✅ Phase 1 Feature Specs: 6/6 Complete
- ✅ Technical Specs: 1/3 Started (SPEC-T-001 done, T-002 and T-003 remaining)
- ⏳ API Specs: 0/5 Pending
