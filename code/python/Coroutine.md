# آموزش کامل Coroutine در Python

Coroutine‌ها یکی از ابزارهای قدرتمند Python برای برنامه‌نویسی **غیرهمزمان (asynchronous)** و **مدیریت هم‌زمانی بدون Thread** هستند. در این مستند، تمامی مراحل، مفاهیم و مثال‌های عملی ارائه شده است.

---

## فهرست مطالب
1. [Coroutine چیست؟](#coroutine-چیست)
2. [تفاوت Coroutine با Function معمولی](#تفاوت-coroutine-با-function-معمولی)
3. [ایجاد Coroutine](#ایجاد-coroutine)
4. [اجرای Coroutine](#اجرای-coroutine)
5. [Await و Async](#await-و-async)
6. [Coroutine با asyncio](#coroutine-با-asyncio)
7. [استفاده‌های پیشرفته](#استفاده‌های-پیشرفته)
8. [مثال عملی](#مثال-عملی)

---

## Coroutine چیست؟

- **Coroutine** یک تابع ویژه است که می‌تواند اجرای خود را **متوقف و سپس دوباره ادامه دهد**.
- این قابلیت باعث می‌شود که بتوانید **کارهای غیرهمزمان** را با سبک برنامه‌نویسی مشابه کدهای همزمان مدیریت کنید.
- در Python، Coroutine‌ها معمولاً با `async def` تعریف می‌شوند.

### نکته:
Coroutine با Generator متفاوت است اما شباهت‌هایی دارد. Generator فقط مقادیر تولید می‌کند، اما Coroutine می‌تواند عملیات غیرهمزمان انجام دهد و `await` بگیرد.

---

## تفاوت Coroutine با Function معمولی

| ویژگی | Function معمولی | Coroutine |
|--------|----------------|-----------|
| تعریف | `def func():` | `async def func():` |
| برگشت | `return` | می‌تواند `await` بگیرد و مقدار برگرداند |
| اجرای همزمان | بلافاصله اجرا می‌شود | برای اجرا نیاز به Event Loop دارد |
| توقف و ادامه | ندارد | دارد (`await`, `yield`) |

---

## ایجاد Coroutine

```python
# تعریف یک coroutine ساده
async def my_coroutine():
    print("شروع Coroutine")
    await asyncio.sleep(1)  # شبیه توقف و انتظار
    print("پایان Coroutine")
````

### نکته:

* بدون `async`, `await` کار نمی‌کند.
* Coroutine فقط یک **object قابل انتظار** تولید می‌کند و برای اجرا نیاز به Event Loop دارد.

---

## اجرای Coroutine

برای اجرای Coroutine دو روش داریم:

### 1. استفاده از asyncio.run (Python 3.7+)

```python
import asyncio

async def hello():
    print("سلام")
    await asyncio.sleep(1)
    print("خداحافظ")

asyncio.run(hello())
```

### 2. استفاده از Event Loop

```python
import asyncio

async def hello():
    print("سلام")
    await asyncio.sleep(1)
    print("خداحافظ")

loop = asyncio.get_event_loop()
loop.run_until_complete(hello())
loop.close()
```

---

## Await و Async

### `async`:

* قبل از تعریف تابع می‌آید.
* مشخص می‌کند که این تابع یک **Coroutine** است.

### `await`:

* انتظار می‌کشد تا یک Coroutine یا Future به پایان برسد.
* فقط داخل یک Coroutine معتبر می‌تواند استفاده شود.

```python
async def task1():
    print("Task1 شروع")
    await asyncio.sleep(2)
    print("Task1 پایان")
```

---

## Coroutine با asyncio

`asyncio` یک ماژول استاندارد Python برای مدیریت **Event Loop** و اجرای Coroutine‌ها است.

### اجرای چند Coroutine همزمان

```python
import asyncio

async def task1():
    await asyncio.sleep(1)
    print("Task1 پایان")

async def task2():
    await asyncio.sleep(2)
    print("Task2 پایان")

async def main():
    await asyncio.gather(task1(), task2())

asyncio.run(main())
```

> خروجی به ترتیب زمان پایان Coroutine‌ها خواهد بود: Task1، سپس Task2

---

## استفاده‌های پیشرفته

1. **Timeout و Cancellation**

```python
async def my_task():
    await asyncio.sleep(5)
    print("کار تمام شد")

async def main():
    try:
        await asyncio.wait_for(my_task(), timeout=2)
    except asyncio.TimeoutError:
        print("زمان تمام شد!")

asyncio.run(main())
```

2. **Coroutine با Generator**

```python
async def counter():
    for i in range(5):
        print(i)
        await asyncio.sleep(1)

asyncio.run(counter())
```

3. **Pipeline غیرهمزمان**

* Coroutine‌ها می‌توانند به صورت **زنجیره‌ای** داده‌ها را پردازش کنند، شبیه به **async iterator**.

---

## مثال عملی

```python
import asyncio
import random

async def download_file(file_id):
    print(f"شروع دانلود {file_id}")
    await asyncio.sleep(random.randint(1, 5))
    print(f"دانلود {file_id} تمام شد")
    return file_id

async def main():
    files = [1, 2, 3, 4, 5]
    results = await asyncio.gather(*(download_file(f) for f in files))
    print("تمام فایل‌ها دانلود شد:", results)

asyncio.run(main())
```

### خروجی نمونه:

```
شروع دانلود 1
شروع دانلود 2
...
دانلود 1 تمام شد
دانلود 3 تمام شد
...
تمام فایل‌ها دانلود شد: [1,2,3,4,5]
```

> مشاهده می‌کنید که همه دانلود‌ها به صورت **غیرهمزمان** انجام شد و سرعت اجرای کل بهبود یافت.

---

## جمع‌بندی

* Coroutine‌ها ابزار قوی برای برنامه‌نویسی غیرهمزمان هستند.
* برای استفاده، نیاز به `async def` و `await` داریم.
* با `asyncio` می‌توان چند Coroutine را همزمان اجرا کرد و کارهای I/O-bound را بهینه کرد.
* قابلیت‌هایی مثل **timeout, cancellation, async iteration** باعث انعطاف بیشتر می‌شوند.

---

**منابع بیشتر برای مطالعه:**

* [Python asyncio documentation](https://docs.python.org/3/library/asyncio.html)
* [PEP 492 – Coroutines with async and await syntax](https://www.python.org/dev/peps/pep-0492/)

