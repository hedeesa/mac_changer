#!/usr/bin/python3
import subprocess
import optparse
import time

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
  time.sleep(2)
  subprocess.call(["sudo","nmcli","networking","on"])

# ----------------------

options= get_switches()
change_mac(options)
network_restart()