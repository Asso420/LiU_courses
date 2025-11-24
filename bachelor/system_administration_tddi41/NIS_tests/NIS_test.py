import subprocess


ip_address_server = "10.0.0.2"
ip_address_client1 = "10.0.0.3"
ip_address_client2 = "10.0.0.4"

#################################TEST###############################
def _defaultdomain(ip_address):
        domain = "nis.example.com"
        result = subprocess.run(f'ssh {ip_address} cat /etc/defaultdomain' , shell=True, stdout=subprocess.PIPE, text=True)
        assert domain in result.stdout

def _nis_server(ip_address):
        nis_server = "10.0.0.2"
        result = subprocess.run(f'ssh {ip_address} ypwhich' , shell=True, stdout=subprocess.PIPE, text=True)
        assert nis_server in result.stdout

def _nis_domain(ip_address):
        nis_domain = "nis.example.com"
        result = subprocess.run(f'ssh {ip_address} domainname' , shell=True, stdout=subprocess.PIPE, text=True)
        assert nis_domain in result.stdout

def _active_service(ip_address, service):
        status = 'active'
        result = subprocess.run(f'ssh {ip_address} systemctl is-active {service}' , shell=True, stdout=subprocess.PIPE, text=True)
        result.stdout.strip() == status

def _nsswitch_config(ip_address):
        passwd_result = subprocess.run(f'ssh {ip_address} grep -c "passwd:.*nis" /etc/nsswitch.conf', shell=True, stdout=subprocess.PIPE, text=True)
        group_result = subprocess.run(f'ssh {ip_address} grep -c "group:.*files.*nis" /etc/nsswitch.conf', shell=True, stdout=subprocess.PIPE, text=True)
        shadow_result = subprocess.run(f'ssh {ip_address} grep -c "shadow:.*files.*nis" /etc/nsswitch.conf', shell=True, stdout=subprocess.PIPE, text=True)
        gshadow_result = subprocess.run(f'ssh {ip_address} grep -c "gshadow:.*compat.*nis" /etc/nsswitch.conf', shell=True, stdout=subprocess.PIPE, text=True)
        assert passwd_result.stdout.strip() == '1'
        assert group_result.stdout.strip() == '1'
        assert shadow_result.stdout.strip() == '1'
        assert gshadow_result.stdout.strip() == '1'

def _check_directory(ip_address):
        result = subprocess.run(f'ssh {ip_address} test -d /var/yp/nis.example.com' , shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0
def _test_check_ypcat_passwd(ip_address):
        result = subprocess.run(f'ssh {ip_address} ypcat passwd' , shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0
def _test_check_ypcat_groups(ip_address):
        result = subprocess.run(f'ssh {ip_address} ypcat group' , shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0
###########################SERVER#################################
def test_defaultdomain_server():
        _defaultdomain(ip_address_server)
def test_domain_server():
        _nis_domain(ip_address_server)
def test_ypserv():
        _active_service(ip_address_server, 'ypserv')
def test_rpcbind():
        _active_service(ip_address_server, 'rpcbind')
def test_directory_server():
        _check_directory(ip_address_server)
def test_ypcat_server():
        _test_check_ypcat_passwd(ip_address_server)
        _test_check_ypcat_groups(ip_address_server)
        


###########################CLIENT-1################################
def test_defaultdomain_client1():
        _defaultdomain(ip_address_client1)
def test_ypwhich_client1 ():
        _nis_server(ip_address_client1)
def test_domain_client1():
        _nis_domain(ip_address_client1)
def test_ypbind_client1():
        _active_service(ip_address_client1, 'ypbind')
def test_nsswitch_client1():
        _nsswitch_config(ip_address_client1)
def test_directory_client1():
        _check_directory(ip_address_client1)
def test_ypcat_client1():
        _test_check_ypcat_passwd(ip_address_client1)
        _test_check_ypcat_groups(ip_address_client1)
###########################CLIENT-2################################
def test_defaultdomain_client2():
        _defaultdomain(ip_address_client2)
def test_ypwhich_client2 ():
        _nis_server(ip_address_client2)
def test_domain_client2():
        _nis_domain(ip_address_client2)
def test_ypbind_client2():
        _active_service(ip_address_client2, 'ypbind')
def test_nsswitch_client2():
        _nsswitch_config(ip_address_client2)
def test_directory_client2():
        _check_directory(ip_address_client2)
def test_ypcat_client2():
        _test_check_ypcat_passwd(ip_address_client2)
        _test_check_ypcat_groups(ip_address_client2)