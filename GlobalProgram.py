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

def MenuService():
	print("You have chosen: Service configuration\n")
	print("1. List of configured services")
	print("2. Create new service")
	print("3. Modify service")
	print("4. Delete service")
	print("5. Go back")

def MenuModify():
	print("What parameter do you want to modify?\n")
	print("1. Guaranteed downstream")
	print("2. Excess downstream")
	print("3. Guaranteed upstream")
	print("4. Excess upstream")
	print("5. VLAN")
	print("6. Modify!\n")

def serviceConf():

	while True:
		MenuService()
		option=input("Please, select what do you want to do: ")

		if int(option) == 1:
			os.system('clear')
			Service.showServices()
			input("Press enter to continue...")
			os.system('clear')
		elif int(option) == 2:
			os.system('clear')
			createService()
			os.system('clear')
		elif int(option) == 3:
			os.system('clear')
			modifyService()
			os.system('clear')
		elif int(option) == 4:
			os.system('clear')
			deleteService()
			os.system('clear')
		elif int(option) == 5:
			os.system('clear')
			return
		else:
			os.system('clear')
			input("Please, introduce a valid option!")
			os.system('clear')


def createService():
	print("You have chosen: Create new service\n")
	typeService = input("Type of service: ")
	VLAN = input("VLAN: ")
	downstream = input("Guaranteed downstream: ")
	eDownstream = input("Excess downstream: ")
	upstream = input("Guaranteed upstream: ")
	eUpstream = input("Excess upstream: ")
	service = Service(downstream, upstream, eDownstream, eUpstream, VLAN, typeService)
	print("\n")
	service.insertConfig()

def modifyService():
	print("You have chosen: Modify service\n")
	Service.showServices()
	id_service=input("Select the ID of the service which you want to modify: ")
	options=Service.getService(id_service)
	service = Service(options[1], options[3], options[2], options[4], options[5], options[6])
	os.system('clear')
	while True:
		print("New configuration:\n")
		service.showConfig()
		MenuModify()
		option=input("Please, select what do you want to do: ")

		if int(option) == 1:
			os.system('clear')
			service.gDownstream=input("Select new guaranteed downstream: ")
			os.system('clear')
		elif int(option) == 2:
			os.system('clear')
			service.excessDownstream=input("Select new excess downstream: ")
			os.system('clear')
		elif int(option) == 3:
			os.system('clear')
			service.gUpstream=input("Select new guaranteed upstream: ")
			os.system('clear')
		elif int(option) == 4:
			os.system('clear')
			service.excessUpstream=input("Select new excess upstream: ")
			os.system('clear')
		elif int(option) == 5:
			os.system('clear')
			service.VLAN=input("Select new VLAN: ")
			os.system('clear')
		elif int(option) == 6:
			os.system('clear')
			input("The service was modified. Press enter to continue...")
			break
		else:
			os.system('clear')
			input("Please, introduce a valid option!")
			os.system('clear')
	service.updateConfig(id_service)

def deleteService():
	print("You have chosen: Delete service\n")
	Service.showServices()
	id_service=input("Select the ID of the service which you want to delete: ")
	Service.deleteConfig(id_service)

def Main():

	os.system("clear")

	while True:
		MenuIni()
		iniOption=input("What do you want to do?: ")

		if int(iniOption) == 1:
			os.system('clear')
			serviceConf()
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

