#!/bin/sh

# check for env variable GOOGLE_PROJECT_ID
if [ ! $GOOGLE_PROJECT_ID ]
then
  echo "[ERROR] Env variable GOOGLE_PROJECT_ID not defined"
  exit
fi

# check for service name
SERVICE=$1
if [ ! $SERVICE ]
then
  echo "[ERROR] Service name not provided"
  exit
fi

# check for version
VERSION=$2
if [ ! $VERSION ]
then
  echo "[ERROR] Version tag not provided"
  exit
fi

# build container
echo ""
echo "BUILD"
echo ""
docker-compose -f production.yml build $SERVICE

# tag version
echo "--------------------"
echo ""
echo "TAG"
echo ""
FINAL_CONTAINER_NAME=gcr.io/$GOOGLE_PROJECT_ID/standup-$SERVICE:$VERSION
docker tag $SERVICE:lastest $FINAL_CONTAINER_NAME

# push to container registry
echo "--------------------"
echo ""
echo "PUSH TO REGISTRY"
echo ""
docker push $FINAL_CONTAINER_NAME