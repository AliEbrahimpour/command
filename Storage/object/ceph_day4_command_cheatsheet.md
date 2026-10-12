# Ceph Day 4 Command Cheat Sheet — RGW / S3

خلاصه دستورات روز چهارم با تمرکز روی **Ceph RGW، S3، User، Bucket، Object، Bucket Index و RGW Data Layout**.

---

## 1) بررسی سرویس RGW

### `ceph orch ls`
**کاربرد:** نمایش سرویس‌های مدیریت‌شده توسط cephadm.

```bash
ceph orch ls
```

### `ceph orch ps --daemon-type rgw`
**کاربرد:** نمایش RGW daemonها و Host محل اجرا.

```bash
ceph orch ps --daemon-type rgw
```

| پارامتر | توضیح |
|---|---|
| `--daemon-type rgw` | فقط RGW daemonها |

---

## 2) Deploy کردن RGW در Lab

```bash
ceph orch apply rgw lab-rgw
```

نمونه با Placement:

```bash
ceph orch apply rgw lab-rgw \
  --placement="2 ceph1 ceph2"
```

> ⚠️ Syntax دقیق Placement را با نسخه Ceph خود بررسی کن.

---

## 3) تست Endpoint

```bash
curl http://RGW-IP:PORT
```

**کاربرد:** بررسی اولیه دسترسی HTTP به RGW.

---

## 4) ساخت RGW User

```bash
radosgw-admin user create \
  --uid=labuser \
  --display-name="Lab User"
```

| پارامتر | توضیح |
|---|---|
| `--uid` | شناسه User |
| `--display-name` | نام نمایشی |

خروجی شامل `access_key` و `secret_key` است.

---

## 5) مشاهده User

```bash
radosgw-admin user info --uid=labuser
```

```bash
radosgw-admin user list
```

---

## 6) تنظیم AWS CLI

```bash
aws configure
```

مقادیر اصلی:

```text
AWS Access Key ID
AWS Secret Access Key
Default region
Output format
```

---

## 7) عملیات S3

### لیست Bucketها

```bash
aws --endpoint-url http://RGW-IP:PORT s3 ls
```

### ساخت Bucket

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3 mb s3://lab-bucket
```

### Upload Object

```bash
echo "Hello RGW" >/tmp/hello.txt

aws --endpoint-url http://RGW-IP:PORT \
  s3 cp /tmp/hello.txt s3://lab-bucket/
```

### List Object

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3 ls s3://lab-bucket/
```

### Download

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3 cp s3://lab-bucket/hello.txt /tmp/downloaded.txt
```

### Delete

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3 rm s3://lab-bucket/hello.txt
```

---

## 8) Head Object

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3api head-object \
  --bucket lab-bucket \
  --key hello.txt
```

**کاربرد:** مشاهده Metadata، Size، ETag و اطلاعات Object.

---

## 9) Upload همراه Metadata

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3api put-object \
  --bucket lab-bucket \
  --key customer/test.txt \
  --body /tmp/hello.txt \
  --metadata customer=100,project=ceph-lab
```

---

## 10) Poolهای RGW

```bash
ceph osd pool ls
```

Poolهای رایج:

```text
.rgw.root
default.rgw.meta
default.rgw.buckets.index
default.rgw.buckets.data
default.rgw.log
default.rgw.control
```

> نام دقیق Poolها به Zone وابسته است.

---

## 11) Bucketها از دید RGW

```bash
radosgw-admin bucket list
```

---

## 12) Bucket Stats

```bash
radosgw-admin bucket stats \
  --bucket=lab-bucket
```

| فیلد | توضیح |
|---|---|
| `owner` | مالک Bucket |
| `id` | Bucket ID |
| `marker` | Marker داخلی |
| `num_shards` | تعداد Index Shard |
| `usage` | میزان مصرف |

---

## 13) Objectهای Data Pool

```bash
rados -p default.rgw.buckets.data ls
```

پیدا کردن Key:

```bash
rados -p default.rgw.buckets.data ls | grep hello.txt
```

> ⚠️ روی Pool بزرگ Production بی‌دلیل اجرا نکن.

---

## 14) Bucket Index Objectها

```bash
rados -p default.rgw.buckets.index ls
```

نمونه:

```text
.dir.<bucket-marker>
.dir.<bucket-marker>.0
.dir.<bucket-marker>.1
```

---

## 15) OMAP Bucket Index

```bash
rados -p default.rgw.buckets.index \
  listomapkeys .dir.<marker>
```

```bash
rados -p default.rgw.buckets.index \
  listomapvals .dir.<marker>
```

> ⚠️ روی Index Production چیزی را دستی حذف نکن.

---

## 16) RGW Metadata

```bash
radosgw-admin metadata list
```

---

## 17) Versioning

### Enable

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3api put-bucket-versioning \
  --bucket lab-bucket \
  --versioning-configuration Status=Enabled
```

### List Versions

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3api list-object-versions \
  --bucket lab-bucket
```

---

## 18) Multipart Upload

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3api list-multipart-uploads \
  --bucket lab-bucket
```

---

## 19) Usage

```bash
radosgw-admin usage show --uid=labuser
```

---

## 20) Quota

```bash
radosgw-admin quota set \
  --quota-scope=user \
  --uid=labuser \
  --max-size=10G \
  --max-objects=10000
```

```bash
radosgw-admin quota enable \
  --quota-scope=user \
  --uid=labuser
```

---

## 21) Bucket Check

```bash
radosgw-admin bucket check --bucket=lab-bucket
```

> ⚠️ روی Bucket بزرگ Production بدون نیاز مشخص اجرا نشود.

---

## 22) Trace کامل S3 Object تا OSD

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3 cp /tmp/hello.txt s3://lab-bucket/hello.txt
```

```bash
radosgw-admin bucket stats --bucket=lab-bucket
```

```bash
rados -p default.rgw.buckets.data ls | grep hello.txt
```

```bash
ceph osd map default.rgw.buckets.data 'RADOS_OBJECT_NAME'
```

```text
S3 Object
 ↓
RGW
 ↓
RADOS Object
 ↓
PG
 ↓
CRUSH
 ↓
OSD
```

---

## 23) خلاصه سریع

| هدف | دستور |
|---|---|
| RGW daemonها | `ceph orch ps --daemon-type rgw` |
| ساخت User | `radosgw-admin user create` |
| User Info | `radosgw-admin user info` |
| Bucket Stats | `radosgw-admin bucket stats` |
| Bucket Create | `aws s3 mb` |
| Upload/Download | `aws s3 cp` |
| Delete | `aws s3 rm` |
| Head | `aws s3api head-object` |
| Versioning | `aws s3api put-bucket-versioning` |
| Multipart | `aws s3api list-multipart-uploads` |
| RGW Pools | `ceph osd pool ls` |
| Data Objects | `rados -p <pool> ls` |
| Index OMAP | `rados listomapkeys/listomapvals` |

---

## 24) هشدار

روی RGW Production بدون شناخت دقیق این کارها را انجام نده:

```text
rados rm
rados rmomapkey
rados rmxattr
```
