import os
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