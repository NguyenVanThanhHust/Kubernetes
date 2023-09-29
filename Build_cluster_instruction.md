# Build cluster instruction
This instruction is for building on virtual machines. I haven't testes it on real machines.

After create 2 virtual machines on Virtual box.
## For node master
If any command required priviledge, add `sudo` before command
Update and upgrade 
```
sudo apt update && sudo apt upgrade
```

Install runtime and text editor
```
sudo apt install -y docker.io vim
```

Verify if docker is installed
```
sudo docker run hello-world
```

Disable swap completely
```
swapoff -a                 # Disable all devices marked as swap in /etc/fstab
sed -e '/swap/ s/^#*/#/' -i /etc/fstab   # Comment the correct mounting point
systemctl mask swap.target               # Completely disabled
```

[Add user to docker group to use docker without sudo](https://docs.docker.com/engine/install/linux-postinstall/)

Reboot for sure
```
sudo reboot
```

Create docker registry to save docker image online
```
docker pull docker.io/library/registry:2
```
```
docker run -d -p 9004:5000 -v $(pwd)registry:/var/lib/registry                             --restart always --name registry registry:2
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
