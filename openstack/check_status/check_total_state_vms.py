#!/usr/bin/python3.6
import sys

from client import OpenstackClient
from utils import Token


def main():
    token = Token()
    client = OpenstackClient(session_auth=token.session_auth)
    servers = client.nova_api.servers.list(search_opts={'all_tenants':1})
    total_vm_start = 0
    total_vm_stop = 0
    for server in servers:
        if server.status== 'ACTIVE':
            total_vm_start += 1
        else:
            total_vm_stop += 1
    if sys.argv[1] == 'runnning':
        print(total_vm_start)
    elif sys.argv[1] == 'shutoff':
        print(total_vm_stop)
            
        
if __name__ == '__main__':
    main()