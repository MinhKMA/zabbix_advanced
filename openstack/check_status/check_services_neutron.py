#!/usr/bin/python3.6
from utils import Token, ListServices
import sys

def main():
    token = Token()
    all_services = ListServices(session_auth=token.session_auth)
    services = all_services.neutron_services_list()
    for service in services:
        if (sys.argv[1] == service['host'] and sys.argv[2] == service['binary']):
            print(service['alive'])

if __name__ == '__main__':
    main()