import subprocess
import re

ip_address_server = "10.0.0.2"
ip_address_client1 = "10.0.0.3"
ip_address_client2 = "10.0.0.4"

#################################TEST_ROUTER###############################

def test_router_conf():
    address = "se.pool.ntp.org"
    result = subprocess.run('cat /etc/ntp.conf | grep se.pool.ntp.org', shell=True, stdout=subprocess.PIPE, text=True)
    assert address in result.stdout

def test_check_restriction():
    address = "127.0.0.1"
    peer_result = subprocess.run( 'grep "restrict.*127.0.0.1" /etc/ntp.conf', shell=True, stdout=subprocess.PIPE, text=True)
    assert address in peer_result.stdout 

def test_check_ntpq():
        result = subprocess.run('ntpq -p' , shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0

#################################FUNCTIONS###############################

def _check_conf(ip_address):
    address = "gw"
    result = subprocess.run(f'ssh {ip_address} cat /etc/ntp.conf | grep server.*gw' , shell=True, stdout=subprocess.PIPE, text=True)
    assert address in result.stdout

def _test_check_ntpq(ip_address):
        result = subprocess.run(f'ssh {ip_address} ntpq -p' , shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0

def _test_ntp_active(ip_address, service):
        status = 'active'
        result = subprocess.run(f'ssh {ip_address} systemctl is-active {service}' , shell=True, stdout=subprocess.PIPE, text=True)
        result.stdout.strip() == status
def _test_check_ntpstat(ip_address):
        result = subprocess.run(f'ssh {ip_address} ntpstat -p' , shell=True, stdout=subprocess.PIPE, text=True)
        assert result.returncode == 0
def _check_time_marginal(ip_address):
       result = subprocess.run(f'ssh {ip_address} ntpstat -p' , shell=True, stdout=subprocess.PIPE, text=True)
       match = re.search(r'(\d+) ms', result.stdout)
       time_ms = int(match.group(1))
       status = False
       if 10 <= time_ms <= 50:
             status = True
       else:
             status = False
       assert status == True
       
#################################CLIENT-1###############################
def test_check_conf_clinet1():
        _check_conf(ip_address_client1)

def test_check_ntpq_client1():
       _test_check_ntpq(ip_address_client1)

def test_ntp_active_client1():
        _test_ntp_active(ip_address_client1, 'ntp')

def test_check_ntpstat_clinet1():
       _test_check_ntpstat(ip_address_client1)

def test_time_marginal_client1():
        _check_time_marginal(ip_address_client1)
#################################CLIENT-2###############################
def test_check_conf_clinet2():
        _check_conf(ip_address_client2)

def test_check_ntpq_client2():
       _test_check_ntpq(ip_address_client2)

def test_ntp_active_client2():
        _test_ntp_active(ip_address_client2, 'ntp')

def test_check_ntpstat_clinet2():
       _test_check_ntpstat(ip_address_client2)

def test_time_marginal_client2():
        _check_time_marginal(ip_address_client2)