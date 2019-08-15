# -*- coding: utf-8 -*-
#
#  Copyright 2019 Martin Schobert <martin@weltregierung.de>
#  

""" The main routine for the sms script """

import argparse
import requests
import os
import sys

ENV_VAR = "SIMPLEFAXDE_PASS"

def login(user, password):
    session = requests.Session()

    r = session.post("https://simple-fax.de/app/", data={'username' : user,
                                                         'password' : password,
                                                         'option' : 'com_users',
                                                         'task' : 'user.login'}, allow_redirects=False)
    
    if "11" in r.text:
        print("+ Logged into service.")
        return session
    elif "error" in r.text:
        print("+ Error detected. Invalid credentials?")
        return None
    else:
        print("+ Unknown error.")
        return None

def send_sms(session, phone, text):
    if session:
        r = session.post("https://simple-fax.de/app/versandbox?task=neuesms",
                         data={'handynummern' : phone,
                               'sms_content' : text,
                               'task' : 'smssenden'})
        
        if r.status_code == 200:
            # It does not make much sense to do further checks:
            # - Code 200 is always returned, but does not mean anything beyond the PHP page is running.
            # - "Ihr SMS ist auf dem Weg!" is always printed, even if you forget the phone number.
            # - An inline image shows a green or red sign, but is not really parsable.
            print("+ SMS maybe sent.")
            return True
        else:
            print("+ Failed to sent SMS.")

    return False
    
def main():

    # process command line arguments
    parser = argparse.ArgumentParser(description='Manage letters via command line', add_help=False)

    parser.add_argument('-h', '--help', action='store_true', dest='help')
    parser.add_argument('--user', help='The simple-fax.de user name. The password is expected to be stored in the environment variable %s.' % ENV_VAR, metavar="MAILADDRESS")
    parser.add_argument('--phone', help='The destination phone number.', metavar="MAILADDRESS")
    parser.add_argument('--text', help='The SMS text to send.', metavar="TEXT")
    parser.add_argument('--stdin', help='Read SMS text from standard in', action='store_true')

    (options, unknown_options) = parser.parse_known_args()
        
                      
    if unknown_options:
        print("+ Unknown options: %s" % unknown_options)
        parser.print_help()
        return

    if options.help:
        parser.print_help()
        return
        
    if options.phone and (options.text or options.stdin) and options.user:
        password = os.environ[ENV_VAR]
        if password is None:
            print("+ Failed to get password from envionment variable %s." % ENV_VAR)
            return
        else:
            session = login(options.user,  password)            
            text = options.text if options.text else "".join(sys.stdin.readlines())
            if session:
                send_sms(session, options.phone, text)
    else:
        parser.print_help()
        return
        
    
if __name__ == "__main__":
    main()

