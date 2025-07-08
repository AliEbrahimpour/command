# 🧊 Ceph RBD with Erasure Coding (k=4, m=2)

This guide demonstrates how to configure and use an erasure-coded pool for **RBD** (RADOS Block Device) in Ceph.

---

## 🔧 1. Create Erasure Code Profile

```bash
ceph osd erasure-code-profile set ec42-profile \
    plugin=jerasure \
    technique=reed_sol_van \
    k=4 \
    m=2 \
    crush-failure-domain=host \
    allow_overwrites=true
```

* `k=4`: Data chunks
* `m=2`: Coding chunks
* `allow_overwrites=true`: Required for RBD support
* `crush-failure-domain=host`: Prevents storing all chunks on the same host

---

## 📦 2. Create Pools

### Erasure Coded Data Pool

```bash
ceph osd pool create rbd_ec_data 128 128 erasure ec42-profile
```

### Replicated Metadata Pool

```bash
ceph osd pool create rbd_ec_metadata 64 64 replicated
```

---

## 🚀 3. Enable RBD Application on Pools

```bash
ceph osd pool application enable rbd_ec_data rbd
ceph osd pool application enable rbd_ec_metadata rbd
rbd pool init rbd_ec_metadata
```

---

## 🔍 4. Verify Pool & Profile Config

```bash
ceph osd pool get rbd_ec_data all
ceph osd erasure-code-profile get ec42-profile
ceph osd pool get rbd_ec_data allow_ec_overwrites
ceph osd pool set rbd_ec_data allow_ec_overwrites true
```

---

## 📷 5. Create an RBD Image

```bash
rbd create --size 1G --data-pool rbd_ec_data rbd_ec_metadata/ec_image_test10
```

> This creates a 1GB RBD image named `ec_image_test10` with data stored in the erasure coded pool and metadata in the replicated pool.

---

## 🔎 6. Check the Image

```bash
rbd info --image ec_image_test10 --pool rbd_ec_metadata
```

---

## 📁 7. Use the Image (Map, Format, Mount)

### Map the Image:

```bash
rbd map ec_image_test10 --pool rbd_ec_metadata
```

### Format the Device:

```bash
mkfs.ext4 /dev/rbd0
```

### Mount the Device:

```bash
mkdir /mnt/myrbd
mount /dev/rbd0 /mnt/myrbd
```

---

## 🧪 8. Write Data for Testing

```bash
cd /mnt/myrbd/
dd if=/dev/zero of=/mnt/myrbd/test.file bs=10M count=10
```

---

## 🧼 9. Cleanup (Optional)

```bash
umount /mnt/myrbd
rbd unmap /dev/rbd0
rbd remove ec_image_test10 --pool rbd_ec_metadata
```

---

## 📘 Notes

* **Erasure Coding is more space-efficient** than replication, but incurs higher CPU usage and write amplification.
* `allow_overwrites=true` is mandatory for using EC pools with RBD.
* You should monitor OSD performance when using EC, especially for write-intensive workloads.

