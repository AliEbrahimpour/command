# Eventlet چیست؟

**Eventlet** یک کتابخانه Python برای برنامه‌نویسی **غیرهمزمان (asynchronous)** و **شبکه‌های همزمان سبُک (concurrent networking)** است.
این کتابخانه به شما اجازه می‌دهد تا از **green threads (threadهای سبُک)** استفاده کنید تا برنامه‌های I/O-bound را بدون نیاز به thread واقعی مدیریت کنید.

---

## ویژگی‌های اصلی Eventlet

1. **همزمانی سبُک با Green Threads**

   * هر green thread حافظه کمی مصرف می‌کند و می‌تواند هزاران عملیات I/O را همزمان مدیریت کند.
2. **سینتکس ساده**

   * برنامه‌نویسی Eventlet شبیه برنامه‌نویسی همزمان معمولی است، اما بدون بلاک شدن I/O.
3. **پشتیبانی از پروتکل‌های شبکه**

   * TCP, UDP, HTTP, WebSocket و غیره.
4. **Integration با WSGI**

   * مناسب برای سرورها و APIهای همزمان.

---

## مقایسه Eventlet با Threadهای معمولی

| ویژگی                  | Thread معمولی | Eventlet (Green Thread)                                          |
| ---------------------- | ------------- | ---------------------------------------------------------------- |
| مصرف حافظه             | بالا          | پایین                                                            |
| تعداد قابل اجرا همزمان | محدود         | هزاران                                                           |
| I/O-bound مناسب        | بله           | بسیار مناسب                                                      |
| CPU-bound مناسب        | بله           | نه، CPU-bound باید multiprocessing یا native threads استفاده شود |

---

## نصب Eventlet

```bash
pip install eventlet
```

---

## شروع کار با Eventlet

### 1. ایجاد یک Green Thread ساده

```python
import eventlet

def task(n):
    print(f"شروع Task {n}")
    eventlet.sleep(1)
    print(f"پایان Task {n}")

# اجرای همزمان
threads = [eventlet.spawn(task, i) for i in range(5)]
for t in threads:
    t.wait()
```

> `eventlet.spawn()` یک green thread جدید ایجاد می‌کند.
> `eventlet.sleep()` برنامه را بلاک نمی‌کند و سایر green thread‌ها می‌توانند اجرا شوند.

---

### 2. استفاده از `eventlet.monkey_patch()`

برای اینکه کتابخانه‌های استاندارد Python (مثل `socket`, `time`) غیرهمزمان شوند، از **monkey patch** استفاده می‌کنیم:

```python
import eventlet
eventlet.monkey_patch()

import time
import socket

def get_google():
    print("شروع اتصال به Google")
    s = socket.create_connection(("www.google.com", 80))
    s.sendall(b"GET / HTTP/1.1\r\nHost: www.google.com\r\n\r\n")
    print(s.recv(1024))
    s.close()

eventlet.spawn(get_google).wait()
```

> با این روش، `socket` به صورت non-blocking عمل می‌کند و green thread دیگر بلاک نمی‌شود.

---

### 3. اجرای چند کار همزمان

```python
import eventlet

def task(name, duration):
    print(f"{name} شروع شد")
    eventlet.sleep(duration)
    print(f"{name} پایان یافت")

pool = eventlet.GreenPool()
for i in range(5):
    pool.spawn(task, f"Task-{i}", i % 3 + 1)

pool.waitall()
```

> `GreenPool()` به شما اجازه می‌دهد یک **مجموعه از green thread‌ها** ایجاد کنید و مدیریت کنید.

---

### 4. Eventlet برای سرورهای شبکه

#### سرور TCP ساده:

```python
import eventlet

def handle(client_sock, addr):
    print(f"اتصال از {addr}")
    client_sock.sendall(b"سلام از Eventlet!\n")
    client_sock.close()

server = eventlet.listen(('0.0.0.0', 6000))
while True:
    new_sock, addr = server.accept()
    eventlet.spawn(handle, new_sock, addr)
```

> این سرور می‌تواند هزاران اتصال همزمان TCP را با استفاده از green thread مدیریت کند.

---

### نکات مهم

1. Eventlet مناسب **I/O-bound** است، نه **CPU-bound**.
2. با `monkey_patch` می‌توان کتابخانه‌های استاندارد Python را به صورت غیرهمزمان اجرا کرد.
3. برای پروژه‌های real-time یا وب‌سرورها، Eventlet گزینه مناسبی است (مثلاً با Flask و Socket.IO).

---

### مثال عملی: دانلود همزمان صفحات وب

```python
import eventlet
eventlet.monkey_patch()

import requests

urls = [
    "http://example.com",
    "http://httpbin.org/get",
    "http://python.org"
]

def fetch(url):
    print(f"شروع دانلود {url}")
    r = requests.get(url)
    print(f"{url} پایان یافت، طول محتوا: {len(r.text)}")

pool = eventlet.GreenPool()
for url in urls:
    pool.spawn(fetch, url)

pool.waitall()
```
