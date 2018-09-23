#!/usr/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
from neutronclient.v2_0 import client as neutron_client

import configparser
import json


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


def services_neutron(sess):
    '''
    check status agent of project neutron in openstack
    :param sess:
    :return: list
    [{'binary': 'neutron-metadata-agent', 'alive': False, 'host': 'compute2'},
     {'binary': 'neutron-metadata-agent', 'alive': True, 'host': 'compute1'},
     {'binary': 'neutron-l3-agent', 'alive': True, 'host': 'controller2'},
     {'binary': 'neutron-l3-agent', 'alive': True, 'host': 'controller3'},
     {'binary': 'neutron-openvswitch-agent', 'alive': False, 'host': 'compute2'},
     {'binary': 'neutron-openvswitch-agent', 'alive': True, 'host': 'compute1'},
     {'binary': 'neutron-l3-agent', 'alive': True, 'host': 'controller1'},
     {'binary': 'neutron-dhcp-agent', 'alive': True, 'host': 'compute1'},
     {'binary': 'neutron-dhcp-agent', 'alive': False, 'host': 'compute2'}]
    '''
    agents_list = []
    neutron = neutron_client.Client(session=sess)
    agents = neutron.list_agents()
    for item in agents["agents"]:
        agent_keys = {'binary', 'alive', 'host'}
        agent_dict = {key: value for key, value in item.items() if key in agent_keys}
        agents_list.append(agent_dict)
    return agents_list


def main():
    sess = auth()
    services = services_neutron(sess)
    data = [{"{#NAME}":service['binary'],
             "{#HOST}":service['host']} for service in services]
    print(json.dumps({"data": data}, indent=4))


if __name__ == '__main__':
    main()
