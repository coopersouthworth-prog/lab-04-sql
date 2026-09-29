-- media_query.sql: posts from September 2026 with author info
SELECT u.username,
       u.email,
       p.title,
       p.posted_at
FROM posts AS p
JOIN users AS u
  ON p.user_id = u.user_id
WHERE p.posted_at >= '2026-09-01'
ORDER BY p.posted_at;
