class Service:

	totDownstream = 0
	totUpstream = 0

	def __init__(self, gDownstream, gUpstream, excessDownstream, excessUpstream, VLAN, idService, typeService):
		self.gDownstream=gDownstream
		self.gUpstream=gUpstream
		self.excessDownstream=excessDownstream
		self.excessUpstream=excessUpstream
		self.VLAN=VLAN
		self.idService=idService
		self.typeService=typeService

		Service.totDownstream=Service.totDownstream+int(gDownstream)+int(excessDownstream)
		Service.totUpstream=Service.totUpstream+int(gUpstream)+int(excessUpstream)

	def mostrarConfig(self):
		print("Guaranteed downstream: " + self.gDownstream +" Mbps")
		print("Excess downstream: " + self.excessDownstream +" Mbps")
		print("Guaranteed upstream: " + self.gUpstream +" Mbps")
		print("Excess upstream: " + self.excessUpstream +" Mbps")
		print("VLAN: "+self.VLAN)
		print("Type of service: "+ self.typeService)