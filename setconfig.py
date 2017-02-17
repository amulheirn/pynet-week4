#!/usr/bin/env python

# Gets a router config using paramiko

import paramiko
from getpass import getpass
import time
import sys

#username = raw_input("Username: ")
username = "pyclass"
password = getpass()
#ipaddr = raw_input("IP Address of Router: ")
ipaddr = "184.105.247.70"


def main():
    r = paramiko.SSHClient()
    r.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        r.connect(ipaddr, username=username, password=password, look_for_keys=False,allow_agent=False, port=22)
    except paramiko.ssh_exception.AuthenticationException:
        print "Authentication error - please try again and check password"
        sys.exit()
    except paramiko.ssh_exception.SSHException:
        print "General SSH exception"
        sys.exit()

    # invoke a shell on the remote connection 
    try:
        remote_conn = r.invoke_shell()
    except paramiko.ssh_exception.SSHException:
        print "Unable to open channel"
        sys.exit()

    # send some commands, wait 1 second
    remote_conn.send("term len 0\n")
    remote_conn.send("enable\n")
    remote_conn.send("conf t\n")
    remote_conn.send("logging buffered 4096\nend\n")

    time.sleep(1)

    # check if the remote connection has data to send us
    # and if so, print the output

    if remote_conn.recv_ready() == True:
        output = remote_conn.recv(5000)
        print output
    else:
        print 'no output'


    remote_conn.close()

if __name__ == "__main__":
    main()
