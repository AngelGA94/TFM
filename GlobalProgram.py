import os
import requests
from requests.auth import HTTPBasicAuth
from classes import *

def MenuIni():
	print ("Welcome to the service management system.")
	print("1. Service configuration")
	print("2. Attach service to ONT")
	print("3. Detach service from ONT")
	print("4. Modify service attached to ONT")
	print("5. Exit")

def serviceConf():

	print("You have chosen: Service configuration\n")
	servicio = Service("30", "10", "5", "5", "833", "1", "internet")
	servicio.showConfig()
	
	url="http://192.168.56.101:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:346653127080/flow-node-inventory:table/"+servicio.idService
	head = {'Content-type':'application/yang.data+json','Accept':'application/json, text/plain'}
	payload='''{
    "table": [
        {
            "id": "1",
            "flow": [
                {
                    "id": "flow-up",
                    "match": {
                        "vlan-match": {
                            "vlan-id": {
                                "vlan-id-present": "false",
                                "vlan-id": "833"
                            }
                        },
                        "ipv4-source": "192.168.0.102/24"
                    },
                    "instructions": {
                        "instruction": [
                            {
                                "order": "1",
                                "apply-actions": {
                                    "action": [
                                        {
                                            "order": "0",
                                            "output-action": {
                                                "output-node-connector": "NORMAL",
                                                "max-length": "0"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "order": "0",
                                "meter": {
                                    "meter-id": "11"
                                }
                            }
                        ]
                    },
                    "flow-name": "flow-up",
                    "installHw": "false",
                    "barrier": "false",
                    "strict": "false",
                    "table_id": "1"
                },
                {
                    "id": "flow-down",
                    "match": {
                        "vlan-match": {
                            "vlan-id": {
                                "vlan-id-present": "false",
                                "vlan-id": "833"
                            }
                        },
                        "ipv4-destination": "192.168.0.102/24"
                    },
                    "instructions": {
                        "instruction": [
                            {
                                "order": "1",
                                "apply-actions": {
                                    "action": [
                                        {
                                            "order": "0",
                                            "output-action": {
                                                "output-node-connector": "NORMAL",
                                                "max-length": "0"
                                            }
                                        }
                                    ]
                                }
                            },
                            {
                                "order": "0",
                                "meter": {
                                    "meter-id": "12"
                                }
                            }
                        ]
                    },
                    "flow-name": "flow-down",
                    "installHw": "false",
                    "barrier": "false",
                    "strict": "false",
                    "table_id": "1"
                }
            ]
        }
    ]
}'''
	meterup='''{
    "meter": [
        {
            "flags": "meter-kbps",
            "meter-id": "11",
            "barrier": "true",
            "meter-name": "meterup",
            "container-name": "meterup",
            "meter-band-headers": {
                "meter-band-header": [
                    {
                        "band-id": "0",
                        "meter-band-types": {
                            "flags": "ofpmbt-drop"
                        },
                        "band-rate": "10000",
                        "band-burst-size": "0",
                        "drop-rate": "15000",
                        "drop-burst-size": "0"
                    }
                ]
            }
        }
    ]
}'''
	meterdown='''{
    "meter": [
        {
            "flags": "meter-kbps",
            "meter-id": "12",
            "barrier": "true",
            "meter-name": "meterdown",
            "container-name": "meterdown",
            "meter-band-headers": {
                "meter-band-header": [
                    {
                        "band-id": "0",
                        "meter-band-types": {
                            "flags": "ofpmbt-drop"
                        },
                        "band-rate": "30000",
                        "band-burst-size": "0",
                        "drop-rate": "35000",
                        "drop-burst-size": "0"
                    }
                ]
            }
        }
    ]
}'''
	ret = requests.put(url,auth=HTTPBasicAuth('admin', 'admin'),headers=head,data=payload)



def Main():

	while True:
		MenuIni()
		iniOption=input("What do you want to do?: ")

		if int(iniOption) == 1:
			os.system('clear')
			serviceConf()
			input("opcion 1")
			os.system('clear')
		elif int(iniOption) == 2:
			os.system('clear')
			input("opcion 2")
			os.system('clear')
		elif int(iniOption) == 3:
			os.system('clear')
			input("opcion 3")
			os.system('clear')
		elif int(iniOption) == 4:
			os.system('clear')
			input("opcion 4")
			os.system('clear')
		elif int(iniOption) == 5:
			os.system('clear')
			quit("See you!")
		else:
			os.system('clear')
			input("Please, introduce a valid option!")
			os.system('clear')

if __name__ == '__main__':
	Main()

