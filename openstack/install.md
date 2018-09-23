# Theo dõi trạng thái các services openstack 

## Mô tả cách thực hiện  

zabbix agent trên zabbix server sẽ discovery ra các services của từng project trong openstack sau đó gán tên các services vào macro trong zabbix. Sử dụng script và định nghĩa chúng trong file zabbix_agent.conf, 

## Các bước thực hiện 

### Bước 1: Setup môi trường python 

```sh 
curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
python get-pip.py
yum install python-devel gcc wget -y
pip install python-openstackclient
pip install python-neutronclient
```

### Bước 2: Sự dụng các scripts check 

- Thư mục đặt các script `/usr/local/bin`
    + Tạo file `config.cfg` khai báo thông tin connect đến cụm openstack

    ```sh
    cd /usr/local/bin && vim config.cfg

    [controller]

    ip = 192.168.30.15
    username = admin
    password = Welcome123
    project_domain_name = default
    project_name = admin
    user_domain_name = default
    auth_url = http://192.168.40.15:5000/v3
    ```



#### Status services của project nova

```sh
cd /usr/local/bin && vim discover_services_nova.py
```
- Sử dụng script python như sau:

```sh
#!/usr/bin/python
from keystoneauth1.identity import v3
from keystoneauth1 import session
import novaclient.client as nova_client

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
    data = [{"{#NAME}":service['service_name'],
             "{#HOST}":service['host']} for service in services]
    print(json.dumps({"data": data}, indent=4))


if __name__ == '__main__':
    main()
```

- Kiểm tra lại 

```sh
[root@kvm01 bin]# python discover_services_nova.py 
{
    "data": [
        {
            "{#HOST}": "controller1", 
            "{#NAME}": "nova-scheduler"
        }, 
        {
            "{#HOST}": "controller1", 
            "{#NAME}": "nova-consoleauth"
        }, 
        {
            "{#HOST}": "controller1", 
            "{#NAME}": "nova-conductor"
        }, 
        {
            "{#HOST}": "controller2", 
            "{#NAME}": "nova-consoleauth"
        }, 
        {
            "{#HOST}": "controller2", 
            "{#NAME}": "nova-conductor"
        }, 
        {
            "{#HOST}": "controller2", 
            "{#NAME}": "nova-scheduler"
        }, 
        {
            "{#HOST}": "controller3", 
            "{#NAME}": "nova-scheduler"
        }, 
        {
            "{#HOST}": "controller3", 
            "{#NAME}": "nova-conductor"
        }, 
        {
            "{#HOST}": "controller3", 
            "{#NAME}": "nova-consoleauth"
        }, 
        {
            "{#HOST}": "compute2", 
            "{#NAME}": "nova-compute"
        }, 
        {
            "{#HOST}": "compute1", 
            "{#NAME}": "nova-compute"
        }
    ]
}
```

- Tạo script python kiểm tra status của từng service 

```sh 
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
```

- Kiểm tra:

```sh 
[root@kvm01 bin]# python check_services_nova.py compute1 nova-compute
up
```

- Phân quyền

```chmod +x /usr/local/bin/*```

- Sửa file cấu hình zabbix_agent.conf

```sh
[root@kvm01 bin]# tail -2 /etc/zabbix/zabbix_agentd.conf
UserParameter=nova.service,/usr/local/bin/discover_services_nova.py
/usr/local/bin/discover_services_cinder.py
UserParameter=check.nova[*],/usr/local/bin/check_services_nova.py $1 $2
```

- Trên dashboard zabbix

Tạo một template 

<img src="https://i.imgur.com/aC9u0JE.png">

Tạo discovery rule

<img src="https://i.imgur.com/P3xaMzF.png">


<img src="https://i.imgur.com/iaxxkjz.png">

Tạo item prototypes 

<img src='https://i.imgur.com/15nWZOv.png'>

<img src="https://i.imgur.com/HHwxFSS.png">

<img src="https://i.imgur.com/twOkqFj.png">

Sau đó vào latest data để kiểm tra 

<img src="https://i.imgur.com/INc8eba.png">

Nice ^^

#### Status services của project neutron và cinder

Làm tương tự như nova
