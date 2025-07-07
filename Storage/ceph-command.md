
# Ceph Storage Setup – README

This document outlines key commands for configuring and managing Ceph Storage, including setting up the Manager daemons and retrieving erasure coding profiles.

---

## 📦 Prerequisites

Ensure you are operating in a Ceph cluster environment with orchestration (`cephadm`) enabled. You must have appropriate administrative privileges to run these commands.

---



## 🧮 Erasure Coding Profile (EC)

Erasure coding is a method of data protection that provides storage efficiency and fault tolerance. Ceph uses *erasure code profiles* to define how redundancy is configured.

### 🔍 View Default EC Profile

```bash
ceph osd erasure-code-profile get default
```

* This retrieves the parameters of the default erasure coding profile.
* Typical output includes:

  * `k` and `m`: Number of data and coding chunks
  * `plugin`: Erasure coding plugin in use (e.g., `jerasure`)
  * `technique`: Technique such as `reed_sol_van`
  * `crush-failure-domain`: Level at which redundancy is applied (e.g., `host`)

---

## 🔗 References

* [Ceph Orchestrator Documentation](https://docs.ceph.com/en/latest/cephadm/)
* [Erasure Coding in Ceph](https://docs.ceph.com/en/latest/rados/operations/erasure-code/)

