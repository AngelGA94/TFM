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
	print("1. Create new service")
	print("2. Modify service")
	print("3. Delete service")
	print("4. Go back")

def serviceConf():

	while True:
		MenuService()
		option=input("Please, select what do you want to do: ")

		if int(option) == 1:
			os.system('clear')
			createService()
			os.system('clear')
		elif int(option) == 2:
			os.system('clear')
			input("opcion 2")
			os.system('clear')
		elif int(option) == 3:
			os.system('clear')
			deleteService()
			os.system('clear')
		elif int(option) == 4:
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
	servicio = Service(downstream, upstream, eDownstream, eUpstream, VLAN, typeService)
	print("\n")
	servicio.insertConfig()

def deleteService():
	print("You have chosen: Delete service\n")
	Service.showServices()
	id_service=input("Select the ID of the service which you want to delete: ")
	Service.deleteConfig(id_service)

def Main():

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

