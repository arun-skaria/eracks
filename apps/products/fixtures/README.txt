These fixtures are for testing:

- products-2.yaml

This contains the DMZ product, and all its dependencies, and is referenced specifically in the unit tests.
(by the quotes app, for one).


OLD DOCS & FIXTURES, SUPERSEDED AS OF Sep 2016 - JJW:

- products.yaml

This has one product, DMZ, pk=2, which is used in tests.py, with all its necessary related objects -
prodopts, options, choices, categories, etc


- products-all.yaml

This has the full dunp of all the products, prodopts, options, choices, categories, and choicecategoriues for the model.

This takes a long time to load into the test database, and hence is used minimally if at all in the test suite.


To refresh the products.yaml after model migrations, you may do:

./manage.py generate_fixtures products.models.Product 2 >apps/products/fixtures/products.yaml

From the main project directory.


To refresh all the fixtures, including these, see:

scripts/dump_test_fixtures.sh


We should consider auto-dumping fixtures from current db at the start of the test suite

j


