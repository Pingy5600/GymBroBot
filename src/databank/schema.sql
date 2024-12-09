CREATE TABLE IF NOT EXISTS pr (
 id SERIAL PRIMARY KEY,
 user_id varchar(30) NOT NULL,
 exercise varchar(30) NOT NULL,
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

 