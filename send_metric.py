#!/usr/bin/python
'''
./send.py 192.168.30.69 server compute1.vm01 1
{"failed": 0, "chunk": 1, "total": 1, "processed": 1, "time": "0.000100"}
'''

import logging
import sys
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from pyzabbix import ZabbixMetric, ZabbixSender

# argument check
if len(sys.argv)<4:
  print "USAGE: zabbixServer hostId key value"
  print "EXAMPLE: 127.0.0.1 myhost mystr1 testvalue"
  sys.exit(1)

# simple parse for arguments
zserver = sys.argv[1]
if zserver.lower().startswith("http"):
  print "Do not prefix the zabbix server name with 'http' or 'https', just specify the hostname or IP"
  sys.exit(1)
hostId = sys.argv[2]
key = sys.argv[3]
value = sys.argv[4]
port = 10051


# Send metrics to zabbix trapper
packet = [
  ZabbixMetric(hostId, key, value)
  # multiple metrics can be sent in same call for effeciency
  #,ZabbixMetric(hostId, 'anotherkey', 'anothervalue')
]

result = ZabbixSender(zserver,port,use_config=None).send(packet)
print result
