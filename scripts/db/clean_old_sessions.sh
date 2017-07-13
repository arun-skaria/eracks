# Clean old sessions, compact / vacuum db

sudo -u postgres psql <<EOF

-- Connect to eracksdb - could also use ./manage.py dbshell
\c eracksdb

-- Show size beforehand
SELECT pg_size_pretty(pg_total_relation_size('django_session'));

-- Delete old sessions which expired prior to today/now
DELETE FROM django_session WHERE expire_date <now();

-- Vacuum the sessions table, by far the largest (typically ~250MB after vacuum)
VACUUM FULL django_session;

-- Show size afterward
SELECT pg_size_pretty(pg_total_relation_size('django_session'));

-- vacuum whole db too
VACUUM FULL;

EOF

