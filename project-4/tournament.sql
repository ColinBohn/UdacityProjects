-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

create table matches(
    winner INT NOT NULL,
    loser INT NOT NULL
);
create table players(
    id SERIAL,
    name TEXT NOT NULL,
    PRIMARY KEY (id)
);

create view standings AS
SELECT
p.id AS id,
p.name AS name,
(SELECT COUNT(1) FROM matches m WHERE m.winner = p.id) AS wins,
(SELECT COUNT(1) FROM matches m WHERE m.winner = p.id OR m.loser = p.id) AS matches
FROM PLAYERS p 
GROUP BY p.id
ORDER BY wins desc;