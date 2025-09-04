#!/bin/bash
# Build Docker images for Kubernetes deployment
docker build -f Dockerfile.python -t demo-python-app:latest .
docker build -f Dockerfile.mysql -t demo-mysql:latest .