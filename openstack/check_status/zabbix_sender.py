from pyzabbix import ZabbixMetric, ZabbixSender
from utils import Token, ListServices
from client import OpenstackClient

packet = []
zserver = 'IP_zabbix_server'
port = 10051
hostId = 'host_agent_send_to'
key_volumes_available = 'volumes[available]'
key_volumes_more = 'volumes[more]'
key_volumes_total = 'volumes[total]'
key_vms_total = 'vms[total]'
key_vms_running = 'vms[running]'
key_vms_stop = 'vms[stop]'

def check_volumes(client):
    volumes = client.cinder_api.volumes.list(search_opts={'all_tenants':1})
    total_volumes = len(volumes)
    total_volumes_available = 0
    total_volumes_more = 0
    for volume in volumes:
        if volume.status == 'available':
            total_volumes_available += 1
        else:
            total_volumes_more += 1
    packet_volumes = [ZabbixMetric(hostId, key_volumes_total, total_volumes),
                      ZabbixMetric(hostId, key_volumes_available, total_volumes_available),
                      ZabbixMetric(hostId, key_volumes_more, total_volumes_more)]
    return packet_volumes
    

def check_vms(client):
    vms = client.nova_api.servers.list(search_opts={'all_tenants':1})
    total_vms = len(vms)
    total_vms_running = 0
    total_vms_stop = 0
    for vm in vms:
        if vm.status == 'ACTIVE':
            total_vms_running += 1
        else:
            total_vms_stop += 1
    packet_vms = [ZabbixMetric(hostId, key_vms_total, total_vms),
                  ZabbixMetric(hostId, key_vms_running, total_vms_running),
                  ZabbixMetric(hostId, key_vms_stop, total_vms_stop)]
    return packet_vms


def main():
    token = Token()
    client = OpenstackClient(session_auth=token.session_auth)
    packet_vms = check_vms(client)
    packet_volumes = check_volumes(client)
    packet.extend(packet_vms)
    packet.extend(packet_volumes)
    result = ZabbixSender(zserver,port,use_config=None).send(packet)
    return result


if __name__ == '__main__':
    main()
    