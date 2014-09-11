from .space_objects import SpaceObjects



class Planet(SpaceObjects):
	"""	
		Planet is the template that provides all the data available for a planet. 
		origHab = Tuple
		origConc = Tuple

	"""
	def __init__(self, x, y, ID, name, origHab, origConc):
		super(Planet, self).__init__(x, y, ID)
		self.name = name
		self.origHab = origHab
		self.origConc = origConc



	def getOrigHab(self):
		#print ("%s" % (self.origHab))
		return self.origHab

	def getName(self):

		#print ("%s" % (self.name))
		return self.name