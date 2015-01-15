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

    if ip == None:
        print("Couldn't find any endpoint matching '{}'. Known endpoints: ".format(endpoint))
        show_endpoints()
        sys.exit()

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
        uri = args[1] if arg_count == 3 else default_dial_uri
        do_xcommand(ip, 'xcommand dial number: ' + uri)

    elif action == "--search" and arg_count == 3:
        search(ip, args[1])


def connect_to(ip, user="admin", cmd=""):
    user = user + "@" + ip
    cmd = " ".join(["ssh", user, cmd])
    print(cmd)
    os.system(cmd)

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
    ip = get_endpoints().get(endpoint_name)
    return ip

def show_names():
    e = get_endpoints()
    for endpoint in e:
        print(endpoint)

def show_endpoints():
    e = get_endpoints()
    width = max([len(x) for x in e.values()])

    for ip, endpoint in e.items():
        print(ip.ljust(width) + " - " + endpoint)

#def find_uri(ip):
#    subprocess.check_output("echo 'xstatus sip profile 1 registration 1 uri' | ssh admin@10.54.80.30 /bin/tsh", shell=True)

def get_endpoints():
    endpoints = {}
    with open(endpoints_file, 'r') as file:
        for line in file:
            endpoint = line.strip().split()
            if len(endpoint) > 1:
                endpoints[endpoint[1]] = endpoint[0]

    return endpoints



if (__name__ == "__main__"):

    args = sys.argv[1:] # pop first element which is script name
    arg_count = len(args)

    if (arg_count < 1 or args[0] == "--help"):
        sys.exit(help)

    action = args[0]
    endpoint = args[-1] if arg_count > 1 else default_endpoint
    main(endpoint, action)

