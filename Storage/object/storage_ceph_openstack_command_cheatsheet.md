# Storage / Ceph / OpenStack Command Cheat Sheet

این فایل خلاصه‌ی دستورات مطرح‌شده تا این مرحله از آموزش **Block Storage، Filesystem، Ceph RBD، RADOS، PG، CRUSH، OSD و OpenStack/Cinder** است.

> هدف: مرور سریع دستورها همراه با کاربرد، مثال کامل و پارامترهای مهم.

---

# 1) Linux Filesystem & Block Device

## `lsblk`

**کاربرد:** نمایش Block Deviceها، پارتیشن‌ها، Filesystem و Mount Pointها.

### مثال کامل

```bash
lsblk -f
```

### خروجی نمونه

```text
NAME   FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sda
├─sda1 ext4   1.0         db3bb021-e1b1-420e-b04d-32fad79221f9   90G     5% /
└─sda2 swap   1           ...
sdb    xfs    5           ...
```

### پارامترهای مهم

| پارامتر | توضیح |
|---|---|
| `-f` | نمایش Filesystem، UUID، Label و Mount Point |
| `-o` | تعیین ستون‌های خروجی |
| `NAME` | نام Device |
| `SIZE` | ظرفیت |
| `TYPE` | نوع Device |
| `LOG-SEC` | Logical sector size |
| `PHY-SEC` | Physical sector size |

### نمونه برای بررسی Sector Size

```bash
lsblk -o NAME,SIZE,TYPE,LOG-SEC,PHY-SEC
```

---

## `df`

**کاربرد:** نمایش میزان مصرف و فضای آزاد Filesystemهای Mount شده.

### مثال کامل

```bash
df -Th
```

### پارامترهای مهم

| پارامتر | توضیح |
|---|---|
| `-h` | نمایش Human-readable مثل GiB |
| `-T` | نمایش نوع Filesystem |

### نکته

`df` فضای آزاد را از دید **Filesystem داخل سیستم‌عامل** نشان می‌دهد، نه ظرفیت آزاد واقعی Ceph Cluster.

---

## `findmnt`

**کاربرد:** مشخص کردن اینکه یک مسیر روی چه Filesystem/Deviceای Mount شده است.

### مثال کامل

```bash
findmnt /
```

### مثال

```text
TARGET SOURCE    FSTYPE OPTIONS
/      /dev/sda1 ext4   rw,relatime
```

### پارامتر مهم

| پارامتر | توضیح |
|---|---|
| `TARGET` | مسیر Mount |
| `SOURCE` | Device یا Backend |
| `FSTYPE` | نوع Filesystem |

---

## `stat`

**کاربرد:** نمایش Metadata یک File یا Directory.

### مثال کامل

```bash
stat /tmp/storage-lab/photos/2026/test.txt
```

### اطلاعات مهم

| فیلد | توضیح |
|---|---|
| `Size` | اندازه فایل |
| `Blocks` | Blockهای مصرف‌شده |
| `IO Block` | اندازه Block ترجیحی I/O |
| `Inode` | شماره inode |
| `Access` | Permission |
| `Uid/Gid` | Owner و Group |
| `Modify` | زمان تغییر محتوا |
| `Change` | زمان تغییر Metadata |

---

## `ls -li`

**کاربرد:** نمایش فایل همراه با inode.

### مثال کامل

```bash
ls -li /tmp/storage-lab/photos/2026/test.txt
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `-l` | Long format |
| `-i` | نمایش inode |

---

## `mkfs.xfs`

**کاربرد:** ساخت XFS Filesystem روی Block Device.

> ⚠️ این دستور تمام اطلاعات Device هدف را از بین می‌برد.

### مثال کامل

```bash
mkfs.xfs /dev/vdb
```

### پارامتر اصلی

| پارامتر | توضیح |
|---|---|
| `/dev/vdb` | Block Device هدف |

---

## `mount`

**کاربرد:** Mount کردن Filesystem روی یک Directory.

### مثال کامل

```bash
mkdir -p /data
mount /dev/vdb /data
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `/dev/vdb` | Device |
| `/data` | Mount Point |

---

## `xfs_info`

**کاربرد:** نمایش ساختار و Geometry یک XFS Filesystem.

### مثال کامل

```bash
xfs_info /data
```

### موارد مهم خروجی

| فیلد | توضیح |
|---|---|
| `bsize` | Filesystem block size |
| `blocks` | تعداد Blockها |
| `sectsz` | Sector size |
| `agcount` | تعداد Allocation Group |

---

## `tune2fs`

**کاربرد:** نمایش یا تغییر تنظیمات ext2/ext3/ext4.

### مثال امن برای مشاهده

```bash
tune2fs -l /dev/vdb1
```

### پارامتر

| پارامتر | توضیح |
|---|---|
| `-l` | فقط نمایش Superblock information |

---

## `fstrim`

**کاربرد:** اعلام Blockهای آزادشده Filesystem به Storage Layer برای Reclaim Space.

### مثال کامل

```bash
fstrim -av
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `-a` | اجرا روی همه Filesystemهای سازگار |
| `-v` | نمایش مقدار Trim شده |

### مسیر مفهومی

```text
Filesystem
  ↓
DISCARD / TRIM
  ↓
virtio / QEMU
  ↓
RBD
  ↓
Ceph / BlueStore
```

---

# 2) Linux File / I/O Test Commands

## `dd`

**کاربرد:** ایجاد یک Write Sequential ساده برای تست تخصیص Storage.

### مثال کامل

```bash
dd if=/dev/zero \
   of=/data/test.img \
   bs=1M \
   count=1024 \
   oflag=direct
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `if=` | Input file |
| `of=` | Output file |
| `bs=` | Block size هر عملیات |
| `count=` | تعداد Blockها |
| `oflag=direct` | تلاش برای Direct I/O و دور زدن Page Cache |

### نتیجه

```text
1 MiB × 1024 ≈ 1 GiB write
```

---

## `fio`

**کاربرد:** تست حرفه‌ای I/O مثل Random Read/Write، Latency و IOPS.

### مثال کامل

```bash
fio \
  --name=rbd-test \
  --filename=/data/fio.test \
  --size=2G \
  --rw=randwrite \
  --bs=4k \
  --iodepth=32 \
  --direct=1
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `--name=` | نام Job |
| `--filename=` | فایل یا Device هدف |
| `--size=` | حجم تست |
| `--rw=` | نوع workload |
| `--bs=` | I/O block size |
| `--iodepth=` | Queue depth |
| `--direct=1` | استفاده از Direct I/O |

### مثال‌های `--rw`

| مقدار | کاربرد |
|---|---|
| `read` | Sequential Read |
| `write` | Sequential Write |
| `randread` | Random Read |
| `randwrite` | Random Write |
| `randrw` | Random Read/Write |

---

# 3) OpenStack Volume / Cinder

## `openstack volume create`

**کاربرد:** ساخت Cinder Volume.

### مثال کامل

```bash
openstack volume create \
  --size 100 \
  --type ceph \
  db-volume
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `--size 100` | سایز Volume بر حسب GiB |
| `--type ceph` | Volume Type |
| `db-volume` | نام Volume |

### مسیر کنترل

```text
OpenStack CLI
 ↓
Cinder API
 ↓
Cinder Scheduler
 ↓
cinder-volume
 ↓
RBD Driver
 ↓
Ceph RBD Image
```

---

## `openstack volume show`

**کاربرد:** مشاهده وضعیت و اطلاعات Volume.

### مثال کامل

```bash
openstack volume show db-volume
```

### موارد مهم

| فیلد | توضیح |
|---|---|
| `id` | UUID Volume |
| `size` | ظرفیت |
| `status` | available / in-use |
| `type` | Volume Type |
| `attachments` | اتصال به VM |

---

## `openstack server add volume`

**کاربرد:** Attach کردن Volume به یک VM.

### مثال کامل

```bash
openstack server add volume vm01 db-volume
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `vm01` | Server Name/UUID |
| `db-volume` | Volume Name/UUID |

### مسیر

```text
Nova
 ↓
nova-compute
 ↓
libvirt
 ↓
QEMU
 ↓
librbd
 ↓
Ceph
```

---

## `openstack volume set --size`

**کاربرد:** Extend کردن Logical Size یک Volume.

### مثال

```bash
openstack volume set --size 200 VOLUME_UUID
```

> بعد از Extend کردن Cinder Volume معمولاً باید Partition و Filesystem داخل Guest نیز Extend شوند.

---

# 4) Ceph Cluster Status

## `ceph -s`

**کاربرد:** مهم‌ترین دستور برای مشاهده وضعیت کلی Cluster.

### مثال

```bash
ceph -s
```

### بخش‌های مهم

| بخش | توضیح |
|---|---|
| `cluster` | FSID و Health |
| `services` | MON/MGR/OSD و سرویس‌ها |
| `data` | Pool/PG/Object/Usage |
| `io` | Read/Write throughput |

---

## `ceph health detail`

**کاربرد:** نمایش جزئیات Warning/Errorهای Health.

### مثال

```bash
ceph health detail
```

---

# 5) Ceph Daemons / Hosts

## `ceph orch host ls`

**کاربرد:** نمایش Hostهای تحت مدیریت cephadm.

### مثال

```bash
ceph orch host ls
```

### فیلدهای مهم

| فیلد | توضیح |
|---|---|
| `HOST` | Hostname |
| `ADDR` | IP |
| `LABELS` | Cephadm labels |
| `STATUS` | وضعیت Host |

---

## `ceph orch ps`

**کاربرد:** نمایش Daemonهای مدیریت‌شده توسط cephadm.

### مثال

```bash
ceph orch ps
```

### موارد مهم

```text
mon
mgr
osd
rgw
mds
prometheus
alertmanager
```

---

## `ceph orch daemon stop/start`

**کاربرد:** Stop/Start یک Ceph daemon.

> ⚠️ فقط برای Lab یا Maintenance کنترل‌شده.

### مثال

```bash
ceph orch daemon stop osd.2
```

برگرداندن:

```bash
ceph orch daemon start osd.2
```

### پارامتر

| مقدار | توضیح |
|---|---|
| `osd.2` | نام دقیق Daemon |

---

# 6) MON / Quorum / Maps

## `ceph mon dump`

**کاربرد:** نمایش Monitor Map.

### مثال

```bash
ceph mon dump
```

### موارد مهم

| فیلد | توضیح |
|---|---|
| `epoch` | Version فعلی MonMap |
| `fsid` | Cluster FSID |
| `mon.*` | اعضای MON |
| `addr` | IP/Port |

---

## `ceph quorum_status`

**کاربرد:** بررسی Quorum مانیتورها.

### مثال

```bash
ceph quorum_status
```

### مفهوم

در Cluster سه MON:

```text
3 MON → حداقل 2 عضو برای quorum
```

---

## `ceph osd dump`

**کاربرد:** نمایش OSDMap، Poolها و تنظیمات مرتبط.

### مثال

```bash
ceph osd dump
```

### موارد مهم

```text
epoch
pool
size
min_size
pg_num
osd.X up/down
osd.X in/out
```

---

# 7) OSD Topology / Capacity

## `ceph osd tree`

**کاربرد:** نمایش OSDها در CRUSH hierarchy همراه با UP/DOWN و IN/OUT.

### مثال

```bash
ceph osd tree
```

### فیلدها

| فیلد | توضیح |
|---|---|
| `ID` | OSD/Bucket ID |
| `CLASS` | hdd / ssd / nvme |
| `WEIGHT` | CRUSH weight |
| `TYPE NAME` | root/host/osd |
| `STATUS` | up/down |
| `REWEIGHT` | OSD reweight |

---

## `ceph osd df tree`

**کاربرد:** نمایش Capacity و Utilization OSDها در ساختار CRUSH.

### مثال

```bash
ceph osd df tree
```

### فیلدهای مهم

| فیلد | توضیح |
|---|---|
| `SIZE` | ظرفیت OSD |
| `RAW USE` | مصرف Physical |
| `DATA` | Data |
| `%USE` | درصد استفاده |
| `VAR` | میزان انحراف از میانگین |

---

# 8) CRUSH

## `ceph osd crush tree`

**کاربرد:** نمایش CRUSH hierarchy.

### مثال

```bash
ceph osd crush tree
```

### ساختار نمونه

```text
root default
├── host ceph1
│   ├── osd.0
│   └── osd.1
├── host ceph2
│   ├── osd.2
│   └── osd.3
```

---

## `ceph osd crush rule ls`

**کاربرد:** نمایش CRUSH Ruleها.

### مثال

```bash
ceph osd crush rule ls
```

---

## `ceph osd crush rule dump`

**کاربرد:** نمایش جزئیات Ruleهای CRUSH.

### مثال

```bash
ceph osd crush rule dump
```

### موارد مهم

| مورد | توضیح |
|---|---|
| `take` | Root/Device class مبدا |
| `chooseleaf` | نوع Failure Domain |
| `host` | Replicaها روی Host جدا |
| `rack` | Replicaها روی Rack جدا |
| `emit` | خروجی Placement |

---

# 9) Pool

## `ceph osd pool ls`

**کاربرد:** لیست Poolها.

### مثال

```bash
ceph osd pool ls
```

---

## `ceph osd pool ls detail`

**کاربرد:** نمایش Poolها با تنظیمات کامل.

### مثال

```bash
ceph osd pool ls detail
```

### موارد مهم

```text
pool id
size
min_size
pg_num
pgp_num
crush_rule
application
```

---

## `ceph osd pool create`

**کاربرد:** ساخت Pool.

### مثال Lab

```bash
ceph osd pool create labpool
```

> ⚠️ در Production قبل از ساخت Pool باید PG Autoscaler، CRUSH Rule، Replication/EC و Application بررسی شوند.

---

## `ceph osd pool application enable`

**کاربرد:** مشخص کردن Application استفاده‌کننده از Pool.

### مثال

```bash
ceph osd pool application enable labpool rados
```

### پارامترها

| مقدار | توضیح |
|---|---|
| `labpool` | Pool |
| `rados` | Application label |

نمونه‌های دیگر:

```text
rbd
cephfs
rgw
```

---

## `ceph osd pool get`

**کاربرد:** مشاهده یک Property از Pool.

### مثال‌ها

```bash
ceph osd pool get labpool size
```

```bash
ceph osd pool get labpool min_size
```

```bash
ceph osd pool get labpool pg_num
```

```bash
ceph osd pool get labpool pg_autoscale_mode
```

### Propertyها

| Property | توضیح |
|---|---|
| `size` | تعداد Replica مطلوب |
| `min_size` | حداقل Replica برای I/O |
| `pg_num` | تعداد PG |
| `pg_autoscale_mode` | وضعیت PG Autoscaler |

---

# 10) PG Autoscaler / Balancer

## `ceph osd pool autoscale-status`

**کاربرد:** مشاهده پیشنهاد/وضعیت PG Autoscaler.

### مثال

```bash
ceph osd pool autoscale-status
```

---

## `ceph balancer status`

**کاربرد:** مشاهده وضعیت Ceph MGR Balancer.

### مثال

```bash
ceph balancer status
```

### Mode رایج

```text
upmap
```

---

# 11) RADOS Object Operations

## `rados -p <pool> put`

**کاربرد:** ذخیره مستقیم یک فایل به عنوان RADOS Object.

### مثال کامل

```bash
echo "Hello Ceph RADOS" >/tmp/hello.txt

rados -p labpool put hello-object /tmp/hello.txt
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `-p labpool` | Pool |
| `put` | عملیات Write |
| `hello-object` | Object Name |
| `/tmp/hello.txt` | فایل Source |

---

## `rados -p <pool> ls`

**کاربرد:** نمایش Objectهای یک Pool.

### مثال

```bash
rados -p labpool ls
```

> ⚠️ روی Pool بسیار بزرگ Production می‌تواند سنگین باشد.

---

## `rados -p <pool> get`

**کاربرد:** خواندن RADOS Object و ذخیره در فایل.

### مثال

```bash
rados -p labpool get hello-object /tmp/output.txt
cat /tmp/output.txt
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `get` | عملیات Read |
| `hello-object` | Object |
| `/tmp/output.txt` | فایل مقصد |

---

## RADOS Namespace

**کاربرد:** قرار دادن Objectهای همنام در Namespaceهای مختلف یک Pool.

### مثال

```bash
rados -p mypool \
  --namespace customer1 \
  put photo.jpg photo.jpg
```

Namespace دیگر:

```bash
rados -p mypool \
  --namespace customer2 \
  put photo.jpg photo.jpg
```

### پارامترها

| پارامتر | توضیح |
|---|---|
| `-p mypool` | Pool |
| `--namespace customer1` | RADOS namespace |
| `photo.jpg` | Object Name |

---

# 12) Object → PG → OSD Mapping

## `ceph osd map`

**کاربرد:** پیدا کردن PG و OSDهای مسئول یک Object.

### مثال کامل

```bash
ceph osd map labpool hello-object
```

### خروجی نمونه

```text
osdmap e100
pool 'labpool' (7)
object 'hello-object'
-> pg 7.1a
-> up ([12,4,27], p12)
-> acting ([12,4,27], p12)
```

### تفسیر

| مقدار | معنی |
|---|---|
| `e100` | OSDMap epoch |
| `pool (7)` | Pool ID |
| `pg 7.1a` | PG ID |
| `up` | Target set طبق Map |
| `acting` | OSDهای فعلی مسئول |
| `p12` | Primary OSD |

---

# 13) PG Status / Debug

## `ceph pg stat`

**کاربرد:** خلاصه وضعیت تمام PGها.

### مثال

```bash
ceph pg stat
```

### Stateهای مهم

```text
active+clean
active+degraded
active+undersized
peering
recovering
backfilling
remapped
inconsistent
```

---

## `ceph pg dump`

**کاربرد:** نمایش اطلاعات گسترده PGها.

### مثال

```bash
ceph pg dump
```

> روی Cluster بزرگ خروجی بسیار حجیم است.

---

## `ceph pg <PGID> query`

**کاربرد:** مشاهده جزئیات یک PG خاص.

### مثال

```bash
ceph pg 7.1a query
```

### فیلدهای مهم

```text
state
up
acting
recovery_state
peer_info
info
```

---

## `ceph pg map`

**کاربرد:** Mapping یک PG به OSDها.

### مثال

```bash
ceph pg map 7.1a
```

---

# 14) Scrub / Deep Scrub

## Scrub

**کاربرد:** بررسی Consistency بین Replicaهای یک PG.

### مثال

```bash
ceph pg scrub 7.1a
```

یا بسته به نسخه:

```bash
ceph tell 7.1a scrub
```

---

## Deep Scrub

**کاربرد:** بررسی عمیق‌تر Content/Checksum Replicaها.

### مثال

```bash
ceph tell 7.1a deep-scrub
```

> ⚠️ Deep Scrub می‌تواند I/O ایجاد کند؛ در Production بدون برنامه‌ریزی اجرا نشود.

---

# 15) Ceph RBD

## `rbd ls`

**کاربرد:** نمایش RBD Imageهای یک Pool.

### مثال

```bash
rbd ls -p volumes
```

### پارامتر

| پارامتر | توضیح |
|---|---|
| `-p volumes` | RBD Pool |

---

## `rbd info`

**کاربرد:** نمایش اطلاعات یک RBD Image.

### مثال

```bash
rbd info volumes/volume-1341bb17-9304-42a5-9913-1bcf2c117cee
```

### فیلدهای مهم

| فیلد | توضیح |
|---|---|
| `size` | Logical Capacity |
| `objects` | تعداد Objectهای بالقوه |
| `order` | log2 Object Size |
| `object size` | اندازه RBD Object |
| `block_name_prefix` | Prefix نام RADOS Objectها |
| `features` | قابلیت‌هایی مثل layering/object-map |

### مثال

```text
order 22
```

یعنی:

```text
2^22 bytes = 4 MiB
```

---

## `rbd du`

**کاربرد:** مقایسه Logical Size با Actual Allocated Usage.

### مثال

```bash
rbd du volumes/volume-UUID
```

### خروجی نمونه

```text
NAME          PROVISIONED   USED
volume-UUID       100 GiB   3 GiB
```

### مفهوم

```text
PROVISIONED = Logical size
USED        = Allocated data
```

---

# 16) پیدا کردن RBD Objectهای واقعی

ابتدا Prefix را پیدا کن:

```bash
rbd info volumes/volume-UUID
```

مثلاً:

```text
block_name_prefix: rbd_data.123abc
```

سپس:

```bash
rados -p volumes ls | grep rbd_data.123abc
```

> ⚠️ روی Poolهای بزرگ Production این روش می‌تواند بسیار سنگین باشد.

---

# 17) Libvirt / QEMU / Nova Compute

## `virsh list`

**کاربرد:** لیست Domainهای libvirt.

در Kolla:

```bash
docker exec nova_libvirt virsh list --all
```

### پارامتر

| پارامتر | توضیح |
|---|---|
| `--all` | نمایش Running و Stopped |

---

## `virsh domblklist`

**کاربرد:** نمایش Diskهای یک VM و Backend آن‌ها.

### مثال

```bash
docker exec nova_libvirt \
  virsh domblklist instance-00000123
```

### خروجی نمونه

```text
Target   Source
-------------------------------------------
vda      ...
vdb      volumes/volume-UUID
```

---

## `virsh dumpxml`

**کاربرد:** مشاهده XML کامل VM و Storage Backend.

### مثال

```bash
docker exec nova_libvirt \
  virsh dumpxml instance-00000123
```

برای پیدا کردن RBD:

```bash
docker exec nova_libvirt \
  virsh dumpxml instance-00000123 |
grep -A15 -B3 "protocol='rbd'"
```

### موارد مهم در XML

```xml
<source protocol='rbd' name='volumes/volume-UUID'>
```

```xml
<target dev='vdb' bus='virtio'/>
```

```xml
<auth username='cinder'>
```

---

# 18) Kolla Logs

## Cinder Volume Log

**کاربرد:** پیدا کردن Create/Attach/Initialize Connection مربوط به یک Volume.

### مثال

```bash
grep -i 'VOLUME_UUID' \
  /var/log/kolla/cinder/cinder-volume.log
```

---

## Nova Compute Log

**کاربرد:** بررسی Attach/Hotplug Volume روی Compute.

### مثال

```bash
grep -i 'VOLUME_UUID' \
  /var/log/kolla/nova/nova-compute.log
```

---

# 19) بررسی Cinder RBD Config در Kolla

**کاربرد:** پیدا کردن Backend و تنظیمات RBD.

### مثال

```bash
docker exec cinder_volume \
  grep -nE \
  'volume_driver|rbd_pool|rbd_user|rbd_store_chunk_size|rbd_ceph_conf' \
  /etc/cinder/cinder.conf
```

### پارامترهای مهم

| پارامتر | توضیح |
|---|---|
| `volume_driver` | Cinder backend driver |
| `rbd_pool` | Pool مربوط به Volumeها |
| `rbd_user` | CephX user |
| `rbd_store_chunk_size` | RBD object/chunk size بر حسب MiB |
| `rbd_ceph_conf` | مسیر ceph.conf |

---

# 20) یک مسیر عملی کامل برای Trace کردن Volume

## مرحله 1 — ساخت Volume

```bash
openstack volume create \
  --size 10 \
  --type ceph \
  rbd-lab
```

## مرحله 2 — مشاهده UUID

```bash
openstack volume show rbd-lab
```

## مرحله 3 — پیدا کردن Image در Ceph

```bash
rbd ls -p volumes
```

## مرحله 4 — بررسی Image

```bash
rbd info volumes/volume-UUID
```

## مرحله 5 — بررسی Actual Usage

```bash
rbd du volumes/volume-UUID
```

## مرحله 6 — Attach به VM

```bash
openstack server add volume vm01 rbd-lab
```

## مرحله 7 — داخل Guest

```bash
lsblk -f
```

## مرحله 8 — روی Compute

```bash
docker exec nova_libvirt \
  virsh domblklist instance-00000123
```

## مرحله 9 — بررسی XML

```bash
docker exec nova_libvirt \
  virsh dumpxml instance-00000123 |
grep -A15 -B3 "protocol='rbd'"
```

## مرحله 10 — Write تست

```bash
dd if=/dev/zero \
   of=/data/test.img \
   bs=1M \
   count=1024 \
   oflag=direct
```

## مرحله 11 — بررسی افزایش Usage

```bash
rbd du volumes/volume-UUID
```

---

# 21) مسیر عملی کامل برای Trace کردن RADOS Object

## ایجاد Pool

```bash
ceph osd pool create labpool
```

## Enable Application

```bash
ceph osd pool application enable labpool rados
```

## ایجاد فایل

```bash
echo "Hello Ceph RADOS" >/tmp/hello.txt
```

## Put Object

```bash
rados -p labpool put hello-object /tmp/hello.txt
```

## List Object

```bash
rados -p labpool ls
```

## Object Mapping

```bash
ceph osd map labpool hello-object
```

فرض:

```text
pg 7.1a
acting [12,4,27]
```

## بررسی PG

```bash
ceph pg 7.1a query
```

## پیدا کردن OSDها در Topology

```bash
ceph osd tree
```

## بررسی CRUSH

```bash
ceph osd crush tree
```

---

# 22) خطرناک / فقط Lab

این دستورات در Production بدون Change Plan و بررسی Cluster اجرا نشوند:

```bash
ceph orch daemon stop osd.X
```

```bash
ceph pg scrub PGID
```

```bash
ceph tell PGID deep-scrub
```

و هر نوع دستور احتمالی آینده مثل:

```text
ceph osd out
ceph osd down
ceph osd purge
```

باید با دقت بسیار زیاد استفاده شود.

---

# 23) خلاصه‌ی ذهنی مهم‌ترین دستورات

| هدف | دستور |
|---|---|
| وضعیت Cluster | `ceph -s` |
| Health دقیق | `ceph health detail` |
| OSD topology | `ceph osd tree` |
| OSD capacity | `ceph osd df tree` |
| CRUSH hierarchy | `ceph osd crush tree` |
| CRUSH rules | `ceph osd crush rule dump` |
| Poolها | `ceph osd pool ls detail` |
| PG status | `ceph pg stat` |
| PG detail | `ceph pg <PGID> query` |
| Object → PG/OSD | `ceph osd map <pool> <object>` |
| Direct RADOS write | `rados -p <pool> put ...` |
| Direct RADOS read | `rados -p <pool> get ...` |
| RBD list | `rbd ls -p <pool>` |
| RBD detail | `rbd info <pool>/<image>` |
| RBD usage | `rbd du <pool>/<image>` |
| Linux block devices | `lsblk -f` |
| Filesystem usage | `df -Th` |
| File metadata | `stat <file>` |
| Mount source | `findmnt <path>` |
| libvirt disks | `virsh domblklist` |
| VM XML | `virsh dumpxml` |

---

# 24) مهم‌ترین Mappingها برای مرور

```text
File
 ↓
Filesystem blocks
 ↓
Block Device / Offset
 ↓
virtio
 ↓
QEMU
 ↓
librbd
 ↓
RBD Object
 ↓
RADOS Object
 ↓
PG
 ↓
CRUSH
 ↓
Primary + Replica OSDs
 ↓
BlueStore
 ↓
Physical SSD/HDD
```

و برای RADOS مستقیم:

```text
Object Name
 ↓
Hash
 ↓
PG
 ↓
CRUSH
 ↓
Acting Set
 ↓
Primary OSD
 ↓
Replica OSDs
```

---

# 25) واژه‌های مهم در خروجی دستورات

| واژه | معنی |
|---|---|
| `up` | OSD daemon reachable |
| `down` | OSD unreachable |
| `in` | OSD در Placement شرکت می‌کند |
| `out` | OSD از Placement خارج است |
| `primary` | OSD اصلی PG |
| `replica` | نسخه‌های دیگر PG |
| `up set` | Target Placement طبق Map |
| `acting set` | OSDهای فعلی مسئول PG |
| `active+clean` | سالم و کامل |
| `degraded` | Replica ناقص |
| `undersized` | Acting Set کوچکتر از Size |
| `peering` | توافق OSDها روی PG state |
| `recovering` | بازسازی Missing Objectها |
| `backfilling` | انتقال Data برای Placement جدید |
| `remapped` | Mapping جدید هنوز کامل اعمال نشده |
| `inconsistent` | اختلاف بین Replicaها |
| `epoch` | Version یک Cluster Map |

---

# 26) سه نوع Capacity که نباید قاطی شوند

## داخل VM

```bash
df -h
```

نمایش:

```text
Filesystem Free Space
```

## RBD

```bash
rbd du volumes/volume-UUID
```

نمایش:

```text
Logical vs Allocated RBD Space
```

## Ceph Cluster

```bash
ceph df
```

نمایش:

```text
Raw / Pool Capacity
```

---

# 27) `ceph df`

**کاربرد:** مشاهده مصرف Storage در سطح Cluster و Pool.

### مثال

```bash
ceph df
```

### فیلدهای مهم

| فیلد | توضیح |
|---|---|
| `RAW STORAGE` | ظرفیت Physical Cluster |
| `TOTAL` | کل ظرفیت |
| `USED` | مصرف |
| `AVAIL` | فضای آزاد |
| `POOLS` | مصرف Logical Poolها |
| `%USED` | درصد استفاده |

---

# پایان Cheat Sheet

برای مرور سریع این ترتیب پیشنهاد می‌شود:

```text
Linux:
lsblk → findmnt → df → stat

OpenStack:
volume create → volume show → server add volume

RBD:
rbd ls → rbd info → rbd du

RADOS:
put/get/ls → ceph osd map

Ceph Core:
ceph -s → osd tree → osd df tree → crush tree

PG:
pg stat → pg query → pg map

Compute:
virsh domblklist → virsh dumpxml
```
