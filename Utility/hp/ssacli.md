# 📘 README: HP `ssacli` CLI Tool (Ubuntu 20.04)

## 🔧 Install `ssacli`

```bash
# Add HPE repository
curl https://downloads.linux.hpe.com/SDR/hpPublicKey2048.pub | sudo apt-key add -
sudo curl -o /etc/apt/sources.list.d/hpe.list https://downloads.linux.hpe.com/SDR/repo/mcp/ubuntu/hpe.list
sudo apt update

# Install ssacli
sudo apt install ssacli
```

---

## 🔍 Show All Physical Drives (RAID & Non-RAID)

```bash
sudo ssacli controller slot=0 physicaldrive all show
```

Look for drives with status `Unassigned` or `No Configuration` → these are not in any RAID array.

---

## 📦 Show All Logical Drives (RAIDs)

```bash
sudo ssacli controller slot=0 logicaldrive all show
```

---

## 🆕 Create RAID0 on a Single Drive

Replace `1I:1:2` with the actual unassigned drive ID:

```bash
sudo ssacli controller slot=0 create type=ld drives=1I:1:2 raid=0
```

---

## 🔁 Create RAID1 on Two Drives

Example:

```bash
sudo ssacli controller slot=0 create type=ld drives=1I:1:2,2I:1:1 raid=1
```

---

## ❌ Delete a RAID (Logical Drive)

⚠️ Warning: This will erase data in the array.

```bash
sudo ssacli controller slot=0 logicaldrive 1 delete
```

---

## 🧾 View Drive Details (with Serial Number / Model)

```bash
sudo ssacli controller slot=0 physicaldrive all show detail
```

---

## 📁 Example Script: Create RAID0 for Each Unassigned Drive

> This will find all unassigned drives and create a separate RAID0 for each:

```bash
#!/bin/bash
DRIVES=$(sudo ssacli controller slot=0 physicaldrive all show | grep Unassigned | awk '{print $2}')
for DRIVE in $DRIVES; do
    echo "Creating RAID0 for drive $DRIVE..."
    sudo ssacli controller slot=0 create type=ld drives=$DRIVE raid=0
done
```


