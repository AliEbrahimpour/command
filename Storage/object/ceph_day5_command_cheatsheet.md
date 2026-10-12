# Ceph Day 5 Command Cheat Sheet — Production RGW Design

خلاصه دستورات روز پنجم با تمرکز روی **Production RGW، Pool Design، EC، Placement، Sharding، Quota، Multisite و Capacity Audit**.

---

## 1) RGW HA

```bash
ceph orch ps --daemon-type rgw
```

**کاربرد:** بررسی تعداد RGWها، Hostها و وضعیت سرویس.

---

## 2) Zone Configuration

```bash
radosgw-admin zone get
```

موارد مهم:

```text
placement_pools
index_pool
data_pool
data_extra_pool
storage_classes
```

---

## 3) Realm / Zonegroup / Zone

```bash
radosgw-admin realm list
```

```bash
radosgw-admin zonegroup list
```

```bash
radosgw-admin zone list
```

```bash
radosgw-admin zone get
```

---

## 4) Pool Audit

```bash
ceph osd pool ls detail
```

| مورد | توضیح |
|---|---|
| Type | replicated / erasure |
| `size` | Replica Count |
| `min_size` | حداقل Replica |
| `pg_num` | تعداد PG |
| CRUSH rule | Placement |
| autoscaler | وضعیت |

---

## 5) EC Profile

```bash
ceph osd erasure-code-profile ls
```

```bash
ceph osd erasure-code-profile get PROFILE_NAME
```

موارد مهم:

```text
k
m
plugin
crush-failure-domain
crush-device-class
```

---

## 6) CRUSH Audit

```bash
ceph osd crush tree
```

```bash
ceph osd crush rule ls
```

```bash
ceph osd crush rule dump
```

---

## 7) Device Class

```bash
ceph osd tree
```

Classها:

```text
hdd
ssd
nvme
```

---

## 8) PG Autoscaler

```bash
ceph osd pool autoscale-status
```

```bash
ceph osd pool get POOL pg_autoscale_mode
```

---

## 9) Bucket Stats / Sharding

```bash
radosgw-admin bucket stats --bucket=lab-bucket
```

دنبال:

```text
num_shards
usage
objects
placement_rule
```

---

## 10) Dynamic Resharding

```bash
ceph config get client.rgw rgw_dynamic_resharding
```

```bash
ceph config get client.rgw rgw_max_objs_per_shard
```

---

## 11) Quota

```bash
radosgw-admin quota set \
  --quota-scope=user \
  --uid=labuser \
  --max-size=10T \
  --max-objects=10000000
```

```bash
radosgw-admin quota enable \
  --quota-scope=user \
  --uid=labuser
```

```bash
radosgw-admin user info --uid=labuser
```

---

## 12) Versioning Audit

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3api get-bucket-versioning \
  --bucket lab-bucket
```

---

## 13) Lifecycle Audit

```bash
aws --endpoint-url http://RGW-IP:PORT \
  s3api get-bucket-lifecycle-configuration \
  --bucket lab-bucket
```

---

## 14) Usage

```bash
radosgw-admin usage show --uid=labuser
```

---

## 15) Capacity

```bash
ceph df
```

```bash
ceph osd df tree
```

| فیلد | توضیح |
|---|---|
| RAW TOTAL | Raw Capacity |
| RAW USED | مصرف Raw |
| AVAIL | فضای آزاد |
| POOL STORED | Logical Stored |
| OBJECTS | Object Count |

---

## 16) Health

```bash
ceph -s
```

```bash
ceph health detail
```

---

## 17) Network / MTU Audit

```bash
ip -br link
```

```bash
ip link show
```

```bash
ip route
```

---

## 18) Object Size Test

### Small

```bash
dd if=/dev/urandom of=/tmp/small.bin bs=4K count=1
```

### Medium

```bash
dd if=/dev/urandom of=/tmp/medium.bin bs=1M count=100
```

### Large

```bash
dd if=/dev/urandom of=/tmp/large.bin bs=1M count=1024
```

Upload:

```bash
time aws --endpoint-url http://RGW-IP:PORT \
  s3 cp /tmp/large.bin s3://lab-bucket/
```

---

## 19) RGW Config

```bash
ceph config dump | grep -i rgw
```

Option مشخص:

```bash
ceph config get client.rgw OPTION_NAME
```

---

## 20) Production Audit Sequence

```text
ceph orch ps --daemon-type rgw
↓
radosgw-admin zone get
↓
ceph osd pool ls detail
↓
ceph osd erasure-code-profile ls
↓
ceph osd erasure-code-profile get PROFILE
↓
ceph osd crush tree
↓
ceph osd crush rule dump
↓
ceph osd pool autoscale-status
↓
radosgw-admin bucket stats
↓
ceph df
```

---

## 21) فرمول‌های مهم

### Replication

```text
Required Raw
≈ Logical Data × Replica Count ÷ Target Utilization
```

### EC

```text
Raw Factor = (k + m) / k

Required Raw
≈ Logical Data × Raw Factor ÷ Target Utilization
```

مثال:

```text
EC 4+2 → 1.5x
```

---

## 22) خلاصه سریع

| هدف | دستور |
|---|---|
| RGW HA | `ceph orch ps --daemon-type rgw` |
| Zone | `radosgw-admin zone get` |
| Realm | `radosgw-admin realm list` |
| Zonegroup | `radosgw-admin zonegroup list` |
| Pool Audit | `ceph osd pool ls detail` |
| EC | `ceph osd erasure-code-profile get` |
| CRUSH | `ceph osd crush tree` |
| Rules | `ceph osd crush rule dump` |
| Autoscaler | `ceph osd pool autoscale-status` |
| Sharding | `radosgw-admin bucket stats` |
| Capacity | `ceph df` |
| OSD Capacity | `ceph osd df tree` |

---

## 23) هشدار

قبل از تغییر Production این موارد باید بررسی شوند:

```text
k
m
Failure Domain
Host/Rack Count
Device Class
CRUSH Rule
Recovery Cost
Capacity Reserve
```
