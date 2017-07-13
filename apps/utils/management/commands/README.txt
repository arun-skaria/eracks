JJW 9/4/16
==========

In an attempt to fix prodopts not being dumped properly by generate_fixtures, I:
- Renamed my slightly older fork to generate_fixtures-jjw
- updated generate_fixtures to the latest 0.2 code from the source:
https://github.com/aRkadeFR/django-generate-fixtures
(0.2 is From July 28th, IIRC)

No change, still doesn't want to dump the FK pointing to me (the prod).
So I updated my fork to match the slighlty newer logic (accumulate "fields"),
and enhanced it to loook for related fields - 

Now it picks up too much, including all the Generic Foreign Key stuff - one prod 
is over half the size of the whole products app dump (and it takes an order of 
magnitude longer to dump).

So I've left the two versions out there for future work if needed.

For now, use the current generate_fixtures - it seems to work OK for most things 
like quotes, customers, etc, as my old one did (albeit without the documentation 
and spelling improvements :-D )

JJW