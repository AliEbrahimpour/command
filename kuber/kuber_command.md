# 🚀 دستورات پرکاربرد Kubernetes

در این فایل، مجموعه‌ای از دستورات پرکاربرد `kubectl` آورده شده است که برای مدیریت کلاستر Kubernetes استفاده می‌شوند.

---

## 🔍 بررسی وضعیت کلی

```bash
kubectl cluster-info              # اطلاعات کلی از کلاستر
kubectl get nodes                 # لیست نودها و وضعیت آن‌ها
kubectl get pods -A              # لیست تمام پادها در همه namespaceها
kubectl get services             # لیست سرویس‌ها در namespace جاری
kubectl get events --sort-by=.metadata.creationTimestamp   # لیست رویدادها به ترتیب زمانی
```

---

## 📦 مدیریت پادها (Pods)

```bash
kubectl get pods                         # لیست پادها در namespace جاری
kubectl describe pod <pod-name>         # جزییات کامل یک پاد
kubectl logs <pod-name>                 # لاگ پاد (برای یک کانتینر)
kubectl logs <pod-name> -c <container>  # لاگ پاد برای یک کانتینر خاص
kubectl exec -it <pod-name> -- /bin/sh  # ورود به پاد با شل
kubectl delete pod <pod-name>           # حذف پاد
```

---

## ⚙️ مدیریت Deploymentها

```bash
kubectl get deployments                   # لیست دیپلویمنت‌ها
kubectl describe deployment <name>       # جزییات یک دیپلویمنت
kubectl create deployment <name> --image=<image>   # ساخت دیپلویمنت جدید
kubectl set image deployment/<name> <container>=<new-image>  # بروزرسانی ایمیج
kubectl rollout status deployment/<name>            # بررسی وضعیت rollout
kubectl rollout undo deployment/<name>              # بازگردانی به نسخه قبلی
```

---

## 🔄 اعمال تغییرات

```bash
kubectl apply -f <file.yaml>              # اعمال تغییرات از فایل yaml
kubectl delete -f <file.yaml>             # حذف منابع تعریف‌شده در فایل
kubectl edit deployment <name>            # ویرایش مستقیم منابع
```

---

## 📁 کار با Namespaceها

```bash
kubectl get namespaces                    # لیست namespaceها
kubectl create namespace <name>           # ساخت namespace جدید
kubectl delete namespace <name>           # حذف namespace
kubectl config set-context --current --namespace=<name>   # تغییر namespace جاری
```

---

## 🔐 کار با ConfigMap و Secret

```bash
kubectl create configmap <name> --from-literal=key=value      # ساخت ConfigMap ساده
kubectl create secret generic <name> --from-literal=key=value # ساخت Secret
kubectl get configmap <name> -o yaml                          # نمایش ConfigMap به صورت yaml
kubectl get secret <name> -o yaml                             # نمایش Secret به صورت yaml (base64)
```

---

## 📡 بررسی دسترسی‌ها و رول‌ها (RBAC)

```bash
kubectl get serviceaccount
kubectl get clusterrolebinding
kubectl describe clusterrole <name>
kubectl auth can-i <verb> <resource> --as=<user>
```

---

## 📂 دیباگ و ابزارها

```bash
kubectl explain <resource>                # توضیح ساختار منابع
kubectl top pod                           # بررسی مصرف منابع پادها (نیاز به metrics server)
kubectl port-forward svc/<svc-name> 8080:80  # فورواد پورت برای دسترسی محلی
kubectl cp <pod-name>:<path> <local-path>   # کپی فایل از پاد
```

---

## ⚠️ دستورات مفید دیگر

```bash
kubectl version --short                   # نسخه سرور و کلاینت
kubectl config view                       # مشاهده تنظیمات kubeconfig
kubectl config get-contexts               # لیست contextهای موجود
kubectl config use-context <name>         # انتخاب context فعال
```

---

> 🧠 نکته: برای منابع مثل `deployment`, `service`, `pod`, و غیره می‌توان از `-o yaml` یا `-o json` برای گرفتن خروجی به فرمت دلخواه استفاده کرد.

