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
kubectl port-forward standalone-app 8081:8080
```

Access program in browser
```
http://127.0.0.1:8080
```
or
```
http://127.0.0.1:8080/docs
```

Create and switch context in kubernets cluster
```
k create namespace dev 
```

Change namespace 
```
k config --set-context --current --namespace=dev
```

Delete pod by name and namespace
```
k delete pod standalone-app -n default
```

