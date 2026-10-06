# دستور `stat` در لینوکس

دستور `stat` اطلاعات کامل‌تری نسبت به `ls -l` درباره‌ی فایل یا دایرکتوری نمایش می‌دهد.

## استفاده پایه

```bash
stat filename
```

مثال:

```bash
stat /etc/passwd
```

---

## مهم‌ترین خروجی‌های `stat`

| فیلد | معنی |
|---|---|
| `File` | نام فایل |
| `Size` | اندازه فایل بر حسب Byte |
| `Blocks` | تعداد Blockهای مصرف‌شده روی دیسک |
| `IO Block` | اندازه Block مناسب برای I/O |
| `Device` | Device/File System محل فایل |
| `Inode` | شماره Inode فایل |
| `Links` | تعداد Hard Linkها |
| `Access` | Permission فایل |
| `Uid` | User مالک فایل |
| `Gid` | Group مالک فایل |
| `Access` Time | آخرین زمان خوانده شدن فایل |
| `Modify` Time | آخرین تغییر محتوای فایل |
| `Change` Time | آخرین تغییر Metadata |
| `Birth` | زمان ایجاد فایل، اگر File System پشتیبانی کند |

---

## سه زمان مهم

| زمان | تغییر با چه عملیاتی؟ |
|---|---|
| `atime` | خواندن فایل |
| `mtime` | تغییر محتوای فایل |
| `ctime` | تغییر Metadata مثل Permission، Owner یا `mtime` |

نکته مهم:

```text
ctime ≠ Creation Time
```

`ctime` یعنی **Change Time**.

---

## مشاهده اطلاعات File System

```bash
stat -f /path
```

مثال:

```bash
stat -f /
```

اطلاعاتی مثل:

- File System Type
- Block Size
- Total Blocks
- Free Blocks
- Total Inodes
- Free Inodes

---

## نمایش فقط یک مقدار خاص

```bash
stat -c FORMAT filename
```

مثال:

```bash
stat -c '%s' file.txt
```

خروجی:

```text
1024
```

یعنی اندازه فایل `1024 Byte` است.

---

## Formatهای مهم

| Format | معنی |
|---|---|
| `%n` | نام فایل |
| `%s` | اندازه فایل |
| `%i` | Inode |
| `%a` | Permission عددی |
| `%A` | Permission خوانا |
| `%U` | Username مالک |
| `%G` | Group مالک |
| `%u` | UID |
| `%g` | GID |
| `%h` | تعداد Hard Link |
| `%x` | Access Time |
| `%y` | Modify Time |
| `%z` | Change Time |
| `%w` | Birth Time |
| `%F` | نوع فایل |

---

## مثال‌های کاربردی

### Permission فایل

```bash
stat -c '%a' file.txt
```

```text
644
```

### Permission خوانا

```bash
stat -c '%A' file.txt
```

```text
-rw-r--r--
```

### Owner

```bash
stat -c '%U' file.txt
```

### Group

```bash
stat -c '%G' file.txt
```

### Inode

```bash
stat -c '%i' file.txt
```

### Size

```bash
stat -c '%s' file.txt
```

### نوع فایل

```bash
stat -c '%F' file.txt
```

---

## ساخت خروجی سفارشی

```bash
stat -c 'File: %n | Size: %s | Owner: %U | Permission: %a | Inode: %i' file.txt
```

نمونه خروجی:

```text
File: test.txt | Size: 2048 | Owner: root | Permission: 644 | Inode: 123456
```

---

## بررسی چند فایل

```bash
stat file1 file2 file3
```

یا:

```bash
stat *.log
```

---

## تفاوت سریع `ls` و `stat`

| دستور | کاربرد |
|---|---|
| `ls -l` | مشاهده سریع مشخصات فایل |
| `stat` | مشاهده جزئیات کامل Metadata فایل |
| `stat -f` | مشاهده اطلاعات File System |

---

## خلاصه حفظی

```bash
stat file
```

اطلاعات کامل فایل.

```bash
stat -f /
```

اطلاعات File System.

```bash
stat -c '%s' file
```

اندازه فایل.

```bash
stat -c '%a' file
```

Permission عددی.

```bash
stat -c '%U:%G' file
```

Owner و Group.

```bash
stat -c '%i' file
```

Inode.

```bash
stat -c '%y' file
```

آخرین زمان تغییر محتوا.

### نکته طلایی

```text
atime = Access
mtime = Modify Content
ctime = Change Metadata
Birth = Creation
```
