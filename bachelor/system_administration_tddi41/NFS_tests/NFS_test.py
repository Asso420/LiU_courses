import subprocess
import re

ip_address_server = "10.0.0.2"
ip_address_client1 = "10.0.0.3"
ip_address_client2 = "10.0.0.4"

#################################SERVER-TESTS############################
def _export_list(directory):
    ip_address = '10.0.0.2'
    client_1 = '10.0.0.3'
    client_2 = '10.0.0.4'
    result = subprocess.run(f'ssh {ip_address} showmount -e | grep {directory}' , shell=True, stdout=subprocess.PIPE, text=True)
    assert client_1 in result.stdout
    assert client_2 in result.stdout
    
def export_rights(directory):
    ip_address = '10.0.0.2'
    client_1 = '10.0.0.3'
    client_2 = '10.0.0.4'
    rights = '(rw,sync,no_subtree_check,root_squash)'
    result_client1 = subprocess.run(f'ssh {ip_address} cat /etc/exports | grep {directory} | grep {client_1}' , shell=True, stdout=subprocess.PIPE, text=True)  
    result_client2 = subprocess.run(f'ssh {ip_address} cat /etc/exports | grep {directory} | grep {client_2}' , shell=True, stdout=subprocess.PIPE, text=True)
    assert rights in result_client1.stdout
    assert rights in result_client2.stdout

def test_export_rights():
      export_rights('home1')
      export_rights('home2')
      export_rights('/usr/local')

def test_export_direc():
    _export_list('home1')
    _export_list('home2')
    _export_list('/usr/local')
#################################FUNCTIONS###############################
def mount_user_local(ip_address):
    output = "10.0.0.2:/usr/local"
    result = subprocess.run(f'ssh {ip_address} df -h | grep 10.0.0.2:/usr/local' , shell=True, stdout=subprocess.PIPE, text=True)
    assert output in result.stdout #result ==10.0.0.2:/usr/local   24G  2.0G   21G   9% /mnt/user_local
def _nsswitch_config(ip_address):
    result = subprocess.run(f'ssh {ip_address} grep -c "automount:.*nis" /etc/nsswitch.conf', shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip() == '1'
def _fstab(ip_address):
    output = "10.0.0.2:/usr/local /mnt/user_local nfs rw,defaults 0 0"
    result = subprocess.run(f'ssh {ip_address} cat /etc/fstab| grep 10.0.0.2:/usr/local' , shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip() == output
def _auto_master(ip_address):
    output = "+auto.master"
    result = subprocess.run(f'ssh {ip_address} cat /etc/auto.master| grep +auto.master' , shell=True, stdout=subprocess.PIPE, text=True)
    assert result.stdout.strip() == output

#################################Client-1###############################
def test_user_local_client1():
    mount_user_local(ip_address_client1)
def test_nss_config_client1():
    _nsswitch_config(ip_address_client1)
def test_fstab_client1():
    _fstab(ip_address_client1)
def test_auto_master_client1():
    _auto_master(ip_address_client1)


#################################Client-2###############################
def test_user_local_client2():
    mount_user_local(ip_address_client2)
def test_nss_config_client2():
    _nsswitch_config(ip_address_client2)
def test_fstab_client2():
    _fstab(ip_address_client2)
def test_auto_master_client2():
    _auto_master(ip_address_client2)

