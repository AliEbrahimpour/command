curl --silent --remote-name --location https://github.com/ceph/ceph/raw/pacific/src/cephadm/cephadm
chmod +x cephadm
./cephadm add-repo --release pacific
./cephadm install

cephadm bootstrap --mon-ip 172.16.104.120 --allow-fqdn-hostname
cephadm install ceph-common
ceph orch apply mon --unmanaged

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


rbd pool init cinder-volumes
ceph osd pool application enable cinder-volumes rbd



ceph auth get-or-create client.cinder mon 'profile rbd' osd 'profile rbd pool=volumes, profile rbd pool=vms, profile rbd-read-only pool=images' mgr 'profile rbd pool=volumes, profile rbd pool=vms'






