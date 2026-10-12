# Ceph Day 6 Command Cheat Sheet — OpenStack + Ceph

خلاصه دستورات روز ششم با تمرکز روی **Keystone، Glance، Cinder، Nova، RBD و RGW integration**.

---

## 1) Poolهای OpenStack

```bash
ceph osd pool ls
```

رایج:

```text
images
volumes
vms
backups
```

---

## 2) Initialize RBD Pool

```bash
rbd pool init images
```

```bash
rbd pool init volumes
```

```bash
rbd pool init vms
```

> ⚠️ برای Pool جدید.

---

## 3) CephX

```bash
ceph auth ls
```

```bash
ceph auth get client.cinder
```

```bash
ceph auth get client.glance
```

```bash
ceph auth get client.cinder-backup
```

---

## 4) نمونه ساخت client.glance

```bash
ceph auth get-or-create client.glance \
  mon 'profile rbd' \
  osd 'profile rbd pool=images' \
  mgr 'profile rbd pool=images'
```

> ⚠️ Caps را مطابق معماری واقعی تنظیم کن.

---

## 5) Keystone / Service Catalog

```bash
openstack service list
```

```bash
openstack catalog list
```

```bash
openstack endpoint list
```

```bash
openstack token issue
```

---

## 6) Glance Images

```bash
openstack image list
```

```bash
openstack image show IMAGE_UUID
```

RBD:

```bash
rbd ls -p images
```

```bash
rbd info images/IMAGE_NAME
```

---

## 7) ساخت Image

```bash
openstack image create \
  --disk-format raw \
  --container-format bare \
  --file ubuntu.raw \
  ubuntu
```

| پارامتر | توضیح |
|---|---|
| `--disk-format raw` | Disk format |
| `--container-format bare` | Container format |
| `--file` | Source file |

---

## 8) Cinder Volumes

```bash
openstack volume list
```

```bash
openstack volume show VOLUME_UUID
```

### ساخت Volume

```bash
openstack volume create \
  --size 10 \
  --type ceph \
  test-volume
```

---

## 9) RBD Volumeها

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

## 10) Attach / Detach

```bash
openstack server add volume \
  VM_NAME \
  VOLUME_UUID
```

```bash
openstack server remove volume \
  VM_NAME \
  VOLUME_UUID
```

---

## 11) Nova

```bash
openstack server list
```

```bash
openstack server show VM_NAME
```

---

## 12) Libvirt در Kolla

```bash
docker exec nova_libvirt virsh list --all
```

```bash
docker exec nova_libvirt \
  virsh domblklist INSTANCE
```

```bash
docker exec nova_libvirt \
  virsh dumpxml INSTANCE
```

RBD XML:

```bash
docker exec nova_libvirt \
  virsh dumpxml INSTANCE | \
  grep -A15 -B3 "protocol='rbd'"
```

---

## 13) داخل VM

```bash
lsblk
```

---

## 14) Nova RBD Config

```bash
docker exec nova_compute \
  grep -nE \
  'images_type|images_rbd_pool|images_rbd_ceph_conf' \
  /etc/nova/nova.conf
```

---

## 15) Glance RBD Config

```bash
docker exec glance_api \
  grep -nE \
  'rbd_store_pool|rbd_store_user|rbd_store_ceph_conf|rbd_store_chunk_size' \
  /etc/glance/glance-api.conf
```

---

## 16) Cinder RBD Config

```bash
docker exec cinder_volume \
  grep -nE \
  'volume_driver|rbd_pool|rbd_user|rbd_secret_uuid|rbd_store_chunk_size' \
  /etc/cinder/cinder.conf
```

---

## 17) Logs

### Cinder

```bash
grep -i 'VOLUME_UUID' \
  /var/log/kolla/cinder/cinder-volume.log
```

### Nova

```bash
grep -i 'VOLUME_UUID' \
  /var/log/kolla/nova/nova-compute.log
```

---

## 18) object-store در Keystone

```bash
openstack service list
```

```bash
openstack catalog list
```

```bash
openstack endpoint list \
  --service object-store
```

---

## 19) ساخت object-store Service

```bash
openstack service create \
  --name=swift \
  --description="Swift Service" \
  object-store
```

> فقط هنگام پیاده‌سازی واقعی Integration.

---

## 20) RGW + Keystone Config

```bash
ceph config dump | grep -i keystone
```

```bash
ceph config get client.rgw rgw_keystone_url
```

Optionهای مهم:

```text
rgw_keystone_url
rgw_keystone_accepted_roles
rgw_keystone_implicit_tenants
rgw_s3_auth_use_keystone
```

---

## 21) RGW Daemon

```bash
ceph orch ps --daemon-type rgw
```

---

## 22) Trace Volume

```text
openstack volume list
↓
openstack volume show UUID
↓
rbd ls -p volumes
↓
rbd info volumes/volume-UUID
↓
virsh domblklist
↓
virsh dumpxml
```

---

## 23) Trace Image

```text
openstack image list
↓
openstack image show UUID
↓
rbd ls -p images
↓
rbd info images/IMAGE
```

---

## 24) خلاصه سریع

| هدف | دستور |
|---|---|
| Poolها | `ceph osd pool ls` |
| CephX | `ceph auth ls` |
| Cinder CephX | `ceph auth get client.cinder` |
| Glance CephX | `ceph auth get client.glance` |
| Image List | `openstack image list` |
| Volume List | `openstack volume list` |
| Server List | `openstack server list` |
| RBD Images | `rbd ls -p images` |
| RBD Volumes | `rbd ls -p volumes` |
| RBD Detail | `rbd info` |
| RBD Usage | `rbd du` |
| Attach | `openstack server add volume` |
| Libvirt Disk | `virsh domblklist` |
| XML | `virsh dumpxml` |
| Catalog | `openstack catalog list` |
| Endpoint | `openstack endpoint list` |
| Token | `openstack token issue` |

---

## 25) Authentication Mapping

| مسیر | Authentication |
|---|---|
| User → OpenStack | Keystone |
| Cinder → Ceph | CephX |
| Glance → Ceph | CephX |
| QEMU → Ceph | CephX via libvirt secret |
| Swift Client → RGW | Keystone Token |
| S3 Client → RGW | Access/Secret/SigV4 یا Keystone-backed |

---

## 26) نکته کلیدی

بعد از Attach:

```text
VM
 ↓
QEMU
 ↓
librbd
 ↓
Ceph
```

Cinder API در مسیر دائمی I/O نیست.
