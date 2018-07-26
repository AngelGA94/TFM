import mysql.connector
import telnetlib
import time
import requests
from requests.auth import HTTPBasicAuth
from prettytable import PrettyTable
import xml.etree.cElementTree as etree
import subprocess

class Service:

	#totDownstream = 0
	#totUpstream = 0
	#id_service=0

	def __init__(self, gDownstream, gUpstream, excessDownstream, excessUpstream, VLAN, VLANpriority, typeService):
		self.gDownstream=gDownstream
		self.gUpstream=gUpstream
		self.excessDownstream=excessDownstream
		self.excessUpstream=excessUpstream
		self.VLAN=VLAN
		self.VLANpriority=VLANpriority
		#self.idService=idService
		self.typeService=typeService

		#Service.totDownstream=Service.totDownstream+int(gDownstream)+int(excessDownstream)
		#Service.totUpstream=Service.totUpstream+int(gUpstream)+int(excessUpstream)

	def showConfig(self):
		t = PrettyTable(['Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'VLAN Priority', 'Type of service'])
		t.add_row([str(self.gDownstream)+" Kbps", str(self.excessDownstream)+" Kbps",str(self.gUpstream)+" Mbps",str(self.excessUpstream)+" Mbps",self.VLAN,self.VLANpriority,self.typeService])
		print(t)

	def insertConfig(self):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		# query="select sum(gDownstream) from services"
		# cursor.execute(query)
		# for i in cursor:
		# 	print(int(i)+2)
		# input()
		query="insert into services (gDownstream, excessDownstream, gUpstream, excessUpstream, VLAN, typeService, VLANpriority) values ('"+str(self.gDownstream)+"', '"+str(self.excessDownstream)+"', '"+str(self.gUpstream)+"', '"+str(self.excessUpstream)+"', '"+str(self.VLAN)+"', '"+self.typeService+"', '"+str(self.VLANpriority)+"')"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()

	def updateConfig(self,id_service):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="update services set gDownstream='"+str(self.gDownstream)+"', excessDownstream='"+str(self.excessDownstream)+"', gUpstream='"+str(self.gUpstream)+"', excessUpstream='"+str(self.excessUpstream)+"', VLAN='"+str(self.VLAN)+"', VLANpriority='"+str(self.VLANpriority)+"' where id_service='"+id_service+"'"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()		

	def showServices():
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services"
		cursor.execute(query)
		t = PrettyTable(['ID', 'Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'VLAN Priority', 'Type of service'])
		for (id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService,VLANpriority) in cursor:
			t.add_row([id_service, str(gDownstream)+" Kbps", str(excessDownstream)+" Kbps",str(gUpstream)+" Mbps",str(excessUpstream)+" Mbps",VLAN,VLANpriority,typeService])

		print(t)

		cursor.close()
		cnx.close()

	def deleteConfig(id_service):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="delete from services where id_service='"+id_service+"'"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()
		input("Ther service was deleted. Press enter to continue...")

	def getService(id_service):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services where id_service='"+id_service+"'"
		cursor.execute(query)
		for (id_service,gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService, VLANpriority) in cursor:
			options=[id_service,gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,VLANpriority,typeService]
		#service = Service(cursor.downstream, cursor.upstream, cursor.eDownstream, cursor.eUpstream, cursor.VLAN, cursor.typeService)
		cursor.close()
		cnx.close()
		return options
	def servicio_Internet_Video(self,ID_ONU,MAC_ONU,id_service,n_service,WANinstance):
			   
		# Creación de los vectores en los que se almacenarán los parámetros 
		# internos de configuración
		port_ID = []
		alloc_ID = [] 
		tcont_ID = []
		num_instancia = []
		puntero = []
		ds_profile_index = []

		# Creación de los vectores en los que se almacenarán los parámetros 
		# de configuracion que el USUARIO deberá introducir: identificador de VLAN,
		# ancho de banda Downstream garantizado y en exceso y ancho de banda Upstream
		# garantizado y Best Effort
		VLAN_ID = []
		VLAN_PRIORITY =[]
		BW_Downstream_GR = []
		BW_Downstream_Excess = []
		BW_Upstream_GR = []
		BW_Upstream_BE = []
		Type_Service= []


		#Aqui se guarda el log        
		nombre_fichero = 'Servicio_Internet_ONU_MAC_' + MAC_ONU + '.txt'
		outfile = open(nombre_fichero, 'a')

		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		# cursor.execute("select count(id_ont) from ont_service where id_ont='"+str(MAC_ONU)+"' and configuration = 'CLI'")
		# n_service=cursor.fetchone()
		# and typeService='Internet'??
		if n_service>0:
			cursor.execute("select gDownstream, excessDownstream, gUpstream, excessUpstream, VLAN, VLANpriority, typeService from services where id_service in (select id_service from ont_service where id_ont='"+MAC_ONU+"' and configuration='CLI')")
			old_service_data=cursor.fetchall()
			i=0
			while i<n_service:
				BW_Downstream_GR.append(str(int(old_service_data[i][0])))
				BW_Downstream_Excess.append(str(int(old_service_data[i][1])))
				BW_Upstream_GR.append(str(int(old_service_data[i][2])))
				BW_Upstream_BE.append(str(int(float(old_service_data[i][2])+float(old_service_data[i][3]))))
				VLAN_ID.append(str(old_service_data[i][4]))
				VLAN_PRIORITY.append(str(old_service_data[i][5]))
				Type_Service.append(old_service_data[i][6])
				i=i+1
		cursor.close()
		cnx.close()

		#Se añaden datos del nuevo servicio

		VLAN_ID.append(str(self.VLAN))
		VLAN_PRIORITY.append(str(self.VLANpriority))
		BW_Downstream_GR.append(str(int(self.gDownstream)))
		BW_Downstream_Excess.append(str(int(self.excessDownstream)))
		BW_Upstream_GR.append(str(int(self.gUpstream)))
		BW_Upstream_BE.append(str(int(float(self.gUpstream)+float(self.excessUpstream))))
		Type_Service.append(self.typeService)

		i=0

		print("Numero de servicios ya configurados: "+str(n_service))

		# if n_service[0] >= 1:
		# 	cursor.execute("select max(alloc_port), max(pointer), max(instance) from ont_service where id_ont='"+MAC_ONU+"' and configuration = 'CLI'")
		# 	alloc_pointer_instance=cursor.fetchone()

		# 	port_ID.append(alloc_pointer_instance[0]+1)
		# 	alloc_ID.append(alloc_pointer_instance[0]+1)
		# 	num_instancia.append(alloc_pointer_instance[2]+1)
		# 	tcont_ID.append(n_service[0])
		# 	puntero.append(alloc_pointer_instance[1]+1)
		# 	cursor.close()
		# 	cnx.close()
		while i<(n_service+1):
			# Para que no se solapen puertos y allocs-ID, se asignan en función del identficiador
			# de la ONU y del número de servicio en cuestión
			port_ID.append(600+100*ID_ONU+i)
			alloc_ID.append(600+100*ID_ONU+i) 
			# Estos valores se asignan de este modo también para evitar solapamientos
			num_instancia.append(i+3)
			tcont_ID.append(i)
			puntero.append(32768+i)
			i=i+1


		# En los sucesivos bucles, se irán pidiendo los parámetros de configuración al usuario.
			            
		# Primer bucle: se piden el identificador VLAN que corresponda a cada servicio
		# La VLAN 833 conecta con un servidor DHCP que asigna la dirección mientras que 
		# la VLAN 806 recibe una IP de forma estática (no la tiene que introducir el usuario)
		# Las etiquetas VLAN van de 1 a 4094. Si el usuario introduce un valor fuera de ese
		# rango, se le volverá a pedir que introduzca el valor. Hay que recordar que la red
		# solo ofrece servicio en las VLAN 833 y 806

		i=0
		while i<(n_service+1):
			
			print("El identificador VLAN para el servicio "+str(i+1)+" es:", VLAN_ID[i])                                                  
			print("\n")
			
			print("La prioridad VLAN para el servicio "+str(i+1)+" es:", VLAN_PRIORITY[i])                                                  
			print("\n")

			print("El ancho de banda Downstream garantizado en Kbps para el servicio "+str(i+1)+" es:", BW_Downstream_GR[i])
				   
			print("El ancho de banda Downstream en exceso en Kbps para el servicio "+str(i+1)+" es:", BW_Downstream_Excess[i])       
			print("\n")
			
			print("El ancho de banda Upstream garantizado en Mbps para el servicio "+str(i+1)+" es:", BW_Upstream_GR[i])                 
			print("\n")                                                            
			
			print("El ancho de banda Upstream BE en Mbps para el servicio "+str(i+1)+" es:", BW_Upstream_BE[i])
			print("\n")
			i=i+1
		i=0
			                
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
			    
		# A la hora de introducir variables en la declaración de cadenas, aunque sean números,
		# se deben introducir en forma de string. Por ello, aparece a lo largo del programa muchas
		# ocasiones la función str(), que convierte una variable en string
		ID_ONU = str(ID_ONU)
			    
		# A continuación, se definen todos los comandos necesarios para dar el servicio de Datos.
		# Posteriormente serán ejecutados en el CLI con la función write.
		# Primero se crea el canal OMCI de comunicación (con el mismo identificador que el de la ONU por convención)
		# Se resetean las entidades MIB que pudiera haber y se activa fec en uplink (pasos opcionales)
		inicio = "configure \n olt-device 0 \n olt-channel 0 \n onu-local " + ID_ONU + " \n omci-port  " + ID_ONU + "  \n exit \n onu-omci  " + ID_ONU + "  \n ont-data mib-reset \n exit \n fec direction uplink  " + ID_ONU + "  \n onu-local  " + ID_ONU + "  \n"              
		tn.write(inicio.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Se crean, dentro del menú de la ONU a configurar, tantos Alloc-ID como servicios
		i=0
		while i<(n_service+1):
			allocID = "alloc-id " + str(alloc_ID[i]).strip('[]') + " \n"
			tn.write(allocID.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1
			    
		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Cada Alloc-ID irá asociado a un puerto (por convención, se utiliza el mismo identificador)
		# Estos Alloc-IDs y puertos no se pueden utilizar para otras ONUs ni para otros servicios
		i=0
		while i<(n_service+1):
			portalloc = "port " + str(port_ID[i]).strip('[]') + " alloc-id  " + str(alloc_ID[i]).strip('[]') + " \n"
			tn.write(portalloc.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1
			   
		# Desde el menú de configuración del canal OMCI de comunicación, se crean las entidades
		# MIB que forman el servicio de Internet. Estas entidades vienen en el estándar GPON.    
		omci = "onu-omci " + ID_ONU + " \n"
		tn.write(omci.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Creación de las entidades T-Cont (colas). Cada servicio está asociado con un T-Cont 
		# y está vinculado a un Alloc-ID
		i=0
		while i<(n_service+1):
			tcont = "t-cont set slot-id 128 t-cont-id " + str(tcont_ID[i]).strip('[]') + " alloc-id " + str(alloc_ID[i]).strip('[]') + "  \n"
			tn.write(tcont.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# Creación de MAC Brigde Service Profile. Se asociará esta entidad con los MAC Bridge 
		# Port Configuration Data a través del bridge-group-id en los siguientes comandos.
		macservice = "mac-bridge-service-profile create slot-id 0 bridge-group-id 1 spanning-tree-ind true learning-ind true atm-port-bridging-ind true priority 32000 max-age 1536 hello-time 256 forward-delay 1024 unknown-mac-address-discard false mac-learning-depth 255 dynamic-filtering-ageing-time 1000 \n"
		# Creación del primer MAC Bridge Port Configuration Data. Irá asociado a la entidad 
		# extended-vlan-tagging-operation-config-data. Para ello, el tp-type (tipo del punto 
		# de terminación del MAC Bridge) ha de ser lan y el puntero tp-ptr debe tener el mismo 
		# valor que el nº de instancia de la entidad extended-vlan-tagging-operation-config-data.
		macbridge1 = "mac-bridge-pcd create instance 1 bridge-id-ptr 1 port-num 1 tp-type lan tp-ptr 257 port-priority 2 port-path-cost 32 port-spanning-tree-ind true encap-method llc lanfcs-ind forward \n"
		tn.write(macservice.encode('ascii') + b"\n")
		time.sleep(0.2)
		tn.write(macbridge1.encode('ascii') + b"\n")
		time.sleep(0.2)

		if "Video" in Type_Service:
			# Creación del segundo MAC Bridge Port Configuration Data. Esta entidad está 
			# vinculada al servicio multicast. Se asocia a la entidad Multicast GEM Interworking 
			# Termination Poing. Para ello, el tipo de puntero (tp-type) ha de ser de tipo multicast 
			# (mc-gem) y el tp-ptr ha de coincidir con el nº de instancia la entidad Multicast GEM
			# Interworking Termination Poing.
			macbridge2 = "mac-bridge-pcd create instance 2 bridge-id-ptr 1 port-num 2 tp-type mc-gem tp-ptr 2 port-priority 0 port-path-cost 1 port-spanning-tree-ind true encap-method llc lanfcs-ind forward  \n"
			tn.write(macbridge2.encode('ascii') + b"\n")
			time.sleep(0.2)
		# Creación de los restantes Mac Brigde Port Configuration Data. Irán asociado a la entidades 
		# VLAN-tagging-filter-data mediante los números de instancia. También irán asociados a los 
		# GEM Interworking Termination Point mediante el tp-type (tipo gem) y el tp-ptr, que
		# tiene que coincidir con el número de instancia del GEM Interworking Termination Point
		i=0
		while i<(n_service+1): 
			macbridge3 = "mac-bridge-pcd create instance " + str(num_instancia[i]).strip('[]') + " bridge-id-ptr 1 port-num " + str(num_instancia[i]).strip('[]') + " tp-type gem tp-ptr " + str(num_instancia[i]).strip('[]') + " port-priority 0 port-path-cost 1 port-spanning-tree-ind true encap-method llc lanfcs-ind forward  \n"
			tn.write(macbridge3.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		if "Video" in Type_Service:
			# Creación del GEM Port Network CTP vinculado al servicio multicast. Está asociado al puerto
			# 4094 (en el que va el servicio multicast). Se diferencia de la entidad que forma el servicio Ethernet
			# en que direction ya no es de tipo bidirectional sino de tipo ani-to-uni. Asimismo, esta entidad está
			# asociada a la entidad Multicast GEM Interworking Termination Point: el nº de instancia debe coincidir con
			# el campo gem-port-nwk-ctp-conn-ptr de la otra entidad.
			gemport_multicast = "gem-port-network-ctp create instance 2 port-id 4094 t-cont-ptr 0 direction ani-to-uni traffic-mgnt-ptr-ustream 0 traffic-descriptor-profile-ptr 0 priority-queue-ptr-downstream 0 traffic-descriptor-profile-ds-ptr 0 enc-key-ring 0  \n"
			tn.write(gemport_multicast.encode('ascii') + b"\n")
			time.sleep(0.2)
			    
		# Creación de los GEM Port Network CTP, que irán asociado a los puertos especificados 
		# anteriormente. Los identificadores tienen que coincidir con el gem-port-nwk-ct-conn-ptr 
		# de los GEM Interworking Termination Point.
		i=0
		while i<(n_service+1):
			gemport = "gem-port-network-ctp create instance " + str(num_instancia[i]).strip('[]') + " port-id  " + str(port_ID[i]).strip('[]') + "  t-cont-ptr " + str(puntero[i]).strip('[]') + " direction bidirectional traffic-mgnt-ptr-ustream 0 traffic-descriptor-profile-ptr 0 priority-queue-ptr-downstream 0 traffic-descriptor-profile-ds-ptr 0 enc-key-ring 0 \n"
			tn.write(gemport.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		if "Video" in Type_Service:
			# Creación del Multicast GEM Interworking Termination Point (en este punto, se produce la 
			# transformación de flujo de bytes a tramas GEM y viceversa). Esta entidad está vinculada al
			# servicio multicast. Se vincula al GEM Port Netwok CTP de tipo multicast mediante el campo
			# gem-port-nwk-ctp-conn-ptr. También se asocia con el MAC Bridge Port Configuration Data de
			# tipo multicast. Para ello, hay que seleccionar como interwork-option mac-bridge y el campo 
			# service-profile-ptr debe tener el valor que se indica en la declaración del comando. 
			# El número de instancia debe ser el mismo que el tp-ptr del MAC Bridge Point Configuration Data asociado.
			multicast_geminterworking = "multicast-gem-interworking-termination-point create instance 2 gem-port-nwk-ctp-conn-ptr 2 interwork-option mac-bridge service-prof-ptr 65535 interwork-tp-ptr 0 gal-prof-ptr 65535 gal-lpbk-config 0 \n"
			tn.write(multicast_geminterworking.encode('ascii') + b"\n")
			time.sleep(0.2)

		# Creación de los GEM Interworking Termination Point (en este punto, se produce la 
		# transformación de flujo de bytes a tramas GEM y viceversa). Estas entidades se vinculan 
		# a los GEM Port Network CTP a través del campo gem-port-nwk-ctp-conn-ptr, que debe coincidir 
		# con el número de instancia que  utilizado en el GEM Port Network CTP. Estas entidades también 
		# se asocian con los MAC Bridge Port Configuration. Para ello, hay que seleccionar como 
		# interwork-option mac-bridge-lan y el campo service-profile-ptr debe ser un 1. 
		# El número de instancia debe ser el mismo que el tp-ptr del MAC Bridge Point Configuration Data.     
		i=0
		while i<(n_service+1):
			geminterworking = "gem-interworking-termination-point create instance " + str(num_instancia[i]).strip('[]') + " gem-port-nwk-ctp-conn-ptr " + str(num_instancia[i]).strip('[]') + " interwork-option mac-bridge-lan service-profile-ptr 1 interwork-tp-ptr 0 gal-profile-ptr 0 \n"
			tn.write(geminterworking.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# Creación de los VLAN Tagging Filter Data con los identficadores VLAN definidos arriba. 
		# Los números de instancia deben coincidir con los de los MAC Bridge Port Configuration Data asociados.
		i=0
		while i<(n_service+1):
			vlantagging = "vlan-tagging-filter-data create instance " + str(num_instancia[i]).strip('[]') + "  forward-operation h-vid-a vlan-tag1 " + str(VLAN_ID[i]).strip('[]') + " vlan-priority1 " + str(VLAN_PRIORITY[i]).strip('[]')+ " vlan-tag2 null vlan-priority2 null vlan-tag3 null vlan-priority3 null vlan-tag4 null vlan-priority4 null vlan-tag5 null vlan-priority5 null vlan-tag6 null vlan-priority6 null vlan-tag7 null vlan-priority7 null vlan-tag8 null vlan-priority8 null vlan-tag9 null vlan-priority9 null vlan-tag10 null vlan-priority10 null vlan-tag11 null vlan-priority11 null vlan-tag12 null vlan-priority12 null \n"
			tn.write(vlantagging.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# Creación de la entidad Extended VLAN Tagging Operation Config Data, que será configurada en el paso posterior. 
		# Sirve para gestionar los identificadores VLAN. Esta entidad está asociada al primer MAC Bridge Port Configuration Data 
		# a través del número de instancia, que coincide con el tp-ptr del MAC Bridge Port Configuration Data.
		extendedvlan = "extended-vlan-tagging-operation-config-data create instance 257 association-type pptp-eth-uni associated-me-ptr 257 \n"
		tn.write(extendedvlan.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Configuración de la entidadExtended VLAN Tagging Operation Config Data. Se debe configurar
		# para cada identificador VLAN.
		i=0
		while i<(n_service+1):
			extendedvlanconf = "extended-vlan-tagging-operation-config-data set instance 257 operations-entry filter-outer-prio filter-prio-no-tag filter-outer-vid none filter-outer-tpid none filter-inner-prio filter-prio-none filter-inner-vid " + str(VLAN_ID[i]).strip('[]') + " filter-inner-tpid none filter-ethertype none treatment-tag-to-remove 1 treatment-outer-prio none treatment-outer-vid copy-from-inner treatment-outer-tpid tpid-de-copy-from-outer treatment-inner-prio 0 treatment-inner-vid " + str(VLAN_ID[i]).strip('[]') + " treatment-inner-tpid tpid-de-copy-from-inner\n"
			tn.write(extendedvlanconf.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Configuración de las reglas VLAN en la OLT asociadas a los puertos definidos al principio de la función
		i=0
		while i<(n_service+1):
			reglasvlan = "vlan uplink configuration port-id " + str(port_ID[i]).strip('[]') + " min-cos 0 max-cos 7 de-bit disable primary-tag-handling false \n vlan uplink handling port-id  " + str(port_ID[i]).strip('[]') + "  primary-vlan none destination datapath c-vlan-handling no-change s-vlan-handling no-change new-c-vlan 0 new-s-vlan 0 \n"
			tn.write(reglasvlan.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1
			    
		# Creación de los perfiles de ancho de banda en sentido Downstream con los parámetros 
		# definidos por el usuario anteriormente.
		i=0
		while i<(n_service+1):
			perfildownstreamconf = "policing downstream profile committed-max-bw " + str(BW_Downstream_GR[i]).strip('[]') + " committed-burst-size 1023 excess-max-bw " + str(BW_Downstream_Excess[i]).strip('[]') + " excess-burst-size 1023 \n"
			tn.write(perfildownstreamconf.encode('ascii') + b"\n")
			time.sleep(0.2)
				    
			#Se extrae el ds_profile_index proporcionado por el OLT
			while True:
				line = tn.read_until(b"\n").decode("utf-8")  # Read one line
				outfile.write(line)
				if 'downstream_profile_index' in line:  # last line, no more read
					ds_profile_index.append(line[26:])
					#ds_profile_index.append()
					break
			i=i+1
		i=0	       
		# Asignación de los perfiles de ancho de banda Downstream a los puertos correspondientes
		# mediante los índices de perfil buscados anteriormente.
		while i<(n_service+1):
			perfildownstreamassign = "policing downstream port-configuration entity port-id " + str(port_ID[i]).strip('[]') + " ds-profile-index " + str(ds_profile_index[i]).strip('[]') + " \n"    
			tn.write(perfildownstreamassign.encode('ascii') + b"\n")    
			time.sleep(0.2)
			i=i+1

		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Desde el menú de configuración del algoritmo DBA, se definirián los perfiles de
		# ancho de banda en sentido Upstream
		dba = "pon \n dba pythagoras 0 \n "
		tn.write(dba.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Cada perfil upstream irá asociado a un Alloc-ID y estará configurado con los
		# parámetros que haya definido el usuario.
		i=0
		while i<(n_service+1):
			perfilupstream = "sla " + str(alloc_ID[i]).strip('[]') + " service data status-report nsr gr-bw " + str(BW_Upstream_GR[i]).strip('[]') + " gr-fine 0 be-bw " + str(BW_Upstream_BE[i]).strip('[]') + " be-fine 0 \n"     
			tn.write(perfilupstream.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# El comando end hace salir directamente al modo privilegiado en la estructura
		# de menús del CLI
		final = "end \n"
		tn.write(final.encode('ascii') + b"\n")
		time.sleep(0.2)         
			    
		# Se vuelcan todos los datos en el fichero definido anteriormente (la opción 'a'
		# hace que los datos se añadan al final del fichero) de forma que el fichero recogerá
		# toda la configuración del servicio de Internet
		data = tn.read_very_eager().decode() 
		outfile.write(data)
		outfile.write("\n\n\n")
		outfile.close()
			    
		# Una vez configurado el servicio, se muestra un mensaje al usuario            
		print("Servicio de Internet configurado. \n")


		#Meto en la bse de datos la configuracion
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="insert into ont_service (id_ont, id_service, alloc_port, pointer, profile, instance, WANinstance, configuration) values ('"+str(MAC_ONU)+"', '"+str(id_service)+"', '"+str(port_ID[n_service])+"', '"+str(puntero[n_service])+"', '"+str(ds_profile_index[n_service])+"','"+str(num_instancia[n_service])+"','"+str(WANinstance)+"', 'CLI')"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()
			                                
		return

	def borrar_configuracion(ID_ONU,MAC_ONU,id_service):

		 # Host y puerto al que se hace la conexión Telnet para acceder al CLI                    
		host = "172.26.128.38"
		port = "4551"
     
		# Claves de acceso al CLI
		password1 = "TLNT25"
		password2 = "TLNT145"
		enable = "enable"

		ID_ONU = str(ID_ONU)
    
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
    
		# En este bucle, se buscarán los puertos configurados y se borrarán los perfiles
		# de anchos de banda asociados a estos puertos. Posteriormente, se borrarán las entidades
		# que forman los servicios.
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor(buffered=True)
		cursor.execute("select alloc_port, profile, instance from ont_service where id_ont='"+MAC_ONU+"' and id_service='"+id_service+"' and configuration='CLI'")
		port_ID=cursor.fetchone()
		cursor.execute("select typeService from services where id_service='"+id_service+"'")
		typeService=cursor.fetchone()

		inicio = "configure \n olt-device 0 \n olt-channel 0 \n"                
		tn.write(inicio.encode('ascii') + b"\n")
		time.sleep(0.2)

		#Borra asociacion profile-port
		delprofileport = "no policing downstream port-configuration entity port-id " + str(port_ID[0]) + " \n"
		tn.write(delprofileport.encode('ascii') + b"\n")
		time.sleep(0.2)

		#Borra port 
		portalloc = "no port " + str(port_ID[0]) + " \n"
		tn.write(portalloc.encode('ascii') + b"\n")
		time.sleep(0.2)

		#Borro GEM Ports

		omci = "onu-omci " + ID_ONU + " \n"
		tn.write(omci.encode('ascii') + b"\n")
		time.sleep(0.2)

		gemport = "gem-port-network-ctp delete instance " + str(port_ID[2]) + " \n"
		tn.write(gemport.encode('ascii') + b"\n")
		time.sleep(0.2)

		geminterworking = "gem-interworking-termination-point delete instance " + str(port_ID[2]) + " \n"
		tn.write(geminterworking.encode('ascii') + b"\n")
		time.sleep(0.2)

		if typeService[0] == "Video":
			gemportVideo = "gem-port-network-ctp delete instance 2 \n"
			tn.write(gemportVideo.encode('ascii') + b"\n")
			time.sleep(0.2)

			multicast = "multicast-gem-interworking-termination-point delete instance 2 \n"
			tn.write(multicast.encode('ascii') + b"\n")
			time.sleep(0.2)
		#Borro VLAN tagging filter data y extended VLAN

		vlantagging = "vlan-tagging-filter-data delete instance " + str(port_ID[2]) + " \n"
		tn.write(vlantagging.encode('ascii') + b"\n")
		time.sleep(0.2)

		extendedvlan = "extended-vlan-tagging-operation-config-data delete instance 257 \n exit \n"
		tn.write(extendedvlan.encode('ascii') + b"\n")
		time.sleep(0.2)


		#Borra profile
		delprofile = "no policing downstream profile ds-profile-index " + str(port_ID[1]) + " \n"
		tn.write(delprofile.encode('ascii') + b"\n")
		time.sleep(0.2)

		#Del alloc-id de la ONT
		delAllocID = "onu-local "+str(ID_ONU)+" \n no alloc-id "+str(port_ID[0])+" \n end \n"
		tn.write(delAllocID.encode('ascii') + b"\n")
		time.sleep(0.2)
		
		# Tras borrar los perfiles de ancho de banda, se borrar las entidades MIB presentes en 
		# el canal OMCI asociado a la ONU.
		# borrar_MIB = "configure \n olt-device 0 \n olt-channel 0 \n onu-local " + ID_ONU + " \n omci-port  " + ID_ONU + "  \n exit \n onu-omci  " + ID_ONU + " \n ont-data mib-reset \n exit \n end \n"
		# tn.write(borrar_MIB.encode('ascii') + b"\n")
		# time.sleep(2)

		data = tn.read_very_eager().decode() 
		outfile = open("borrado.txt", 'a')
		outfile.write(data)
		outfile.write("\n\n\n")
		outfile.close()
    
		return

	def showAttachedServices(MAC_ONU):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services where id_service in (select id_service from ont_service where id_ont='"+MAC_ONU+"' and configuration='CLI')"
		cursor.execute(query)
		t = PrettyTable(['ONT', 'ID', 'Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'VLAN Priority','Type of service'])
		#print(cursor.fetchall())
		for (id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService, VLANpriority) in cursor:
			t.add_row([MAC_ONU, id_service, str(gDownstream)+" Kbps", str(excessDownstream)+" Kbps",str(gUpstream)+" Mbps",str(excessUpstream)+" Mbps",VLAN,VLANpriority,typeService])

		print(t)

		cursor.close()
		cnx.close()

	def showAttachedOpenFlowServices(MAC_ONU):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services where id_service in (select id_service from ont_service where id_ont='"+MAC_ONU+"' and configuration='OpenFlow')"
		cursor.execute(query)
		t = PrettyTable(['ONT', 'ID', 'Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'VLAN Priority','Type of service'])
		#print(cursor.fetchall())
		for (id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService, VLANpriority) in cursor:
			t.add_row([MAC_ONU, id_service, str(gDownstream)+" Kbps", str(excessDownstream)+" Kbps",str(gUpstream)+" Mbps",str(excessUpstream)+" Mbps",VLAN,VLANpriority,typeService])

		print(t)

		cursor.close()
		cnx.close()


	def showAllAttachedServices():
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services where id_service in (select id_service from ont_service) and configuration = 'CLI'"
		cursor.execute(query)
		t = PrettyTable(['ONT', 'ID', 'Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'VLAN Priority', 'Type of service'])
		#print(cursor.fetchall())
		for (id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService) in cursor:
			t.add_row([MAC_ONU, id_service, str(gDownstream)+" Kbps", str(excessDownstream)+" Kbps",str(gUpstream)+" Mbps",str(excessUpstream)+" Mbps",VLAN,VLANpriority,typeService])

		print(t)

		cursor.close()
		cnx.close()
	def modifyAttachedService(self, ID_ONU, MAC_ONU, id_service):

		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select alloc_port, profile from ont_service where id_ont='"+str(MAC_ONU)+"' and id_service='"+str(id_service)+"'"
		cursor.execute(query)
		param=cursor.fetchone()
		host = "172.26.128.38"
		port = "4551"
     
		# Claves de acceso al CLI
		password1 = "TLNT25"
		password2 = "TLNT145"
		enable = "enable"

		ID_ONU = str(ID_ONU)
    
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

		inicio = "configure \n olt-device 0 \n olt-channel 0 \n"
		tn.write(inicio.encode('ascii') + b"\n")
		time.sleep(0.2)

		#Borra asociacion profile-port
		delprofileport = "no policing downstream port-configuration entity port-id " + str(param[0]) + " \n"
		tn.write(delprofileport.encode('ascii') + b"\n")
		time.sleep(0.2)
		#Borra profile
		delprofile = "no policing downstream profile ds-profile-index " + str(param[1]) + " \n"
		tn.write(delprofile.encode('ascii') + b"\n")
		time.sleep(0.2)
		# Creación de los perfiles de ancho de banda en sentido Downstream con los parámetros 
		# definidos por el usuario anteriormente.
		perfildownstreamconf = "policing downstream profile committed-max-bw " + str(int(self.gDownstream)) + " committed-burst-size 1023 excess-max-bw " + str(int(self.excessDownstream)) + " excess-burst-size 1023 \n"
		tn.write(perfildownstreamconf.encode('ascii') + b"\n")
		time.sleep(0.2)
		# Asignación de los perfiles de ancho de banda Downstream a los puertos correspondientes
		# mediante los índices de perfil buscados anteriormente.
		perfildownstreamassign = "policing downstream port-configuration entity port-id " + str(param[0]) + " ds-profile-index " + str(param[1]) + " \n"    
		tn.write(perfildownstreamassign.encode('ascii') + b"\n")
		time.sleep(0.2)
		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Desde el menú de configuración del algoritmo DBA, se definirián los perfiles de
		# ancho de banda en sentido Upstream
		dba = "pon \n dba pythagoras 0 \n "
		tn.write(dba.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Cada perfil upstream irá asociado a un Alloc-ID y estará configurado con los
		# parámetros que haya definido el usuario.
		perfilupstream = "sla " + str(param[0]) + " service data status-report nsr gr-bw " + str(int(self.gUpstream)) + " gr-fine 0 be-bw " + str(int(self.gUpstream)+int(self.excessUpstream)) + " be-fine 0 \n"     
		tn.write(perfilupstream.encode('ascii') + b"\n")
		time.sleep(0.2)

		# El comando end hace salir directamente al modo privilegiado en la estructura
		# de menús del CLI
		final = "end \n"
		tn.write(final.encode('ascii') + b"\n")
		time.sleep(0.2)         
			    
		# Se vuelcan todos los datos en el fichero definido anteriormente (la opción 'a'
		# hace que los datos se añadan al final del fichero) de forma que el fichero recogerá
		# toda la configuración del servicio de Internet
		data = tn.read_very_eager().decode() 
		outfile = open("log_mod.txt", 'a')
		outfile.write(data)
		outfile.write("\n\n\n")
		outfile.close()
	def servicio_Internet_OpenFlow(self,ID_ONU,MAC_ONU,id_service):
			   
		#Tengo que configurar un upstream y un downstream OpenFlow
		#Donstream -> OVS en ordenador
		#Upstream -> OVS en ONT
		#Un flow OpenFlow en cada OVS por servicio dentro de la tabla 0.
		#Ejemplo: configurar en la ONT 1 un servicio de internet de 20 Mbps simétricos sin exceso
		#Primero envío al controlador el meter del downstream y del upstream. Cada meter va a un OVS diferente. ->Datos de Upstream y Downstream
		#Configuro un flow con id "flow{id_Service}" con una prioridad alta en cada ovs
		#Mirar encoders JSON para construir mejor el programa
		if MAC_ONU == "54-4c-52-49-5b-01-f6-90":
			ovs_upstream="" #Id del OVS para el upstream en los servicios del ONT f6-90
			mac_upstream=""
			mac_downstream=""
		elif MAC_ONU == "54-4c-52-49-5b-01-f7-30":
			ovs_upstream="346653127080" #Id del OVS para el upstream en los servicios del ONT f7-30
			mac_upstream="78:3d:5b:01:f7:30"
			ipQuery="192.168.0.104" #Distincion video/internet
		elif MAC_ONU == "54-4c-52-49-5b-01-f6-d8":
			ovs_upstream="346653124572" #Id del OVS para el upstream en los servicios del ONT f6-d8
			mac_upstream="78:3d:5b:01:f6:d8"
			mac_downstream="78:3d:5b:01:f6:dc"
		elif MAC_ONU == "54-4c-52-49-5b-01-f7-28":
			ovs_upstream="" #Id del OVS para el upstream en los servicios del ONT f7-28
			mac_upstream=""
			mac_downstream=""

		proc = subprocess.Popen('arp -a',stdout=subprocess.PIPE,shell=True)
		(out, err) = proc.communicate()
		out=out.decode()
		
		posicion=out.find(ipQuery)
		mac_downstream=out[(posicion+18):(posicion+35)]

		head = {'Content-type':'application/yang.data+json','Accept':'application/json, text/plain'}

		urlDownstream="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:159303472399026/flow-node-inventory:table/0/flow/flow"+str(40+int(id_service))
		urlUpstream="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ovs_upstream+"/flow-node-inventory:table/0/flow/flow"+str(40+int(id_service))
		urlMeterDown="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:159303472399026/flow-node-inventory:meter/"+str(int(int(self.gDownstream)/1024))
		urlMeterUp="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ovs_upstream+"/flow-node-inventory:meter/"+str(int(self.gUpstream))

		flowDown='''{
					    "flow": [
					        {
					            "id": "flow'''+str(40+int(id_service))+'''",
					            "match": {
					                "ethernet-match": {
					                    "ethernet-destination": {
					                        "address": "'''+mac_downstream+'''"
					                    }
					                },
					                "vlan-match": {
					                    "vlan-id": {
					                        "vlan-id-present": "false"
					                    }
					                }
					            },
					            "instructions": {
					                "instruction": [
					                    {
					                        "order": 5,
					                        "meter": {
					                            "meter-id": '''+str(int(int(self.gDownstream)/1024))+'''
					                        }
					                    },
					                    {
					                        "order": "1",
					                        "apply-actions": {
					                            "action": [
					                                {
					                                    "order": "1",
					                                    "output-action": {
					                                        "output-node-connector": "NORMAL"
					                                    }
					                                }
					                            ]
					                        }
					                    }
					                ]
					            },
					            "flow-name": "flow'''+str(40+int(id_service))+'''",
					            "priority": "8000",
					            "idle-timeout": "0",
					            "hard-timeout": "0",
					            "cookie": "478478457845784600",
					            "table_id": "0"
					        }
					    ]
					}'''
		meterDown='''{
					    "meter": [
					        {
					            "flags": "meter-kbps",
					            "meter-id": "'''+str(int(int(self.gDownstream)/1024))+'''",
					            "meter-name": "mymeter",
					            "container-name": "mymeter",
					            "meter-band-headers": {
					                "meter-band-header": [
					                    {
					                        "band-id": "0",
					                        "meter-band-types": {
					                            "flags": "ofpmbt-drop"
					                        },
					                        "band-rate": "'''+str(int(self.gDownstream))+'''",
					                        "band-burst-size": "0",
					                        "drop-rate": "'''+str(int(self.gDownstream))+'''",
					                        "drop-burst-size": "0"
					                    }
					                ]
					            }
					        }
					    ]
					}'''
		flowUp='''{
					    "flow": [
					        {
					            "id": "flow'''+str(40+int(id_service))+'''",
					            "match": {
					                "ethernet-match": {
					                    "ethernet-destination": {
					                        "address": "'''+mac_upstream+'''"
					                    }
					                }
					            },
					            "instructions": {
					                "instruction": [
					                    {
					                        "order": 5,
					                        "meter": {
					                            "meter-id": '''+str(int(self.gUpstream))+'''
					                        }
					                    },
					                    {
					                        "order": "1",
					                        "apply-actions": {
					                            "action": [
					                                {
					                                    "order": "1",
					                                    "output-action": {
					                                        "output-node-connector": "NORMAL"
					                                    }
					                                }
					                            ]
					                        }
					                    }
					                ]
					            },
					            "flow-name": "flow'''+str(40+int(id_service))+'''",
					            "priority": "8000",
					            "idle-timeout": "0",
					            "hard-timeout": "0",
					            "cookie": "478478457845784600",
					            "table_id": "0"
					        }
					    ]
					}'''
		meterUp='''{
					    "meter": [
					        {
					            "flags": "meter-kbps",
					            "meter-id": "'''+str(int(self.gUpstream))+'''",
					            "meter-name": "mymeter",
					            "container-name": "mymeter",
					            "meter-band-headers": {
					                "meter-band-header": [
					                    {
					                        "band-id": "0",
					                        "meter-band-types": {
					                            "flags": "ofpmbt-drop"
					                        },
					                        "band-rate": "'''+str(int(self.gUpstream)*1024)+'''",
					                        "band-burst-size": "0",
					                        "drop-rate": "'''+str(int(self.gUpstream)*1024)+'''",
					                        "drop-burst-size": "0"
					                    }
					                ]
					            }
					        }
					    ]
					}'''
		requests.put(urlMeterDown,auth=HTTPBasicAuth('admin', 'admin'),headers=head,data=meterDown)
		requests.put(urlDownstream,auth=HTTPBasicAuth('admin', 'admin'),headers=head,data=flowDown)
		requests.put(urlMeterUp,auth=HTTPBasicAuth('admin', 'admin'),headers=head,data=meterUp)
		requests.put(urlUpstream,auth=HTTPBasicAuth('admin', 'admin'),headers=head,data=flowUp)

		#Meto en la bse de datos la configuracion
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		cursor.execute("insert into ont_service (id_ont, id_service, configuration) values ('"+str(MAC_ONU)+"', '"+str(id_service)+"', 'OpenFlow')")
		cnx.commit()
		cursor.close()
		cnx.close()
		print("Servicio de Internet configurado. \n")

	def borrar_configuracion_OpenFlow(self,ID_ONU,MAC_ONU,id_service):
		if MAC_ONU == "54-4c-52-49-5b-01-f6-90":
			ovs_upstream="" #Id del OVS para el upstream en los servicios del ONT f6-90
			mac_upstream=""
			mac_downstream=""
		elif MAC_ONU == "54-4c-52-49-5b-01-f7-30":
			ovs_upstream="346653127080" #Id del OVS para el upstream en los servicios del ONT f7-30
			mac_upstream="78:3d:5b:01:f7:30"
			mac_downstream="78:3d:5b:01:f7:34"
		elif MAC_ONU == "54-4c-52-49-5b-01-f6-d8":
			ovs_upstream="" #Id del OVS para el upstream en los servicios del ONT f6-d8
			mac_upstream=""
			mac_downstream=""
		elif MAC_ONU == "54-4c-52-49-5b-01-f7-28":
			ovs_upstream="" #Id del OVS para el upstream en los servicios del ONT f7-28
			mac_upstream=""
			mac_downstream=""

		head = {'Content-type':'application/yang.data+json','Accept':'application/json, text/plain'}

		urlDownstream="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:159303472399026/flow-node-inventory:table/0/flow/flow"+str(40+int(id_service))
		urlUpstream="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ovs_upstream+"/flow-node-inventory:table/0/flow/flow"+str(40+int(id_service))
		urlMeterDown="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:159303472399026/flow-node-inventory:meter/"+str(int(int(self.gDownstream)/1024))
		urlMeterUp="http://10.0.103.45:8181/restconf/config/opendaylight-inventory:nodes/node/openflow:"+ovs_upstream+"/flow-node-inventory:meter/"+str(int(self.gUpstream))
		requests.delete(urlMeterDown,auth=HTTPBasicAuth('admin', 'admin'))
		requests.delete(urlDownstream,auth=HTTPBasicAuth('admin', 'admin'))
		requests.delete(urlMeterUp,auth=HTTPBasicAuth('admin', 'admin'))
		requests.delete(urlUpstream,auth=HTTPBasicAuth('admin', 'admin'))
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		cursor.execute("delete from ont_service where id_ont='"+MAC_ONU+"' and id_service='"+id_service+"' and configuration = 'OpenFlow'")
		cnx.commit()
		cursor.close()
		cnx.close()
		print("\nLa configuración de la ONU con MAC " + MAC_ONU + " y el servicio "+id_service+" ha sido borrada.\n")
		input("Press enter to continue...")

	def servicio_Video(self,ID_ONU,MAC_ONU,id_service,n_service):
			   
		# Creación de los vectores en los que se almacenarán los parámetros 
		# internos de configuración
		port_ID = []
		alloc_ID = [] 
		tcont_ID = []
		num_instancia = []
		puntero = []
		ds_profile_index = []

		# Creación de los vectores en los que se almacenarán los parámetros 
		# de configuracion que el USUARIO deberá introducir: identificador de VLAN,
		# ancho de banda Downstream garantizado y en exceso y ancho de banda Upstream
		# garantizado y Best Effort
		VLAN_ID = []
		VLAN_PRIORITY =[]
		BW_Downstream_GR = []
		BW_Downstream_Excess = []
		BW_Upstream_GR = []
		BW_Upstream_BE = []


		#Aqui se guarda el log        
		nombre_fichero = 'Servicio_Internet+Video_ONU_MAC_' + MAC_ONU + '.txt'
		outfile = open(nombre_fichero, 'a')

		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		# cursor.execute("select count(id_ont) from ont_service where id_ont='"+str(MAC_ONU)+"' and configuration = 'CLI'")
		# n_service=cursor.fetchone()
		if n_service>0:
			# and typeService='Video'??
			cursor.execute("select gDownstream, excessDownstream, gUpstream, excessUpstream, VLAN, VLANpriority from services where id_service in (select id_service from ont_service where id_ont='"+MAC_ONU+"' and configuration='CLI')")
			old_service_data=cursor.fetchall()
			i=0
			while i<n_service:
				BW_Downstream_GR.append(str(int(old_service_data[i][0])))
				BW_Downstream_Excess.append(str(int(old_service_data[i][1])))
				BW_Upstream_GR.append(str(int(old_service_data[i][2])))
				BW_Upstream_BE.append(str(int(float(old_service_data[i][2])+float(old_service_data[i][3]))))
				VLAN_ID.append(str(old_service_data[i][4]))
				VLAN_PRIORITY.append(str(old_service_data[i][5]))
				i=i+1
		cursor.close()
		cnx.close()

		i=0

		print("Numero de servicios ya configurados: "+str(n_service))

		# if n_service[0] >= 1:
		# 	cursor.execute("select max(alloc_port), max(pointer), max(instance) from ont_service where id_ont='"+MAC_ONU+"' and configuration = 'CLI'")
		# 	alloc_pointer_instance=cursor.fetchone()

		# 	port_ID.append(alloc_pointer_instance[0]+1)
		# 	alloc_ID.append(alloc_pointer_instance[0]+1)
		# 	num_instancia.append(alloc_pointer_instance[2]+1)
		# 	tcont_ID.append(n_service[0])
		# 	puntero.append(alloc_pointer_instance[1]+1)
		# 	cursor.close()
		# 	cnx.close()
		while i<(n_service+1):
			# Para que no se solapen puertos y allocs-ID, se asignan en función del identficiador
			# de la ONU y del número de servicio en cuestión
			port_ID.append(600+100*ID_ONU+i)
			alloc_ID.append(600+100*ID_ONU+i) 
			# Estos valores se asignan de este modo también para evitar solapamientos
			num_instancia.append(i+3)
			tcont_ID.append(i)
			puntero.append(32768+i)
			i=i+1


		# En los sucesivos bucles, se irán pidiendo los parámetros de configuración al usuario.
			            
		# Primer bucle: se piden el identificador VLAN que corresponda a cada servicio
		# La VLAN 833 conecta con un servidor DHCP que asigna la dirección mientras que 
		# la VLAN 806 recibe una IP de forma estática (no la tiene que introducir el usuario)
		# Las etiquetas VLAN van de 1 a 4094. Si el usuario introduce un valor fuera de ese
		# rango, se le volverá a pedir que introduzca el valor. Hay que recordar que la red
		# solo ofrece servicio en las VLAN 833 y 806

		i=0
		while i<(n_service+1):
			VLAN_ID.append(str(self.VLAN))
			print("El identificador VLAN para el servicio es:", VLAN_ID[i])                                                  
			print("\n")

			VLAN_PRIORITY.append(str(self.VLANpriority))
			print("La prioridad VLAN para el servicio es:", VLAN_PRIORITY[i])                                                  
			print("\n")
				    
			# Segundo bucle: se pide el ancho de banda garantizado en sentido Downstream.
			# Este ancho de banda se introduce en Kbps y debe estar entre 0 y 2488000 (aunque
			# a efectos prácticos no tiene sentido meter más de 600000 Kbps, aproximadamente). 
			# El CLI solo admite múltiplos de 64 Kbps de manera que el programa trunca el 
			# valor del usuario para que coincida con un múltiplo de 64 Kbps.

			BW_Downstream_GR.append(str(int(self.gDownstream)))
			print("El ancho de banda Downstream garantizado en Kbps es:", BW_Downstream_GR[i])
				    
			# Tercer bucle: se pide el ancho de banda en exceso en sentido Downstream.
			# Este ancho de banda se introduce en Kbps y debe estar entre 0 y 2488000 (aunque
			# a efectos prácticos no tiene sentido que la suma del garantizado y exceso sea
			# mayor que 600000 Kbps, aproximadamente). El CLI solo admite múltiplos de 64 Kbps 
			# de manera que el programa trunca el valor del usuario para que coincida con
			# un múltiplo de 64 Kbps.
			BW_Downstream_Excess.append(str(int(self.excessDownstream)))
			print("El ancho de banda Downstream en exceso en Kbps es:", BW_Downstream_Excess[i])       
			print("\n")
				     
			# Cuarto bucle: se pide el ancho de banda garantizado en sentido Upstream.
			# Este ancho de banda se introduce en Mbps y debe estar entre 0 y 1244 (aunque
			# a efectos prácticos no tiene sentido meter más de 600 Mbps, aproximadamente).
			BW_Upstream_GR.append(str(int(self.gUpstream)))
			print("El ancho de banda Upstream garantizado en Mbps es:", BW_Upstream_GR[i])                 
			print("\n")
				    
			# Quinto bucle: se pide el ancho de banda garantizado Best Effort Upstream.
			# Este ancho de banda se introduce en Mbps, debe estar entre 0 y 1244 (aunque
			# a efectos prácticos no tiene sentido meter más de 600 Mbps, aproximadamente) y 
			# tiene que ser igualo mayor que el ancho de banda Upstream garantizado (el valor Best 
			# Effort es el mayor ancho de banda que podrá recibir la ONU)                                                            
			BW_Upstream_BE.append(str(int(float(self.gUpstream)+float(self.excessUpstream))))
			print("El ancho de banda Upstream BE en Mbps es:", BW_Upstream_BE[i])
			print("\n")
			i=i+1
		i=0
			                
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
			    
		# A la hora de introducir variables en la declaración de cadenas, aunque sean números,
		# se deben introducir en forma de string. Por ello, aparece a lo largo del programa muchas
		# ocasiones la función str(), que convierte una variable en string
		ID_ONU = str(ID_ONU)
			    
		# A continuación, se definen todos los comandos necesarios para dar el servicio de Datos.
		# Posteriormente serán ejecutados en el CLI con la función write.
		# Primero se crea el canal OMCI de comunicación (con el mismo identificador que el de la ONU por convención)
		# Se resetean las entidades MIB que pudiera haber y se activa fec en uplink (pasos opcionales)
		inicio = "configure \n olt-device 0 \n olt-channel 0 \n onu-local " + ID_ONU + " \n omci-port  " + ID_ONU + "  \n exit \n onu-omci  " + ID_ONU + "  \n ont-data mib-reset \n exit \n fec direction uplink  " + ID_ONU + "  \n onu-local  " + ID_ONU + "  \n"              
		tn.write(inicio.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Se crean, dentro del menú de la ONU a configurar, tantos Alloc-ID como servicios
		i=0
		while i<(n_service+1):
			allocID = "alloc-id " + str(alloc_ID[i]).strip('[]') + " \n"
			tn.write(allocID.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1
			    
		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Cada Alloc-ID irá asociado a un puerto (por convención, se utiliza el mismo identificador)
		# Estos Alloc-IDs y puertos no se pueden utilizar para otras ONUs ni para otros servicios
		i=0
		while i<(n_service+1):
			portalloc = "port " + str(port_ID[i]).strip('[]') + " alloc-id  " + str(alloc_ID[i]).strip('[]') + " \n"
			tn.write(portalloc.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1
			   
		# Desde el menú de configuración del canal OMCI de comunicación, se crean las entidades
		# MIB que forman el servicio de Internet. Estas entidades vienen en el estándar GPON.    
		omci = "onu-omci " + ID_ONU + " \n"
		tn.write(omci.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Creación de las entidades T-Cont (colas). Cada servicio está asociado con un T-Cont 
		# y está vinculado a un Alloc-ID
		i=0
		while i<(n_service+1):
			tcont = "t-cont set slot-id 128 t-cont-id " + str(tcont_ID[i]).strip('[]') + " alloc-id " + str(alloc_ID[i]).strip('[]') + "  \n"
			tn.write(tcont.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# Creación de MAC Brigde Service Profile. Se asociará esta entidad con los MAC Bridge 
		# Port Configuration Data a través del bridge-group-id en los siguientes comandos.
		macservice = "mac-bridge-service-profile create slot-id 0 bridge-group-id 1 spanning-tree-ind true learning-ind true atm-port-bridging-ind true priority 32000 max-age 1536 hello-time 256 forward-delay 1024 unknown-mac-address-discard false mac-learning-depth 255 dynamic-filtering-ageing-time 1000 \n"
		# Creación del primer MAC Bridge Port Configuration Data. Irá asociado a la entidad 
		# extended-vlan-tagging-operation-config-data. Para ello, el tp-type (tipo del punto 
		# de terminación del MAC Bridge) ha de ser lan y el puntero tp-ptr debe tener el mismo 
		# valor que el nº de instancia de la entidad extended-vlan-tagging-operation-config-data.
		macbridge1 = "mac-bridge-pcd create instance 1 bridge-id-ptr 1 port-num 1 tp-type lan tp-ptr 257 port-priority 2 port-path-cost 32 port-spanning-tree-ind true encap-method llc lanfcs-ind forward \n"
		tn.write(macservice.encode('ascii') + b"\n")
		time.sleep(0.2)
		tn.write(macbridge1.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Creación del segundo MAC Bridge Port Configuration Data. Esta entidad está 
		# vinculada al servicio multicast. Se asocia a la entidad Multicast GEM Interworking 
		# Termination Poing. Para ello, el tipo de puntero (tp-type) ha de ser de tipo multicast 
		# (mc-gem) y el tp-ptr ha de coincidir con el nº de instancia la entidad Multicast GEM
		# Interworking Termination Poing.    
		macbridge2 = "mac-bridge-pcd create instance 2 bridge-id-ptr 1 port-num 2 tp-type mc-gem tp-ptr 2 port-priority 0 port-path-cost 1 port-spanning-tree-ind true encap-method llc lanfcs-ind forward  \n"
		tn.write(macbridge2.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Creación de los restantes Mac Brigde Port Configuration Data. Irán asociado a la entidades 
		# VLAN-tagging-filter-data mediante los números de instancia. También irán asociados a los 
		# GEM Interworking Termination Point mediante el tp-type (tipo gem) y el tp-ptr, que
		# tiene que coincidir con el número de instancia del GEM Interworking Termination Point
		i=0
		while i<(n_service+1): 
			macbridge3 = "mac-bridge-pcd create instance " + str(num_instancia[i]).strip('[]') + " bridge-id-ptr 1 port-num " + str(num_instancia[i]).strip('[]') + " tp-type gem tp-ptr " + str(num_instancia[i]).strip('[]') + " port-priority 0 port-path-cost 1 port-spanning-tree-ind true encap-method llc lanfcs-ind forward  \n"
			tn.write(macbridge3.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# Creación del GEM Port Network CTP vinculado al servicio multicast. Está asociado al puerto
		# 4094 (en el que va el servicio multicast). Se diferencia de la entidad que forma el servicio Ethernet
		# en que direction ya no es de tipo bidirectional sino de tipo ani-to-uni. Asimismo, esta entidad está
		# asociada a la entidad Multicast GEM Interworking Termination Point: el nº de instancia debe coincidir con
		# el campo gem-port-nwk-ctp-conn-ptr de la otra entidad.
		gemport_multicast = "gem-port-network-ctp create instance 2 port-id 4094 t-cont-ptr 0 direction ani-to-uni traffic-mgnt-ptr-ustream 0 traffic-descriptor-profile-ptr 0 priority-queue-ptr-downstream 0 traffic-descriptor-profile-ds-ptr 0 enc-key-ring 0  \n"
		tn.write(gemport_multicast.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Creación de los GEM Port Network CTP, que irán asociado a los puertos especificados 
		# anteriormente. Los identificadores tienen que coincidir con el gem-port-nwk-ct-conn-ptr 
		# de los GEM Interworking Termination Point.
		i=0
		while i<(n_service+1):
			gemport = "gem-port-network-ctp create instance " + str(num_instancia[i]).strip('[]') + " port-id  " + str(port_ID[i]).strip('[]') + "  t-cont-ptr " + str(puntero[i]).strip('[]') + " direction bidirectional traffic-mgnt-ptr-ustream 0 traffic-descriptor-profile-ptr 0 priority-queue-ptr-downstream 0 traffic-descriptor-profile-ds-ptr 0 enc-key-ring 0 \n"
			tn.write(gemport.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1


		# Creación del Multicast GEM Interworking Termination Point (en este punto, se produce la 
		# transformación de flujo de bytes a tramas GEM y viceversa). Esta entidad está vinculada al
		# servicio multicast. Se vincula al GEM Port Netwok CTP de tipo multicast mediante el campo
		# gem-port-nwk-ctp-conn-ptr. También se asocia con el MAC Bridge Port Configuration Data de
		# tipo multicast. Para ello, hay que seleccionar como interwork-option mac-bridge y el campo 
		# service-profile-ptr debe tener el valor que se indica en la declaración del comando. 
		# El número de instancia debe ser el mismo que el tp-ptr del MAC Bridge Point Configuration Data asociado
		multicast_geminterworking = "multicast-gem-interworking-termination-point create instance 2 gem-port-nwk-ctp-conn-ptr 2 interwork-option mac-bridge service-prof-ptr 65535 interwork-tp-ptr 0 gal-prof-ptr 65535 gal-lpbk-config 0 \n"
		tn.write(multicast_geminterworking.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Creación de los GEM Interworking Termination Point (en este punto, se produce la 
		# transformación de flujo de bytes a tramas GEM y viceversa). Estas entidades se vinculan 
		# a los GEM Port Network CTP a través del campo gem-port-nwk-ctp-conn-ptr, que debe coincidir 
		# con el número de instancia que  utilizado en el GEM Port Network CTP. Estas entidades también 
		# se asocian con los MAC Bridge Port Configuration. Para ello, hay que seleccionar como 
		# interwork-option mac-bridge-lan y el campo service-profile-ptr debe ser un 1. 
		# El número de instancia debe ser el mismo que el tp-ptr del MAC Bridge Point Configuration Data.     
		i=0
		while i<(n_service+1):
			geminterworking = "gem-interworking-termination-point create instance " + str(num_instancia[i]).strip('[]') + " gem-port-nwk-ctp-conn-ptr " + str(num_instancia[i]).strip('[]') + " interwork-option mac-bridge-lan service-profile-ptr 1 interwork-tp-ptr 0 gal-profile-ptr 0 \n"
			tn.write(geminterworking.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# Creación de los VLAN Tagging Filter Data con los identficadores VLAN definidos arriba. 
		# Los números de instancia deben coincidir con los de los MAC Bridge Port Configuration Data asociados.
		i=0
		while i<(n_service+1):
			vlantagging = "vlan-tagging-filter-data create instance " + str(num_instancia[i]).strip('[]') + "  forward-operation h-vid-a vlan-tag1 " + str(VLAN_ID[i]).strip('[]') + " vlan-priority1 " + str(VLAN_PRIORITY[i]).strip('[]')+ " vlan-tag2 null vlan-priority2 null vlan-tag3 null vlan-priority3 null vlan-tag4 null vlan-priority4 null vlan-tag5 null vlan-priority5 null vlan-tag6 null vlan-priority6 null vlan-tag7 null vlan-priority7 null vlan-tag8 null vlan-priority8 null vlan-tag9 null vlan-priority9 null vlan-tag10 null vlan-priority10 null vlan-tag11 null vlan-priority11 null vlan-tag12 null vlan-priority12 null \n"
			tn.write(vlantagging.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# Creación de la entidad Extended VLAN Tagging Operation Config Data, que será configurada en el paso posterior. 
		# Sirve para gestionar los identificadores VLAN. Esta entidad está asociada al primer MAC Bridge Port Configuration Data 
		# a través del número de instancia, que coincide con el tp-ptr del MAC Bridge Port Configuration Data.
		extendedvlan = "extended-vlan-tagging-operation-config-data create instance 257 association-type pptp-eth-uni associated-me-ptr 257 \n"
		tn.write(extendedvlan.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Configuración de la entidadExtended VLAN Tagging Operation Config Data. Se debe configurar
		# para cada identificador VLAN.
		i=0
		while i<(n_service+1):
			extendedvlanconf = "extended-vlan-tagging-operation-config-data set instance 257 operations-entry filter-outer-prio filter-prio-no-tag filter-outer-vid none filter-outer-tpid none filter-inner-prio filter-prio-none filter-inner-vid " + str(VLAN_ID[i]).strip('[]') + " filter-inner-tpid none filter-ethertype none treatment-tag-to-remove 1 treatment-outer-prio none treatment-outer-vid copy-from-inner treatment-outer-tpid tpid-de-copy-from-outer treatment-inner-prio 0 treatment-inner-vid " + str(VLAN_ID[i]).strip('[]') + " treatment-inner-tpid tpid-de-copy-from-inner\n"
			tn.write(extendedvlanconf.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Configuración de las reglas VLAN en la OLT asociadas a los puertos definidos al principio de la función
		i=0
		while i<(n_service+1):
			reglasvlan = "vlan uplink configuration port-id " + str(port_ID[i]).strip('[]') + " min-cos 0 max-cos 7 de-bit disable primary-tag-handling false \n vlan uplink handling port-id  " + str(port_ID[i]).strip('[]') + "  primary-vlan none destination datapath c-vlan-handling no-change s-vlan-handling no-change new-c-vlan 0 new-s-vlan 0 \n"
			tn.write(reglasvlan.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1
			    
		# Creación de los perfiles de ancho de banda en sentido Downstream con los parámetros 
		# definidos por el usuario anteriormente.
		i=0
		while i<(n_service+1):
			perfildownstreamconf = "policing downstream profile committed-max-bw " + str(BW_Downstream_GR[i]).strip('[]') + " committed-burst-size 1023 excess-max-bw " + str(BW_Downstream_Excess[i]).strip('[]') + " excess-burst-size 1023 \n"
			tn.write(perfildownstreamconf.encode('ascii') + b"\n")
			time.sleep(0.2)
				    
			#Se extrae el ds_profile_index proporcionado por el OLT
			while True:
				line = tn.read_until(b"\n").decode("utf-8")  # Read one line
				outfile.write(line)
				if 'downstream_profile_index' in line:  # last line, no more read
					ds_profile_index.append(line[26:])
					#ds_profile_index.append()
					break
			i=i+1
		i=0	       
		# Asignación de los perfiles de ancho de banda Downstream a los puertos correspondientes
		# mediante los índices de perfil buscados anteriormente.
		while i<(n_service+1):
			perfildownstreamassign = "policing downstream port-configuration entity port-id " + str(port_ID[i]).strip('[]') + " ds-profile-index " + str(ds_profile_index[i]).strip('[]') + " \n"    
			tn.write(perfildownstreamassign.encode('ascii') + b"\n")    
			time.sleep(0.2)
			i=i+1

		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Desde el menú de configuración del algoritmo DBA, se definirián los perfiles de
		# ancho de banda en sentido Upstream
		dba = "pon \n dba pythagoras 0 \n "
		tn.write(dba.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Cada perfil upstream irá asociado a un Alloc-ID y estará configurado con los
		# parámetros que haya definido el usuario.
		i=0
		while i<(n_service+1):
			perfilupstream = "sla " + str(alloc_ID[i]).strip('[]') + " service data status-report nsr gr-bw " + str(BW_Upstream_GR[i]).strip('[]') + " gr-fine 0 be-bw " + str(BW_Upstream_BE[i]).strip('[]') + " be-fine 0 \n"     
			tn.write(perfilupstream.encode('ascii') + b"\n")
			time.sleep(0.2)
			i=i+1

		# El comando end hace salir directamente al modo privilegiado en la estructura
		# de menús del CLI
		final = "end \n"
		tn.write(final.encode('ascii') + b"\n")
		time.sleep(0.2)         
			    
		# Se vuelcan todos los datos en el fichero definido anteriormente (la opción 'a'
		# hace que los datos se añadan al final del fichero) de forma que el fichero recogerá
		# toda la configuración del servicio de Internet
		data = tn.read_very_eager().decode() 
		outfile.write(data)
		outfile.write("\n\n\n")
		outfile.close()
			    
		# Una vez configurado el servicio, se muestra un mensaje al usuario            
		print("Servicio de Internet+Video configurado. \n")


		#Meto en la bse de datos la configuracion
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="insert into ont_service (id_ont, id_service, alloc_port, pointer, profile, instance, WANinstance, configuration) values ('"+str(MAC_ONU)+"', '"+str(id_service)+"', '"+str(port_ID[n_service])+"', '"+str(puntero[n_service])+"', '"+str(ds_profile_index[n_service])+"','"+str(num_instancia[n_service])+"','"+str(n_service+1)+"', 'CLI')"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()
			                                
		return