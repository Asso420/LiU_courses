#!/bin/sh
echo "Flushing iptables rules..."
#sleep 1
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
echo "Setting iptables rules..."
# Enter your rules here

#iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

#-------DNS------------
#iptables -A INPUT -i eth0 -p udp -d 10.19.1.12 --dport 53 -j ACCEPT

iptables -A FORWARD -i eth0 -d 10.19.1.12 -p udp --dport 53 -j ACCEPT
iptables -A FORWARD -i eth1 -d 10.19.1.142 -p udp --dport 53 -j ACCEPT
iptables -A FORWARD -s 10.19.1.12 -p udp --sport 53 -j ACCEPT
iptables -A FORWARD -s 10.19.1.12 -o eth0 -p udp --sport 53 -j ACCEPT

#---------------Mail----------------------
iptables -A FORWARD -i eth0 -d 10.19.1.11 -p tcp --dport 25 -j ACCEPT
iptables -A FORWARD -s 10.19.1.11 -d 10.19.1.141 -p tcp --dport 25 -j ACCEPT
iptables -A FORWARD -s 10.19.1.141 -o eth0 -p tcp --dport 25 -j ACCEPT
iptables -A FORWARD -i eth2 ! -s 10.19.1.141 -p tcp --dport 25 -j DROP

#----------------------web--------------------
iptables -A FORWARD -i eth0 -d 10.19.1.10 -p tcp --dport 80 -j ACCEPT

#---------------------Firewall-------------------
iptables -A INPUT -i lo -j ACCEPT
iptables -A OUTPUT -o lo -j ACCEPT
iptables -A INPUT -i eth0 -p udp --dport 520 -j ACCEPT
iptables -A INPUT -i eth2 -p tcp --dport 22 -j ACCEPT
iptables -P INPUT DROP

#-------OTHER-----------------------
iptables -t nat -A POSTROUTING -s 192.168.12.0/24 -o eth0 -j SNAT --to-source 10.19.0.1

iptables -A FORWARD -i eth0 -o eth2 -p udp --dport 500 -j ACCEPT
iptables -A FORWARD -i eth0 -o eth2 -p esp -j ACCEPT
iptables -A FORWARD -i eth0 -o eth2 -p ah -j ACCEPT

iptables -A FORWARD -p icmp --icmp-type echo-request -j ACCEPT
iptables -A FORWARD -p icmp --icmp-type destination-unreachable -j ACCEPT
iptables -A FORWARD -p icmp --icmp-type time-exceeded -j ACCEPT

#------Default rules----------------
iptables -P FORWARD DROP
#iptables -A FORWARD -i eth0 -o eth1 -j REJECT
#iptables -A FORWARD -i eth0 -o eth2 -j REJECT
#iptables -A FORWARD -i eth1 -o eth2 -j REJECT
#iptables -A FORWARD -i eth1 -o eth0 -j REJECT
iptables -A FORWARD -i eth2 -o eth0 -j ACCEPT
iptables -A FORWARD -i eth2 -o eth1 -j ACCEPT


#iptables -A INPUT -p tcp --dport 22 -j ACCEPT
#iptables -A FORWARD -s 10.0.0.0/24 -p udp --dport 53 -j ACCEPT

echo "Setting iptables rules... done"

