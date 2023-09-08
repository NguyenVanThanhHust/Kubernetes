# Kubernetes
This is where I learn about Kubernetes. 

First install and create virtual machines on ubuntu:
https://linuxize.com/post/how-to-install-vagrant-on-ubuntu-20-04/

Create virtual machine with ubuntu 22.04
https://www.tutorialworks.com/linux-vm-vagrant/

In virtual machine:
Run
```
sudo apt update
```
```
sudo apt upgrade
```
Install docker + vim
```
sudo apt install -y docker.io vim
```
Verify with 
```
sudo docker run hello-world
```

Create docker registry
```
docker pull docker.io/library/registry:2
```
```
docker run -d -p 9004:5000 -v $(pwd)/registry:/var/lib/registry \
							--restart always --name registry registry:2
```


Test docker registry
```
docker pull busybox
```
```
docker tag busybox 10.0.2.15:9004/busybox
```
```
docker push 10.0.2.15:9004/busybox
```

Check docker image:
```
docker image ls -a
```
Result should be something like:
```
REPOSITORY               TAG       IMAGE ID       CREATED       SIZE
registry                 2         0030ba3d620c   4 weeks ago   24.1MB
10.0.2.15:9004/busybox   latest    a416a98b71e2   7 weeks ago   4.26MB
busybox                  latest    a416a98b71e2   7 weeks ago   4.26MB
```

Install necessary package
```
sudo apt-get install -y apt-transport-https ca-certificates curl
```

Follow instruction in [kubernetes instruction](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/)

Create cluster online:
```
kubeadm init --upload-certs --apiserver-advertise-address=10.0.2.15 --pod-network-cidr=10.100.0.0/16
```

For create offline:

Check list of images need for creating cluster:
```
kubeadm config images list
```
Result should be:
```
registry.k8s.io/kube-apiserver:v1.28.1
registry.k8s.io/kube-controller-manager:v1.28.1
registry.k8s.io/kube-scheduler:v1.28.1
registry.k8s.io/kube-proxy:v1.28.1
registry.k8s.io/pause:3.9
registry.k8s.io/etcd:3.5.9-0
registry.k8s.io/coredns/coredns:v1.10.1
```

For each image, we pull, tag and push to our docker registry:
```
docker pull registry.k8s.io/kube-apiserver:v1.28.1
docker tag registry.k8s.io/kube-apiserver:v1.28.1 10.0.2.15:9004/kube-apiserver:v1.28.1
docker push 10.0.2.15:9004/kube-apiserver:v1.28.1
```

```
docker pull registry.k8s.io/kube-controller-manager:v1.28.1
docker tag registry.k8s.io/kube-controller-manager:v1.28.1 10.0.2.15:9004/kube-controller-manager:v1.28.1
docker push 10.0.2.15:9004/kube-controller-manager:v1.28.1
```

```
docker pull registry.k8s.io/kube-proxy:v1.28.1
docker tag registry.k8s.io/kube-proxy:v1.28.1 10.0.2.15:9004/kube-proxy:v1.28.1
docker push 10.0.2.15:9004/kube-proxy:v1.28.1
```

```
docker pull registry.k8s.io/pause:3.9
docker tag registry.k8s.io/pause:3.9 10.0.2.15:9004/pause:3.9
docker push 10.0.2.15:9004/pause:3.9
```

```
docker pull registry.k8s.io/etcd:3.5.9-0
docker tag registry.k8s.io/etcd:3.5.9-0 10.0.2.15:9004/etcd:3.5.9-0
docker push 10.0.2.15:9004/etcd:3.5.9-0
```

```
docker pull registry.k8s.io/coredns:v1.10.1
docker tag registry.k8s.io/coredns:v1.10.1 10.0.2.15:9004/coredns:v1.10.1
docker push 10.0.2.15:9004/coredns:v1.10.1
```


Create cluster offline

```
kubeadm init --upload-certs --apiserver-advertise-address=10.0.2.15 --pod-network-cidr=10.100.0.0/16 --image-repository 10.0.2.15:9004/kubeadm --ignore-preflight-errors ImagePull
```
