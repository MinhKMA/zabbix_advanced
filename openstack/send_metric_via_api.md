# Giám sát tài nguyên trong OpenStack

## 1. Môi trường

### Trên zabbix agent 

- Cài đặt python3.6
- Install packages requiments

    ```
    pip3.6 install python-openstackclient
    pip3.6 install python-neutronclient
    pip3.6 install py-zabbix
    ```

## 2.Setup trên dashboard

- Thêm các item trong application theo type check là zabbix trapper 

    <img src="https://i.imgur.com/MK3bWSo.png">

- Làm tương tự:

    <img src="https://i.imgur.com/wn4IJyk.png">

## 3.Setup trên agent

- Tải và đặt các scripts vào thư mục `/usr/local/bin/`:

    ```
    wget https://raw.githubusercontent.com/MinhKMA/zabbix_advanced/master/openstack/check_status/config.cfg
    wget https://raw.githubusercontent.com/MinhKMA/zabbix_advanced/master/openstack/check_status/client.py
    wget https://raw.githubusercontent.com/MinhKMA/zabbix_advanced/master/openstack/check_status/utils.py
    wget https://raw.githubusercontent.com/MinhKMA/zabbix_advanced/master/openstack/check_status/zabbix_sender.py
    ```

- Sửa các thông số trong file `config.cfg` và `zabbix_sender.py`

    + Trong config.cfg khai báo thông tin xác thực với openstack
    + Trong zabbix_sender.py khai bao key của các item trong zabbix được cài đặt trên dashboard zabbix ở dưới 

- Phần quyền

    ```
    chmod +x /usr/local/bin/*
    ````

- Chạy zabbix trong crontab 

    ```
    contab -e 0 * * * * /usr/local/bin/zabbix_sender.py
    ```

## Kết quả 

<img src="https://i.imgur.com/b80XH6C.png">