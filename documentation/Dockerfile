FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds
COPY ./documentation/requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Adds our application code to the image
COPY ./documentation code
WORKDIR code

EXPOSE 8001
CMD ["mkdocs", "serve"]
