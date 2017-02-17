#!/usr/bin/env python

# Gets a router config using paramiko

import paramiko
from getpass import getpass
import time


#username = raw_input("Username: ")
username = "pyclass"
password = getpass()
#ipaddr = raw_input("IP Address of Router: ")
ipaddr = "184.105.247.70"

r = paramiko.SSHClient()

r.set_missing_host_key_policy(paramiko.AutoAddPolicy())

r.connect(ipaddr, username=username, password=password, look_for_keys=False,allow_agent=False, port=22)

# invoke a shell on the remote connection 

remote_conn = r.invoke_shell()


remote_conn.send("term len 0\n")
remote_conn.send("show version\n")
remote_conn.send("show ip int brief\n")
time.sleep(1)

# check if the remote connection has data to send us
# and if so, print the output

if remote_conn.recv_ready() == True:
    output = remote_conn.recv(5000)
    print output
else:
    print 'no output'



remote_conn.close()
