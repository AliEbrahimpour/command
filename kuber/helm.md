# Install Helm
```
wget https://get.helm.sh/helm-$(curl -s https://api.github.com/repos/helm/helm/releases/latest | grep -oP '"tag_name": "\K(.*)(?=")')-linux-amd64.tar.gz
tar -zxvf helm-x.x.x-linux-amd64.tar.gz
sudo mv linux-amd64/helm /usr/local/bin/helm
helm version
```





# Git Repo
[the Releases page](https://github.com/helm/helm/releases/latest)
