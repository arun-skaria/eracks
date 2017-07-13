## Run this in prod, then check in, to update to the latest full db

./manage.py dumpdata --format=yaml bloglets     >apps/bloglets/fixtures/bloglets-all.yaml
./manage.py dumpdata --format=yaml customers    >apps/customers/fixtures/customers-all.yaml
./manage.py dumpdata --format=yaml products     >apps/products/fixtures/products-all.yaml
./manage.py dumpdata --format=yaml sqls         >apps/sqls/fixtures/sqls-all.yaml
./manage.py dumpdata --format=yaml catax        >apps/catax/fixtures/catax-all.yaml
./manage.py dumpdata --format=yaml home         >apps/home/fixtures/home-all.yaml
./manage.py dumpdata --format=yaml orders       >apps/orders/fixtures/orders-all.yaml
./manage.py dumpdata --format=yaml quotes       >apps/quotes/fixtures/quotes-all.yaml
./manage.py dumpdata --format=yaml quickpages   >fixtures/quickpages-all.yaml 

#./manage.py dumpdata --format=yaml --pks=160,161,162 auth.permission >fixtures/auth-all.yaml
#./manage.py dumpdata --format=yaml --exclude auth.permission --exclude auth.group_permissions auth >fixtures/auth-all.yaml

# not sure this one is needed now, check test suites - JJW 9/29/16
./manage.py dumpdata --format=yaml --exclude auth.permission auth >fixtures/auth-all.yaml


## These next three are the 'all' dump to restore the full db - JJW 9/29/16

./manage.py dumpdata --format yaml --natural-primary --natural-foreign auth.permission >fixtures/auth.permission.yaml
./manage.py dumpdata --format yaml --natural-primary                   contenttypes    >fixtures/contenttypes.yaml

./manage.py dumpdata --format yaml --natural-foreign -e auth.permission -e contenttypes -e social_django -e sessions >fixtures/all.yaml



#/manage.py dumpdata --format yaml -e auth.permission -e auth.group_permissions -e contenttypes -e social_auth -e sessions >fixtures/all.yaml

# No longer needed; deleted AnonymousUser
#./scripts/fixtures/exclude_pk.py fixtures/auth-all.yaml auth.user -1 >x && mv x fixtures/auth-all.yaml

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
