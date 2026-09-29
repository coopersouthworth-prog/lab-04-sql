
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    user_id     INT          NOT NULL,
    username    VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL,
    created_at  DATETIME     NOT NULL,
    PRIMARY KEY (user_id)
);

CREATE TABLE posts (
    post_id    INT          NOT NULL,
    user_id    INT          NOT NULL,
    title      VARCHAR(200) NOT NULL,
    body       TEXT,
    posted_at  DATETIME     NOT NULL,
    PRIMARY KEY (post_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- Seed users
INSERT INTO users VALUES (1,  'alice',   'alice@example.com',   '2026-01-05 09:00:00');
INSERT INTO users VALUES (2,  'bob',     'bob@example.com',     '2026-01-12 14:30:00');
INSERT INTO users VALUES (3,  'carmen',  'carmen@example.com',  '2026-02-01 08:15:00');
INSERT INTO users VALUES (4,  'dev',     'dev@example.com',     '2026-02-20 19:45:00');
INSERT INTO users VALUES (5,  'elena',   'elena@example.com',   '2026-03-03 11:10:00');
INSERT INTO users VALUES (6,  'farid',   'farid@example.com',   '2026-03-18 16:00:00');
INSERT INTO users VALUES (7,  'grace',   'grace@example.com',   '2026-04-09 10:20:00');
INSERT INTO users VALUES (8,  'hiro',    'hiro@example.com',    '2026-05-14 13:05:00');
INSERT INTO users VALUES (9,  'imani',   'imani@example.com',   '2026-06-22 07:50:00');
INSERT INTO users VALUES (10, 'jonah',   'jonah@example.com',   '2026-07-30 21:40:00');

-- Seed posts (every user_id must exist in users)
INSERT INTO posts VALUES (101, 1,  'Hello world',            'My first post!',                    '2026-08-01 10:00:00');
INSERT INTO posts VALUES (102, 2,  'Learning SQL',           'JOINs finally make sense.',         '2026-08-03 12:15:00');
INSERT INTO posts VALUES (103, 1,  'Weekend hike',           'Photos from McAfee Knob.',          '2026-08-10 18:30:00');
INSERT INTO posts VALUES (104, 3,  'Coffee rankings',        'Ranking every cafe on the Corner.', '2026-08-15 08:45:00');
INSERT INTO posts VALUES (105, 4,  'Python tips',            'Use f-strings, but not in SQL.',    '2026-08-21 15:00:00');
INSERT INTO posts VALUES (106, 5,  'Book review',            'Thoughts on a great novel.',        '2026-09-02 20:10:00');
INSERT INTO posts VALUES (107, 6,  'Pandas vs SQL',          'When to use which.',                '2026-09-07 09:30:00');
INSERT INTO posts VALUES (108, 7,  'Garden update',          'Tomatoes are finally red.',         '2026-09-12 17:25:00');
INSERT INTO posts VALUES (109, 2,  'Indexes explained',      'Why queries get faster.',           '2026-09-18 11:55:00');
INSERT INTO posts VALUES (110, 10, 'Fall playlist',          'Songs for studying.',               '2026-09-25 22:00:00');
