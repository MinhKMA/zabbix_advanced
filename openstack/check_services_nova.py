#!/usr/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
import novaclient.client as nova_client

import configparser
import sys

def ini_file_loader():
    """ Load configuration from ini file"""

    parser = configparser.SafeConfigParser()
    parser.read('/usr/local/bin/config.cfg')
    config_dict = {}

    for section in parser.sections():
        for key, value in parser.items(section, True):
            config_dict['%s-%s' % (section, key)] = value
    return config_dict


def auth(username=None, password=None, project_domain_name=None, project_name=None,
         user_domain_name=None, auth_url=None):
    """ get session authentication"""
    config_dict = ini_file_loader()
    username = username or config_dict['controller-username']
    password = password or config_dict['controller-password']
    project_domain_name = project_domain_name or config_dict['controller-project_domain_name']
    project_name = project_name or config_dict['controller-project_name']
    user_domain_name = user_domain_name or config_dict['controller-user_domain_name']
    auth_url = auth_url or config_dict['controller-auth_url']
    auth = v3.Password(auth_url=auth_url,
                       user_domain_name=user_domain_name,
                       username=username, password=password,
                       project_domain_name=project_domain_name,
                       project_name=project_name)
    sess = session.Session(auth=auth)
    return sess


def services_nova(sess):
    '''
    check status service of project nova in openstack
    :param sess:
    :return: list
    [{'service_name': 'nova-scheduler', 'host': 'controller1', 'state': 'up'},
     {'service_name': 'nova-consoleauth', 'host': 'controller1', 'state': 'up'},
     {'service_name': 'nova-conductor', 'host': 'controller1', 'state': 'up'},
     {'service_name': 'nova-consoleauth', 'host': 'controller2', 'state': 'up'},
     {'service_name': 'nova-conductor', 'host': 'controller2', 'state': 'up'},
     {'service_name': 'nova-scheduler', 'host': 'controller2', 'state': 'up'},
     {'service_name': 'nova-scheduler', 'host': 'controller3', 'state': 'up'},
     {'service_name': 'nova-conductor', 'host': 'controller3', 'state': 'up'},
     {'service_name': 'nova-consoleauth', 'host': 'controller3', 'state': 'up'},
     {'service_name': 'nova-compute', 'host': 'compute2', 'state': 'down'},
     {'service_name': 'nova-compute', 'host': 'compute1', 'state': 'up'}]
    '''
    nova = nova_client.Client("2.1", session=sess)
    services = nova.services.list()
    services_list = []
    for service in services:
        service_dict = {'service_name':service.binary,
                        'host':service.host,
                        'state':service.state}
        services_list.append(service_dict)
    return services_list


def main():
    sess = auth()
    services = services_nova(sess)
    for service in services:
        if (sys.argv[1] == service['host'] and sys.argv[2] == service['service_name']):
            print(service['state'])


if __name__ == '__main__':
    main()
