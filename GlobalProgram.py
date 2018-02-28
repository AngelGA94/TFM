import os
import requests
import time
import math
import os.path as path
import telnetlib
from requests.auth import HTTPBasicAuth
from classes import *
import xml.etree.cElementTree as etree
from prettytable import PrettyTable

def get_ID_ONU():
    
    # Host y puerto al que se hace la conexión Telnet para acceder al CLI                    
    host = "172.26.128.38"
    port = "4551"
     
    # Claves de acceso al CLI
    password1 = "TLNT25"
    password2 = "TLNT145"
    enable = "enable"
    
    # Acceso al CLI: conexión Telnet al host y puerto indicados anteriormente
    tn = telnetlib.Telnet(host,port,1)
    # Mediante la función write de telnetlib, escritura de los comandos que permiten
    # acceder al menú de privilegios del CLI
    tn.write(password1.encode('ascii') + b"\n")      
    time.sleep(0.1)     
    tn.write(enable.encode('ascii') + b"\n")
    time.sleep(0.1)     
    tn.write(password2.encode('ascii') + b"\n")
    time.sleep(0.1) 
    
    # Declaración y escritura del comando que permite ver las ONUs conectadas a 
    # la red así como sus direcciones MAC
    comandos = "configure \n olt-device 0 \n olt-channel 0 \n show serial-number allocated \n"   
    tn.write(comandos.encode('ascii') + b"\n") 
    time.sleep(0.1)
    
    # Lectura de los datos (tanto enviados como recibidos) del CLI y volcado en 
    # un fichero de texto para su posterior análisis
    data = tn.read_very_eager().decode()
    # Se abre el fichero con modo de escritura, de esta forma cada vez que cambie
    # el estado de la red el fichero se sobreescribirá con la información nueva
    outfile = open('IDs_ONUs.txt', 'w')
    # Se escriben los datos procedentes de la escritura de los comandos de arriba
    outfile.write(data)
    # Ciere del fichero
    outfile.close()
    
    # Creación del vector que almacenará las direcciones MAC de las ONUs conectadas
    MAC = []
    # Se abre el archivo anterior en modo lectura
    outfile = open('IDs_ONUs.txt', 'r')
    # Se almacenan todas las lineas del fichero con la función readlines()
    lines = outfile.readlines()
    # Bucle que recorre cada línea del fichero
    for line in lines:
        # Se almacenan todas las palabras de cada línea
        palabras = line.split()
        # Bucle que recorre cada palabra de la línea
        for p in palabras:
            # Si los 18 primeros caracteres de una palabra coinciden con los indicados,
            # se trata de una direccion MAC -> Se ha detectado una ONU
            if p[:18]=='54-4c-52-49-5b-01-':
                # Se añade la MAC al vector. La posición en la que se añade indica
                # el identificador de la ONU.
                MAC.append(p)

#            FORMA DE BUSCAR ONUs ONU A ONU -> Menos eficiente y hay que añadir código
#            si se conecta alguna ONU más a la red 
#            if p=='54-4c-52-49-5b-01-f6-90':  
#                MAC[id_ONU] = '54-4c-52-49-5b-01-f6-90'
#                id_ONU = id_ONU + 1
#            if p=='54-4c-52-49-5b-01-f7-30':
#                MAC[id_ONU] = '54-4c-52-49-5b-01-f7-30'
#                id_ONU = id_ONU + 1
#            if p=='54-4c-52-49-5b-01-f6-d8':
#                MAC[id_ONU] = '54-4c-52-49-5b-01-f6-d8'
#                id_ONU = id_ONU + 1
#            if p=='54-4c-52-49-5b-01-f7-28':
#                MAC[id_ONU] = '54-4c-52-49-5b-01-f7-28'
#                id_ONU = id_ONU + 1
    
    # Cierre del archivo                          
    outfile.close()
    
    # Si existe un fichero con este nombre en el directorio de trabajo, sale de la función
    # devolviendo el vector de direcciones MAC
    if path.exists("configuracionGPON.xml"):
        return MAC
    
    # Si no existe, se ha de crear el fichero XML        
    else:
        # Se define el elemento raíz
        root = etree.Element("RedGPON") 
        
        # Se añaden las ONUs (el nº de ONUs es la longitud del vector de direcciones MAC)
        i=0
        while i<len(MAC):
            # Cada ONU se añade con su dirección MAC como un subelemento del elemento raíz
            ONU = etree.SubElement(root,"ONU", MAC=MAC[i])
            i=i+1

#            FORMA DE CREAR EL ÁRBOL ONU A ONU -> Menos eficiente y hay que añadir código
#            si se conecta alguna ONU más a la red 
#            ONU1 = etree.SubElement(root,"ONU", MAC='54-4c-52-49-5b-01-f6-90')               
#            ONU2 = etree.SubElement(root,"ONU", MAC='54-4c-52-49-5b-01-f7-30')
#            ONU3 = etree.SubElement(root,"ONU", MAC='54-4c-52-49-5b-01-f6-d8')
#            ONU4 = etree.SubElement(root,"ONU", MAC='54-4c-52-49-5b-01-f7-28')       
            
        # Se crea el árbol XML y se escribe en el fichero con el nombre indicado
        tree = etree.ElementTree(root)
        tree.write("configuracionGPON.xml")  
        # Se devuelve el vector de direcciones MAC
        return MAC

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

def attachService():
	print("You have chosen: attach service to ONT\n")
	Service.showServices()
	id_service=input("Select the ID of the service which you want to attach to the ONT: ")
	options=Service.getService(id_service)
	service = Service(options[1], options[3], options[2], options[4], options[5], options[6])
	MAC = get_ID_ONU()
	
	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor()
	t = PrettyTable(['ID','ONT'])
	for i in MAC:
		cursor.execute("select id_ont from ont where id_ont='"+i+"'")
		if str(cursor.fetchone()) == "None":
			cursor.execute("insert into ont (id_ont) values ('"+i+"')")
		t.add_row([MAC.index(i), i])
	cnx.commit()
	cursor.close()
	cnx.close()

	print(t)
	id_onu=input("Select ID: ")
	service.servicio_Internet(int(id_onu),MAC[int(id_onu)],id_service)
	input("Enter to continue...")

def detachService():
	print("You have chosen: detach service from ONT\n")
	MAC = get_ID_ONU()
	
	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor()
	t = PrettyTable(['ID','ONT'])
	for i in MAC:
		cursor.execute("select id_ont from ont where id_ont='"+i+"'")
		if str(cursor.fetchone()) == "None":
			cursor.execute("insert into ont (id_ont) values ('"+i+"')")
		t.add_row([MAC.index(i), i])
	cnx.commit()
	cursor.close()
	cnx.close()

	print(t)
	id_onu=input("Select ID: ")
	Service.showAttachedServices(MAC[int(id_onu)])
	Service.borrar_configuracion(int(id_onu),MAC[int(id_onu)])

def createService():
	print("You have chosen: Create new service\n")
	typeService = input("Type of service: ")
	VLAN = input("VLAN: ")
	downstream = input("Guaranteed downstream: ")
	downstream = int(downstream)/64
	downstream = math.floor(downstream)*64
	eDownstream = input("Excess downstream: ")
	eDownstream = int(eDownstream)/64
	eDownstream = math.floor(eDownstream)*64
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
			service.gDownstream=input("Select new guaranteed downstream (Kbps): ")
			service.gDownstream = int(service.gDownstream)/64
			service.gDownstream = math.floor(service.gDownstream)*64
			os.system('clear')
		elif int(option) == 2:
			os.system('clear')
			service.excessDownstream=input("Select new excess downstream (Kbps): ")
			service.excessDownstream = int(service.excessDownstream)/64
			service.excessDownstream = math.floor(service.excessDownstreamm)*64
			os.system('clear')
		elif int(option) == 3:
			os.system('clear')
			service.gUpstream=input("Select new guaranteed upstream (Mbps): ")
			os.system('clear')
		elif int(option) == 4:
			os.system('clear')
			service.excessUpstream=input("Select new excess upstream (Mbps): ")
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
			attachService()
			os.system('clear')
		elif int(iniOption) == 3:
			os.system('clear')
			detachService()
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



