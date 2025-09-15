# OpenObserve — Installation with Docker Compose and Agent

## 1. Prerequisites
- Linux server with Docker and Docker Compose installed.
- At least 2 vCPU and 4 GB RAM.

---

## 2. Start OpenObserve with Docker Compose

Create a file named `docker-compose.yml`:

```yaml
version: '3.8'
services:
  openobserve:
    image: openobserve/openobserve:latest
    container_name: openobserve
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - O2_MODE=single
      - O2_ADMIN_EMAIL=admin@example.com
      - O2_ADMIN_PASSWORD=changeme
    volumes:
      - ./data:/data
````

Run:

```bash
docker compose up -d
```

Access the UI:

```
http://<server-ip>:8080
```

Login with:

* **Email:** `admin@example.com`
* **Password:** `changeme`

---

## 3. Install OpenObserve Agent (Collector)

Create a file named `agent-docker-compose.yml`:

```yaml
version: '3.8'
services:
  o2-agent:
    image: openobserve/agent:latest
    container_name: o2-agent
    restart: unless-stopped
    environment:
      - O2_URL=http://openobserve:8080
      - O2_ORG=default
      - O2_STREAM=default
      - O2_TOKEN=<YOUR_INGEST_TOKEN>
    volumes:
      - /var/log:/var/log:ro
```

Run:

```bash
docker compose -f agent-docker-compose.yml up -d
```

---

## 4. Verify

* In the OpenObserve UI, check **Streams → default**.
* Logs from `/var/log` on the host should appear.

---
