import re
import subprocess
import optparse

parser = optparse.OptionParser()
parser.add_option("-i", "--interface", dest="interface", help="Interface to change its MAC address")
parser.add_option("-m", "--mac", dest="new_mac", help="new MAC address")

(options, arguments) = parser.parse_args()

interfaces = subprocess.check_output(f"ifconfig", shell=True)
interfaces_decoded = interfaces.decode('utf-8')
available_interfaces = re.findall(r"(\w+): flags=", interfaces_decoded)


def Welcome():
    print('''
             AVAILABLE INTERFACES
    -----------------------------------
    -----------------------------------''')

    print(re.findall(r"(\w+): flags=", interfaces_decoded))


def Mac_Changer():
    usr_interface = options.interface or input("Interface> ")
    new_mac = options.new_mac or input("new MAC> ")

    for interface in available_interfaces:
        if usr_interface == interface:
            current_mac = subprocess.check_output(f"ifconfig {interface} | grep ether", shell=True)
            current_mac_decoded = current_mac.decode('utf-8')
            current_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", current_mac_decoded)

            if current_mac:
                print(f"[+] Current MAC address is {current_mac.group(0)}")
            else:
                print('[+]No Mac address Found')

            print(f"[+] Changing MAC address for {interface} to {new_mac}")
            subprocess.call(["ifconfig", interface, "down"])
            subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
            subprocess.call(["ifconfig", interface, "up"])
            new_changed_mac = subprocess.check_output(f"ifconfig {interface} | grep ether", shell=True)
            new_changed_mac_decoded = new_changed_mac.decode('utf-8')
            output = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", new_changed_mac_decoded)

            if output.group(0) == new_mac:
                print(f"[+] Success New MAC address {output.group(0)}")
            else:
                print(f"{new_mac} was not able to be assigned")

            break
    else:
        print('!!Interface Not Found!!')


Welcome()
Mac_Changer()
