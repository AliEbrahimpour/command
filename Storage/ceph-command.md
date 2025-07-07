# 🧠 Best Admin Commands for Ceph Storage

This guide provides a quick reference to essential Ceph admin commands that help with monitoring, managing, and troubleshooting Ceph clusters. Whether you're running Ceph for block (RBD), object (RGW), or file (CephFS) storage, these commands will help you stay in control.

---

## 🔍 Cluster Status and Health

```bash
ceph status
ceph health detail
ceph df
ceph osd df
ceph osd utilization
ceph osd pool stats
```

---

## 📦 Pool Management

```bash
# List all pools
ceph osd pool ls detail

# Create a pool (replicated)
ceph osd pool create <pool-name> <pg_num> <pgp_num>

# Create an EC pool
ceph osd pool create <ec-pool-name> <pg_num> <pgp_num> erasure <profile-name>

# Show pool usage
ceph df detail
```

---

## 🔧 OSD Management

```bash
# Show OSD tree and status
ceph osd tree
ceph osd stat
ceph osd df tree

# Mark OSD in/out/up/down
ceph osd out <id>
ceph osd in <id>
ceph osd down <id>
ceph osd crush reweight <id> <weight>

# Reweight-by-utilization
ceph osd reweight-by-utilization
```

---

## 🧩 Erasure Coding

```bash
# List erasure code profiles
ceph osd erasure-code-profile ls

# Get details of EC profile
ceph osd erasure-code-profile get <profile-name>

# Create a new EC profile
ceph osd erasure-code-profile set <profile-name> k=4 m=2 crush-failure-domain=osd
```

---

## 👮 Authentication & Keyring

```bash
# List auth entities
ceph auth list

# Get key for a user
ceph auth get client.admin
ceph auth get-key client.admin
```

---

## 👨‍💼 MGR and MON Management

```bash
# MGR placement
ceph orch apply mgr --placement="<host1>,<host2>,<host3>"

# List MONs
ceph mon dump

# Add MON
ceph orch daemon add mon <hostname>
```

---

## 📜 RBD Operations

```bash
# List RBD images
rbd ls -p <pool-name>

# Show image info
rbd info <pool-name>/<image-name>

# Bench test
rbd bench <pool-name>/<image-name> --io-type read --io-size 4K --io-threads 16 --io-total 1G
```

---

## 🚨 Troubleshooting & Debug

```bash
# Check logs
journalctl -u ceph-*

# Dump recent health logs
ceph health detail

# Disk usage by object
ceph osd df | sort -k 8 -n
```

---

## 🔁 Cluster Ops

```bash
# Balancer
ceph balancer status
ceph balancer on
ceph balancer execute

# Rebalance OSDs
ceph osd reweight-by-utilization

# Compact OSD RocksDB
ceph tell osd.* compact
```

---

## 📊 Dashboard

```bash
# Enable dashboard
ceph mgr module enable dashboard

# Set dashboard creds
ceph dashboard set-login-credentials admin <password>

# Get dashboard URL
ceph mgr services
```

---

## 🔒 Maintenance

```bash
# Set noout (prevent rebalancing during maintenance)
ceph osd set noout

# Unset noout
ceph osd unset noout

# Safely stop OSD
systemctl stop ceph-osd@<id>
```

---

## ✅ Checklist Before Shutdown

```bash
ceph osd set noout
ceph -s             # Ensure healthy
ceph osd tree       # Locate target host/OSD
systemctl stop ceph.target
```

---

## 📁 CephFS Commands

```bash
# Mount CephFS
mount -t ceph <mon-ip>:6789:/ /mnt/cephfs -o name=admin,secret=<key>

# List filesystems
ceph fs ls

# Get status
ceph fs status
```

---

## 📚 References

* [Ceph Docs](https://docs.ceph.com/en/latest/)
* [Ceph CLI Cheatsheet](https://docs.ceph.com/en/latest/rados/operations/tools/)

