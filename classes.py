import mysql.connector
import telnetlib
import time
from prettytable import PrettyTable
import xml.etree.cElementTree as etree

class Service:

	#totDownstream = 0
	#totUpstream = 0
	#id_service=0

	def __init__(self, gDownstream, gUpstream, excessDownstream, excessUpstream, VLAN, typeService):
		self.gDownstream=gDownstream
		self.gUpstream=gUpstream
		self.excessDownstream=excessDownstream
		self.excessUpstream=excessUpstream
		self.VLAN=VLAN
		#self.idService=idService
		self.typeService=typeService

		#Service.totDownstream=Service.totDownstream+int(gDownstream)+int(excessDownstream)
		#Service.totUpstream=Service.totUpstream+int(gUpstream)+int(excessUpstream)

	def showConfig(self):
		t = PrettyTable(['Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'Type of service'])
		t.add_row([str(self.gDownstream)+" Kbps", str(self.excessDownstream)+" Kbps",str(self.gUpstream)+" Mbps",str(self.excessUpstream)+" Mbps",self.VLAN,self.typeService])
		print(t)

	def insertConfig(self):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		# query="select sum(gDownstream) from services"
		# cursor.execute(query)
		# for i in cursor:
		# 	print(int(i)+2)
		# input()
		query="insert into services (gDownstream, excessDownstream, gUpstream, excessUpstream, VLAN, typeService) values ('"+str(self.gDownstream)+"', '"+str(self.excessDownstream)+"', '"+str(self.gUpstream)+"', '"+str(self.excessUpstream)+"', '"+str(self.VLAN)+"', '"+self.typeService+"')"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()

	def updateConfig(self,id_service):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="update services set gDownstream='"+str(self.gDownstream)+"', excessDownstream='"+str(self.excessDownstream)+"', gUpstream='"+str(self.gUpstream)+"', excessUpstream='"+str(self.excessUpstream)+"',VLAN='"+str(self.VLAN)+"' where id_service='"+id_service+"'"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()		

	def showServices():
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services"
		cursor.execute(query)
		t = PrettyTable(['ID', 'Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'Type of service'])
		for (id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService) in cursor:
			t.add_row([id_service, str(gDownstream)+" Kbps", str(excessDownstream)+" Kbps",str(gUpstream)+" Mbps",str(excessUpstream)+" Mbps",VLAN,typeService])

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
		for (id_service,gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService) in cursor:
			options=[id_service,gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService]
		#service = Service(cursor.downstream, cursor.upstream, cursor.eDownstream, cursor.eUpstream, cursor.VLAN, cursor.typeService)
		cursor.close()
		cnx.close()
		return options
	def servicio_Internet(self,ID_ONU,MAC_ONU,id_service):
			   
		# Creación de los vectores en los que se almacenarán los parámetros 
		# internos de configuración
		port_ID = []
		alloc_ID = [] 
		tcont_ID = []
		num_instancia = []
		puntero = []
		ds_profile_index = []

		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select count(id_ont) from ont_service where id_ont='"+str(MAC_ONU)+"'"
		cursor.execute(query)
		n_service=cursor.fetchone()
		
		i=0
		if n_service[0] >= 1:
			cursor.execute("select max(alloc_port), max(pointer) from ont_service where id_ont='"+MAC_ONU+"'")
			alloc_pointer=cursor.fetchone()
			port_ID.append(alloc_pointer[0]+1)
			alloc_ID.append(alloc_pointer[0]+1)
			num_instancia.append(n_service[0]+2)
			tcont_ID.append(n_service[0])
			puntero.append(alloc_pointer[1]+1)
			ds_profile_index.append(n_service[0])
			cursor.close()
			cnx.close()
		else:
			# Para que no se solapen puertos y allocs-ID, se asignan en función del identficiador
			# de la ONU y del número de servicio en cuestión
			port_ID.append(600+100*ID_ONU+i)
			alloc_ID.append(600+100*ID_ONU+i) 
			# Estos valores se asignan de este modo también para evitar solapamientos
			num_instancia.append(i+2)
			tcont_ID.append(i)
			puntero.append(32768+i)
			ds_profile_index.append(i)
			    
		# Creación de los vectores en los que se almacenarán los parámetros 
		# de configuracion que el USUARIO deberá introducir: identificador de VLAN,
		# ancho de banda Downstream garantizado y en exceso y ancho de banda Upstream
		# garantizado y Best Effort
		VLAN_ID = []
		BW_Downstream_GR = []
		BW_Downstream_Excess = []
		BW_Upstream_GR = []
		BW_Upstream_BE = []

		# En los sucesivos bucles, se irán pidiendo los parámetros de configuración al usuario.
			            
		# Primer bucle: se piden el identificador VLAN que corresponda a cada servicio
		# La VLAN 833 conecta con un servidor DHCP que asigna la dirección mientras que 
		# la VLAN 806 recibe una IP de forma estática (no la tiene que introducir el usuario)
		# Las etiquetas VLAN van de 1 a 4094. Si el usuario introduce un valor fuera de ese
		# rango, se le volverá a pedir que introduzca el valor. Hay que recordar que la red
		# solo ofrece servicio en las VLAN 833 y 806            
		VLAN_ID.append(str(self.VLAN))
		print("El identificador VLAN para el servicio es:", VLAN_ID[i])                                                  
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
		BW_Upstream_BE.append(str(int(self.gUpstream+self.excessUpstream)))
		print("El ancho de banda Upstream BE en Mbps es:", BW_Upstream_BE[i])
		print("\n")
			                
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
		allocID = "alloc-id " + str(alloc_ID[i]).strip('[]') + " \n"
		tn.write(allocID.encode('ascii') + b"\n")
		time.sleep(0.2) 
			    
		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Cada Alloc-ID irá asociado a un puerto (por convención, se utiliza el mismo identificador)
		# Estos Alloc-IDs y puertos no se pueden utilizar para otras ONUs ni para otros servicios

		portalloc = "port " + str(port_ID[i]).strip('[]') + " alloc-id  " + str(alloc_ID[i]).strip('[]') + " \n"
		tn.write(portalloc.encode('ascii') + b"\n")
		time.sleep(0.2)
			   
		# Desde el menú de configuración del canal OMCI de comunicación, se crean las entidades
		# MIB que forman el servicio de Internet. Estas entidades vienen en el estándar GPON.    
		omci = "onu-omci " + ID_ONU + " \n"
		tn.write(omci.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Creación de las entidades T-Cont (colas). Cada servicio está asociado con un T-Cont 
		# y está vinculado a un Alloc-ID
		tcont = "t-cont set slot-id 128 t-cont-id " + str(tcont_ID[i]).strip('[]') + " alloc-id " + str(alloc_ID[i]).strip('[]') + "  \n"
		tn.write(tcont.encode('ascii') + b"\n")
		time.sleep(0.2)

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
			    
		# Creación de los restantes Mac Brigde Port Configuration Data. Irán asociado a la entidades 
		# VLAN-tagging-filter-data mediante los números de instancia. También irán asociados a los 
		# GEM Interworking Termination Point mediante el tp-type (tipo gem) y el tp-ptr, que
		# tiene que coincidir con el número de instancia del GEM Interworking Termination Point  
		macbridge2 = "mac-bridge-pcd create instance " + str(num_instancia[i]).strip('[]') + " bridge-id-ptr 1 port-num " + str(num_instancia[i]).strip('[]') + " tp-type gem tp-ptr " + str(num_instancia[i]).strip('[]') + " port-priority 0 port-path-cost 1 port-spanning-tree-ind true encap-method llc lanfcs-ind forward  \n"
		tn.write(macbridge2.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Creación de los GEM Port Network CTP, que irán asociado a los puertos especificados 
		# anteriormente. Los identificadores tienen que coincidir con el gem-port-nwk-ct-conn-ptr 
		# de los GEM Interworking Termination Point.   
		gemport = "gem-port-network-ctp create instance " + str(num_instancia[i]).strip('[]') + " port-id  " + str(port_ID[i]).strip('[]') + "  t-cont-ptr " + str(puntero[i]).strip('[]') + " direction bidirectional traffic-mgnt-ptr-ustream 0 traffic-descriptor-profile-ptr 0 priority-queue-ptr-downstream 0 traffic-descriptor-profile-ds-ptr 0 enc-key-ring 0 \n"
		tn.write(gemport.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Creación de los GEM Interworking Termination Point (en este punto, se produce la 
		# transformación de flujo de bytes a tramas GEM y viceversa). Estas entidades se vinculan 
		# a los GEM Port Network CTP a través del campo gem-port-nwk-ctp-conn-ptr, que debe coincidir 
		# con el número de instancia que  utilizado en el GEM Port Network CTP. Estas entidades también 
		# se asocian con los MAC Bridge Port Configuration. Para ello, hay que seleccionar como 
		# interwork-option mac-bridge-lan y el campo service-profile-ptr debe ser un 1. 
		# El número de instancia debe ser el mismo que el tp-ptr del MAC Bridge Point Configuration Data.     

		geminterworking = "gem-interworking-termination-point create instance " + str(num_instancia[i]).strip('[]') + " gem-port-nwk-ctp-conn-ptr " + str(num_instancia[i]).strip('[]') + " interwork-option mac-bridge-lan service-profile-ptr 1 interwork-tp-ptr 0 gal-profile-ptr 0 \n"
		tn.write(geminterworking.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Creación de los VLAN Tagging Filter Data con los identficadores VLAN definidos arriba. 
		# Los números de instancia deben coincidir con los de los MAC Bridge Port Configuration Data asociados.
		vlantagging = "vlan-tagging-filter-data create instance " + str(num_instancia[i]).strip('[]') + "  forward-operation h-vid-a vlan-tag1 " + str(VLAN_ID[i]).strip('[]') + " vlan-priority1 0  vlan-tag2 null vlan-priority2 null vlan-tag3 null vlan-priority3 null vlan-tag4 null vlan-priority4 null vlan-tag5 null vlan-priority5 null vlan-tag6 null vlan-priority6 null vlan-tag7 null vlan-priority7 null vlan-tag8 null vlan-priority8 null vlan-tag9 null vlan-priority9 null vlan-tag10 null vlan-priority10 null vlan-tag11 null vlan-priority11 null vlan-tag12 null vlan-priority12 null \n"
		tn.write(vlantagging.encode('ascii') + b"\n")
		time.sleep(0.2)

		# Creación de la entidad Extended VLAN Tagging Operation Config Data, que será configurada en el paso posterior. 
		# Sirve para gestionar los identificadores VLAN. Esta entidad está asociada al primer MAC Bridge Port Configuration Data 
		# a través del número de instancia, que coincide con el tp-ptr del MAC Bridge Port Configuration Data.
		extendedvlan = "extended-vlan-tagging-operation-config-data create instance 257 association-type pptp-eth-uni associated-me-ptr 257 \n"
		tn.write(extendedvlan.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Configuración de la entidadExtended VLAN Tagging Operation Config Data. Se debe configurar
		# para cada identificador VLAN.
		extendedvlanconf = "extended-vlan-tagging-operation-config-data set instance 257 operations-entry filter-outer-prio filter-prio-no-tag filter-outer-vid none filter-outer-tpid none filter-inner-prio filter-prio-none filter-inner-vid " + str(VLAN_ID[i]).strip('[]') + " filter-inner-tpid none filter-ethertype none treatment-tag-to-remove 1 treatment-outer-prio none treatment-outer-vid copy-from-inner treatment-outer-tpid tpid-de-copy-from-outer treatment-inner-prio 0 treatment-inner-vid " + str(VLAN_ID[i]).strip('[]') + " treatment-inner-tpid tpid-de-copy-from-inner\n"
		tn.write(extendedvlanconf.encode('ascii') + b"\n")
		time.sleep(0.2)

		# El comando exit hace salir hacia el menú anterior del CLI en la estructura de menús  
		salir = "exit \n"
		tn.write(salir.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Configuración de las reglas VLAN en la OLT asociadas a los puertos definidos al principio de la función
		reglasvlan = "vlan uplink configuration port-id " + str(port_ID[i]).strip('[]') + " min-cos 0 max-cos 7 de-bit disable primary-tag-handling false \n vlan uplink handling port-id  " + str(port_ID[i]).strip('[]') + "  primary-vlan none destination datapath c-vlan-handling no-change s-vlan-handling no-change new-c-vlan 0 new-s-vlan 0 \n"
		tn.write(reglasvlan.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Creación de los perfiles de ancho de banda en sentido Downstream con los parámetros 
		# definidos por el usuario anteriormente. 
		perfildownstreamconf = "policing downstream profile committed-max-bw " + str(BW_Downstream_GR[i]).strip('[]') + " committed-burst-size 1023 excess-max-bw " + str(BW_Downstream_Excess[i]).strip('[]') + " excess-burst-size 1023 \n"
		tn.write(perfildownstreamconf.encode('ascii') + b"\n")
		time.sleep(0.2)
			    
		# Nombre del fichero en el que se guardará la configuración del servicio de Internet            
		nombre_archivo = 'Servicio_Internet_ONU_MAC_' + MAC_ONU + '.txt'
			    
		# Al crear los perfiles de  ancho de banda en sentido de bajada, el CLI devuelve un 
		# índice de perfil. Para asociar los perfiles creados, se deben utilizar esos índices
		# de perfil y asociarlos a los puertos definidos anteriormente. Para ello, se vuelcan los datos
		# enviados y recibidos del CLI en un fichero, del que se extraerán esos índices.
		datos_perfil = tn.read_very_eager().decode()
		outfile = open(nombre_archivo, 'a')
		outfile.write(datos_perfil)
		outfile.close()
		outfile = open(nombre_archivo, 'r')             
		lines = outfile.readlines()
		true_ds_profile = 0
		# Se busca el índice de perfil que primero aparezca en el fichero.
		for i in range (0,500):
			if true_ds_profile == 1:
			   break                
			j = str(i)
			cadena = 'downstream_profile_index: ' + j + ' '
			for line in lines:
			    if cadena in line:
			        j = int(j)
			        ds_profile_index[0] = j
			        true_ds_profile = 1            
			    
		outfile.close()
		i=0	       
		# Asignación de los perfiles de ancho de banda Downstream a los puertos correspondientes
		# mediante los índices de perfil buscados anteriormente.
		perfildownstreamassign = "policing downstream port-configuration entity port-id " + str(port_ID[i]).strip('[]') + " ds-profile-index " + str(ds_profile_index[i]).strip('[]') + " \n"    
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
		perfilupstream = "sla " + str(alloc_ID[i]).strip('[]') + " service data status-report nsr gr-bw " + str(BW_Upstream_GR[i]).strip('[]') + " gr-fine 0 be-bw " + str(BW_Upstream_BE[i]).strip('[]') + " be-fine 0 \n"     
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
		outfile = open(nombre_archivo, 'a')
		outfile.write(data)
		outfile.write("\n\n\n")
		outfile.close()
			    
		# Una vez configurado el servicio, se muestra un mensaje al usuario            
		print("Servicio de Internet configurado. \n")


		#Meto en la bse de datos la configuracion
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="insert into ont_service (id_ont, id_service, alloc_port, pointer) values ('"+str(MAC_ONU)+"', '"+str(id_service)+"', '"+str(port_ID[0])+"', '"+str(puntero[0])+"')"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()
   
		# # Actualización del fichero XML con los datos configurados 
		# doc = etree.parse("configuracionGPON.xml")
		# # Extracción del elemento raíz
		# redGPON = doc.getroot()
			    
		# # Obtención del índice correspondiente a la ONU que se está configurando.
		# # Para ello, se hace una comparación de las diferentes direcciones MAC con 
		# # la de la ONU a configurar.
		# index=0
		# true_index=0
		# while true_index==0:
		# 	for attr,value in redGPON[index].items():
		# 		if value == MAC_ONU:
		# 			true_index=1
		# 			break
		# 		index=index+1
			    
		# # Se borra cualquier configuración anterior que en este caso, al configurar un
		# # nuevo servicio, se va a desechar
		# num_servicios = len(redGPON[index])
		# i=0
		# while i<num_servicios:
		# 	redGPON[index].remove(redGPON[index][0])
		# 	i=i+1
			    
		# # Se actualiza la parte del árbol correspondiente a la ONU en cuestión con los
		# # parámetros que ha definido el usuario. Se utiliza la función SubElement para
		# # crear el servicio así como los parámetros del mismo.
		# i=0
		# while i < num_servicios_Internet:       
		# 	Servicio = etree.SubElement(redGPON[index], "Servicio", tipo='Internet')
		# 	VLAN = etree.SubElement(redGPON[index][i], "VLAN_ID").text = str(VLAN_ID[i]).strip('[]')
		# 	BW_Down_GR = etree.SubElement(redGPON[index][i], "BW_Down_GR").text = str(BW_Downstream_GR[i]).strip('[]')                        
		# 	BW_Down_Excess = etree.SubElement(redGPON[index][i], "BW_Down_Excess").text = str(BW_Downstream_Excess[i]).strip('[]')
		# 	BW_Up_GR = etree.SubElement(redGPON[index][i], "BW_Up_GR").text = str(BW_Upstream_GR[i]).strip('[]')                        
		# 	BW_Up_BE = etree.SubElement(redGPON[index][i], "BW_Up_BE").text = str(BW_Upstream_BE[i]).strip('[]')   
		# 	i=i+1                            
			    
		# # Finalmente se crea el nuevo árbol actualizado y se escribe en el fichero
		# doc = etree.ElementTree(redGPON)
		# doc.write("configuracionGPON.xml")
			                                
		return

		# Función servicio_Video(ID_ONU,MAC_ONU,num_servicios_Video): permite configurar
		# servicios de Internet + Vídeo (el servicio multicast del vídeo debe ir sobre uno
		# Ethernet para gestionar el tráfico IMGP asociado) y toma como parámetros el identificador de la ONU 
		# (posición en el vector de direcciones MAC), la MAC y el número de servicios a configurar. 
		# Guarda la configuración actual en un fichero txt (esta configuración es temporal y se 
		# mantiene mientras no se apague la red ni se cambie al modo de gestión TGMS). 
		# La función también actualiza el fichero XML para recuperar configuraciones
		# cuando se apaga la red o se cambia al TGMS.
	def borrar_configuracion(ID_ONU,MAC_ONU):

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
		cursor = cnx.cursor()
		cursor.execute("select alloc_port from ont_service where id_ont='"+MAC_ONU+"'")
		portIDs=cursor.fetchall()
		for port_ID in portIDs:
			borrar_perfil = "configure \n olt-device 0 \n olt-channel 0 \n no policing downstream port-configuration entity port-id " + str(port_ID) + " \n end \n"
			tn.write(borrar_perfil.encode('ascii') + b"\n")
			time.sleep(0.1)
		
		# Tras borrar los perfiles de ancho de banda, se borrar las entidades MIB presentes en 
		# el canal OMCI asociado a la ONU.
		borrar_MIB = "configure \n olt-device 0 \n olt-channel 0 \n onu-local " + ID_ONU + " \n omci-port  " + ID_ONU + "  \n exit \n onu-omci  " + ID_ONU + " \n ont-data mib-reset \n exit \n end \n"
		tn.write(borrar_MIB.encode('ascii') + b"\n")
		time.sleep(2)

		cursor.execute("delete from ont_service where id_ont='"+MAC_ONU+"'")
		cnx.commit()
		cursor.close()
		cnx.close()
		# Finalmente se borra el fichero de configuración.
		# Una vez borrado, se muestra un mensaje informando al usuario.
		print("\nLa configuración de la ONU con MAC " + MAC_ONU + " ha sido borrada.\n")
		input("Press enter to continue...")
    
		# # Actualización del archivo XML con los datos borrados
		# doc = etree.parse("configuracionGPON.xml")
		# # Extracción del elemento raíz
		# redGPON = doc.getroot()
    
		#  # Obtención del índice correspondiente a la ONU cuya configuración se va a borrar.
		# # Para ello, se hace una comparación de las diferentes direcciones MAC con 
		# # la de la ONU en cuestión.
		# index=0
		# true_index=0
		# while true_index==0:
		# 	for attr,value in redGPON[index].items():
		# 		if value == MAC_ONU:
		# 			true_index=1
		# 			break
		# 		index=index+1
    
		# # Se borra la configuración de dicha ONU
		# num_servicios = len(redGPON[index])
		# i=0
		# while i<num_servicios:
		# 	redGPON[index].remove(redGPON[index][0])
		# 	i=i+1
    
		# # Finalmente se crea el nuevo árbol modificado y se escribe en el fichero XML
		# doc = etree.ElementTree(redGPON)
		# doc.write("configuracionGPON.xml")
    
		return

	def showAttachedServices(MAC_ONU):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services where id_service in (select id_service from ont_service where id_ont='"+MAC_ONU+"')"
		cursor.execute(query)
		t = PrettyTable(['ONT', 'ID', 'Guaranteed Downstream', 'Excess Downstream', 'Guaranteed Upstream', 'Excess Upstream', 'VLAN', 'Type of service'])
		#print(cursor.fetchall())
		for (id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService) in cursor:
			t.add_row([MAC_ONU, id_service, str(gDownstream)+" Kbps", str(excessDownstream)+" Kbps",str(gUpstream)+" Mbps",str(excessUpstream)+" Mbps",VLAN,typeService])

		print(t)

		cursor.close()
		cnx.close()
		input("Press enter to continue...")