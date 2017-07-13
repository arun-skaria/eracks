echo SET UP ENVO
./manage.py compilethemes && \
./manage.py collectstatic --link --noinput -v1 && \
echo large      | ./manage.py fb_version_generate -v0 >/dev/null && \
echo big        | ./manage.py fb_version_generate -v0 >/dev/null && \
echo medium     | ./manage.py fb_version_generate -v0 >/dev/null && \
echo small      | ./manage.py fb_version_generate -v0 >/dev/null && \
echo thumbnail  | ./manage.py fb_version_generate -v0 >/dev/null && \
echo SET UP ENVO DONE
