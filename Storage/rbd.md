

# 📘 دستورات RBD در Ceph (نسخه Mimic)

> منبع:
> [Ceph Documentation – RBD Commands](https://docs.ceph.com/en/mimic/rbd/rados-rbd-cmds/)

> https://docs.ceph.com/en/latest/rbd/rados-rbd-cmds/




---


## 🧱 ۱. ایجاد Pool برای RBD

```
ceph osd pool create <pool-name> <pg-num>
rbd pool init <pool-name>
```

---

## 👤 ۲. ایجاد کاربر برای دسترسی به RBD

```
ceph auth get-or-create client.<ID> mon 'profile rbd' osd 'profile rbd pool=<pool-name>, profile rbd-read-only pool=<pool-name>'
```

> 🔑 خروجی این دستور را می‌توان در فایل `/etc/ceph/ceph.client.<ID>.keyring` ذخیره کرد.

---

## 💽 ۳. ایجاد یک Image جدید

```
rbd create --size <size-in-MB> <pool-name>/<image-name>
```

مثال:

```
rbd create --size 1024 swimmingpool/bar
```

---

## 📋 ۴. لیست‌کردن Image‌ها

```
rbd ls
rbd ls <pool-name>
rbd trash ls
rbd trash ls <pool-name>
```

---

## 🔍 ۵. مشاهده اطلاعات یک Image

```
rbd info <image-name>
rbd info <pool-name>/<image-name>
```

---

## 📏 ۶. تغییر اندازه یک Image

```
rbd resize --size <new-size-in-MB> <image-name>
rbd resize --size <new-size-in-MB> <image-name> --allow-shrink
```

---

## 🗑️ ۷. حذف یک Image

```
rbd rm <image-name>
rbd rm <pool-name>/<image-name>
rbd trash mv <pool-name>/<image-name>
rbd trash rm <pool-name>/<image-id>
```

---

## ♻️ ۸. بازیابی یک Image از Trash

```
rbd trash restore <image-id>
rbd trash restore <pool-name>/<image-id>
rbd trash restore <pool-name>/<image-id> --image <new-name>
```

---

## 📝 نکات مهم:

* **پیش‌نیاز**: برای استفاده از دستورات RBD، باید به یک کلاستر Ceph فعال دسترسی داشته باشید.
* **پیش‌فرض‌ها**:

  * اگر نام pool مشخص نشود، از pool پیش‌فرض `rbd` استفاده می‌شود.
  * اگر شناسه کاربر مشخص نشود، از کاربر `admin` استفاده می‌شود.
* **Trash**: انتقال image‌ها به trash امکان حذف با تأخیر را فراهم می‌کند. برای حذف نهایی، باید از دستور `rbd trash rm` استفاده کنید.

---
