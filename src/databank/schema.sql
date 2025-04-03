CREATE TABLE IF NOT EXISTS pr (
  id SERIAL PRIMARY KEY,
  user_id varchar(30) NOT NULL,
  exercise varchar(75) NOT NULL,
  weight decimal NOT NULL DEFAULT 0,
  lifted_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS schema (
  id SERIAL PRIMARY KEY,
  monday varchar(256) NOT NULL,
  tuesday varchar(256) NOT NULL,
  wednesday varchar(256) NOT NULL,
  thursday varchar(256) NOT NULL,
  friday varchar(256) NOT NULL,
  saturday varchar(256) NOT NULL,
  sunday varchar(256) NOT NULL
);

CREATE TABLE IF NOT EXISTS reps (
  id SERIAL PRIMARY KEY,
  user_id varchar(30) NOT NULL,
  exercise varchar(75) NOT NULL,
  weight decimal NOT NULL DEFAULT 0,
  lifted_at timestamp DEFAULT CURRENT_TIMESTAMP,
  reps INTEGER NOT NULL DEFAULT 0
);
 
CREATE TABLE IF NOT EXISTS reminders (
  id SERIAL PRIMARY KEY,
  user_id varchar(20) NOT NULL,
  subject varchar(100) NOT NULL,
  time timestamp NOT NULL
);

CREATE TABLE IF NOT EXISTS bangamble (
  id SERIAL PRIMARY KEY,
  user_id varchar(20) NOT NULL,
  current_win_streak INTEGER DEFAULT 0,
  highest_win_streak INTEGER DEFAULT 0,
  current_loss_streak INTEGER DEFAULT 0,
  highest_loss_streak INTEGER DEFAULT 0,
  total_wins INTEGER DEFAULT 0,
  total_losses INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS pushups (
  user_id BIGINT PRIMARY KEY,
  count INT DEFAULT 0,
  double_or_nothing_used BOOLEAN DEFAULT FALSE
);

-- Nodig voor als table al bestond
ALTER TABLE pushups ADD COLUMN IF NOT EXISTS double_or_nothing_used BOOLEAN DEFAULT FALSE;

CREATE TABLE IF NOT EXISTS pushups_done (
  user_id BIGINT PRIMARY KEY,
  count INT NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS badges (
  id SERIAL PRIMARY KEY,  
  name TEXT UNIQUE NOT NULL,  -- Name of the badge
  description TEXT,  -- Short description of the badge
  icon_url TEXT,  -- URL to badge image/icon
  rarity TEXT CHECK (rarity IN ('Common', 'Rare', 'Epic', 'Legendary')) NOT NULL DEFAULT 'Common',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS user_badges (
  user_id BIGINT NOT NULL,
  badge_id INTEGER REFERENCES badges(id) ON DELETE CASCADE,
  earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (user_id, badge_id)
);