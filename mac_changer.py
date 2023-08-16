import subprocess
import optparse


parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")

(options, arguments) = parser.parse_args()
def Welcome():
    print('''
             AVAILABLE INTERFACES
    -----------------------------------
    -----------------------------------''')

    subprocess.call(f"ip addr show", shell=True)

def Mac_Changer():
    interfaces = ['wlan0', 'eth0', 'l0', 'docker0']
    interface = options.interface or input("Interface> ")
    new_mac = options.new_mac or input("new MAC> ")
    for x in interfaces:
        if interface == x:
            print(f"[+] Changing MAC address for {interface} to {new_mac}")
            subprocess.call(["ifconfig", interface, "down"])
            subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
            subprocess.call(["ifconfig", interface, "up"])
            subprocess.call(f"ifconfig {interface} | grep ether", shell=True)
            break
    else:
        print('!!Interface Not Found!!')



Welcome()
Mac_Changer()








