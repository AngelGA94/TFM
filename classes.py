import mysql.connector
from prettytable import PrettyTable

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
		t.add_row([str(self.gDownstream)+" Mbps", str(self.excessDownstream)+" Mbps",str(self.gUpstream)+" Mbps",str(self.excessUpstream)+" Mbps",self.VLAN,self.typeService])
		print(t)

	def insertConfig(self):
		cnx = mysql.connector.connect(user='root', password='tfg_2017',host='127.0.0.1',database='gponServices')
		cursor = cnx.cursor()
		query="select sum(gDownstream) from services"
		cursor.execute(query)
		for i in cursor:
			print(int(i)+2)
		input()
		# query="insert into services (gDownstream, excessDownstream, gUpstream, excessUpstream, VLAN, typeService) values ('"+str(self.gDownstream)+"', '"+str(self.excessDownstream)+"', '"+str(self.gUpstream)+"', '"+str(self.excessUpstream)+"', '"+str(self.VLAN)+"', '"+self.typeService+"')"
		# cursor.execute(query)
		# cnx.commit()

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
			t.add_row([id_service, str(gDownstream)+" Mbps", str(excessDownstream)+" Mbps",str(gUpstream)+" Mbps",str(excessUpstream)+" Mbps",VLAN,typeService])

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



