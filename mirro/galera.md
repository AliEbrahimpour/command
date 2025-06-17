# Installing MariaDB 10.6 on Ubuntu 20.04 (Using Iranian Mirrors)

This guide helps you install MariaDB 10.6 on Ubuntu 20.04 using Iranian mirrors to avoid issues caused by blocked or slow access to the official MariaDB repository.

---

## 1. Remove any old MariaDB repo file (if exists)

```bash
sudo rm -f /etc/apt/sources.list.d/mariadb.list
````

---

## 2. Create a new MariaDB repo file

```bash
sudo nano /etc/apt/sources.list.d/mariadb.list
```

Add one of the following lines (you can try more than one if needed):

```bash
deb [arch=amd64] http://mirror.mobinhost.com/mariadb/repo/10.6/ubuntu focal main
deb [arch=amd64] http://mirror.parsvds.com/mariadb/repo/10.6/ubuntu focal main
deb [arch=amd64] http://mirror.hostiran.net/mariadb/repo/10.6/ubuntu focal main
```

---

## 3. Add the GPG key

If `apt-key` is available:

```bash
sudo apt-key adv --fetch-keys 'https://mirror.mobinhost.com/mariadb/repo/10.6/ubuntu/mariadb-keyring.gpg'
```

> Or use this alternative:

```bash
curl -fsSL https://mirror.mobinhost.com/mariadb/repo/10.6/ubuntu/mariadb-keyring.gpg | sudo gpg --dearmor -o /usr/share/keyrings/mariadb-keyring.gpg
```

Then update your repo line in `mariadb.list` to:

```bash
deb [signed-by=/usr/share/keyrings/mariadb-keyring.gpg] http://mirror.mobinhost.com/mariadb/repo/10.6/ubuntu focal main
```

---

## 4. Update and install MariaDB

```bash
sudo apt update
sudo apt install mariadb-server
```

---

## 5. Start and enable the service

```bash
sudo systemctl start mariadb
sudo systemctl enable mariadb
```

---

## 6. Run the security setup

```bash
sudo mysql_secure_installation
```

Follow the prompts to secure your MariaDB installation.

---

## 7. Check MariaDB status

```bash
sudo systemctl status mariadb
```

---

✅ Your MariaDB 10.6 should now be installed and running on Ubuntu 20.04 using local Iranian mirrors.


