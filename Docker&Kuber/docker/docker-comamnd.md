# Remove All Docker Images

To remove **all Docker images** from your system, run the following command:

```bash
docker rmi -f $(docker images -aq)
```

### Explanation:
- `docker images -aq`: Lists all Docker image IDs.
- `docker rmi -f`: Forcefully removes the listed images.

---

## Optional: Full Cleanup

To remove **all unused containers, images, networks, and volumes**, use:

```bash
docker system prune -a --volumes
```

> ⚠️ **Warning:** This will delete all Docker data, including:
> - Unused containers
> - All images
> - Unused networks
> - All volumes

Make sure to back up anything important before running this.

---

## References
- [Docker CLI Documentation](https://docs.docker.com/engine/reference/commandline/cli/)
```
