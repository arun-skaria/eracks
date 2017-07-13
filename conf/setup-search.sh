echo SET UP SEARCH
cd eracks
pwd
mkdir -p whoosh_index
chmod -R g+w whoosh_index/
chown -R www-data:www-data whoosh_index/
../manage.py rebuild_index --noinput
chmod -R g+w whoosh_index/
chown -R www-data:www-data whoosh_index/
# ln -r would also work, but leaves messy ../../ in front
ln -vs $(dirname `pwd`)/scripts/cron/update_index.sh /etc/cron.hourly/update_eracks_search_index
echo SET UP SEARCH DONE
