CREATE TABLE rounds (
    id SERIAL PRIMARY KEY,
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    winner_vote_id INTEGER
);
CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    round_id INTEGER,
    vote INTEGER NOT NULL,
    username VARCHAR(100) NOT NULL,
    UNIQUE(username, round_id)
);

ALTER TABLE rounds
    ADD CONSTRAINT fk_winner_vote_id 
        FOREIGN KEY (winner_vote_id) 
        REFERENCES votes(id);

ALTER TABLE votes
    ADD CONSTRAINT fk_round_id
        FOREIGN KEY (round_id)
        REFERENCES rounds(id)

