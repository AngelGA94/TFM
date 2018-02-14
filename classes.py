import mysql.connector

class Service:

	#totDownstream = 0
	#totUpstream = 0
	id_service=0

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
		print("VLAN: "+self.VLAN)
		print("Type of service: "+ self.typeService)
		print("Guaranteed downstream: " + self.gDownstream +" Mbps")
		print("Excess downstream: " + self.excessDownstream +" Mbps")
		print("Guaranteed upstream: " + self.gUpstream +" Mbps")
		print("Excess upstream: " + self.excessUpstream +" Mbps")

	def insertConfig(self):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="insert into services (gDownstream, excessDownstream, gUpstream, excessUpstream, VLAN, typeService) values ('"+self.gDownstream+"', '"+self.excessDownstream+"', '"+self.gUpstream+"', '"+self.excessUpstream+"', '"+self.VLAN+"', '"+self.typeService+"')"
		cursor.execute(query)
		cnx.commit()

		cursor.close()
		cnx.close()

	def showServices():
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select * from services"
		cursor.execute(query)
		for (id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService) in cursor:
			print("{} {} {} {} {} {} {}".format(id_service, gDownstream, excessDownstream,gUpstream,excessUpstream,VLAN,typeService))


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



