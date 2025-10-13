# Managing Reserved Blocks on ext4 Filesystems

This guide explains how to **view, adjust, and verify reserved space** (`-m` parameter) on an ext4 filesystem safely — even when the partition is mounted (e.g., `/`).

---

## 🧩 What Are Reserved Blocks?

By default, ext4 reserves **5% of total disk space** for the `root` user and system daemons.  
This ensures:
- Critical services (like journaling or logging) can still write even when the disk is almost full.  
- System boots remain reliable under low disk space conditions.

---

## ⚙️ Check Current Reserved Space

Run:
```bash
sudo tune2fs -l /dev/sda2 | grep -E 'Reserved block|Filesystem block size'
````

Example output:

```
Reserved block count:     2302136
Reserved blocks percentage: 5%
Filesystem block size:    4096
```

---

## 🔧 Adjust Reserved Blocks Percentage

To change from **5% → 2%**:

```bash
sudo tune2fs -m 2 /dev/sda2
```

Example output:

```
Setting reserved blocks percentage to 2% (921000 blocks)
```

This change:

* Is **instant** (takes <1 second)
* Is **safe** on mounted ext4 filesystems
* Requires **no fsck or umount**

You can freely increase or decrease the percentage later — no risk of data loss.

---

## 🧮 Check Space Difference

Compare disk space before and after change:

```bash
df -h /
```

Expected result:

* Available space (`Avail`) increases after reducing the reserved percentage.

---

## 🧰 Verify Filesystem Health (Optional)

You can check filesystem health safely in read-only mode:

```bash
sudo fsck -n /dev/sda2
```

Expected output:

```
/dev/sda2: clean, 223942/28778496 files, 108287663/115106816 blocks
```

If the state is `clean`, no further action is needed.

---

## 🧯 Optional: Force Filesystem Check on Next Boot

If you ever want to verify or repair automatically at boot:

```bash
sudo touch /forcefsck
sudo reboot
```

---

## ⚠️ Best Practices

| Recommendation                               | Description                                   |
| -------------------------------------------- | --------------------------------------------- |
| Run `sync` before reboot                     | Ensure all writes are flushed to disk         |
| Avoid changing when disk is 99% full         | Might cause temporary display inconsistencies |
| Keep at least 1–2% reserved                  | For critical services and logs                |
| Use `fsck -n` instead of `fsck` on live root | Prevent accidental writes on a mounted system |

---

## ✅ Quick Summary

| Action            | Command                      | Safe During Mount?  | Typical Duration |
| ----------------- | ---------------------------- | ------------------- | ---------------- |
| Check reserved %  | `tune2fs -l /dev/sda2`       | ✅                   | Instant          |
| Change reserved % | `tune2fs -m 2 /dev/sda2`     | ✅                   | < 2 sec          |
| Read-only check   | `fsck -n /dev/sda2`          | ✅                   | Few sec          |
| Repair check      | `fsck /dev/sda2` *(offline)* | ⚠️ Only in recovery | Depends on size  |

---

### 🧠 Example Workflow

```bash
sync
sudo tune2fs -l /dev/sda2 | grep 'Reserved'
sudo tune2fs -m 2 /dev/sda2
sudo tune2fs -l /dev/sda2 | grep 'Reserved'
df -h /
sync && sudo reboot
```

