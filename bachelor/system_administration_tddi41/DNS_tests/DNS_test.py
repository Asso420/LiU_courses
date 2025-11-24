import subprocess
ip_domain_list = [
    ("10.0.0.1", "gw.gruppnamn.example.com."),
    ("10.0.0.2", "gruppnamn.example.com."),
    ("10.0.0.3", "client-1.gruppnamn.example.com."),
    ("10.0.0.4", "client-2.gruppnamn.example.com."),
]
ip_address_router, domain_name_router = ip_domain_list[0]
ip_address_server, domain_name_server = ip_domain_list[1]
ip_address_client1, domain_name_client1 = ip_domain_list[2]
ip_address_client2, domain_name_client2 = ip_domain_list[3]
######################################TEST#####################################
def _nameserver(ip_address):
        nameserver = "10.0.0.2"
        result = subprocess.run(f'ssh {ip_address} cat /etc/resolv.conf | grep nameserver' , shell=True, stdout=subprocess.PIPE, text=True)
        assert nameserver in result.stdout

def _test_forward_dig(ip_address_ssh, ip_address, domain_name):
       result = subprocess.run(f'ssh {ip_address_ssh} dig +short {domain_name}' , shell=True, stdout=subprocess.PIPE, text=True)
       assert result.stdout.strip() == ip_address

def _test_reverse_dig(ip_address_ssh, ip_address, domain_name):
      result = subprocess.run(f'ssh {ip_address_ssh} dig +short -x {ip_address}' , shell=True, stdout=subprocess.PIPE, text=True)
      assert result.stdout.strip() == domain_name
      

################################SERVER#####################################

def test_nameserver_server():
    _nameserver(ip_address_server) 

def test_forward_dig_router_server():
    _test_forward_dig(ip_address_server, ip_address_router, domain_name_router )
        
def test_forward_dig_client1_server():
      _test_forward_dig(ip_address_server, ip_address_client1, domain_name_client1 )
        
def test_forward_dig_client2_server():
      _test_forward_dig(ip_address_server, ip_address_client2, domain_name_client2 )
        
def test_reverse_dig_router_server():
      _test_reverse_dig(ip_address_server, ip_address_router, domain_name_router )
        
def test_reverse_dig_client1_server():
      _test_reverse_dig(ip_address_server, ip_address_client1, domain_name_client1)
        
def test_reverse_dig_client2_server():
      _test_reverse_dig(ip_address_server, ip_address_client2, domain_name_client2)
def test_zone_forward():
      zone = "gruppnamn.example.com"
      result = subprocess.run(f'ssh 10.0.0.2 named-checkzone {zone} /etc/bind/zones/{zone} | grep OK', shell=True, stdout=subprocess.PIPE, text=True)
      assert result.stdout.strip() == 'OK'
def test_zone_reverse():
      zone = "rev.0.0.10"
      result = subprocess.run(f'ssh 10.0.0.2 named-checkzone {zone} /etc/bind/zones/{zone} | grep OK', shell=True, stdout=subprocess.PIPE, text=True)
      assert result.stdout.strip() == 'OK'
def test_configuration_file():
      path = '/etc/bind/named.conf.local'
      result = subprocess.run(f'ssh 10.0.0.2 named-checkconf {path}', shell=True, stdout=subprocess.PIPE, text=True)
      return_code = result.returncode
      assert return_code == 0

def test_bind_status():
    ip_address = "10.0.0.2"
    result = subprocess.run(f"ssh {ip_address} systemctl status bind9 | grep active ", shell=True, stdout=subprocess.PIPE, text=True)
    assert "running" in result.stdout
      
################################ROUTER#####################################
def _test_forward_dig_router(ip_address, domain_name):
       result = subprocess.run(f'dig +short {domain_name}' , shell=True, stdout=subprocess.PIPE, text=True)
       assert result.stdout.strip() == ip_address
def _test_reverse_dig_router(ip_address, domain_name):
      result = subprocess.run(f'dig +short -x {ip_address}' , shell=True, stdout=subprocess.PIPE, text=True)
      assert result.stdout.strip() == domain_name
def test_nameserver_router():
        nameserver = "10.0.0.2"
        result = subprocess.run('cat /etc/resolv.conf | grep nameserver' , shell=True, stdout=subprocess.PIPE, text=True)
        assert nameserver in result.stdout

def test_forward_dig_server_router():
       _test_forward_dig_router(ip_address_server, domain_name_server)
        
def test_forward_dig_client1_router():
       _test_forward_dig_router(ip_address_client1, domain_name_client1)
        
def test_forward_dig_client2_router():
       _test_forward_dig_router(ip_address_client2, domain_name_client2)
        
def test_reverse_dig_server_router():
       _test_reverse_dig_router(ip_address_server, domain_name_server)
        
def test_reverse_dig_client1_router():
        _test_reverse_dig_router(ip_address_client1, domain_name_client1)
        
def test_reverse_dig_client2_router():
        _test_reverse_dig_router(ip_address_client2, domain_name_client2)
################################CLIENT-1####################################

def test_nameserver_client1():
        _nameserver(ip_address_client1)

def test_forward_dig_server_client1():
       _test_forward_dig(ip_address_client1, ip_address_server, domain_name_server)
        
def test_forward_dig_router_client1():
       _test_forward_dig(ip_address_client1, ip_address_router, domain_name_router)
        
def test_forward_dig_client2_client1():
       _test_forward_dig(ip_address_client1, ip_address_client2, domain_name_client2)
        
def test_reverse_dig_server_client1():
       _test_reverse_dig(ip_address_client1, ip_address_server, domain_name_server)
        
def test_reverse_dig_router_client1():
       _test_reverse_dig(ip_address_client1, ip_address_router, domain_name_router)
        
def test_reverse_dig_client2_client1():
       _test_reverse_dig(ip_address_client1, ip_address_client2, domain_name_client2)
################################CLIENT-2####################################

def test_nameserver_client2():
        _nameserver(ip_address_client2)

def test_forward_dig_server_client2():
        _test_forward_dig(ip_address_client2, ip_address_server, domain_name_server)
def test_forward_dig_router_client2():
        _test_forward_dig(ip_address_client2, ip_address_router, domain_name_router)
def test_forward_dig_client1_client2():
        _test_forward_dig(ip_address_client2, ip_address_client1, domain_name_client1)
def test_reverse_dig_server_client2():
        _test_reverse_dig(ip_address_client2, ip_address_server, domain_name_server)
def test_reverse_dig_router_client2():
        _test_reverse_dig(ip_address_client2, ip_address_router, domain_name_router)
def test_reverse_dig_client1_client2():
        _test_reverse_dig(ip_address_client2, ip_address_client1, domain_name_client1)