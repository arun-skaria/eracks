# These should be cut/pasted by hand & run from project directory, not the directory this file is in! - JJW

# This will dump a quote (55143 is referenced in quotes/tests.py), with all its dependent records - BUT:
# you may have to hand-edit to ensure that the custoemr is createed BEFORE the user - 
# otherwise you'll get the Unique key constraint error -
# see the signal and def create_user_profile at the bottom of customers/models.py
./manage.py generate_fixtures quotes.models.Quote 55143 >apps/quotes/fixtures/quotes.yaml

# Also, you have to use generate_fixtures from the "bottom up" - if you want quote line items, use this:
./manage.py generate_fixtures quotes.models.QuoteLineItem 55144 >apps/quotes/fixtures/quotes-55143.yaml

# Single fixture with all dependencies for the DMZ product (Referenced in the quotes tests):
./manage.py generate_fixtures products.models.Product 1 >apps/products/fixtures/products-1.yaml
./manage.py generate_fixtures products.models.Product 2 >apps/products/fixtures/products-2.yaml
# NOTE: does not properly dump prodopts - use product-all for products (see below)

# Single fixture with all dependencies for the Meest customer (Referenced directly in the customer tests)
./manage.py generate_fixtures customers.models.Customer 54730 >apps/customers/fixtures/customers-54730.yaml

# Single fixture with all dependencies for the NPR customer image (Referenced directly in the customer tests)
./manage.py generate_fixtures customers.models.CustomerImage 53336 >apps/customers/fixtures/customers-customerimage-53336.yaml

# All product fixtures - 4MB, but works; dumping a sibnlge product does not properly pick up prodopts - 
# I made some preliminary enhancements in utils/management/commands/generate_fixtures/jjw, but it picks up too much, and:
# a) dumps 2.2MB (out of 4MB for the whole products app!)
# b) still NFG, bombs on generic FK stuff - 
# So use regular dumpdata - 
 ./manage.py dumpdata --format=yaml products >apps/products/fixtures/products-all.yaml
# TODO: Pre-dump prod fixtures to temp-products.yaml for buzz through DB options, and automate this script and (further) the test suite :-)

# NFG:
./manage.py generate_fixtures home.models.FeaturedImage 56721 >>apps/home/fixtures/featuredimage-56721.yaml

# Almost there - make a fixtures/temp dir, and dump all these there
./manage.py dumpdata --format=yaml home >apps/home/fixtures/home-all.yaml
./manage.py dumpdata --format=yaml quickpages >conf/env/src/django-quickpages/quickpages/fixtures/quickpages-all.yaml 



# The below are here mostly for historical and notes value - 
# they are intended for experimentation and trail-and-error - JJW

# Depending on virtualenv, use one of these two:
#./manage.py dumpdata quickpages --format=yaml --all >conf/env/src/django-quickpages/quickpages/fixtures/quickpages.yaml
./manage.py dumpdata quickpages --format=yaml --all >conf/src/django-quickpages/quickpages/fixtures/quickpages.yaml

./manage.py dumpdata home.featuredimage      --pks=53685,53686,56721 --format=yaml >apps/home/fixtures/home.yaml
./manage.py dumpdata auth.user               --pks=2,3,4,42,43         --format=yaml >apps/customers/fixtures/users.yaml
./manage.py dumpdata customers.customer      --pks=2,54987,55132,54730 --format=yaml >apps/customers/fixtures/customers.yaml
./manage.py dumpdata customers.customerimage --pks=53336,53337,53338 --format=yaml >>apps/customers/fixtures/customers.yaml
./manage.py dumpdata customers.testimonial   --pks=53380,53381,53382 --format=yaml >>apps/customers/fixtures/customers.yaml
./manage.py dumpdata customers.address       --pks=54276,54731,54732 --format=yaml >>apps/customers/fixtures/customers.yaml

./manage.py dumpdata quotes.quote            --pks=1,55143,55149     --format=yaml $all >apps/quotes/fixtures/quotes.yaml
./manage.py dumpdata quotes.quotelineitem    --pks=1,55144,55150     --format=yaml $all >>apps/quotes/fixtures/quotes.yaml

./manage.py generate_fixtures products.models.Product 2 >apps/products/fixtures/products.yaml
./manage.py generate_fixtures products.models.Product 55174 >>apps/products/fixtures/products.yaml
echo >>apps/products/fixtures/products.yaml


# - - - new things tried:

./manage.py dumpdata auth.user               --pks=2,50,123,153 --natural-primary --format=yaml >apps/customers/fixtures/customers.yaml
./manage.py dumpdata customers.customer      --pks=2,54987,55132,54730 --natural-primary --natural-foreign --format=yaml >>apps/customers/fixtures/customers.yaml


./manage.py dumpdata auth.user               --pks=2,3,4,42,43,50,123,153 --format=yaml >>apps/customers/fixtures/customers.yaml



./manage.py dumpdata customers.customer      --pks=54730 --natural-foreign --format=yaml >apps/customers/fixtures/customers.yaml
./manage.py dumpdata customers.customerimage --pks=53336,53337,53338 --format=yaml >>apps/customers/fixtures/customers.yaml
./manage.py dumpdata customers.testimonial   --pks=53380,53381,53382 --format=yaml >>apps/customers/fixtures/customers.yaml
./manage.py dumpdata customers.address       --pks=54276,54731,54732 --format=yaml >>apps/customers/fixtures/customers.yaml

orders - old!
  custs 2 3 4

./manage.py generate_fixtures orders.models.Order 57138 >>apps/orders/fixtures/orders.yaml
# includes 56122 spotterrf - 57138 is a recent order fm them
