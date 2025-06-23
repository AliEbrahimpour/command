## 🖥️ HPE Smart Array Management with `hpssacli`

### 📦 Requirements

* HPE server with a Smart Array RAID controller (e.g., P440ar, P840, etc.)
* `hpssacli` installed on your Linux system (usually available from HPE support site)

---

### 🔍 List All Controllers

```bash
hpssacli ctrl all show
```

Example output:

```
Smart Array P440ar in Slot 0 (sn: ABC123456)
```

Use the `slot` number in all further commands.

---

### 💿 List All Physical Drives

```bash
hpssacli ctrl slot=0 pd all show
```

To see more detailed info for each drive:

```bash
hpssacli ctrl slot=0 pd all show detail
```

---

### ⚙️ Create RAID 0 on a Single Disk

To create one Logical Drive (RAID 0) on one physical disk:

```bash
hpssacli ctrl slot=0 create type=ld drives=1I:1:13 raid=0
```

To create separate RAID 0 arrays on multiple disks:

```bash
hpssacli ctrl slot=0 create type=ld drives=1I:1:13 raid=0
hpssacli ctrl slot=0 create type=ld drives=2I:1:14 raid=0
hpssacli ctrl slot=0 create type=ld drives=2I:1:15 raid=0
```

---

### 📂 List All Logical Drives (RAID volumes)

```bash
hpssacli ctrl slot=0 ld all show
```

Or detailed:

```bash
hpssacli ctrl slot=0 ld all show detail
```

---

### ❌ Delete a Logical Drive (RAID volume)

**Warning: This will destroy all data on that volume.**

First, find the Logical Drive ID (e.g., 1, 2, 3):

```bash
hpssacli ctrl slot=0 ld all show
```

Then delete the Logical Drive:

```bash
hpssacli ctrl slot=0 ld 2 delete
```

---

### 🧪 Check which Logical Drive a Disk Belongs To

```bash
hpssacli ctrl slot=0 pd 2I:1:15 show detail
```

Look for lines like:

```
Array: A
Logical Drive: 2
```

---

### 📁 Generate Diagnostic Report (read-only)

```bash
hpssaducli -adu -txt -v
```

