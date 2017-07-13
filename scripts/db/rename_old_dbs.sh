# This script renames the old dbs and keeps three backups - it assumes the presence of an eRacks user.
# So create the eracks user first if you don't already have one (eg, a new instance).

sudo -u postgres psql <<EOF

-- Ensure no other tasks are accessing pg db - should be only one row (me)
SELECT * FROM pg_stat_activity;

-- Keep three backups - drop oldest one and rename others:
DROP DATABASE IF EXISTS eracksdb_old3;
ALTER DATABASE eracksdb_old2 RENAME TO eracksdb_old3;
ALTER DATABASE eracksdb_old RENAME TO eracksdb_old2;
ALTER DATABASE eracksdb RENAME TO eracksdb_old;

-- Now, create new eracks db
CREATE DATABASE eracksdb owner eracks;

-- Now, update comments appropriately
COMMENT ON DATABASE eracksdb is 'Copy of eRacks Production Database for dev';
COMMENT ON DATABASE eracksdb_old is 'Old copy of eRacks Production Database for dev';
COMMENT ON DATABASE eracksdb_old2 is 'Older copy of eRacks Production Database for dev';
COMMENT ON DATABASE eracksdb_old3 is 'Oldest copy of eRacks Production Database for dev';

EOF

