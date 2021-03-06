
from pandac.PandaModules import (
        Quat,OdeBody, OdeMass, OdeBoxGeom, BitMask32)
from math import sin

from model.SurfaceType import SurfaceType

class MovingPlane:
	''' moving plane '''
	id = 0

	MODEL = "../egg/box.egg"
	
	def __init__(self, space, pos, dim, surface = SurfaceType.FLOOR):
		'''
		kirjoita numerot float muodossa 1.0
		@param space: fysiikka-avaruus?
		'''
		MovingPlane.id += 1
		self.id = id
		self.dim = dim # dimension
		self.pos = pos # position
		self.h = ( dim[0]/2, dim[1]/2, dim[2]/2 ) # center
		self.t = 0

		self.geom = OdeBoxGeom( space, dim[0], dim[1], dim[2])
		space.setSurfaceType( self.geom, surface )
		
		
			
		self.model = loader.loadModel(self.MODEL)
		self.model.setScale( dim[0], dim[1], dim[2] )
		# http://www.panda3d.org/wiki/index.php/Creating_a_New_Node_Class
		self.model.flattenLight()
		self.model.reparentTo(render)
		
		self.rotate = False
		
		if surface == SurfaceType.SAND:
			self.model.setColor( 1, 0, 0 )
		self.updateModelNode()

	def updateModelNode(self):
		pos = self.pos
		h = self.h
		if(self.rotate):
			self.t = self.t + 0.03
			rot = pos[2] + 2*sin( self.t )
			self.geom.setPosition( pos[0], pos[1], rot)
			self.model.setPos(pos[0]-h[0], pos[1]-h[1], rot-h[2])
		else:
			self.geom.setPosition( pos[0], pos[1], pos[2])
			self.model.setPos(pos[0]-h[0], pos[1]-h[1], pos[2]-h[2])

	def getId(self):
		return id;

	def getGeom(self):
		return self.geom

	def removeNode(self):
		self.model.removeNode()
		self.geom = None
		
	def setPosition( self, pos ):
		self.pos = pos
		
	def setInterval( pos1, pos2 ):
		pass

	def setSpeed( self, speed):
		pass
