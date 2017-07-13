echo SET UP DB - USER & DBNAME
./scripts/db/ensure_eracks_user.sh
./scripts/db/rename_old_dbs.sh
echo SET UP DB - MIGRATE
./manage.py migrate
echo SET UP DB - LOAD FIXTURES

./manage.py loaddata fixtures/contenttypes.yaml 2>&1
./manage.py loaddata fixtures/auth.permission.yaml 2>&1
./manage.py loaddata fixtures/all.yaml 2>&1

#./manage.py loaddata apps/bloglets/fixtures/bloglets-all.yaml
#./manage.py loaddata apps/customers/fixtures/customers-all.yaml
#./manage.py loaddata apps/products/fixtures/products-all.yaml
#./manage.py loaddata apps/sqls/fixtures/sqls-all.yaml
#./manage.py loaddata apps/catax/fixtures/catax-all.yaml
#./manage.py loaddata apps/home/fixtures/home-all.yaml
#./manage.py loaddata apps/orders/fixtures/orders-all.yaml
#./manage.py loaddata apps/quotes/fixtures/quotes-all.yaml
#./manage.py loaddata fixtures/quickpages-all.yaml
echo SET UP DB DONE
