# Ceph Day 7 Command Cheat Sheet — End-to-End Failure Lab

خلاصه دستورات روز هفتم با تمرکز روی **Failure Testing، Recovery، RGW HA، OSD Failure، MON/MGR Failover، Cinder/Keystone و Data Integrity**.

> ⚠️ فقط Lab. روی Production بدون Change Plan اجرا نکن.

---

## 1) Baseline

```bash
ceph -s
```

```bash
ceph health detail
```

```bash
ceph pg stat
```

```bash
ceph osd tree
```

```bash
ceph orch ps
```

شرایط مناسب:

```text
HEALTH_OK
PGs active+clean
```

---

## 2) فایل تست S3

```bash
dd if=/dev/urandom \
  of=/tmp/day7-object.bin \
  bs=1M \
  count=100
```

```bash
sha256sum /tmp/day7-object.bin
```

---

## 3) Upload / Download

```bash
aws --endpoint-url https://s3.lab.example.com \
  s3 cp /tmp/day7-object.bin \
  s3://day7-lab/day7-object.bin
```

```bash
aws --endpoint-url https://s3.lab.example.com \
  s3 cp \
  s3://day7-lab/day7-object.bin \
  /tmp/day7-download.bin
```

```bash
sha256sum /tmp/day7-download.bin
```

---

## 4) Trace Object

```bash
radosgw-admin bucket stats --bucket=day7-lab
```

```bash
rados -p default.rgw.buckets.data ls | grep day7-object
```

```bash
ceph osd map \
  default.rgw.buckets.data \
  'RADOS_OBJECT_NAME'
```

```bash
ceph pg PGID query
```

```bash
ceph pg map PGID
```

---

# Failure 1 — RGW

## 5) RGW Daemonها

```bash
ceph orch ps --daemon-type rgw
```

Stop:

```bash
ceph orch daemon stop rgw.<DAEMON_NAME>
```

Test:

```bash
aws --endpoint-url https://s3.lab.example.com \
  s3 ls s3://day7-lab/
```

Start:

```bash
ceph orch daemon start rgw.<DAEMON_NAME>
```

---

# Failure 2 — OSD

## 6) noout کوتاه‌مدت

```bash
ceph osd add-noout osd.17
```

Stop:

```bash
ceph orch daemon stop osd.17
```

بررسی:

```bash
ceph -s
ceph health detail
ceph pg stat
ceph osd tree
```

Start:

```bash
ceph orch daemon start osd.17
```

Remove noout:

```bash
ceph osd rm-noout osd.17
```

Recovery Watch:

```bash
watch -n 2 ceph -s
```

---

# Failure 3 — Primary OSD

```bash
ceph osd add-noout osd.8
```

```bash
ceph orch daemon stop osd.8
```

```bash
ceph pg PGID query
```

```bash
ceph pg map PGID
```

برگرداندن:

```bash
ceph orch daemon start osd.8
ceph osd rm-noout osd.8
```

---

# Failure 4 — MON

## 7) MONها

```bash
ceph orch ps --daemon-type mon
```

```bash
ceph quorum_status --format json-pretty
```

Stop یک MON:

```bash
ceph orch daemon stop mon.<NAME>
```

Start:

```bash
ceph orch daemon start mon.<NAME>
```

> ⚠️ در Cluster سه MON، دو MON را عمداً Down نکن.

---

# Failure 5 — MGR

```bash
ceph mgr dump
```

```bash
ceph orch daemon stop mgr.<NAME>
```

```bash
ceph mgr dump
```

```bash
ceph orch daemon start mgr.<NAME>
```

---

# OpenStack / RBD Lab

## 8) ساخت Volume

```bash
openstack volume create \
  --size 5 \
  day7-volume
```

```bash
openstack volume show day7-volume
```

---

## 9) RBD Volume

```bash
rbd ls -p volumes
```

```bash
rbd info volumes/volume-UUID
```

```bash
rbd du volumes/volume-UUID
```

---

## 10) Attach

```bash
openstack server add volume \
  day7-vm \
  day7-volume
```

---

## 11) Libvirt Trace

```bash
docker exec nova_libvirt \
  virsh domblklist INSTANCE
```

```bash
docker exec nova_libvirt \
  virsh dumpxml INSTANCE | \
  grep -A15 -B3 "protocol='rbd'"
```

---

## 12) داخل VM

```bash
lsblk
```

```bash
sudo mkfs.xfs /dev/vdb
```

```bash
sudo mkdir -p /mnt/day7
sudo mount /dev/vdb /mnt/day7
```

---

## 13) Write / Integrity

```bash
sudo dd \
  if=/dev/urandom \
  of=/mnt/day7/data.bin \
  bs=1M \
  count=500 \
  oflag=direct
```

```bash
sha256sum /mnt/day7/data.bin
```

---

## 14) FIO

```bash
sudo fio \
  --name=day7 \
  --filename=/mnt/day7/fio-test \
  --size=1G \
  --rw=randrw \
  --rwmixread=70 \
  --bs=4k \
  --iodepth=16 \
  --direct=1
```

---

## 15) پیدا کردن RBD Object

```bash
rbd info volumes/volume-UUID
```

Prefix را بردار و:

```bash
rados -p volumes ls | \
  grep 'rbd_data.xxxxx' | \
  head
```

Mapping:

```bash
ceph osd map \
  volumes \
  rbd_data.xxxxx.0000000000000000
```

---

# Failure 6 — OSD هنگام VM I/O

```bash
ceph osd add-noout osd.22
```

```bash
ceph orch daemon stop osd.22
```

در VM:

```bash
sudo fio \
  --name=day7-failure \
  --filename=/mnt/day7/fio-failure \
  --size=1G \
  --rw=randrw \
  --bs=4k \
  --iodepth=16 \
  --direct=1
```

برگرداندن:

```bash
ceph orch daemon start osd.22
ceph osd rm-noout osd.22
```

---

# Failure 7 — Cinder API

پیدا کردن Containerها:

```bash
docker ps --format '{{.Names}}' | grep cinder
```

I/O موجود داخل VM:

```bash
while true; do
  date >> /mnt/day7/alive.log
  sync
  sleep 1
done
```

مشاهده:

```bash
tail -f /mnt/day7/alive.log
```

---

# Failure 8 — Keystone

```bash
openstack token issue
```

**انتظار:** Auth و عملیات جدید Control Plane مشکل پیدا می‌کنند؛ Data Plane موجود ممکن است ادامه پیدا کند.

---

## 16) Recovery Monitoring

```bash
ceph -s
```

```bash
ceph health detail
```

```bash
ceph pg stat
```

```bash
ceph osd tree
```

```bash
ceph pg PGID query
```

---

## 17) Integrity بعد از Recovery

### S3

```bash
aws --endpoint-url https://s3.lab.example.com \
  s3 cp \
  s3://day7-lab/day7-object.bin \
  /tmp/final-download.bin
```

```bash
sha256sum /tmp/final-download.bin
```

### VM

```bash
sha256sum /mnt/day7/data.bin
```

---

## 18) Golden Troubleshooting Set

```bash
ceph -s
ceph health detail
ceph osd tree
ceph osd df tree
ceph osd crush tree
ceph osd pool ls detail
ceph pg stat
ceph pg PGID query
ceph osd map POOL OBJECT
rbd info POOL/IMAGE
rbd du POOL/IMAGE
radosgw-admin bucket stats --bucket=BUCKET
ceph orch ps
```

---

## 19) Failure Matrix

| Failure | انتظار |
|---|---|
| یک RGW Down | با LB/RGW دوم، S3 ادامه دارد |
| یک OSD Down | PG degraded؛ I/O ممکن است ادامه یابد |
| Primary OSD Down | Peering و Primary جدید |
| OSD Back | Recovery و `active+clean` |
| یک MON از 3 | Quorum باقی می‌ماند |
| Active MGR | Standby Promote می‌شود |
| Cinder API Down | عملیات جدید مشکل؛ I/O قبلی مستقل |
| Keystone Down | Auth/Control Plane مشکل |
| زیر `min_size` | PGهای مربوط unavailable |

---

## 20) قانون اجرای تست

```text
Failure Test
↓
Recovery
↓
active+clean
↓
Next Test
```
