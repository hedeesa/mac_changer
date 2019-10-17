#!/usr/bin/python3
#By hedeesa @ https://github.com/hedeesa

import subprocess
import optparse
import time
import re

# ----------------------

def get_switches():
  parser = optparse.OptionParser()
  parser.add_option("-i","--interface",dest="interface",help="Name of the interface you want to change its mac")
  parser.add_option("-m","--mac",dest="new_mac",help="Add your new MAC")
  (options, args) = parser.parse_args()
  if not options.interface:
    parser.error("please enter the name of interface, check --help for more info")
  if not options.new_mac:
    parser.error("please enter a new MAC Address, check --help for more info")

  return options  


def change_mac(options):
  print("[+] changing the MAC Address of "+ options.interface + " to "+ options.new_mac)
  subprocess.call(["sudo","ifconfig",options.interface,"down"])
  subprocess.call(["sudo","ifconfig",options.interface,"hw","ether",options.new_mac])
  subprocess.call(["sudo","ifconfig",options.interface,"up"])

  
def network_restart():
  print("[+] Restarting Network")
  subprocess.call(["sudo","nmcli","networking","off"])
  subprocess.call(["sudo","nmcli","networking","on"])
  print("[+] Done!")


def check_interface(options):
  ifconfig=subprocess.getoutput("ifconfig "+options.interface )
  if "Device not found" in ifconfig:
    print("[-] The Interface is not found, Please Check Again.")
    return 0
  else: 
    result_mac=re.search(r"(\w\w:){5}\w\w",ifconfig)
    if result_mac:
      return result_mac.group(0)
    else:
      print("[-] This Interface does not have MAC address")
      return 0


def check_mac(options):
  result_mac=re.match(r"(\w\w:){5}\w\w",options.new_mac)
  if not result_mac:
    print("[-] The length of MAC Address id not Valid, Please Check Again.")
    return 0
  else:
    return 1


def check_process(options):
  ifconfig=subprocess.getoutput("ifconfig "+options.interface )
  q=re.search(r"(\w\w:){5}\w\w",ifconfig)
  if q.group(0) == options.new_mac:
    print("[+] The MAC Address of "+options.interface+ " has changed to "+options.new_mac+" Successfully!")
    return 1
  else:
    print("[-] Something Went Wrong!")
    print("[-] Process is Aborted!")
    return 0

  
# ----------------------

options= get_switches()
result_int=check_interface(options)
result_mac=check_mac(options)
if result_int==0 or result_mac==0 :
  print("[-] Process is Aborted!")
else: 
  change_mac(options)
  process=check_process(options)
  if process==1 :
    network_restart()



