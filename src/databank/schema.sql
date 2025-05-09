CREATE TABLE IF NOT EXISTS users (
  user_id BIGINT PRIMARY KEY,
  color TEXT,
  bodyweight DECIMAL,

  count INT DEFAULT 0, /* pushups todo */
  done INT NOT NULL DEFAULT 0, /*pushups done */

  pushups_to_clear INT DEFAULT 0 /* to clear before double or nothing can be used again */
);

CREATE TABLE IF NOT EXISTS pr (
  id SERIAL PRIMARY KEY,
  user_id varchar(30) NOT NULL,
  exercise varchar(75) NOT NULL,
  weight decimal NOT NULL DEFAULT 0,
  lifted_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS reps (
  id SERIAL PRIMARY KEY,
  user_id varchar(30) NOT NULL,
  exercise varchar(75) NOT NULL,
  weight decimal NOT NULL DEFAULT 0,
  lifted_at timestamp DEFAULT CURRENT_TIMESTAMP,
  reps INTEGER NOT NULL DEFAULT 0
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

CREATE TABLE IF NOT EXISTS pushup_event (
  id SERIAL PRIMARY KEY,
  user_id BIGINT NOT NULL,
  amount INT NOT NULL,
  reason TEXT NOT NULL,
  date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

ALTER TABLE pushup_event ADD COLUMN IF NOT EXISTS date TIMESTAMP DEFAULT CURRENT_TIMESTAMP; 