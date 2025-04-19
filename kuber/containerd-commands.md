# 🐳 دستورات پرکاربرد containerd

برای کار با containerd از ابزار CLI به نام `ctr` استفاده می‌کنیم. این ابزار قابلیت‌های اصلی مثل اجرای کانتینر، مدیریت ایمیج، لاگ‌ها و ... را فراهم می‌کند.

---

## 🧰 اطلاعات پایه

```bash
ctr version                # نمایش نسخه containerd
ctr plugins ls             # لیست پلاگین‌های فعال containerd
ctr --help                 # نمایش راهنمای کلی
```

---

## 📦 مدیریت ایمیج‌ها

```bash
ctr images pull docker.io/library/nginx:latest        # دانلود یک ایمیج
ctr images ls                                         # لیست ایمیج‌های موجود
ctr images rm <image-name>                            # حذف یک ایمیج
ctr images export image.tar <image-name>              # خروجی گرفتن از ایمیج
ctr images import image.tar                           # ایمپورت کردن ایمیج از فایل
```

---

## 🚀 اجرای کانتینر

> containerd مستقیماً از runtime پایین‌تری به نام **runc** استفاده می‌کنه، پس اجرای کانتینر پیچیده‌تر از Docker هست.

```bash
ctr run -t --rm docker.io/library/nginx:latest mynginx /bin/sh
```

> ⚠️ توجه: این دستور یک کانتینر به نام `mynginx` ایجاد کرده و وارد شل آن می‌شود. برای اجرای پس‌زمینه و پیچیده‌تر باید از namespace و task استفاده کرد.

---

## 🧪 ساخت و اجرای یک Task

```bash
ctr namespaces ls                                   # لیست namespaceها
ctr namespaces create dev                           # ایجاد namespace جدید
ctr run -n dev -d --rm docker.io/library/nginx:latest nginx /usr/sbin/nginx
```

---

## 🔄 مدیریت کانتینرها و Taskها

```bash
ctr containers ls                                   # لیست کانتینرها
ctr tasks ls                                        # لیست تسک‌ها
ctr tasks kill <task-id>                            # ارسال سیگنال به یک task
ctr tasks delete <task-id>                          # حذف یک task
```

---

## 📁 کار با Snapshotها و Volume

```bash
ctr snapshots ls                                    # لیست snapshotها
ctr snapshots rm <snapshot-id>                      # حذف snapshot
```

---

## 🔧 سایر دستورات مفید

```bash
ctr c create <image> <container-id>                 # ساخت کانتینر بدون اجرا
ctr t start <container-id>                          # اجرای task از کانتینر ساخته شده
ctr t exec --exec-id <id> -t <container-id> <cmd>   # اجرای دستور در task فعال
```

---

> 🧠 نکته: containerd بیشتر برای استفاده برنامه‌محور و توسط Kubernetes یا CRI-O طراحی شده. استفاده دستی از آن با `ctr` برای تست یا دیباگ مفید است، ولی برای تولید بیشتر توسط orchestration tools مثل Kubernetes کنترل می‌شود.

