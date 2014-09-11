
"""
 	may want to always return:
 	(objectID, (x,y), speed, destinationID, (destinationX, destinationY)) 
 	if immobile 
 		destination relevant items set to None

""" 


class SpaceObjects(object):
	"""
		SpaceObjects is the parent class of all objects in the universe. 
			(x,y) = current location
			speed = current speed (note for some this will always be '0' - unless there is a mod! :) ) 
			(destinationX, destinationY) = next targeted location
			newSpeed = new speed coming from orders (this speed will become 'speed'). 

	"""

	def __init__(self, x, y, ID):
		self.ID = ID
		self.x = x
		self.y = y
		self.speed = 0
		self.destinationX = self.x
		self.destinationY = self.y
		self.newSpeed = self.speed


	def getID(self):
		return self.ID

	def getCurrentCoord(self):
		""" returns a tuple  """ 
		return (self.x, self.y)

	def setCurrentCoord(self, x, y):
		self.x = x
		self.y = y

	def printCurrentCoord(self):
		print ("(x = %, y = %)", self.x, self.y)

	def getDestinationCoord(self):
		""" returns a tuple """
		return (self.destinationX, self.destinationY)







class Minefields(SpaceObjects):
	"""
		Minefield information here
	"""
	pass




class PacketsAndSalvage(SpaceObjects):
	"""	Salvage in Standard Stars are minerals that can be retrieved by any who are co-located. Velocity is 0.
		Packets in Standard Stars minerals combined at a base with a Mass Driver (see tech tree) with a velocity(~5-14) 
		that typically has a planet destination. 
	"""
	def __init__(self, arg):
		super(PacketsAndSalvage, self).__init__()
		self.arg = arg
		




