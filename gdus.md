
### 1. **دیدن سرویس‌ها (Bus Names) روی یک Bus خاص**

```bash
gdbus list-names --system
```

یا

```bash
gdbus list-names --session
```

* `--system` → سرویس‌های روی System Bus
* `--session` → سرویس‌های روی Session Bus

---

### 2. **لیست مسیرها (Objects) برای یک سرویس**

```bash
gdbus introspect --system \
  --dest org.freedesktop.NetworkManager \
  --object-path /
```

* برای دیدن ساختار Object Pathها و متدها و پراپرتی‌ها استفاده می‌شود.
* `--dest` اسم سرویس و `--object-path` مسیر شیء است.

---

### 3. **اجرای یک متد (Call)**

```bash
gdbus call --system \
  --dest org.freedesktop.NetworkManager \
  --object-path /org/freedesktop/NetworkManager \
  --method org.freedesktop.NetworkManager.GetDevices
```

* خروجی معمولاً در قالب **tuple** یا **array** D-Bus است.

---

### 4. **خواندن یک پراپرتی**

```bash
gdbus call --system \
  --dest org.freedesktop.NetworkManager \
  --object-path /org/freedesktop/NetworkManager \
  --method org.freedesktop.DBus.Properties.Get \
  "org.freedesktop.NetworkManager" "Version"
```

---

### 5. **نوشتن روی یک پراپرتی**

```bash
gdbus call --system \
  --dest org.freedesktop.NetworkManager \
  --object-path /org/freedesktop/NetworkManager \
  --method org.freedesktop.DBus.Properties.Set \
  "org.freedesktop.NetworkManager" "WirelessEnabled" "<true>"
```

* توجه کن که نوع داده باید طبق فرمت D-Bus داده شود (مثل `<true>` برای boolean).

---

### 6. **شنیدن سیگنال‌ها**

```bash
gdbus monitor --system \
  --dest org.freedesktop.NetworkManager
```

* برای debug یا بررسی رویدادهای زنده خیلی کاربردی است.

---

### 7. **اجرای introspection کامل یک مسیر**

```bash
gdbus introspect --system \
  --dest org.freedesktop.NetworkManager \
  --object-path /org/freedesktop/NetworkManager
```

* دقیقاً ساختار XML اینترفیس، متدها و سیگنال‌ها را نشان می‌دهد.

---

### 8. **ارسال سیگنال دستی (Testing)**

```bash
gdbus emit --session \
  --object-path /com/example/TestObject \
  --signal com.example.TestSignal "Hello World"
```

* برای تست سرویس‌هایی که به سیگنال گوش می‌دهند.

---

### 9. **لیست پراپرتی‌ها به‌صورت کامل**

```bash
gdbus introspect --system \
  --dest org.freedesktop.NetworkManager \
  --object-path /org/freedesktop/NetworkManager \
  --only-properties
```

*(این آپشن در بعضی نسخه‌ها موجود است)*

---

```bash
gdbus call \
    --session \
    --dest org.freedesktop.Notifications \
    --object-path /org/freedesktop/Notifications \
    --method org.freedesktop.Notifications.Notify \
    "" \
    "uint32 0" \
    "dialog-information" \
    "سلام رفیق!" \
    "این یک اعلان آزمایشی از D-Bus است." \
    "[]" \
    "{}" \
    "int32 5000"

```
