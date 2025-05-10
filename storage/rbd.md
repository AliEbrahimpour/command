
# 📘 دستورات RBD در Ceph (نسخه Mimic)

> منبع: [Ceph Documentation – RBD Commands](https://docs.ceph.com/en/mimic/rbd/rados-rbd-cmds/)

---

## 🧱 ۱. ایجاد Pool برای RBD

```bash
# ایجاد یک pool جدید
ceph osd pool create <pool-name> <pg-num>

# مقداردهی اولیه به pool برای استفاده توسط RBD
rbd pool init <pool-name>
```

---

## 👤 ۲. ایجاد کاربر برای دسترسی به RBD

```bash
# ایجاد کاربر با دسترسی مشخص به pool‌ها
ceph auth get-or-create client.<ID> mon 'profile rbd' osd 'profile rbd pool=<pool-name>, profile rbd-read-only pool=<pool-name>'
```

> 🔑 خروجی این دستور را می‌توان در فایل `/etc/ceph/ceph.client.<ID>.keyring` ذخیره کرد.

---

## 💽 ۳. ایجاد یک Image جدید

```bash
# ایجاد یک image با اندازه مشخص در pool مورد نظر
rbd create --size <size-in-MB> <pool-name>/<image-name>
```

> مثال: ایجاد یک image به نام `bar` با اندازه 1GB در pool `swimmingpool`:

```bash
rbd create --size 1024 swimmingpool/bar
```

---

## 📋 ۴. لیست‌کردن Image‌ها

```bash
# لیست‌کردن image‌ها در pool پیش‌فرض (rbd)
rbd ls

# لیست‌کردن image‌ها در یک pool خاص
rbd ls <pool-name>

# لیست‌کردن image‌هایی که برای حذف در نظر گرفته شده‌اند (trash)
rbd trash ls

# لیست‌کردن image‌های trash در یک pool خاص
rbd trash ls <pool-name>
```

---

## 🔍 ۵. مشاهده اطلاعات یک Image

```bash
# مشاهده اطلاعات یک image خاص
rbd info <image-name>

# مشاهده اطلاعات یک image خاص در یک pool مشخص
rbd info <pool-name>/<image-name>
```

---

## 📏 ۶. تغییر اندازه یک Image

```bash
# افزایش اندازه یک image
rbd resize --size <new-size-in-MB> <image-name>

# کاهش اندازه یک image (با اجازه کاهش)
rbd resize --size <new-size-in-MB> <image-name> --allow-shrink
```

---

## 🗑️ ۷. حذف یک Image

```bash
# حذف مستقیم یک image
rbd rm <image-name>

# حذف یک image از یک pool خاص
rbd rm <pool-name>/<image-name>

# انتقال یک image به trash (حذف با تأخیر)
rbd trash mv <pool-name>/<image-name>

# حذف نهایی یک image از trash
rbd trash rm <pool-name>/<image-id>
```

---

## ♻️ ۸. بازیابی یک Image از Trash

```bash
# بازیابی یک image از trash در pool پیش‌فرض
rbd trash restore <image-id>

# بازیابی یک image از trash در یک pool خاص
rbd trash restore <pool-name>/<image-id>

# بازیابی و تغییر نام یک image هنگام بازیابی
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

اگر نیاز به توضیح بیشتر یا مثال‌های عملی برای هر یک از این دستورات داری، خوشحال می‌شم کمکت کنم! 😊
