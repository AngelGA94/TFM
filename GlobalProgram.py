import os
import requests
import time
import math
import os.path as path
import telnetlib
from requests.auth import HTTPBasicAuth
from classes import *
import xml.etree.cElementTree as etree
from lxml import etree as ET
from prettytable import PrettyTable
from conexion import Telnet, borrarSer
from RouterConf import routerConf
from selectONU import get_ID_ONU
from RouterConf import incluirServicio, borrarServicios
import threading


def MenuIni():
	print ("Welcome to the service management system.")
	print("1. Service configuration")
	print("2. Attach service to ONT")
	print("3. Detach service from ONT")
	print("4. OpenFlow configuration")
	print("5. ONT Router configuration")
	print("6. Exit")

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
	print("6. VLAN Priority")
	print("7. Modify!\n")

def MenuOpenFlow():
	print("You have chosen: OpenFlowConfig\n")
	print("1. Service configuration")
	print("2. Attach OpenFlow service to ONT")
	print("3. Detach OpenFlow service from ONT")
	print("4. Go back")

def serviceConf():

	while True:
		MenuService()
		option=input("Please, select what do you want to do: ")
		try:	
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
		except ValueError:
			os.system('clear')
			input("Please, introduce a valid option!")
			os.system('clear')

def attachService():
	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor(buffered=True)
	print("You have chosen: attach service to ONT\n")
	cursor.execute("select id_service from services")
	ids=cursor.fetchall()

	aux=False
	while not aux:
		Service.showServices()
		id_service=input("Select the ID of the service which you want to attach to the ONT: ")
		for k in ids:
			if int(id_service) in k:
				aux = True
				break
		if not aux:
			os.system('clear')
			input("Service not found.")
			os.system('clear')

	options=Service.getService(id_service)
	service = Service(options[1], options[3], options[2], options[4], options[5], options[6],options[7])
	MAC = get_ID_ONU()
	
	t = PrettyTable(['ID','ONT'])
	for i in MAC:
		cursor.execute("select id_ont from ont where id_ont='"+i+"'")
		if str(cursor.fetchone()) == "None":
			cursor.execute("insert into ont (id_ont) values ('"+i+"')")
		t.add_row([MAC.index(i), i])


	while True:
		print(t)
		id_onu=input("Select ID: ")
		if int(id_onu) in range(0,len(MAC)):
			break
		else:
			os.system('clear')
			input("ONU not found.")
			os.system('clear')
	#No dejo configurar servicios ya configurados
	cursor.execute("select id_ont from ont_service where id_service='"+id_service+"' and configuration = 'CLI'")
	ont_configs = cursor.fetchall()
	for k in ont_configs:
		if MAC[int(id_onu)] in k:
			os.system('clear')
			print("Service "+id_service+" is running in "+MAC[int(id_onu)])
			input("Press any key to continue...")
			os.system('clear')
			return

	cursor.execute("select count(id_ont) from ont_service where id_ont='"+MAC[int(id_onu)]+"' and configuration = 'CLI'")
	n_service=cursor.fetchone()
	cursor.execute("select VLAN from services where id_service='"+id_service+"'")
	VLAN=cursor.fetchone()
	if n_service[0]>0:
		if os.path.isfile("ServicioInternet_"+MAC[int(id_onu)]+".conf"):
			doc=ET.parse("ServicioInternet_"+MAC[int(id_onu)]+".conf")
		else:
			doc=ET.parse("Plantilla_"+MAC[int(id_onu)]+".conf")
		Multi=False
		if service.typeService == 'Video':
			Multi=True
		WANinst=incluirServicio(doc,VLAN[0],Multi)
		doc.write("ServicioInternet_"+MAC[int(id_onu)]+".conf",encoding="utf-8",xml_declaration=True,method='xml')
		s=Telnet(MAC[int(id_onu)])
		if s==0:
			input('ERROR: The ONT host is unreachable.')
			return
		time.sleep(90)

		cursor.execute("select id_service from services where id_service in (select id_service from ont_service where id_ont='"+MAC[int(id_onu)]+"' and configuration='CLI')")
		id_services=cursor.fetchall()

		for k in id_services:
			Service.borrar_configuracion(int(id_onu),MAC[int(id_onu)],str(k[0]))
		# time.sleep(30)
	else:
		doc=ET.parse("Plantilla_"+MAC[int(id_onu)]+".conf")
		Multi=False
		if service.typeService == 'Video':
			Multi=True
		WANinst=incluirServicio(doc,VLAN[0],Multi)
		doc.write("ServicioInternet_"+MAC[int(id_onu)]+".conf",encoding="utf-8",xml_declaration=True,method='xml')
	cursor.close()
	cnx.close()
	#if service.typeService =='Internet':
	service.servicio_Internet_Video(int(id_onu),MAC[int(id_onu)],id_service,n_service[0],WANinst)
	# elif service.typeService =='Video':
	# 	service.servicio_Video(int(id_onu),MAC[int(id_onu)],id_service,n_service[0])
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
	while True:
		print(t)
		id_onu=input("Select ID: ")
		if int(id_onu) in range(0,len(MAC)):
			break
		else:
			os.system('clear')
			input("ONU not found.")
			os.system('clear')
	cursor.execute("select id_service from ont_service where id_ont='"+MAC[int(id_onu)]+"' and configuration='CLI'")
	ids=cursor.fetchall()

	if not ids:
		os.system('clear')
		input("ONT "+MAC[int(id_onu)]+" hasn't any attached service")
		return

	aux=False
	while not aux:
		Service.showAttachedServices(MAC[int(id_onu)])
		id_service=input("Select the ID of the service which you want to detach from the ONT: ")
		for k in ids:
			if int(id_service) in k:
				aux = True
				break
		if not aux:
			os.system('clear')
			input("Service not found.")
			os.system('clear')
	# cursor.execute("select WANinstance from ont_service where id_service='"+id_service+"' and configuration='CLI'")
	# WANinstance=cursor.fetchone()
	# if os.path.isfile("ServicioInternet_"+MAC[int(id_onu)]+".conf"):
	# 	doc=ET.parse("ServicioInternet_"+MAC[int(id_onu)]+".conf")
	# else:
	# 	print("No existe servicio")
	# 	return
	# wan=borrarServicios(doc,str(WANinstance[0]))
	# if wan==0:
	# 	return
	# s=borrarSer(MAC[int(id_onu)],str(wan))
	# if s==0:
	# 	return
	# doc.write("ServicioInternet_"+MAC[int(id_onu)]+".conf",encoding="utf-8",xml_declaration=True,method='xml')
	WanUpdate(MAC[int(id_onu)], id_service)
	Service.borrar_configuracion(int(id_onu),MAC[int(id_onu)],id_service)
	cursor.execute("delete from ont_service where id_ont='"+MAC[int(id_onu)]+"' and id_service='"+id_service+"' and configuration = 'CLI'")

	# Finalmente se borra el fichero de configuración.
	# Una vez borrado, se muestra un mensaje informando al usuario.
	print("\nLa configuración de la ONU con MAC " + MAC[int(id_onu)] + " y el servicio "+id_service+" ha sido borrada.\n")
	input("Press enter to continue...")
	cnx.commit()
	cursor.close()
	cnx.close()

def createService():
	print("You have chosen: Create new service\n")

	while True:
		try:
			typeService = input("Type of service (Internet: 0, Video: 1): ")
			if int(typeService) not in range(0,2):
				raise ValueError()
			else:
				if typeService == 0:
					typeService="Internet"
				else:
					typeService="Video"
				break
		except ValueError:
			input('Error: select 0 (Internet) or 1 (Video)')
			os.system('clear')

	while True:
		try:
			VLAN = input("VLAN [0-4095]: ")
			if int(VLAN) not in range(0,4096):
				raise ValueError()
			else:
				break
		except ValueError:
			input('Error: select a number between 0 and 4095')
			os.system('clear')

	while True:
		try:
			VLANpriority = input("VLAN Priority [0-7]: ")
			if int(VLANpriority) not in range(0,8):
				raise ValueError()
			else:
				break
		except ValueError:
			input('Error: select a number between 0 and 8')
			os.system('clear')

	while True:
		try:
			downstream = input("Guaranteed downstream (Kbps) [0-2488000]: ")
			if int(downstream) not in range(0,2488001):
				raise ValueError()
			else:
				downstream = int(downstream)/64
				downstream = math.floor(downstream)*64
				break
		except ValueError:
			input('Error: select a number between 0 and 2488000')
			os.system('clear')

	while True:
		try:
			eDownstream = input("Excess downstream (Kbps) [0-2488000]: ")
			if int(eDownstream) not in range(0,2488001):
				raise ValueError()
			else:
				eDownstream = int(eDownstream)/64
				eDownstream = math.floor(eDownstream)*64
				break
		except ValueError:
			input('Error: select a number between 0 and 2488000')
			os.system('clear')

	while True:
		try:
			upstream = input("Guaranteed upstream (Mbps) [0-1244]: ")
			if int(upstream) not in range(0,1245):
				raise ValueError()
			else:
				break
		except ValueError:
			input('Error: select a number between 0 and 1244')
			os.system('clear')

	while True:
		try:
			eUpstream = input("Excess upstream (Mbps) [0-1244]: ")
			if int(eUpstream) not in range(0,1245):
				raise ValueError()
			else:
				break
		except ValueError:
			input('Error: select a number between 0 and 1244')
			os.system('clear')

	service = Service(downstream, upstream, eDownstream, eUpstream, VLAN, VLANpriority, typeService)
	print("\n")
	service.insertConfig()

def modifyService():
	print("You have chosen: Modify service\n")
	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor(buffered=True)
	cursor.execute("select id_service from services")
	ids=cursor.fetchall()

	aux=False
	while not aux:
		Service.showServices()
		id_service=input("Select the ID of the service which you want to attach to the ONT: ")
		for k in ids:
			if int(id_service) in k:
				aux = True
				break
		if not aux:
			os.system('clear')
			input("Service not found.")
			os.system('clear')

	options=Service.getService(id_service)
	service = Service(options[1], options[3], options[2], options[4], options[5], options[6], options[7])
	os.system('clear')
	while True:
		print("New configuration:\n")
		service.showConfig()
		MenuModify()
		try:
			option=input("Please, select what do you want to do: ")

			if int(option) == 1:
				os.system('clear')
				while True:
					try:
						downstream = input("Select a new guaranteed downstream (Kbps) [0-2488000]: ")
						if int(downstream) not in range(0,2488001):
							raise ValueError()
						else:
							downstream = int(downstream)/64
							service.gDownstream = math.floor(downstream)*64
							break
					except ValueError:
						input('Error: select a number between 0 and 2488000')
						os.system('clear')
				os.system('clear')
			elif int(option) == 2:
				os.system('clear')
				while True:
					try:
						eDownstream = input("Select a new excess downstream (Kbps) [0-2488000]: ")
						if int(eDownstream) not in range(0,2488001):
							raise ValueError()
						else:
							eDownstream = int(eDownstream)/64
							service.excessDownstream = math.floor(eDownstream)*64
							break
					except ValueError:
						input('Error: select a number between 0 and 2488000')
						os.system('clear')
				os.system('clear')
			elif int(option) == 3:
				os.system('clear')
				while True:
					try:
						service.gUpstream = input("Select a new guaranteed upstream (Mbps) [0-1244]: ")
						if int(service.gUpstream) not in range(0,1245):
							raise ValueError()
						else:
							break
					except ValueError:
						input('Error: select a number between 0 and 1244')
						os.system('clear')
				os.system('clear')
			elif int(option) == 4:
				os.system('clear')
				while True:
					try:
						service.excessUpstream = input("Select a new excess upstream (Mbps) [0-1244]: ")
						if int(service.excessUpstream) not in range(0,1245):
							raise ValueError()
						else:
							break
					except ValueError:
						input('Error: select a number between 0 and 1244')
						os.system('clear')
				os.system('clear')
			elif int(option) == 5:
				os.system('clear')
				while True:
					try:
						service.VLAN = input("Select a new VLAN [0-4095]: ")
						if int(service.VLAN) not in range(0,4096):
							raise ValueError()
						else:
							break
					except ValueError:
						input('Error: select a number between 0 and 4095')
						os.system('clear')
				os.system('clear')
			elif int(option) == 6:
				os.system('clear')
				while True:
					try:
						service.VLANpriority = input("Select a new VLAN Priority [0-7]: ")
						if int(service.VLANpriority) not in range(0,8):
							raise ValueError()
						else:
							break
					except ValueError:
						input('Error: select a number between 0 and 8')
						os.system('clear')
				os.system('clear')
			elif int(option) == 7:
				os.system('clear')
				input("The service was modified. Press enter to continue...")
				break
			else:
				os.system('clear')
				input("Please, introduce a valid option!")
				os.system('clear')
		except ValueError:
			os.system('clear')
			input("Please, introduce a valid option!")
			os.system('clear')

	service.updateConfig(id_service)
	MAC = get_ID_ONU()

	#Selecciono las onts de la base de datos que tienen configurado el servicio modificado
	cursor.execute("select id_ont from ont_service where id_service='"+id_service+"'")
	ont_ID=cursor.fetchall()
	if ont_ID: #Si hay onts con el servicio que se ha modificado activo:
		#Resetear de forma paralela todas las onts con el servicio modificado configurado
		threads = []
		for u in ont_ID:
			t = threading.Thread(target=Telnet, args=(u[0],))
			threads.append(t)
			t.start()
		time.sleep(90)
		for i in MAC: #Recorro las ONTs conectadas al OLT
			for k in ont_ID: #Recorro las ONTs con el servicio configurado
				if i == k[0]: #Actualiza valores del servicio si dicho servicio está siendo utilizado por una ONT
					#Telnet(i)#Reset de la ONT
					#time.sleep(90)
					WanUpdate(i,id_service)
					Service.borrar_configuracion(MAC.index(i),i,id_service) #Borra el servicio
					cursor.execute("delete from ont_service where id_ont='"+i+"' and id_service='"+id_service+"' and configuration = 'CLI'")
					cnx.commit()

					#Reconfigura el servicio con las nueva configuración, así como el resto de servicios de la ONT
					cursor.execute("select count(id_ont) from ont_service where id_ont='"+i+"' and configuration = 'CLI'")
					n_service=cursor.fetchone() #Numero de servicios en el ONT sin contar el modificado
					cursor.execute("select VLAN from services where id_service='"+id_service+"'") #Coge la VLAN del servicio modificado
					if n_service[0]>0:
						#Si hay más servicios a parte del modificado, borro su configuración
						cursor.execute("select id_service from services where id_service in (select id_service from ont_service where id_ont='"+i+"' and configuration='CLI')")
						id_services=cursor.fetchall()
						for j in id_services:
							Service.borrar_configuracion(int(id_onu),i,str(j[0]))
					service.servicio_Internet_Video(MAC.index(i),i,id_service,n_service[0]) #Lo reconfigura con nuevos parametros
	cursor.close()
	cnx.close()

def deleteService():
	print("You have chosen: Delete service\n")
	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor(buffered=True)
	cursor.execute("select id_service from services")
	ids=cursor.fetchall()
	aux=False
	while not aux:
		Service.showServices()
		id_service=input("Select the ID of the service which you want to delete: ")
		for k in ids:
			if int(id_service) in k:
				aux = True
				break
		if not aux:
			os.system('clear')
			input("Service not found.")
			os.system('clear')
	#Desacoplo el servicio a borrar de las ONT en las que esta configurado
	#Selecciono las onts de la base de datos que tienen configurado el servicio modificado
	cursor.execute("select id_ont from ont_service where id_service='"+id_service+"'")
	ont_ID=cursor.fetchall()
	if ont_ID: #Si hay onts con el servicio que se ha modificado activo:
		MAC = get_ID_ONU()
		for i in MAC: #Recorro las ONTs conectadas al OLT
			for j in ont_ID: #Recorro las ONTs con el servicio configurado
				if i == j[0]: #Actualiza valores del servicio si dicho servicio está siendo utilizado por una ONT
					WanUpdate(i,id_service)
					Service.borrar_configuracion(MAC.index(i),i,id_service) #Borra el servicio
					cursor.execute("delete from ont_service where id_ont='"+i+"' and id_service='"+id_service+"' and configuration = 'CLI'")
					cnx.commit()
	Service.deleteConfig(id_service)
	cursor.close()
	cnx.close()

def openFlowConfig():
	os.system("clear")

	while True:
		MenuOpenFlow()
		try:
			iniOption=input("What do you want to do?: ")

			if int(iniOption) == 1:
				os.system('clear')
				serviceConf()
				os.system('clear')
			elif int(iniOption) == 2:
				os.system('clear')
				attachOpenFlowService()
				os.system('clear')
			elif int(iniOption) == 3:
				os.system('clear')
				detachOpenFlowService()
				os.system('clear')
			elif int(iniOption) == 4:
				os.system('clear')
				return
			else:
				os.system('clear')
				input("Please, introduce a valid option!")
				os.system('clear')
		except ValueError:
			os.system('clear')
			input("Please, introduce a valid option!")

def attachOpenFlowService():
	print("You have chosen: attach OpenFlow service to ONT\n")

	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor()
	cursor.execute("select id_service from services")
	ids=cursor.fetchall()

	aux=False
	while not aux:
		Service.showServices()
		id_service=input("Select the ID of the service which you want to attach to the ONT: ")
		for k in ids:
			if int(id_service) in k:
				aux = True
				break
		if not aux:
			os.system('clear')
			input("Service not found.")
			os.system('clear')
	options=Service.getService(id_service)
	service = Service(options[1], options[3], options[2], options[4], options[5], options[6],options[7])
	MAC = get_ID_ONU()
	
	t = PrettyTable(['ID','ONT'])
	for i in MAC:
		cursor.execute("select id_ont from ont where id_ont='"+i+"'")
		if str(cursor.fetchone()) == "None":
			cursor.execute("insert into ont (id_ont) values ('"+i+"')")
		t.add_row([MAC.index(i), i])

	cnx.commit()
	cursor.close()
	cnx.close()

	while True:
		print(t)
		id_onu=input("Select ID: ")
		if int(id_onu) in range(0,len(MAC)):
			break
		else:
			os.system('clear')
			input("ONU not found.")
			os.system('clear')	
	service.servicio_Internet_OpenFlow(int(id_onu),MAC[int(id_onu)],id_service)

	input("Enter to continue...")

def detachOpenFlowService():
	print("You have chosen: detach OpenFlow service from ONT\n")
	MAC = get_ID_ONU()
	
	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor()
	t = PrettyTable(['ID','ONT'])
	for i in MAC:
		cursor.execute("select id_ont from ont where id_ont='"+i+"'")
		if str(cursor.fetchone()) == "None":
			cursor.execute("insert into ont (id_ont) values ('"+i+"')")
		t.add_row([MAC.index(i), i])
	while True:
		print(t)
		id_onu=input("Select ID: ")
		if int(id_onu) in range(0,len(MAC)):
			break
		else:
			os.system('clear')
			input("ONU not found.")
			os.system('clear')
	cursor.execute("select id_service from ont_service where id_ont='"+MAC[int(id_onu)]+"' and configuration='OpenFlow'")
	ids=cursor.fetchall()

	aux=False
	while not aux:
		Service.showAttachedOpenFlowServices(MAC[int(id_onu)])
		id_service=input("Select the ID of the service which you want to detach from the ONT: ")
		for k in ids:
			if int(id_service) in k:
				aux = True
				break
		if not aux:
			os.system('clear')
			input("Service not found.")
			os.system('clear')
	options=Service.getService(id_service)
	service = Service(options[1], options[3], options[2], options[4], options[5], options[6],options[7])
	service.borrar_configuracion_OpenFlow(int(id_onu),MAC[int(id_onu)],id_service)

	cursor.close()
	cnx.close()
def WanUpdate(i,id_service):
	cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
	cursor = cnx.cursor(buffered=True)
	cursor.execute("select WANinstance from ont_service where id_service='"+id_service+"' and configuration='CLI'")
	WANinstance=cursor.fetchone()
	if os.path.isfile("ServicioInternet_"+i+".conf"):
		doc=ET.parse("ServicioInternet_"+i+".conf")
	else:
		print("No existe servicio")
		return
	wan=borrarServicios(doc,str(WANinstance[0]))
	if wan==0:
		return
	s=borrarSer(i,str(wan))
	if s==0:
		return
	doc.write("ServicioInternet_"+i+".conf",encoding="utf-8",xml_declaration=True,method='xml')
	cursor.close()
	cnx.close()

def Main():

	os.system("clear")

	while True:
		MenuIni()
		try:
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
				openFlowConfig()
				os.system('clear')
			elif int(iniOption) == 5:
				routerConf()
				os.system('clear')
			elif int(iniOption) == 6:
				os.system('clear')
				quit("See you!")
			else:
				os.system('clear')
				input("Please, introduce a valid option!")
				os.system('clear')
		except ValueError:
			os.system('clear')
			input("Please, introduce a valid option!")
			os.system('clear')

if __name__ == '__main__':
	Main()



