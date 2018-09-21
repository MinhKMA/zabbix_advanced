```pip install pyzabbix```

```sh
from pyzabbix import ZabbixAPI, ZabbixAPIException

ZABBIX_SERVER = 'http://192.168.30.69/zabbix'
user='Admin'
password='zabbix'
zapi = ZabbixAPI(url=ZABBIX_SERVER, user=user, password=password)
host_name = 'server'
hosts = zapi.host.get(filter={"host": host_name}, selectInterfaces=["interfaceid"])
if hosts:
     host_id = hosts[0]["hostid"]
     print("Found host id {0}".format(host_id))
item = zapi.item.create(
             hostid=host_id,
             name='chacogi',
             key_='compute1.vm01',
             type=2,
             value_type=3,
             interfaceid=hosts[0]["interfaces"][0]["interfaceid"],
             delay=30
         )
```
