import subprocess


def test_router_(): 
    name = 'gw'
    result = subprocess.run("cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip() == name

def test_router_ip():
    ip_address = '10.0.0.1'
    result = subprocess.run("cat /etc/network/interfaces | grep 10.0.0.1", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip().split()
    trash = output[0]
    ip = ' '.join(output[1:]) if len(output) > 1 else ''
    assert ip.strip() == ip_address


def test_router_netmask():
    netmask = '255.255.255.0'
    result = subprocess.run("cat /etc/network/interfaces | grep 255.255.255.0", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip().split()
    trash = output[0]
    net = ' '.join(output[1:]) if len(output) > 1 else ''
    assert net.strip() == netmask
 
def test_ip_forwarding_on():
    assert  subprocess.run("cat /proc/sys/net/ipv4/ip_forward",shell=True, stdout=subprocess.PIPE, text=True)

def test_masquerad():
    result = subprocess.run("nft list table ip nat | grep masquerade", shell=True, stdout=subprocess.PIPE, text=True)
    assert "masquerade" in result.stdout

def test_router_reach_unknown():
    result = subprocess.run("ping -c 1 10.0.2.2", shell=True, check=True)
    return_code = result.returncode
    assert return_code == 0

###################################TESTS##########################################
def _test_hostname(name, ip_address):
    result = subprocess.run(f"ssh {ip_address} cat /etc/hostname", shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip() == name

def _test_ip_address(ip_address):
    result = subprocess.run(f"ssh {ip_address} cat /etc/network/interfaces | grep {ip_address}", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip().split()
    trash = output[0]
    ip = ' '.join(output[1:]) if len(output) > 1 else ''
    assert ip.strip() == ip_address

def _test_netmask(netmask, ip_address):
    result = subprocess.run(f"ssh {ip_address} cat /etc/network/interfaces | grep 255.255.255.0", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip().split()
    trash = output[0]
    net = ' '.join(output[1:]) if len(output) > 1 else ''
    assert net.strip() == netmask

def _test_gateway(gateway, ip_address):
    result = subprocess.run(f"ssh {ip_address} cat /etc/network/interfaces | grep 10.0.0.1", shell=True, stdout=subprocess.PIPE, text=True)
    output = result.stdout.strip().split()
    trash = output[0]
    net = ' '.join(output[1:]) if len(output) > 1 else ''
    assert net.strip() == gateway

def _test_reach_router(ip_address):
    result = subprocess.run(f"ssh {ip_address} ping -c 1 10.0.0.1", shell=True, check=True)
    return_code = result.returncode
    assert return_code == 0

def _test_reach_internet(ip_address):
    result = subprocess.run(f"ssh {ip_address} ping -c 1 8.8.8.8", shell=True, check=True)
    return_code = result.returncode
    assert return_code == 0

def _test_firewall(ip_address):
    result = subprocess.run(f"ssh {ip_address} nft list ruleset | grep 'hook input' | grep 'policy drop' ", shell=True, stdout=subprocess.PIPE, text=True)
    assert "drop" in result.stdout

def _test_firewall_status(ip_address):
    result = subprocess.run(f"ssh {ip_address} systemctl status nftables | grep SUCCESS ", shell=True, stdout=subprocess.PIPE, text=True)
    assert "SUCCESS" in result.stdout

#########################################SERVER############################################
expected_name_server = 'client-1'
ip_address_server = '10.0.0.3'
netmask_server = '255.255.255.0'
gateway_server = '10.0.0.1'

def test_name_server(): 
    _test_hostname(expected_name_server, ip_address_server)

def test_ip_address_server():
    _test_ip_address(ip_address_server)

def test_netmask_server():
    _test_netmask(netmask_server, ip_address_server)

def test_gateway_server():
    _test_gateway(gateway_server, ip_address_server)

def test_reach_router_server():
    _test_reach_router(ip_address_server)

def test_reach_internet_server():
    _test_reach_internet(ip_address_server)

def test_firewall_server():
    _test_firewall(ip_address_server)

def test_firewall_status_server():
    _test_firewall_status(ip_address_server)

###################################CLIENT_1#########################################
expected_name_client1 = 'client-1'
ip_address_client1 = '10.0.0.3'
netmask_client1 = '255.255.255.0'
gateway_client1 = '10.0.0.1'

def test_name_client1(): 
    _test_hostname(expected_name_client1, ip_address_client1)

def test_ip_address_client1():
    _test_ip_address(ip_address_client1)

def test_netmask_client1():
    _test_netmask(netmask_client1, ip_address_client1)

def test_gateway_client1():
    _test_gateway(gateway_client1, ip_address_client1)

def test_reach_router_client1():
    _test_reach_router(ip_address_client1)

def test_reach_internet_client1():
    _test_reach_internet(ip_address_client1)

def test_firewall_client1():
    _test_firewall(ip_address_client1)

def test_firewall_status_client1():
    _test_firewall_status(ip_address_client1)
    

###################################CLIENT_2#########################################
expected_name_client2 = 'client-2'
ip_address_client2 = '10.0.0.4'
netmask_client2 = '255.255.255.0'
gateway_client2 = '10.0.0.1'

def test_name_client2(): 
    _test_hostname(expected_name_client2, ip_address_client2)

def test_ip_address_client2():
    _test_ip_address(ip_address_client2)

def test_netmask_client2():
    _test_netmask(netmask_client2, ip_address_client2)

def test_gateway_client2():
    _test_gateway(gateway_client2, ip_address_client2)

def test_reach_router_client2():
    _test_reach_router(ip_address_client2)

def test_reach_internet_client2():
    _test_reach_internet(ip_address_client2)

def test_firewall_client2():
    _test_firewall(ip_address_client2)

def test_firewall_status_client2():
    _test_firewall_status(ip_address_client2)




























