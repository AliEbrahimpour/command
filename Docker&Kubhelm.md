# Helm Cheat Sheet

## Install Helm

### Linux

```bash
curl https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-3 | bash
```

### Verify

```bash
helm version
```

---

# Repository Management

## Add repo

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
```

## List repos

```bash
helm repo list
```

## Update repos

```bash
helm repo update
```

## Remove repo

```bash
helm repo remove bitnami
```

## Search charts

```bash
helm search repo nginx
```

## Search Hub

```bash
helm search hub nginx
```

---

# Chart Management

## Create chart

```bash
helm create mychart
```

## Lint chart

```bash
helm lint mychart
```

## Package chart

```bash
helm package mychart
```

## Show chart values

```bash
helm show values bitnami/nginx
```

## Show chart info

```bash
helm show chart bitnami/nginx
```

## Pull chart

```bash
helm pull bitnami/nginx
```

## Pull and untar

```bash
helm pull bitnami/nginx --untar
```

---

# Install & Upgrade

## Install release

```bash
helm install mynginx bitnami/nginx
```

## Install with namespace

```bash
helm install mynginx bitnami/nginx -n web --create-namespace
```

## Install with custom values

```bash
helm install mynginx bitnami/nginx -f values.yaml
```

## Override single value

```bash
helm install mynginx bitnami/nginx --set service.type=NodePort
```

## Dry run

```bash
helm install mynginx bitnami/nginx --dry-run --debug
```

## Upgrade release

```bash
helm upgrade mynginx bitnami/nginx
```

## Upgrade with values

```bash
helm upgrade mynginx bitnami/nginx -f values.yaml
```

## Install or upgrade

```bash
helm upgrade --install mynginx bitnami/nginx
```

---

# Release Management

## List releases

```bash
helm list
```

## List all namespaces

```bash
helm list -A
```

## Get release status

```bash
helm status mynginx
```

## Get release history

```bash
helm history mynginx
```

## Rollback release

```bash
helm rollback mynginx 1
```

## Uninstall release

```bash
helm uninstall mynginx
```

---

# Values & Templates

## Get user-supplied values

```bash
helm get values mynginx
```

## Get all values

```bash
helm get values mynginx -a
```

## Render templates locally

```bash
helm template mynginx ./mychart
```

## Render with values

```bash
helm template mynginx ./mychart -f values.yaml
```

## Validate manifests

```bash
helm template mynginx ./mychart | kubectl apply --dry-run=client -f -
```

---

# Debugging

## Debug install

```bash
helm install mynginx bitnami/nginx --debug
```

## Dry-run upgrade

```bash
helm upgrade mynginx bitnami/nginx --dry-run
```

## Check Kubernetes resources

```bash
kubectl get all -n web
```

## Describe pod

```bash
kubectl describe pod POD_NAME -n web
```

## View logs

```bash
kubectl logs POD_NAME -n web
```

---

# Common Useful Flags

| Flag                 | Description         |
| -------------------- | ------------------- |
| `-n`                 | Namespace           |
| `-f`                 | Values file         |
| `--set`              | Override values     |
| `--create-namespace` | Create namespace    |
| `--dry-run`          | Simulate command    |
| `--debug`            | Verbose output      |
| `--wait`             | Wait until ready    |
| `--timeout`          | Set timeout         |
| `--atomic`           | Rollback on failure |

---

# OCI Registry Commands

## Login to registry

```bash
helm registry login registry.example.com
```

## Pull OCI chart

```bash
helm pull oci://registry.example.com/charts/nginx
```

## Push OCI chart

```bash
helm push mychart-0.1.0.tgz oci://registry.example.com/charts
```

---

# Dependency Management

## Update dependencies

```bash
helm dependency update
```

## Build dependencies

```bash
helm dependency build
```

## List dependencies

```bash
helm dependency list
```

---

# Useful Examples

## Install ingress-nginx

```bash
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm repo update

helm install ingress ingress-nginx/ingress-nginx \
  -n ingress-nginx \
  --create-namespace
```

## Install Prometheus Stack

```bash
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts

helm install monitoring prometheus-community/kube-prometheus-stack \
  -n monitoring \
  --create-namespace
```

## Upgrade with rollback safety

```bash
helm upgrade --install app ./chart \
  -n production \
  -f values-prod.yaml \
  --atomic \
  --wait
```

---

# Cleanup

## Delete failed releases

```bash
helm uninstall RELEASE_NAME
```

## Remove old revisions secret/configmaps

```bash
kubectl get secrets -A | grep helm
```

---

# Official Docs

* [Helm Official Website](https://helm.sh?utm_source=chatgpt.com)
* [Helm Commands Documentation](https://helm.sh/docs/helm/?utm_source=chatgpt.com)
* [Helm Chart Best Practices](https://helm.sh/docs/chart_best_practices/?utm_source=chatgpt.com)
