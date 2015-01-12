#!/usr/bin/env python3

import sys
import os

help="""\
Copy your ssh public key to any endpoint, to allow password-free access
Syntax:
 copy_ssh_keys <endpoint_ip>

To only see which commands are used:
 copy_ssh_keys <endpoint_ip> --dry-run

Warning: Any public key already installed on endpoint will be deleted
"""

keyhelp="""\
Not able to find your public key, expected it to be at {public_key}
To generate ssh key:
 ssh-keygen -t rsa -C "your_email@example.com"
"""

def main():
    if len(sys.argv) < 2:
        sys.exit(help)
    
    ip = sys.argv[1]

    dir = "/config/home/admin/.ssh"
    file = dir + "/authorized_keys"
    user = "admin:1001"
    public_key = os.path.expanduser('~') + "/.ssh/id_rsa.pub"
    copy = "scp {key} root@{ip}:{file}".format(file=file, ip=ip, key=public_key)

    if not os.path.isfile(public_key):
        sys.exit(keyhelp.format(public_key=public_key))

    codec(ip, "mkdir -p " + dir)
    codec(ip, "chown {} {} ".format(user, dir))
    shell(copy)
    codec(ip, "chown {} {}".format(user, file))
    codec(ip, "chmod 700 " + dir)
    codec(ip, "chmod 600 " + file)

def codec(ip, command):
    user = "root@" + ip
    cmd = "ssh {user} {command}".format(user=user, command=command)
    shell(cmd)

def shell(cmd):
    print(cmd)
    
    if  len(sys.argv) == 3 and sys.argv[2] == "--dry-run":
        pass
    else:
        os.system(cmd)

if (__name__ == "__main__"):
    main()


