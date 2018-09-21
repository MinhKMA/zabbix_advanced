from pyzabbix import ZabbixAPI, ZabbixAPIException

ZABBIX_SERVER = 'http://192.168.30.69/zabbix'
user='Admin'
password='zabbix'
zapi = ZabbixAPI(url=ZABBIX_SERVER, user=user, password=password)
hostname='vm01'
ip='127.0.0.1'
hostcriado = zapi.host.create(
    host= hostname,
    status= 0,
    interfaces=[{
        "type": 1,
        "main": "1",
        "useip": 1,
        "ip": ip,
        "dns": "",
        "port": 10050
    }],
    groups=[{
        "groupid": 6
    }],
    templates=[{
        "templateid": 10001
    }]
)
