# Download and Install Ceph
```
curl --silent --remote-name --location https://github.com/ceph/ceph/raw/pacific/src/cephadm/cephadm
chmod +x cephadm
./cephadm add-repo --release pacific
./cephadm install
```

# Bootstrap First Monitor Node
```
cephadm bootstrap --mon-ip 172.16.104.120 --allow-fqdn-hostname
cephadm install ceph-common
ceph orch apply mon --unmanaged
```

# Add Other Node
```
ssh-copy-id -f -i /etc/ceph/ceph.pub root@mon2
ssh-copy-id -f -i /etc/ceph/ceph.pub root@mon3

ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph1
ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph2
ssh-copy-id -f -i /etc/ceph/ceph.pub root@ceph3

ceph orch host add mon2 172.16.104.121 --labels _admin
ceph orch host add mon3 172.16.104.122 --labels _admin

ceph orch host add ceph1 172.16.104.123
ceph orch host add ceph2 172.16.104.124
ceph orch host add ceph3 172.16.104.125

ceph orch daemon add osd ceph1:/dev/sdb
ceph orch daemon add osd ceph2:/dev/sdb
ceph orch daemon add osd ceph3:/dev/sdb
```

## Check Status
```
root@mon1:/etc/ceph# ceph orch host ls
HOST   ADDR            LABELS  STATUS  
ceph1  172.16.104.123                  
ceph2  172.16.104.124                  
ceph3  172.16.104.125                  
mon1   172.16.104.120  _admin          
mon2   172.16.104.121  _admin          
mon3   172.16.104.122  _admin  

ceph orch daemon add mon mon2:172.16.104.121
ceph orch daemon add mon mon3:172.16.104.122
```

# Create New Pool Cinder Volume

```
rbd pool init cinder-volumes
ceph osd pool application enable cinder-volumes rbd



ceph auth get-or-create client.cinder mon 'profile rbd' osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images' mgr 'profile rbd pool=volumes, profile rbd pool=vms'
```







## 🧠 Set MGR Daemon Placement

Ceph Manager (`mgr`) daemons provide additional monitoring and module-based capabilities to the cluster. To ensure high availability, it's recommended to deploy multiple `mgr` instances.

### 🔧 Apply MGR Daemons on 3 Hosts

```bash
ceph orch apply mgr --placement="3"
```

* This command instructs the orchestrator to deploy 3 `mgr` daemons across the cluster.
* Placement can also be defined using specific hostnames or labels, for example:

  ```bash
  ceph orch apply mgr --placement="host1,host2,host3"
  ```

---