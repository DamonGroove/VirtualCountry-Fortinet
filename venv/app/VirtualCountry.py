##
# Date: 11/16/2019
# Program Name: Virtual Country
# Description: Creating a Virtual Country
# Author: Damon Sawyer
# Extras: Comparing know IP list to a Dynamic IP list via get request
##
import requests
import ipaddress

# The default file is inthe current directory
myIPsPath = "./my_ips"
# Using Firehol IPlist as an example
dynamicListURI = "https://raw.githubusercontent.com/firehol/blocklist-ipsets/master/firehol_level1.netset"
# The the script file is output to the current directory
scriptFilePath = "./virtualcountry.txt"

# Get user input
print("Welcome to Virtual Country")
print("Please enter the url of an IP list(enter d for default): ")
urlInput = input();
if urlInput != 'd':
    dynamicListURI = urlInput
print("URL used: " + dynamicListURI)

print("Enter the file path of your known ip list(enter d for default): ")
myIPsInput = input();
if myIPsInput != 'd':
    myIPsPath = myIPsInput
print("Know IP list file path: " + myIPsPath)

print("Enter the file path of your Script output(enter d for default): ")
scriptPathInput = input();
if scriptPathInput != 'd':
    scriptFilePath = scriptPathInput
print("Script output file path: " + scriptFilePath)

# Declare global variables
myIPArr = {}
checkcount = 0
gotContent = requests.get(dynamicListURI)

# Main Function
def mainFun():
    with open(myIPsPath) as file:
         myIPArr = list(dict.fromkeys(file.read().split('\n')))
    contentArr = list(dict.fromkeys(gotContent.text.split('\n')))
    print(contentArr.__len__())

    # Overwrite file
    scriptFile = open(scriptFilePath, "w")

    # Setting limits to 65k flat
    maxIPRangeTables = 65000
    # First entry will be 1 not 0 since users usually start with 1
    i = 1
    # User Inputs. Will fail if unsupported characters are included
    geoIPName = "virtual_country"
    geoDescription = "List of bad IPs"

    print("# Building script....")
    print("Known IPs that match up with External IPs: ")

    # Writing to  script file
    scriptFile.write("config system geoip-override" + "\n")
    scriptFile.write("edit " + "\"" + geoIPName + "\"" + "\n")
    scriptFile.write("set description " + "\"" + geoDescription + "\"" + "\n")
    scriptFile.write("config ip-range\n")
    for externalip in contentArr:
        # Adds the subet 32 if the item does not contain a "#", 
        # the max range has not been met and the split of "." returns 4 indexes
        # Then if there is already not a "/" within the item
        if externalip.split('#').__len__() < 2 and i <= maxIPRangeTables and externalip.split('.').__len__() == 4:
            if (externalip.split('/').__len__() > 1) == False:
                externalip = externalip + "/32"

            if isIP(externalip):
                if isUseableIP(externalip):
                    ipRange = netToRange(externalip)
                    scriptFile.write("edit " + str(i) + "\n")
                    scriptFile.write("set start-ip " + str(ipRange[0]) + "\n")
                    scriptFile.write("set end-ip " + str(ipRange[1]) + "\n")
                    scriptFile.write("next\n")
                    compareLists(externalip, myIPArr)
                    i = i + 1

    scriptFile.write("end\n")
    scriptFile.write("next\n")
    scriptFile.write("end\n")
    scriptFile.close()

# Checks if the subnet is useable
def isUseableIP(externalip):
    extNet = ipaddress.ip_network(externalip)
    badZoneA = ipaddress.ip_network('0.0.0.0/8')
    badZoneB = ipaddress.ip_network('127.0.0.0/8')
    badZoneC = ipaddress.ip_network('224.0.0.0/3')
    if extNet.supernet_of(badZoneA) or extNet.supernet_of(badZoneB) or extNet.supernet_of(badZoneC) or \
            extNet.subnet_of(badZoneA) or extNet.subnet_of(badZoneB) or extNet.subnet_of(badZoneC):
        return False
    return True

# This needs to be refactored
# Checks if the item is actually an IP
def isIP(externalip):
    octet = 0
    isIPaddress = True
    while octet < externalip.split('.').__len__():
        if octet == 3:
            if externalip.split('.')[octet].split('/').__len__() == 2:
                if int(externalip.split('.')[octet].split('/')[1]) <= 32 and \
                        int(externalip.split('.')[octet].split('/')[1]) >= 8 and \
                        int(externalip.split('.')[octet].split('/')[0]) >= 0 and \
                        int(externalip.split('.')[octet].split('/')[0]) <= 255:
                    True
                else:
                    isIPaddress == False
            else:
                isIPaddress == False
        elif int(externalip.split('.')[octet]) >= 0 and int(externalip.split('.')[octet]) <= 255:
            True
        else:
            isIPaddress == False
        octet = octet + 1
    return isIPaddress

# Converts Subnets to Ranges
def netToRange(ipNet):
    # print("Converting Subnets to IP ranges")
    startIP = ipaddress.IPv4Network(ipNet)[0]
    endIP = ipaddress.IPv4Network(ipNet)[ipaddress.IPv4Network(ipNet).num_addresses - 1]
    # print(startIP , endIP)
    return startIP, endIP

# Compares an external http IP list to an internal file IP list
def compareLists(externalip, myIPArr):
    for myip in myIPArr:
        if  myip.split('.').__len__() == 4:
            if (myip.split('/').__len__() > 1) == False:
                myip = myip + "/32"

            externalNet = ipaddress.ip_network(externalip)
            myNet = ipaddress.ip_network(myip)

            if externalNet.subnet_of(myNet) or externalNet.supernet_of(myNet):
                print("Known IP: " + myip + " matches " + "External IP: " + externalip)

 # Run
mainFun()
