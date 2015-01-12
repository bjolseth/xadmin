#!/usr/bin/env python3

import sys
import subprocess

endpoints_file = "endpoints.txt"

def main():
    if len(sys.argv) == 1:
        show_endpoints()
    elif (sys.argv[1] == "--root"):
        connect_to(sys.argv[2], "root")
    else:
        connect_to(sys.argv[1])

def connect_to(endpoint, user="admin"):
    ip = get_endpoints().get(endpoint)
    user = user + "@" + ip
    print("ssh " + user)
    subprocess.call(["ssh", user])

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
