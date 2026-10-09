# Ceph Day 2 Command Cheat Sheet

خلاصه‌ی دستورات روز دوم Ceph برای مرور سریع.

---

## 1) وضعیت کلی Cluster

### `ceph -s`
**کاربرد:** نمایش خلاصه وضعیت Cluster.

```bash
ceph -s
```

| بخش | توضیح |
|---|---|
| `cluster` | FSID و Health |
| `services` | MON / MGR / OSD |
| `data` | Pool / PG / Object / Usage |
| `io` | Read / Write فعلی |

### `ceph health detail`
**کاربرد:** نمایش جزئیات Warning و Errorها.

```bash
ceph health detail
```

---

## 2) MON و Quorum

### `ceph mon dump`
**کاربرد:** نمایش Monitor Map.

```bash
ceph mon dump
```

| فیلد | توضیح |
|---|---|
| `epoch` | نسخه MonMap |
| `fsid` | شناسه Cluster |
| `mon.*` | اعضای MON |
| `addr` | IP و Port |

### `ceph quorum_status`
**کاربرد:** بررسی اعضای فعلی Quorum.

```bash
ceph quorum_status
```

مثال مفهومی:

```text
3 MON
↓
حداقل 2 عضو برای Quorum
```

---

## 3) MGR

### `ceph mgr dump`
**کاربرد:** نمایش MGR فعال و Standbyها.

```bash
ceph mgr dump
```

### `ceph mgr module ls`
**کاربرد:** نمایش Moduleهای MGR.

```bash
ceph mgr module ls
```

نمونه Moduleها:

```text
dashboard
prometheus
balancer
orchestrator
```

---

## 4) Host و Daemonها

### `ceph orch host ls`
**کاربرد:** نمایش Hostهای تحت مدیریت cephadm.

```bash
ceph orch host ls
```

| فیلد | توضیح |
|---|---|
| `HOST` | Hostname |
| `ADDR` | IP |
| `LABELS` | Labelها |
| `STATUS` | وضعیت |

### `ceph orch ps`
**کاربرد:** نمایش Daemonهای Ceph.

```bash
ceph orch ps
```

نمونه‌ها:

```text
mon
mgr
osd
rgw
mds
```

---

## 5) OSD

### `ceph osd tree`
**کاربرد:** نمایش OSDها در CRUSH tree همراه با `up/down` و `in/out`.

```bash
ceph osd tree
```

| فیلد | توضیح |
|---|---|
| `ID` | شناسه OSD |
| `CLASS` | hdd / ssd / nvme |
| `WEIGHT` | CRUSH Weight |
| `TYPE NAME` | root / host / osd |
| `STATUS` | up / down |
| `REWEIGHT` | مقدار reweight |

```text
up   = daemon در دسترس است
down = daemon در دسترس نیست
in   = در Placement شرکت می‌کند
out  = از Placement خارج شده
```

### `ceph osd df tree`
**کاربرد:** نمایش Capacity و مصرف OSDها.

```bash
ceph osd df tree
```

| فیلد | توضیح |
|---|---|
| `SIZE` | ظرفیت |
| `RAW USE` | مصرف Physical |
| `DATA` | Data |
| `%USE` | درصد استفاده |
| `VAR` | اختلاف از میانگین |

### `ceph osd dump`
**کاربرد:** نمایش OSDMap و تنظیمات Poolها.

```bash
ceph osd dump
```

موارد مهم:

```text
epoch
osd.X up/down
osd.X in/out
pool
size
min_size
pg_num
```

---

## 6) CRUSH

### `ceph osd crush tree`
**کاربرد:** نمایش CRUSH hierarchy.

```bash
ceph osd crush tree
```

مثال:

```text
root default
├── host ceph1
│   ├── osd.0
│   └── osd.1
├── host ceph2
│   ├── osd.2
│   └── osd.3
```

### `ceph osd crush rule ls`
**کاربرد:** نمایش Ruleهای CRUSH.

```bash
ceph osd crush rule ls
```

### `ceph osd crush rule dump`
**کاربرد:** نمایش جزئیات Ruleهای CRUSH.

```bash
ceph osd crush rule dump
```

| مورد | توضیح |
|---|---|
| `take` | نقطه شروع |
| `chooseleaf` | Failure Domain |
| `host` | تفکیک Replica روی Host |
| `rack` | تفکیک Replica روی Rack |
| `emit` | خروجی Placement |

---

## 7) Pool

### `ceph osd pool ls`
**کاربرد:** نمایش Poolها.

```bash
ceph osd pool ls
```

### `ceph osd pool ls detail`
**کاربرد:** نمایش Poolها همراه با تنظیمات.

```bash
ceph osd pool ls detail
```

| فیلد | توضیح |
|---|---|
| `pool` | Pool ID و Name |
| `size` | تعداد Replica |
| `min_size` | حداقل Replica برای I/O |
| `pg_num` | تعداد PG |
| `pgp_num` | Placement PG count |
| `crush_rule` | CRUSH Rule |

### `ceph osd pool create`
**کاربرد:** ساخت Pool.

```bash
ceph osd pool create labpool
```

> ⚠️ در Production قبل از ساخت Pool باید Replication/EC، CRUSH Rule و PG Autoscaler بررسی شود.

### `ceph osd pool application enable`
**کاربرد:** تعیین Application Pool.

```bash
ceph osd pool application enable labpool rados
```

| مقدار | توضیح |
|---|---|
| `labpool` | Pool |
| `rados` | Application |

### `ceph osd pool get`
**کاربرد:** مشاهده یک Property از Pool.

```bash
ceph osd pool get labpool size
ceph osd pool get labpool min_size
ceph osd pool get labpool pg_num
ceph osd pool get labpool pg_autoscale_mode
```

| Property | توضیح |
|---|---|
| `size` | تعداد Replica مطلوب |
| `min_size` | حداقل Replica برای I/O |
| `pg_num` | تعداد PG |
| `pg_autoscale_mode` | وضعیت Autoscaler |

---

## 8) RADOS Object

### `rados -p <pool> put`
**کاربرد:** ذخیره فایل به عنوان RADOS Object.

```bash
echo "Hello Ceph RADOS" >/tmp/hello.txt
rados -p labpool put hello-object /tmp/hello.txt
```

| پارامتر | توضیح |
|---|---|
| `-p labpool` | Pool |
| `put` | Write |
| `hello-object` | Object Name |
| `/tmp/hello.txt` | Source File |

### `rados -p <pool> ls`
**کاربرد:** لیست Objectهای Pool.

```bash
rados -p labpool ls
```

> ⚠️ روی Pool بسیار بزرگ ممکن است خروجی سنگین شود.

### `rados -p <pool> get`
**کاربرد:** خواندن Object.

```bash
rados -p labpool get hello-object /tmp/output.txt
cat /tmp/output.txt
```

---

## 9) Object → PG → OSD

### `ceph osd map`
**کاربرد:** پیدا کردن PG و OSDهای مسئول یک Object.

```bash
ceph osd map labpool hello-object
```

خروجی نمونه:

```text
osdmap e100
pool 'labpool' (7)
object 'hello-object'
-> pg 7.1a
-> up ([12,4,27], p12)
-> acting ([12,4,27], p12)
```

| مقدار | معنی |
|---|---|
| `e100` | OSDMap epoch |
| `pool (7)` | Pool ID |
| `7.1a` | PG ID |
| `up` | Target OSD Set |
| `acting` | OSDهای فعلی مسئول |
| `p12` | Primary OSD |

---

## 10) PG

### `ceph pg stat`
**کاربرد:** خلاصه وضعیت PGها.

```bash
ceph pg stat
```

| State | معنی |
|---|---|
| `active+clean` | سالم و کامل |
| `active+degraded` | I/O فعال ولی Replica ناقص |
| `active+undersized` | Acting Set کمتر از size |
| `peering` | توافق OSDها روی State |
| `recovering` | Recovery |
| `backfilling` | انتقال Data برای Placement جدید |
| `remapped` | Mapping جدید هنوز کامل نشده |
| `inconsistent` | Replicaها ناسازگارند |

### `ceph pg dump`
**کاربرد:** نمایش اطلاعات گسترده PGها.

```bash
ceph pg dump
```

### `ceph pg <PGID> query`
**کاربرد:** بررسی کامل یک PG.

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

### `ceph pg map`
**کاربرد:** نمایش Mapping یک PG.

```bash
ceph pg map 7.1a
```

---

## 11) PG Autoscaler

### `ceph osd pool autoscale-status`
**کاربرد:** نمایش وضعیت PG Autoscaler.

```bash
ceph osd pool autoscale-status
```

موارد مهم:

```text
POOL
SIZE
TARGET SIZE
RATE
PG_NUM
NEW PG_NUM
AUTOSCALE
```

---

## 12) Balancer

### `ceph balancer status`
**کاربرد:** نمایش وضعیت Balancer.

```bash
ceph balancer status
```

Mode رایج:

```text
upmap
```

---

## 13) Scrub / Deep Scrub

### `ceph pg scrub`
**کاربرد:** اجرای Scrub روی PG.

```bash
ceph pg scrub 7.1a
```

یا بسته به نسخه:

```bash
ceph tell 7.1a scrub
```

### `ceph tell <PGID> deep-scrub`
**کاربرد:** بررسی عمیق‌تر Consistency.

```bash
ceph tell 7.1a deep-scrub
```

> ⚠️ روی Production بدون بررسی Load و نیاز واقعی اجرا نشود.

---

## 14) Failure Lab

### Stop OSD
**کاربرد:** شبیه‌سازی خرابی OSD در Lab.

```bash
ceph orch daemon stop osd.2
```

بعد:

```bash
ceph -s
ceph health detail
ceph pg stat
```

برگرداندن:

```bash
ceph orch daemon start osd.2
```

> ⚠️ فقط در Lab یا Maintenance کنترل‌شده.

---

## 15) Trace کامل یک Object

```bash
ceph osd pool create labpool
```

```bash
ceph osd pool application enable labpool rados
```

```bash
echo "Hello Ceph RADOS" >/tmp/hello.txt
```

```bash
rados -p labpool put hello-object /tmp/hello.txt
```

```bash
rados -p labpool ls
```

```bash
ceph osd map labpool hello-object
```

فرض:

```text
pg 7.1a
acting [12,4,27]
```

بعد:

```bash
ceph pg 7.1a query
```

```bash
ceph osd tree
```

```bash
ceph osd crush tree
```

---

## 16) خلاصه سریع

| هدف | دستور |
|---|---|
| وضعیت Cluster | `ceph -s` |
| Health Detail | `ceph health detail` |
| Quorum | `ceph quorum_status` |
| Monitor Map | `ceph mon dump` |
| MGR | `ceph mgr dump` |
| Hosts | `ceph orch host ls` |
| Daemons | `ceph orch ps` |
| OSD topology | `ceph osd tree` |
| OSD capacity | `ceph osd df tree` |
| OSDMap | `ceph osd dump` |
| CRUSH tree | `ceph osd crush tree` |
| CRUSH rules | `ceph osd crush rule dump` |
| Poolها | `ceph osd pool ls detail` |
| Pool property | `ceph osd pool get` |
| Put Object | `rados -p <pool> put` |
| Get Object | `rados -p <pool> get` |
| List Object | `rados -p <pool> ls` |
| Object Mapping | `ceph osd map` |
| PG Status | `ceph pg stat` |
| PG Detail | `ceph pg <PGID> query` |
| PG Mapping | `ceph pg map` |
| Autoscaler | `ceph osd pool autoscale-status` |
| Balancer | `ceph balancer status` |

---

## 17) مفاهیم مهم

| مفهوم | معنی |
|---|---|
| `up` | OSD daemon در دسترس |
| `down` | OSD در دسترس نیست |
| `in` | در Placement شرکت می‌کند |
| `out` | از Placement خارج است |
| `primary` | OSD اصلی PG |
| `replica` | OSDهای دیگر PG |
| `up set` | Placement هدف |
| `acting set` | OSDهای فعلی مسئول |
| `epoch` | نسخه Map |
| `size` | Replica مطلوب |
| `min_size` | حداقل Replica برای I/O |
| `peering` | توافق OSDها روی PG state |
| `recovery` | بازسازی Data |
| `backfill` | انتقال Data برای Placement جدید |

---

## 18) مسیر ذهنی روز دوم

```text
Object
  ↓
Hash
  ↓
PG
  ↓
CRUSH
  ↓
Up Set
  ↓
Acting Set
  ↓
Primary OSD
  ↓
Replica OSDs
  ↓
BlueStore
  ↓
Physical Disk
```

و:

```text
MON
 ↓
Cluster Maps

Client
 ↓
محاسبه Placement
 ↓
Direct I/O to OSD
```

---

## 19) دستورات حساس

این دستورات روی Production بدون Change Plan اجرا نشوند:

```bash
ceph orch daemon stop osd.X
```

```bash
ceph pg scrub PGID
```

```bash
ceph tell PGID deep-scrub
```

همچنین دستورات مدیریتی مانند:

```text
ceph osd out
ceph osd down
ceph osd purge
```

نیاز به بررسی دقیق دارند.

---

## ترتیب مرور پیشنهادی

```text
ceph -s
↓
ceph osd tree
↓
ceph osd crush tree
↓
ceph osd pool ls detail
↓
rados put/get/ls
↓
ceph osd map
↓
ceph pg stat
↓
ceph pg <PGID> query
```
