FROM python:3.6
ENV PYTHONUNBUFFERED 1

# django settings module
ENV DJANGO_SETTINGS_MODULE=standup.config
ENV DJANGO_CONFIGURATION=Production

# Adds our application code to the image
COPY ./api code
WORKDIR code

# Allows docker to cache installed dependencies between builds
RUN pip install -r requirements.txt

# import google cloud sql proxy
RUN wget https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 -O cloud_sql_proxy
RUN chmod +x cloud_sql_proxy

# expose port
ENV PORT=8000
EXPOSE $PORT

# start google cloud sql proxy, migrates the database,
# uploads staticfiles, and runs the production server
CMD /bin/bash -c "./cloud_sql_proxy -instances=$DB_GOOGLE_INSTANCE_NAME=tcp:$POSTGRES_PORT & python wait_for_postgres.py && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    newrelic-admin run-program gunicorn --bind 0.0.0.0:$PORT --access-logfile - standup.wsgi:application"
