#!/usr/bin/env bash

IMAGE_NAME=iff
IMAGE_LABEL=latest
ENVIRONMENT=gorgias-ml-development
DOCKER_FILE=Dockerfile

IMAGE_TAG="gcr.io/${ENVIRONMENT}/${IMAGE_NAME}:${IMAGE_LABEL}"

docker buildx build --platform linux/amd64 -t ${IMAGE_TAG} -f ${DOCKER_FILE} .
docker push ${IMAGE_TAG}
