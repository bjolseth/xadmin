#!/usr/bin/env python3

import sys
import os

endpoints_file = "endpoints.txt"
default_dial_uri = "tbjolset.ex90@lys.cisco.com"
open_web_in_new_window = False

def main():
    args = sys.argv
    arg_count = len(args)

    if arg_count == 1:
        show_endpoints()

    elif arg_count == 2:
        connect_to(args[1])

    elif (args[1] == "--root"):
        connect_to(args[2], "root")

    elif args[1] == "--answer":
        do_xcommand(args[2], 'xcommand call accept')

    elif args[1] == "--web":
        open_browser(args[2])

    elif args[1] == "--dial" and arg_count == 4:
        uri = args[3] if arg_count == 4 else default_dial_uri
        do_xcommand(args[2], 'xcommand dial number: ' + uri)

    else:
        print("No action")

def connect_to(endpoint, user="admin", cmd=""):
    user = user + "@" + get_ip(endpoint)
    cmd = " ".join(["ssh", user, cmd])
    print(cmd)
    os.system(cmd)

def open_browser(endpoint):
        flag = "--new-window" if open_web_in_new_window else ""
        cmd = "google-chrome {} http://{}".format(flag, get_ip(endpoint))

        print(cmd)
        os.system(cmd)

def do_xcommand(endpoint, xcommand):
    user = "admin@" + get_ip(endpoint)
    cmd = "echo '{xcommand}' | ssh {user} /bin/tsh".format(user=user, xcommand=xcommand)
    print(cmd)
    os.system(cmd)

def get_ip(endpoint_name):
    ip = get_endpoints().get(endpoint_name)
    return ip

def show_endpoints():
    e = get_endpoints()
    for endpoint in e:
        print(endpoint)

def get_endpoints():
    endpoints = {}
    with open(endpoints_file, 'r') as file:
        for line in file:
            endpoint = line.strip().split(' ')
            if len(endpoint) > 1:
                endpoints[endpoint[1]] = endpoint[0]

    return endpoints

if (__name__ == "__main__"):
    main()
