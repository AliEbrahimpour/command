# تفاوت `aws s3` و `aws s3api`

اگر با **AWS CLI** به **Ceph RGW / S3** متصل می‌شویم، به‌طور کلی:

- `aws s3` برای کارهای روزمره و ساده با **Bucket** و **Object**
- `aws s3api` برای عملیات دقیق‌تر، مدیریتی و تنظیمات سطح API

---

## 1. دستورات `aws s3`

`aws s3` یک رابط High-Level است و برای کارهای معمولی با فایل‌ها و Bucketها استفاده می‌شود.

### مشاهده Bucketها

```bash
aws s3 ls
```

### مشاهده Objectهای داخل Bucket

```bash
aws s3 ls s3://mybucket
```

### Upload فایل

```bash
aws s3 cp file.txt s3://mybucket/
```

### Download فایل

```bash
aws s3 cp s3://mybucket/file.txt .
```

### جابه‌جایی فایل

```bash
aws s3 mv file.txt s3://mybucket/
```

### حذف Object

```bash
aws s3 rm s3://mybucket/file.txt
```

### Sync کردن Directory با Bucket

```bash
aws s3 sync /data s3://mybucket/data/
```

### ساخت Bucket

```bash
aws s3 mb s3://mybucket
```

### حذف Bucket

```bash
aws s3 rb s3://mybucket
```

---

## چه زمانی از `aws s3` استفاده کنیم؟

| عملیات | دستور پیشنهادی |
|---|---|
| مشاهده Bucketها | `aws s3 ls` |
| مشاهده Objectها | `aws s3 ls` |
| Upload | `aws s3 cp` |
| Download | `aws s3 cp` |
| Copy | `aws s3 cp` |
| Move | `aws s3 mv` |
| Delete | `aws s3 rm` |
| Sync | `aws s3 sync` |
| ساخت Bucket | `aws s3 mb` |
| حذف Bucket | `aws s3 rb` |

---

# 2. دستورات `aws s3api`

`aws s3api` مستقیماً به عملیات S3 API نزدیک‌تر است و کنترل دقیق‌تری می‌دهد.

### مشاهده Bucketها

```bash
aws s3api list-buckets
```

### ساخت Bucket

```bash
aws s3api create-bucket \
  --bucket mybucket
```

### بررسی وجود Bucket

```bash
aws s3api head-bucket \
  --bucket mybucket
```

### مشاهده اطلاعات Object

```bash
aws s3api head-object \
  --bucket mybucket \
  --key file.txt
```

### Upload یک Object

```bash
aws s3api put-object \
  --bucket mybucket \
  --key file.txt \
  --body file.txt
```

### Download یک Object

```bash
aws s3api get-object \
  --bucket mybucket \
  --key file.txt \
  output.txt
```

### حذف Object

```bash
aws s3api delete-object \
  --bucket mybucket \
  --key file.txt
```

---

# تنظیمات مدیریتی با `s3api`

معمولاً تنظیمات مدیریتی Bucket و Object با `aws s3api` انجام می‌شوند.

## Versioning

مشاهده وضعیت Versioning:

```bash
aws s3api get-bucket-versioning \
  --bucket mybucket
```

فعال کردن Versioning:

```bash
aws s3api put-bucket-versioning \
  --bucket mybucket \
  --versioning-configuration Status=Enabled
```

---

## Bucket Policy

مشاهده Policy:

```bash
aws s3api get-bucket-policy \
  --bucket mybucket
```

ثبت Policy:

```bash
aws s3api put-bucket-policy \
  --bucket mybucket \
  --policy file://policy.json
```

حذف Policy:

```bash
aws s3api delete-bucket-policy \
  --bucket mybucket
```

---

# مواردی که معمولاً با `s3api` انجام می‌شوند

- Bucket Policy
- ACL
- Versioning
- Lifecycle
- CORS
- Encryption
- Object Metadata
- Object Tagging
- Bucket Tagging
- Multipart Upload
- Bucket Location
- Object Lock
- بررسی مشخصات Bucket
- بررسی مشخصات Object

---

# تفاوت ساده

می‌توان این‌طور در نظر گرفت:

```text
                 AWS CLI
                    |
          +---------+---------+
          |                   |
       aws s3              aws s3api
          |                   |
     کار با دیتا          مدیریت و API
          |                   |
       ls / cp             policy
       mv / rm             versioning
       sync                lifecycle
       mb / rb             ACL
                           metadata
                           multipart
```

---

# مثال ساده

برای دیدن فایل‌های یک Bucket:

```bash
aws s3 ls s3://test
```

اما برای دیدن Metadata و مشخصات یک Object:

```bash
aws s3api head-object \
  --bucket test \
  --key image.jpg
```

---

# استفاده با Ceph RGW

در Ceph RGW معمولاً باید آدرس Endpoint را مشخص کنیم.

مثال با `aws s3`:

```bash
aws --endpoint-url https://s3.example.com \
  s3 ls
```

مثال با `aws s3api`:

```bash
aws --endpoint-url https://s3.example.com \
  s3api head-bucket \
  --bucket test
```

> `--endpoint-url` مربوط به خود AWS CLI است و هم با `s3` و هم با `s3api` قابل استفاده است.

---

# جمع‌بندی

قاعده ساده برای به خاطر سپردن:

```text
aws s3
=
کار روزمره با Data

aws s3api
=
مدیریت، تنظیمات و کنترل دقیق API
```

پس:

```text
Upload / Download / List / Sync
→ aws s3

Policy / Versioning / Lifecycle / ACL / Metadata
→ aws s3api
```
