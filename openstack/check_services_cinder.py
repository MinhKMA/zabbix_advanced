#!/usr/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
import cinderclient.v3.client as cinder_client

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


def services_cinder(sess):
    '''
    check status service of project cinder in openstack
    :param sess:
    :return: list
    [{'service_name': 'cinder-volume', 'host': 'ceph@ceph', 'state': 'up'},
     {'service_name': 'cinder-scheduler', 'host': 'ceph', 'state': 'up'},
     {'service_name': 'cinder-backup', 'host': 'ceph', 'state': 'up'},
     {'service_name': 'cinder-volume', 'host': 'ceph@ceph2', 'state': 'down'}]
    '''
    cinder = cinder_client.Client(session=sess)
    services = cinder.services.list()
    services_list = []
    for service in services:
        service_dict = {'service_name':service.binary,
                        'host':service.host,
                        'state':service.state}
        services_list.append(service_dict)
    return services_list


def main():
    sess = auth()
    services = services_cinder(sess)
    for service in services:
        if (sys.argv[1] == service['host'] and sys.argv[2] == service['service_name']):
            print(service['state'])


if __name__ == '__main__':
    main()