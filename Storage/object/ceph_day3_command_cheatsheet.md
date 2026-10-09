# Ceph Day 3 Command Cheat Sheet

خلاصه‌ی دستورات روز سوم Ceph برای مرور سریع.

تمرکز:
- RADOS Object
- xattr / OMAP
- BlueStore
- OSD → Disk
- Replication
- Erasure Coding

---

## 1) Poolها

### `ceph osd pool ls`
**کاربرد:** نمایش Poolهای موجود.

```bash
ceph osd pool ls
```

---

## 2) ساخت Object در RADOS

### `rados -p <pool> put`
**کاربرد:** ذخیره فایل به عنوان RADOS Object.

```bash
echo "Hello Ceph Day 3" >/tmp/day3.txt
rados -p labpool put day3-object /tmp/day3.txt
```

| پارامتر | توضیح |
|---|---|
| `-p labpool` | Pool |
| `put` | Write |
| `day3-object` | Object Name |
| `/tmp/day3.txt` | Source |

---

## 3) خواندن Object

### `rados -p <pool> get`

```bash
rados -p labpool get day3-object /tmp/day3-read.txt
cat /tmp/day3-read.txt
```

| پارامتر | توضیح |
|---|---|
| `get` | Read |
| `day3-object` | Object |
| `/tmp/day3-read.txt` | فایل مقصد |

---

## 4) اطلاعات Object

### `rados -p <pool> stat`
**کاربرد:** نمایش Size و mtime.

```bash
rados -p labpool stat day3-object
```

| فیلد | توضیح |
|---|---|
| `size` | اندازه Object |
| `mtime` | زمان آخرین تغییر |

---

## 5) لیست Objectها

### `rados -p <pool> ls`

```bash
rados -p labpool ls
```

> ⚠️ روی Poolهای بزرگ Production ممکن است خروجی سنگین شود.

---

## 6) xattr

### `rados setxattr`
**کاربرد:** ثبت Metadata کوچک روی Object.

```bash
rados -p labpool setxattr day3-object customer 100
```

```bash
rados -p labpool setxattr day3-object project storage-lab
```

| پارامتر | توضیح |
|---|---|
| `setxattr` | ثبت Attribute |
| `day3-object` | Object |
| `customer` | Key |
| `100` | Value |

### `rados listxattr`

```bash
rados -p labpool listxattr day3-object
```

### `rados getxattr`

```bash
rados -p labpool getxattr day3-object customer
```

### `rados rmxattr`

```bash
rados -p labpool rmxattr day3-object customer
```

> ⚠️ روی Objectهای Production بدون شناخت Metadata داخلی چیزی حذف نکن.

---

## 7) OMAP

### `rados setomapval`
**کاربرد:** ثبت Key/Value در OMAP Object.

```bash
rados -p labpool setomapval day3-object invoice 10001
```

```bash
rados -p labpool setomapval day3-object state active
```

| پارامتر | توضیح |
|---|---|
| `setomapval` | ثبت OMAP |
| `day3-object` | Object |
| `invoice` | Key |
| `10001` | Value |

### `rados listomapkeys`

```bash
rados -p labpool listomapkeys day3-object
```

### `rados listomapvals`

```bash
rados -p labpool listomapvals day3-object
```

### `rados getomapval`

```bash
rados -p labpool getomapval day3-object invoice
```

### `rados rmomapkey`

```bash
rados -p labpool rmomapkey day3-object invoice
```

> ⚠️ روی Objectهای سرویس‌هایی مثل RGW/RBD بدون شناخت ساختار OMAP چیزی حذف نکن.

---

## 8) تفاوت Data / xattr / OMAP

| مورد | کاربرد |
|---|---|
| Object Data | Payload اصلی |
| xattr | Metadata کوچک |
| OMAP | Key/Value Map |
| Object Name | شناسه Object |

```text
RADOS Object
├── Data
├── xattrs
└── OMAP
```

---

## 9) Object → PG → OSD

### `ceph osd map`
**کاربرد:** پیدا کردن PG و OSDهای مسئول Object.

```bash
ceph osd map labpool day3-object
```

خروجی نمونه:

```text
osdmap e201
pool 'labpool' (7)
object 'day3-object'
-> pg 7.1a
-> up ([12,4,27], p12)
-> acting ([12,4,27], p12)
```

| مقدار | معنی |
|---|---|
| `e201` | OSDMap epoch |
| `7` | Pool ID |
| `7.1a` | PG |
| `up` | Target Set |
| `acting` | OSDهای فعلی |
| `p12` | Primary = osd.12 |

---

## 10) PG Detail

### `ceph pg <PGID> query`

```bash
ceph pg 7.1a query
```

موارد مهم:

```text
state
up
acting
recovery_state
peer_info
info
```

---

## 11) OSD و Host

### `ceph osd tree`
**کاربرد:** پیدا کردن Host مربوط به OSDها.

```bash
ceph osd tree
```

نمونه:

```text
host ceph1
  osd.12

host ceph2
  osd.4

host ceph3
  osd.27
```

---

## 12) CRUSH Layout

### `ceph osd crush tree`

```bash
ceph osd crush tree
```

---

## 13) Replication Policy

### `ceph osd pool get <pool> size`

```bash
ceph osd pool get labpool size
```

مثال:

```text
size: 3
```

### `ceph osd pool get <pool> min_size`

```bash
ceph osd pool get labpool min_size
```

مثال:

```text
size = 3
min_size = 2
```

---

## 14) BlueStore / OSD Device Layout

### `ceph-volume lvm list`
**کاربرد:** نمایش OSD و LVM/Device مربوط به آن.

```bash
ceph-volume lvm list
```

| مورد | توضیح |
|---|---|
| `osd id` | OSD ID |
| `osd fsid` | OSD UUID |
| `devices` | Physical Device |
| `lv path` | Logical Volume |
| `type` | block / db / wal |

مسیر:

```text
OSD
 ↓
LVM
 ↓
Physical Disk
```

---

## 15) Block Deviceهای Host

### `lsblk`

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

| ستون | توضیح |
|---|---|
| `NAME` | Device |
| `SIZE` | ظرفیت |
| `TYPE` | disk / part / lvm |
| `FSTYPE` | Filesystem |
| `MOUNTPOINTS` | Mount Point |

---

## 16) پیدا کردن OSD Daemonها

### `ceph orch ps --daemon-type osd`

```bash
ceph orch ps --daemon-type osd
```

**کاربرد:** پیدا کردن OSD و Host اجراکننده آن.

---

## 17) مفاهیم BlueStore

| مورد | توضیح |
|---|---|
| `block` | Device اصلی Object Data |
| `block.db` | RocksDB/Metadata روی Fast Device |
| `block.wal` | WAL جدا در صورت وجود |
| RocksDB | Metadata DB داخلی |
| BlueFS | Filesystem داخلی RocksDB |

---

## 18) وضعیت PG هنگام Failure

### `ceph pg stat`

```bash
ceph pg stat
```

| State | توضیح |
|---|---|
| `active+clean` | سالم |
| `active+degraded` | Replica ناقص |
| `active+undersized` | Acting Set کمتر از size |
| `recovering` | Recovery |
| `backfilling` | انتقال Data |
| `peering` | توافق روی PG state |

---

## 19) Health هنگام Recovery

### `ceph -s`

```bash
ceph -s
```

### `ceph health detail`

```bash
ceph health detail
```

برای بررسی:

```text
Degraded Objects
Recovery
Backfill
OSD Down
PG State
```

---

## 20) ساخت EC Profile

### `ceph osd erasure-code-profile set`

```bash
ceph osd erasure-code-profile set lab-ec-profile   plugin=isa   k=2   m=1   crush-failure-domain=host
```

| پارامتر | توضیح |
|---|---|
| `lab-ec-profile` | Profile Name |
| `plugin=isa` | EC Plugin |
| `k=2` | Data Chunks |
| `m=1` | Coding Chunks |
| `crush-failure-domain=host` | هر Chunk روی Host جدا |

```text
Total chunks = k + m
             = 3
```

> ⚠️ فقط در Lab یا طراحی کنترل‌شده.

---

## 21) مشاهده EC Profile

### `ceph osd erasure-code-profile get`

```bash
ceph osd erasure-code-profile get lab-ec-profile
```

---

## 22) لیست EC Profileها

### `ceph osd erasure-code-profile ls`

```bash
ceph osd erasure-code-profile ls
```

---

## 23) ساخت EC Pool

### `ceph osd pool create ... erasure`

```bash
ceph osd pool create lab-ec erasure lab-ec-profile
```

| مقدار | توضیح |
|---|---|
| `lab-ec` | Pool |
| `erasure` | Pool Type |
| `lab-ec-profile` | Profile |

> ⚠️ تعداد Host و Failure Domain باید با `k+m` سازگار باشد.

---

## 24) تست Object روی EC Pool

```bash
echo "hello erasure coding" >/tmp/ec.txt
```

```bash
rados -p lab-ec put ec-object /tmp/ec.txt
```

```bash
rados -p lab-ec get ec-object /tmp/ec-read.txt
cat /tmp/ec-read.txt
```

---

## 25) Mapping Object در EC Pool

```bash
ceph osd map lab-ec ec-object
```

برای:

```text
k=2
m=1
```

انتظار داریم Acting Set شامل 3 OSD باشد.

---

## 26) بررسی Pool Type

### `ceph osd pool ls detail`

```bash
ceph osd pool ls detail
```

موارد مهم:

```text
replicated
erasure
size
min_size
erasure_code_profile
```

---

## 27) Device Class

### `ceph osd tree`

```bash
ceph osd tree
```

Classهای رایج:

```text
hdd
ssd
nvme
```

---

## 28) CRUSH Rule

### `ceph osd crush rule dump`

```bash
ceph osd crush rule dump
```

موارد مهم:

```text
take
chooseleaf
failure-domain
device class
```

---

## 29) Trace کامل Object

### مرحله 1

```bash
echo "Hello Ceph Day 3" >/tmp/day3.txt
```

### مرحله 2

```bash
rados -p labpool put day3-object /tmp/day3.txt
```

### مرحله 3

```bash
rados -p labpool stat day3-object
```

### مرحله 4

```bash
rados -p labpool setxattr day3-object customer 100
```

### مرحله 5

```bash
rados -p labpool setomapval day3-object state active
```

### مرحله 6

```bash
ceph osd map labpool day3-object
```

فرض:

```text
PG = 7.1a
acting = [12,4,27]
```

### مرحله 7

```bash
ceph pg 7.1a query
```

### مرحله 8

```bash
ceph osd tree
```

### مرحله 9

```bash
ceph-volume lvm list
```

### مرحله 10

```bash
lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS
```

مسیر:

```text
RADOS Object
 ↓
PG
 ↓
Primary + Replica OSDs
 ↓
BlueStore
 ↓
LVM / Block Device
 ↓
Physical Disk
```

---

## 30) Trace کامل xattr

```bash
rados -p labpool setxattr day3-object customer 100
```

```bash
rados -p labpool listxattr day3-object
```

```bash
rados -p labpool getxattr day3-object customer
```

```bash
rados -p labpool rmxattr day3-object customer
```

---

## 31) Trace کامل OMAP

```bash
rados -p labpool setomapval day3-object invoice 10001
```

```bash
rados -p labpool setomapval day3-object state active
```

```bash
rados -p labpool listomapkeys day3-object
```

```bash
rados -p labpool listomapvals day3-object
```

```bash
rados -p labpool getomapval day3-object state
```

```bash
rados -p labpool rmomapkey day3-object invoice
```

---

## 32) خلاصه دستورات روز سوم

| هدف | دستور |
|---|---|
| Object Write | `rados -p <pool> put` |
| Object Read | `rados -p <pool> get` |
| Object Stat | `rados -p <pool> stat` |
| Object List | `rados -p <pool> ls` |
| Set xattr | `rados -p <pool> setxattr` |
| List xattr | `rados -p <pool> listxattr` |
| Get xattr | `rados -p <pool> getxattr` |
| Remove xattr | `rados -p <pool> rmxattr` |
| Set OMAP | `rados -p <pool> setomapval` |
| List OMAP Keys | `rados -p <pool> listomapkeys` |
| List OMAP Values | `rados -p <pool> listomapvals` |
| Get OMAP | `rados -p <pool> getomapval` |
| Remove OMAP Key | `rados -p <pool> rmomapkey` |
| Object Mapping | `ceph osd map` |
| PG Detail | `ceph pg <PGID> query` |
| OSD Tree | `ceph osd tree` |
| Pool Size | `ceph osd pool get <pool> size` |
| Pool Min Size | `ceph osd pool get <pool> min_size` |
| OSD Device Mapping | `ceph-volume lvm list` |
| Block Devices | `lsblk` |
| EC Profile Create | `ceph osd erasure-code-profile set` |
| EC Profile Show | `ceph osd erasure-code-profile get` |
| EC Profile List | `ceph osd erasure-code-profile ls` |
| EC Pool Create | `ceph osd pool create ... erasure` |

---

## 33) Replication vs EC

| ویژگی | Replication | Erasure Coding |
|---|---|---|
| مدل | Full Copy | Data + Coding Chunks |
| مثال | `size=3` | `k=4,m=2` |
| Capacity Cost | بیشتر | کمتر |
| Small Write | ساده‌تر | سنگین‌تر |
| Recovery | ساده‌تر | CPU/Network بیشتر |
| Metadata/OMAP | مناسب | Replicated معمولاً بهتر |
| Large Object Data | مناسب | بسیار مناسب |

---

## 34) دستورات حساس

روی Production بدون شناخت دقیق Object اجرا نکن:

```bash
rados -p <pool> rmxattr ...
```

```bash
rados -p <pool> rmomapkey ...
```

همچنین EC Pool را بدون بررسی این موارد نساز:

```text
k
m
Failure Domain
تعداد Host
Device Class
CRUSH Rule
Recovery Cost
Capacity
```

---

## 35) ترتیب مرور پیشنهادی

```text
rados put/get/stat
↓
xattr
↓
OMAP
↓
ceph osd map
↓
ceph pg query
↓
ceph osd tree
↓
ceph-volume lvm list
↓
lsblk
↓
Replication
↓
Erasure Coding
```

---

## 36) مسیر ذهنی اصلی روز سوم

```text
RADOS Object
 ├── Data
 ├── xattr
 └── OMAP
      ↓
PG
      ↓
CRUSH
      ↓
Primary OSD
      ↓
Replica / EC Chunks
      ↓
BlueStore
 ├── Object Data
 ├── RocksDB
 └── BlueFS
      ↓
block / block.db / block.wal
      ↓
Physical Device
```
