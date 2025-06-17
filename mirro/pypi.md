# Set PyPI Mirror for OpenStack-Ansible

This playbook sets a custom PyPI mirror (`https://mirror-pypi.runflare.com/simple`) on all OpenStack containers and hosts by creating `/etc/pip.conf`.

## 🛠 Usage

Run with:

```bash
openstack-ansible set-pip-mirror.yml
````

## 📁 pip.conf content

```ini
[global]
index-url = https://mirror-pypi.runflare.com/simple
trusted-host = mirror-pypi.runflare.com
```

## 💾 Persistent Configuration
### 📄 `PLAYBOOK.md`

````markdown
# 📘 Ansible Playbook: Set PyPI Mirror for OpenStack-Ansible

This playbook sets a custom PyPI mirror (`https://mirror-pypi.runflare.com/simple`) on **all OpenStack containers and hosts** by writing to `/etc/pip.conf`.

---

## 🧾 File: `set-pip-mirror.yml`

```yaml
---
- name: Set pip.conf with Runflare PyPI mirror on all containers and hosts
  hosts: "all_containers:all_hosts"
  become: true
  tasks:
    - name: Create /etc/pip.conf with mirror-pypi.runflare.com
      copy:
        dest: /etc/pip.conf
        content: |
          [global]
          index-url = https://mirror-pypi.runflare.com/simple
          trusted-host = mirror-pypi.runflare.com
````

---

## 🚀 How to Run

Run the playbook using the `openstack-ansible` command:

```bash
openstack-ansible set-pip-mirror.yml
```


## ✅ Applies To

* All physical hosts (controllers, computes, etc.)
* All OpenStack LXC containers










