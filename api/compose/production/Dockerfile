FROM python:3.6
ENV PYTHONUNBUFFERED 1

# define needed build arguments
ARG django_secret_key
ARG postgres_user
ARG postgres_password
ARG postgres_host
ARG postgres_port
ARG postgres_db
ARG db_google_instance_name
ARG django_aws_access_key_id
ARG django_aws_secret_access_key
ARG django_aws_storage_bucket_name
ARG email_host_user
ARG email_host_password

# envs django
ENV DJANGO_SECRET_KEY=$django_secret_key

# envs database
ENV POSTGRES_USER=$postgres_user
ENV POSTGRES_PASSWORD=$postgres_password
ENV POSTGRES_HOST=$postgres_host
ENV POSTGRES_PORT=$postgres_port
ENV POSTGRES_DB=$postgres_db
ENV DB_GOOGLE_INSTANCE_NAME=$db_google_instance_name
ENV DATABASE_URL=postgres://$postgres_user:$postgres_password@$postgres_host:$postgres_port/$postgres_db

# envs aws storage
ENV DJANGO_AWS_ACCESS_KEY_ID=$django_aws_access_key_id
ENV DJANGO_AWS_SECRET_ACCESS_KEY=$django_aws_secret_access_key
ENV DJANGO_AWS_STORAGE_BUCKET_NAME=$django_aws_storage_bucket_name

# envs email
ENV EMAIL_HOST_USER=$email_host_user
ENV EMAIL_HOST_PASSWORD=$email_host_password

# envs django settings module
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
