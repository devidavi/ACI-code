#!/usr/bin/env python
import requests
import json

#--------------------------
# Authentication POST
#--------------------------
def authentication(username, password, apic):
    auth_url = apic + '/api/aaaLogin.json'
    auth = dict(aaaUser=dict(attributes=dict(name=username, pwd=password)))
    authenticate = requests.post(auth_url, data=json.dumps(auth), verify=False)
    cookies = authenticate.cookies
    return cookies

#-------------------------
# Making Tenant & VRF 
#-------------------------
def make_tenant(cookies, apic):
    tenant_name = raw_input('Tenant name? -->' )
    tenant_url = apic + '/api/node/mo/uni/tn-{}.json'.format(tenant_name)
    vrf = raw_input('VRF name for Tenant? -->' )
    tenant = {"fvTenant":{"attributes":{"dn":"uni/tn-{}".format(tenant_name),"name":tenant_name,"rn":"tn-{}".format(tenant_name),"status":"created"},"children":[{"fvCtx":{"attributes":{"dn":"uni/tn-{}/ctx-{}".format(tenant_name, vrf),"name":vrf,"rn":"ctx-{}".format(vrf),"status":"created"},"children":[]}}]}}
    create_tenant = requests.post(tenant_url, cookies=cookies, data=json.dumps(tenant), verify=False)

#-------------------------
# Make Bridge Domain in Tenant
#-------------------------
def make_BD(cookies, apic):
    BD_name = raw_input('Bridge Domain name? -->' )
    BD_url = apic + '/api/node/mo/uni/tn-example/BD-DB_{}.json'.format(BD_name)
    BD = {"fvBD":{"attributes":{"dn":"uni/tn-{}/BD-BD-{}".format(tenant_name, BD_name),"mac":"00:22:BD:F8:19:FF","name":"BD-{}".format(BD_name),"rn":"BD-BD-{}".format(BD_name),"status":"created"},"children":[{"fvSubnet":{"attributes":{"dn":"uni/tn-{}/BD-BD-{}/subnet-[10.3.2.1/24]".format(tenant_name,BD_name),"ip":"10.3.2.1/24","rn":"subnet-[10.3.2.1/24]","status":"created"},"children":[]}},{"fvRsCtx":{"attributes":{"tnFvCtxName":vrf,"status":"created,modified"},"children":[]}}]}}
    create_BD = requests.post(BD_url, cookies=cookies, data=json.dumps(BD), verify=False)

#-----------------------
# Main Function to call
#-----------------------
def main():
    print ''
    print 'Please fill out the information below...'
    print 'Example URL ---- https://apic (last / isnt need and will throw an error)'
    print '-------------------------------------------------------------------------'
    apic = raw_input('APIC URL -->  ')
    username = raw_input('APIC username -->  ')
    password = raw_input('APIC password -->  ')
    print '-------------------------------------------------------------------------'
    print 'Passing URL= {}, Username= {}, Password= {}'.format(apic, username, password)
    print ''
    authentication(username, password, apic)
    make_tenant(cookies)
    make_BD(cookies)

# ---- CALL MAIN FUNCTION ----
main()

#-----------------------
# POST REFERENCES PULLED FROM API INSPECTOR
#-----------------------
"""
method: POST
url: https://apic/api/node/mo/uni/tn-TEST.json
payload{"fvTenant":{"attributes":{"dn":"uni/tn-TEST","name":"TEST","rn":"tn-TEST","status":"created"},"children":[{"fvCtx":{"attributes":{"dn":"uni/tn-TEST/ctx-TEST","name":"TEST","rn":"ctx-TEST","status":"created"},"children":[]}}]}}


method: POST
url: https://apic/api/node/mo/uni/tn-TEST/BD-BD-TEST.json
payload{"fvBD":{"attributes":{"dn":"uni/tn-TEST/BD-BD-TEST","mac":"00:22:BD:F8:19:FF","name":"BD-TEST","rn":"BD-BD-TEST","status":"created"},"children":[{"fvSubnet":{"attributes":{"dn":"uni/tn-TEST/BD-BD-TEST/subnet-[10.2.2.1/24]","ip":"10.2.2.1/24","rn":"subnet-[10.2.2.1/24]","status":"created"},"children":[]}},{"fvRsCtx":{"attributes":{"tnFvCtxName":"TEST","status":"created,modified"},"children":[]}}]}}
"""