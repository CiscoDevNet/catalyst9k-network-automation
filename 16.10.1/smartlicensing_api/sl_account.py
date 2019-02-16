#!/usr/bin/env python3
#
# Copyright (c) 2018, Cisco and/or its affiliates
# Author: Jay Sharma
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
#The script provides all NB API for CSSM Server necessary for Smart Licensing 
import requests
from argparse import ArgumentParser
import json

def checkSmartAccount(auth_code, sa_domain, status="ACTIVE"):
    """This proc will check if the Smart Account is <status> return true if it is, else return false """
    url = "https://apx.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/search?"

    logm = ""

    querystring = {"domain": sa_domain}
    headers = {
    'content-type': "application/json",
    'Authorization': "",
    'cache-control': "no-cache",
    }

    headers['Authorization'] = auth_code
    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        out = json.loads(response.text)
    except:
        logm = 'Unable to get the response from CSSM. Error:  %s' % response.text
        return logm
    
    accountExists = False
    accountStatus = False
    for account in out['accounts']:
        if account['domain'].upper() == sa_domain.upper():
            accountExists = True
            if account['status'].upper() == status:
                accountStatus = True
                break
            break

    if accountExists and accountStatus:
        return True 

    else:
        return False

def findSmartAccountProperties(auth_code, sa_domain, property='name'):
    """This proc will find the smart account <property> associated with <sa domain>"""
    url = "https://apx.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/search?"

    logm = ""
    account_property = ""
    querystring = {"domain": sa_domain}
    headers = {
    'content-type': "application/json",
    'Authorization': "",
    'cache-control': "no-cache",
    }

    headers['Authorization'] = auth_code
    response = requests.request("GET", url, headers=headers, params=querystring)

    try:
        out = json.loads(response.text)
    except:
        logm = 'Unable to get the response from CSSM. Error:  %s' % response.text
        return (logm)

    accountExists = False
    accountList=[]
    for account in out['accounts']:
        accountList.append(account['domain'])
        if account['domain'].upper() == sa_domain.upper():
            accountExists = True
            account_property = account[property]
            break

    if not accountExists:
        print("Domain %s does not exists! Existing acoounts with this domain are %s" %(sa_domain, out['accounts']))
    return account_property

def availableVA(auth_code, sa_domain, accountType):
    """This proc will list all the available Smart Accounts under <sa_domain> and <accountType>"""
    url = "https://apx.cisco.com/services/api/smart-accounts-and-licensing/v1/accounts/{smartAccountDomain}/{accountType}/virtual-accounts"
    logm = ""
    headers = {
    'content-type': "application/json",
    'Authorization': "",
    'cache-control': "no-cache",
    }
    headers['Authorization'] = auth_code
    response = requests.request("GET", url.format(smartAccountDomain=sa_domain, accountType=accountType), headers=headers)
    try:
        out = json.loads(response.text)
    except:
        logm = 'Unable to get the response from CSSM. Error:  %s' % response.text
        return(logm)

    vaList = []

    for va in out["virtualAccounts"]:
        vaList.append(va['name'])

    return vaList
