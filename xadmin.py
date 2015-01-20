#!/usr/bin/env python3

import sys
import os

endpoints_file = os.path.dirname(os.path.realpath(__file__)) + "/" + "endpoints.txt"
default_dial_uri = "tbjolset.ex90@lys.cisco.com"
default_endpoint = "sx20"
open_web_in_new_window = False

tsh_cmd = "echo '{xcommand}' | ssh {user} /bin/tsh"

help = """\
Quick acces to common operations on endpoints with auto-completion in shell

Commands:
 xlist                      Show all endpoints (from endpoints.txt)
 xadmin <codec>             Ssh as admin to endpoint
 xroot <codec>              Ssh as root to endpoint
 xdial <uri> <codec>        Dial from codec to uri. If none are provided, use your defaults
 xanswer <codec>            Answer any incoming call
 xdisconnect <codec>        Disconnect all calls
 xsearch <word> <codec>     Search in xstatus and xconfig for word
 xweb <codec>               Open web browser for endpoint's web settings (google-chrome required)

Codec name is optional, if not provided, the default is used
"""

def main(endpoint, action):

    try:
        ip = get_ip(endpoint)
        
    except FileNotFoundError:
        sys.exit("Couldn't find endpoint file {}. Please make sure it exists".format(endpoints_file))
        
    except TypeError:
        print("Couldn't find any endpoint matching '{}'. Known endpoints: ".format(endpoint))
        show_endpoints()
        sys.exit(2)

    do_action(ip, action)

def do_action(ip, action):
    if action == "--list":
        show_endpoints()

    elif action == "--listnames":
        show_names()

    elif action == "--admin":
        connect_to(ip)

    elif action == "--root":
        connect_to(ip, "root")

    elif action == "--answer":
        do_xcommand(ip, 'xcommand call accept')

    elif action == "--disconnect":
        do_xcommand(ip, 'xcommand call disconnectall')

    elif action == "--web":
        open_browser(ip)

    elif action == "--dial":
        uri = args[1] if arg_count > 1 else default_dial_uri
        dial(ip, uri)

    elif action == "--search" and arg_count > 1:
        search(ip, args[1])


def connect_to(ip, user="admin", cmd=""):
    user = user + "@" + ip
    cmd = " ".join(["ssh", user, cmd])
    print(cmd)
    os.system(cmd)

def dial(ip, uri):
    if ("@" not in uri):
        uri = get_uri(args[1])

    do_xcommand(ip, 'xcommand dial number: ' + uri)

def search(ip, word):
    user = "admin@" + ip

    for node in ['xstatus', 'xconfig']:
        cmd = tsh_cmd.format(user=user, xcommand=node) + " | grep -i " + word
        print(cmd)
        os.system(cmd)

def open_browser(ip):
        flag = "--new-window" if open_web_in_new_window else ""
        cmd = "google-chrome {} http://{}".format(flag, ip)

        print(cmd)
        os.system(cmd)

def do_xcommand(ip, xcommand):
    user = "admin@" + ip
    cmd = tsh_cmd.format(user=user, xcommand=xcommand)
    print(cmd)
    os.system(cmd)

def get_ip(endpoint_name):
    ip = get_endpoints().get(endpoint_name)[0]
    return ip

def get_uri(endpoint_name):
    uri = get_endpoints().get(endpoint_name)[1]
    return uri

def show_names():
    e = get_endpoints()
    for endpoint in e:
        print(endpoint)

def show_endpoints():
    e = get_endpoints()
    name_width = max([len(name) for name in e.keys()])
    ip_width = max([len(ip) for ip, uri in e.values()])    
    
    for ip, endpoint in e.items():
        print(ip.ljust(name_width) + " - " + endpoint[0].ljust(ip_width) + " - " + endpoint[1])

def find_uri(ip):
    import subprocess
    result = subprocess.check_output("echo 'xstatus sip profile 1 registration 1 uri' | ssh admin@{ip} /bin/tsh".format(ip=ip), shell=True)
    words = result.decode(encoding='UTF-8').split()
    uris = [word for word in words if "@" in word]
    uri = uris[0].replace('"', '') if uris else None
    return uri

def add_entry(ip, name, uri):
    line = " ".join([name, ip, uri])
    with open(endpoints_file, "a") as file:
        file.write("\n" + line)

def get_endpoints():
    endpoints = {}
    with open(endpoints_file, 'r') as file:
        for line in file:
            endpoint = line.strip().split()
            
            if len(endpoint) > 1: # skip empty lines
                endpoints[endpoint[1]] = (endpoint[0].strip(), endpoint[2].strip())

    return endpoints



if (__name__ == "__main__"):

    args = sys.argv[1:] # pop first element which is script name
    arg_count = len(args)

    if (arg_count < 1 or args[1] == "--help"):
        print(help)
        sys.exit()

    commands_with_params = ['--dial', '--search']
    action = args[0]
    endpoint_index = 2 if action in commands_with_params else 1
    endpoint = args[endpoint_index] if arg_count > endpoint_index  else default_endpoint
    main(endpoint, action)

