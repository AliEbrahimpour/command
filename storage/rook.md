راه‌اندازی Rook برای ارائه فضای ذخیره‌سازی Ceph در یک کلاستر Kubernetes شامل چندین مرحله کلیدی است. Rook به عنوان یک orchestrator، Ceph را در Kubernetes مدیریت می‌کند و قابلیت‌هایی مانند بلاک استوریج (RBD)، سیستم فایل مشترک (CephFS) و آبجکت استوریج (S3/Swift) را فراهم می‌کند.

**پیش‌نیازها:**

قبل از شروع، مطمئن شوید که موارد زیر را دارید:

1.  **کلاستر Kubernetes:** یک کلاستر Kubernetes در حال کار (ورژن 1.16 یا بالاتر توصیه می‌شود).
2.  **دسترسی به kubectl:** ابزار `kubectl` روی سیستم شما نصب و پیکربندی شده باشد تا بتوانید با کلاستر Kubernetes خود ارتباط برقرار کنید.
3.  **فضای ذخیره‌سازی Raw:** نودهایی که قرار است به عنوان نودهای ذخیره‌سازی Ceph استفاده شوند، باید دارای دیسک‌های Raw (بدون پارتیشن یا فایل‌سیستم فرمت شده) باشند. Rook به این دیسک‌ها نیاز دارد تا Ceph OSD (Object Storage Daemon) ها را روی آن‌ها راه‌اندازی کند. برای هر نود ذخیره‌سازی حداقل 5 گیگابایت فضای خالی در مسیر مشخص شده برای `dataDirHostPath` لازم است.
4.  **LVM (اختیاری اما توصیه می‌شود):** نصب `lvm2` روی نودهای کلاستر می‌تواند به Rook در مدیریت دیسک‌ها کمک کند.

**مراحل راه‌اندازی Rook Ceph:**

این مراحل بر اساس مستندات رسمی Rook Ceph است و برای یک استقرار استاندارد در محیط تولید طراحی شده است.

**مرحله 1: کلون کردن ریپازیتوری Rook و تغییر دایرکتوری**

ابتدا ریپازیتوری Rook را کلون کنید و به دایرکتوری مثال‌های Kubernetes بروید:

```bash
git clone --single-branch --branch master https://github.com/rook/rook.git
cd rook/deploy/examples/
```

**مرحله 2: استقرار CRD ها (Custom Resource Definitions)**

CRD ها تعاریف منابع سفارشی Kubernetes هستند که Rook برای تعریف و مدیریت منابع Ceph از آن‌ها استفاده می‌کند.

```bash
kubectl create -f crds.yaml
```

**مرحله 3: استقرار Common Resources**

این فایل شامل تنظیمات و منابع مشترکی است که برای عملکرد Rook ضروری هستند، از جمله Role-Based Access Control (RBAC) برای Operator.

```bash
kubectl create -f common.yaml
```

**مرحله 4: استقرار Rook Operator**

Rook Operator مغز متفکر Rook است. این پاد مسئول مدیریت و استقرار اجزای Ceph (مانند مانیتورها، OSD ها، MDS ها و gateways) در کلاستر Kubernetes شما است.

```bash
kubectl create -f operator.yaml
```

**تأیید Operator:**

مطمئن شوید که Operator و Agent Pod ها در حالت `Running` قرار دارند:

```bash
kubectl -n rook-ceph get pod
```

باید پادهایی شبیه به `rook-ceph-operator-xxx` و `rook-ceph-agent-xxx` را ببینید که در حالت `Running` هستند. ممکن است چند دقیقه طول بکشد تا پادها کاملاً آماده شوند.

**مرحله 5: ایجاد کلاستر Ceph**

حالا که Rook Operator در حال اجرا است، می‌توانید کلاستر Ceph خود را ایجاد کنید. فایل `cluster.yaml` شامل پیکربندی کلاستر Ceph شما است. **قبل از اعمال این فایل، حتماً آن را بررسی و مطابق با نیازهای خود ویرایش کنید.**

مهم‌ترین بخش‌هایی که باید ویرایش کنید در `cluster.yaml` عبارتند از:

* **`storage` section:** این بخش تعیین می‌کند که Rook از کدام دیسک‌ها و نودها برای Ceph استفاده کند.
    * **`useAllNodes: true`**: اگر می‌خواهید Rook از تمام نودهای دارای فضای ذخیره‌سازی Raw در کلاستر استفاده کند.
    * **`useAllDevices: true`**: اگر می‌خواهید Rook از تمام دیسک‌های Raw موجود روی نودهای مشخص شده استفاده کند.
    * **`deviceFilter`**: می‌توانید یک فیلتر برای دیسک‌ها مشخص کنید (مثلاً `sdb|sdc` برای استفاده از دیسک‌های `/dev/sdb` و `/dev/sdc`).
    * **`nodes`**: می‌توانید نودهای خاصی را برای میزبانی Ceph OSD ها مشخص کنید.

مثال برای استفاده از تمام نودها و تمام دیسک‌های Raw:

```yaml
# cluster.yaml (قسمت مربوط به storage)
apiVersion: ceph.rook.io/v1
kind: CephCluster
metadata:
  name: rook-ceph
  namespace: rook-ceph
spec:
  cephVersion:
    image: quay.io/ceph/ceph:v17.2.6
  dataDirHostPath: /var/lib/rook
  mon:
    count: 3
    allowMultiplePerNode: false
  # ...
  storage:
    useAllNodes: true
    useAllDevices: true
    # deviceFilter: "sd[b-g]" # مثال: فقط دیسک‌های sdb تا sdg را استفاده کن
    # nodes:
    # - name: "node1"
    #   devices:
    #   - name: "sdb"
    # - name: "node2"
    #   devices:
    #   - name: "sdc"
```

بعد از ویرایش `cluster.yaml`، آن را اعمال کنید:

```bash
kubectl create -f cluster.yaml
```

**تأیید کلاستر Ceph:**

چند دقیقه صبر کنید و وضعیت کلاستر Ceph را بررسی کنید:

```bash
kubectl -n rook-ceph get cephcluster
```

باید `HEALTH_OK` را در ستون `HEALTH` ببینید. همچنین می‌توانید وضعیت پادهای Ceph را بررسی کنید:

```bash
kubectl -n rook-ceph get pod
```

باید پادهای مربوط به `ceph-mon`، `ceph-mgr`، `ceph-osd`، `csi-rbdplugin`، `csi-cephfsplugin` و غیره را در حالت `Running` ببینید.

**مرحله 6: استقرار Rook Toolbox (اختیاری اما توصیه می‌شود)**

Toolbox یک پاد شامل ابزارهای خط فرمان Ceph است که به شما امکان می‌دهد وضعیت کلاستر را بررسی کرده و عملیات پیشرفته را انجام دهید.

```bash
kubectl create -f toolbox.yaml
```

**دسترسی به Toolbox:**

برای ورود به پاد Toolbox:

```bash
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- bash
```

سپس می‌توانید دستورات Ceph را اجرا کنید، به عنوان مثال:

```bash
ceph status
ceph osd status
```

**مرحله 7: ایجاد StorageClass ها برای استفاده از فضای ذخیره‌سازی**

حالا که کلاستر Ceph شما در حال اجرا است، می‌توانید StorageClass ها را ایجاد کنید تا برنامه‌های Kubernetes بتوانند از فضای ذخیره‌سازی ارائه شده توسط Rook استفاده کنند. Rook Ceph سه نوع StorageClass اصلی را پشتیبانی می‌کند:

* **RBD (Block Storage):** برای PersistentVolumeClaim (PVC) های RWO (ReadWriteOnce) مناسب است.
* **CephFS (Shared File System):** برای PVC های RWX (ReadWriteMany) مناسب است.
* **Object Storage (S3/Swift):** برای برنامه‌هایی که نیاز به دسترسی به آبجکت استوریج دارند.

**مثال برای RBD StorageClass:**

```bash
kubectl create -f csi/rbd/storageclass.yaml
```

**مثال برای CephFS StorageClass:**

```bash
kubectl create -f csi/cephfs/storageclass.yaml
```

**مرحله 8: ایجاد PVC و استقرار یک برنامه نمونه**

اکنون می‌توانید یک PVC ایجاد کنید که از StorageClass های Ceph استفاده می‌کند و یک برنامه را برای استفاده از آن مستقر کنید.

**مثال برای PVC RBD و برنامه Nginx:**

1.  **ایجاد PVC (persistent-volume-claim.yaml):**

    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: my-rbd-pvc
      namespace: my-app-namespace # اگر namespace دیگری دارید
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 1Gi
      storageClassName: rook-ceph-block # نام StorageClass که در مرحله قبل ایجاد کردید
    ```

2.  **ایجاد Deployment (deployment.yaml):**

    ```yaml
    apiVersion: apps/v1
    kind: Deployment
    metadata:
      name: nginx-rbd-example
      namespace: my-app-namespace
    spec:
      selector:
        matchLabels:
          app: nginx
      replicas: 1
      template:
        metadata:
          labels:
            app: nginx
        spec:
          containers:
            - name: nginx
              image: nginx
              ports:
                - containerPort: 80
              volumeMounts:
                - mountPath: "/usr/share/nginx/html"
                  name: my-rbd-volume
          volumes:
            - name: my-rbd-volume
              persistentVolumeClaim:
                claimName: my-rbd-pvc
    ```

اعمال کردن:

```bash
kubectl create -f persistent-volume-claim.yaml -n my-app-namespace
kubectl create -f deployment.yaml -n my-app-namespace
```

**تأیید:**

بررسی کنید که PVC شما `Bound` شده و پاد Nginx در حال اجرا است:

```bash
kubectl -n my-app-namespace get pvc
kubectl -n my-app-namespace get pod
```

**نکات مهم:**

* **Namespace:** تمام منابع Rook Ceph (Operator, Cluster, StorageClass ها و ... ) به طور پیش‌فرض در namespace `rook-ceph` ایجاد می‌شوند. اگر می‌خواهید از namespace دیگری استفاده کنید، باید تمام فایل‌های YAML مربوطه را ویرایش کنید.
* **نسخه Rook و Ceph:** همیشه مستندات رسمی Rook (rook.io) را برای آخرین نسخه‌ها و بهترین شیوه‌ها بررسی کنید. نسخه‌های Ceph (مثلاً `v17.2.6` در مثال `cephVersion`) باید با نسخه‌های پشتیبانی شده توسط Rook مطابقت داشته باشند.
* **Troubleshooting:** در صورت بروز مشکل، لاگ‌های پادهای `rook-ceph-operator` و پادهای Ceph (مانند `ceph-mon`, `ceph-osd`) را بررسی کنید. Toolbox نیز ابزار بسیار مفیدی برای عیب‌یابی است.
* **پیکربندی پیشرفته:** Rook امکانات پیکربندی بسیار بیشتری را فراهم می‌کند، مانند:
    * فعال کردن Ceph Dashboard
    * تنظیمات شبکه برای Ceph
    * استفاده از LVM در Rook
    * نودهای اختصاصی برای OSD ها، MON ها و MDS ها
    * Object Storage (S3/Swift)
    * Mirroring و Disaster Recovery
    * مانیتورینگ با Prometheus و Grafana

این مراحل یک راهنمای جامع برای راه‌اندازی اولیه Rook Ceph در Kubernetes است. برای سناریوهای پیچیده‌تر و پیکربندی‌های پیشرفته، به مستندات رسمی Rook مراجعه کنید.
