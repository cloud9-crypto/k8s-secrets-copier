# K8S Secrets Copier to target service namespace
This repo is to hold the python script/Dockerfile for copying the secret from respective source service namespace to destination service namespace

## Requirements
1. Kubectl configured to the Environment Kubernetes cluster
2. Docker installed

## Instructions
Build the docker image

then run kubectl task with the docker image to copy the secret

```
kubectl run <task_name> --image=<image_name>
```

verify secrets copied - by running kubectl command

```
kubectl -n <target_namespace> get secrets
```
