# Install Helm
```
wget https://get.helm.sh/helm-$(curl -s https://api.github.com/repos/helm/helm/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')-linux-amd64.tar.gz
tar -zxvf helm-x.x.x-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
helm version
```

# Kubernetes Packages
[artifacthub](https://artifacthub.io/)


# Manage Wordpress With Helm
## install wordpress with helm
```
helm install my-release oci://registry-1.docker.io/bitnamicharts/wordpress
```
## delete wordpress with helm
```
helm uninstall my-release
```
or
```
helm delete my-release
```
and delete pvc
```
kubectl get pvc
kubectl delete pvc data-my-release-mariadb-0
```


# Git Repo
[the Releases page](https://github.com/helm/helm/releases/latest)
