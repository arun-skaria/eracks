## Run this to load a new db from scratch - BE CAREFUL

echo BE CAREFUL - this overwites the entrie database -

exit

** upd for nat keys JJW 9/29

./manage.py loaddata apps/bloglets/fixtures/bloglets-all.yaml
./manage.py loaddata apps/customers/fixtures/customers-all.yaml
./manage.py loaddata apps/products/fixtures/products-all.yaml
./manage.py loaddata apps/sqls/fixtures/sqls-all.yaml
./manage.py loaddata apps/catax/fixtures/catax-all.yaml
./manage.py loaddata apps/home/fixtures/home-all.yaml
./manage.py loaddata apps/orders/fixtures/orders-all.yaml
./manage.py loaddata apps/quotes/fixtures/quotes-all.yaml
./manage.py loaddata fixtures/quickpages-all.yaml
./manage.py loaddata fixtures/auth-all.yaml


# bloglets
# customers
# products
# sqls
# catax
# home
# orders
# quotes
# quickpages
#
# auth?
