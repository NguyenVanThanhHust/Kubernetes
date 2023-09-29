This is a sample to deploy standalone app in Kubernetes

Build image
```
docker build -t fast_api_img .
```
Push image to docker hub
```
docker tags fast_api_img:latest quaden/docker_images:fast_api_img && docker push quaden/docker_images:fast_api_img
```

Build pods
```
kubectl create -f standalone-pod.yml
```
Forward pods to use
```
kubectl port-forward standalone-app 8080:80
```

Access program in browser
```
http://127.0.0.1:8080
```
or
```
http://127.0.0.1:8080/docs
```