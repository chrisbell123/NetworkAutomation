#env vars
import requests
requests.packages.urllib3.disable_warnings(
    requests.packages.urllib3.exceptions.InsecureRequestWarning)

#modules
import json
import requests

#capture credentials
sdwan_password = input("Enter SD-WAN Password ")
sdwan_username = input("Enter SD-WAN Username ")

#capture new DNS server IP addresses
dns_server_primary = input("Enter Primary DNS Server ")
dns_server_secondary = input("Enter Secondary DNS Server ")

#capture SD-WAN devices
sdwan_ip_addresses = input("Enter SD-WAN IP addresses seperates by a comma ")
sdwan_ip_addresses_list  = sdwan_ip_addresses.split(',')

#set headers
headers = {'Content-Type':'application/json'}

for sdwan in sdwan_ip_addresses_list:
    #login to the sd-wan and create a session cookie
    s = requests.Session()
    response = s.post("https://"+sdwan+"/sdwan/nitro/v1/config/login", verify=False, headers=headers, json={"login":{"username":sdwan_username,"password":sdwan_password}})

    #configure the new DNS servers
    print("Connecting to " + sdwan + " to configure DNS servers "+ dns_server_primary + " as primary and " + dns_server_secondary + " as secondary...")
    response = s.put("https://"+sdwan+"/sdwan/nitro/v1/config/dns_settings", verify=False, headers=headers, json={'dns_settings':{"primary_dns_server_ip":dns_server_primary,"secondary_dns_server_ip":dns_server_secondary}})
              
    #verify state
    finalstate = s.get("https://"+sdwan+"/sdwan/nitro/v1/config/dns_settings", verify=False, headers=headers)
    finalstate_dict = json.loads(finalstate.text)
    if finalstate_dict['dns_settings']['primary_dns_server_ip'] == dns_server_primary and finalstate_dict['dns_settings']['secondary_dns_server_ip'] == dns_server_secondary:
        print("SUCCESS")
        with open("dns_sdwan_update_results.txt", "a") as f:
            f.write('\n')
            f.write(sdwan + " SUCCESS -  updated to use DNS servers " + dns_server_primary + " as primary and " + dns_server_secondary + " as secondary")
    else:
        print("FAILURE")
        with open("dns_sdwan_update_results.txt", "a") as f:
            f.write('\n')
            f.write(sdwan + " FAILURE -  failed to update to DNS servers. They are currently set to " + finalstate_dict['dns_settings']['primary_dns_server_ip'] + " as primary and " + finalstate_dict['dns_settings']['secondary_dns_server_ip'] + " as secondary")

    #log out
    print("Ending Session")
    response = s.delete("https://"+sdwan+"/sdwan/nitro/v1/config/login", verify=False, headers=headers)


      









        