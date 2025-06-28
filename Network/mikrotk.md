# MikroTik CLI – Assign Public IP and Gateway

This guide explains how to configure the MikroTik router via CLI with the following settings:

- **IP Address:** `192.168.1.2`
- **Gateway:** `192.168.1.1`
- **Subnet:** `/30`

## 1. Add IP Address to Interface

Replace `ether1` with your actual interface name:

```bash
/ip address add address=192.168.1.2/30 interface=ether1
````

## 2. Add Default Route (Gateway)

```bash
/ip route add gateway=192.168.1.1
```

## 3. Verify Configuration

Check assigned IPs:

```bash
/ip address print
```

Check routing table:

```bash
/ip route print
```

## Notes

* Make sure no duplicate IPs exist.
* Ensure interface `ether1` is connected to the uplink.
* Use `/30` for point-to-point subnetting (4 IPs: network, 2 hosts, broadcast).

