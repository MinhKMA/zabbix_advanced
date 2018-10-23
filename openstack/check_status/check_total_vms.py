#!/usr/bin/python3.6
from client import OpenstackClient
from utils import Token


def main():
    token = Token()
    client = OpenstackClient(session_auth=token.session_auth)
    print(len(client.nova_api.servers.list(search_opts={'all_tenants':1})))


if __name__ == '__main__':
    main()