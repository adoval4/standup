#!/bin/sh

# Build and deploy
# ================
#
# This script can be used for building and deploying an image update to a google
# kubernetes engine
#
# Usage:
# $ bash build_and_deploy.sh [SERVICE-NAME] [VERSION-TAG]
# 

# check for env variable GOOGLE_PROJECT_ID
if [ ! $GOOGLE_PROJECT_ID ]
then
  echo "[ERROR] Env variable GOOGLE_PROJECT_ID not defined"
  exit
fi

# get google credentials
gcloud container clusters get-credentials standard-cluster-1 --zone us-central1-a --project $GOOGLE_PROJECT_ID

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
FINAL_IMAGE_NAME=gcr.io/$GOOGLE_PROJECT_ID/standup-$SERVICE:$VERSION
docker tag $SERVICE:latest $FINAL_IMAGE_NAME

# push to container registry
echo "--------------------"
echo ""
echo "PUSH TO REGISTRY"
echo ""
docker push $FINAL_IMAGE_NAME

# push to container registry
echo "--------------------"
echo ""
echo "UPDATE DEPLOYMENT CONTAINER IMAGE"
echo ""
DEPLOYMENT=deployments/standup-$SERVICE
CONTAINER_NAME=standup-$SERVICE-sha256
kubectl set image $DEPLOYMENT $CONTAINER_NAME=$FINAL_IMAGE_NAME