DROP TABLE IF EXISTS votes;
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    round_id INTEGER,
    vote INTEGER NOT NULL,
    username VARCHAR(100) NOT NULL,
    UNIQUE(username, round_id)
);


DROP TABLE IF EXISTS rounds;
CREATE TABLE rounds (
    id SERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ
);


ALTER TABLE votes
    ADD CONSTRAINT fk_round_id
        FOREIGN KEY (round_id)
        REFERENCES rounds(id)

