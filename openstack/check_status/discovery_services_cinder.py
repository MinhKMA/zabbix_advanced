#!/usr/bin/python3.6
from utils import Token, ListServices
import json


def main():
    token = Token()
    all_services = ListServices(session_auth=token.session_auth)
    services = all_services.cinder_services_list()
    data = [{"{#NAME}":service['service_name'],
             "{#HOST}":service['host']} for service in services]
    print(json.dumps({"data": data}, indent=4))

if __name__ == '__main__':
    main()
    