# This script creates an eracks user 

sudo -u postgres psql <<EOF
create user eracks with unencrypted password 'Wav3lets9';
EOF

echo PostgreSQL user eracks should now be present


