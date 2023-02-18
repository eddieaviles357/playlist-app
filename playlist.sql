DROP DATABASE IF EXISTS playlist_app;

CREATE DATABASE playlist_app;

\c playlist_app

CREATE TABLE playlists
(
    id SERIAL PRIMARY KEY,
    name VARCHAR(30) NOT NULL,
    description VARCHAR(50) NOT NULL
);

CREATE TABLE songs
(
    id SERIAL PRIMARY KEY,
    title VARCHAR(30) NOT NULL,
    artist VARCHAR(30) NOT NULL
);

CREATE TABLE playlists_songs
(
    playlist_id INTEGER REFERENCES playlists ON DELETE CASCADE,
    song_id INTEGER REFERENCES songs ON DELETE CASCADE,
    PRIMARY KEY (playlist_id, song_id)
);

INSERT INTO playlists (name, description)
VALUES
('cool-list', 'coolest songs'),
('best-list', 'bestest songs'),
('relax-list', 'relaxing songs');

INSERT INTO songs (title, artist)
VALUES
('coolio', 'Mr. Cool'),
('ice', 'Mr. Cool'),
('besties', 'Mrs. Beast'),
('bye', 'Mrs. Beast'),
('gon', 'Senor Gon'),
('killua', 'Senor Gon');

INSERT INTO playlists_songs (playlist_id, song_id)
VALUES
(1, 1),
(1, 2),
(2, 3),
(2, 4),
(3, 6);