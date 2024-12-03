CREATE TABLE IF NOT EXISTS pr (
 id SERIAL PRIMARY KEY,
 user_id varchar(30) NOT NULL,
 exercise varchar(30) NOT NULL,
 weight decimal NOT NULL DEFAULT 0,
 lifted_at timestamp DEFAULT CURRENT_TIMESTAMP
);
