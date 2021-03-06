
# keyboard
from direct.showbase.DirectObject import DirectObject

from model.GameModel import GameModel

from event.Event import createNamedEvent
from event.EventType import EventType

class GameControl(DirectObject):
	'''
	Currently the game can be controlled with a keaboard.
	http://www.panda3d.org/wiki/index.php/Event_Handlers
	'''

	PLAYER_RIGHT_KEY = "arrow_right"
	PLAYER_LEFT_KEY = "arrow_left"
	PLAYER_UP_KEY = "arrow_up"
	PLAYER_DOWN_KEY = "arrow_down"
	PLAYER_JUMP = "space"
	TURN_GRAVITY = "g"
	TURN_GRAVITY2 = "h"
	RESTART_LEVEL = "r"
	SELECT = "enter"
	TOGGLE_VERB = False

	def __init__(self, model, app):
		self.player = 	self.ball = self.app = self.inMenu = self.activeMenu = None
		self.model = model
		
		if (self.model != None):
			#print 'GameControl.__init__ = True'
			self.app = app
			self.inMenu = False
			self.activeMenu = None
			self.model= model
			self.ball = model.getBall()
			self.player = model.getPlayer()
			model.isListening = True
			self.initEvents()
			if self.TOGGLE_VERB:
				print self.ball
				print self
		else:
			#print 'GameControl.__init__ = False'
			self.app = app
			self.bStartInit()
			if self.TOGGLE_VERB:
				print self
			
	def initEvents(self):
		#print 'GameControl.initEvents'
		playerMoveRightOn = createNamedEvent(
			self.player.name, EventType.PLAYER_MOVE_RIGHT_ON
		)
		playerMoveRightOff = createNamedEvent(
			self.player.name, EventType.PLAYER_MOVE_RIGHT_OFF
		)
		playerMoveLeftOn = createNamedEvent(
			self.player.name, EventType.PLAYER_MOVE_LEFT_ON
		)
		playerMoveLeftOff = createNamedEvent(
			self.player.name, EventType.PLAYER_MOVE_LEFT_OFF
		)
		playerJumpOn = createNamedEvent(
			self.player.name, EventType.PLAYER_JUMP_ON
		)
		playerJumpOff = createNamedEvent(
			self.player.name, EventType.PLAYER_JUMP_OFF
		)

		self.accept(playerMoveRightOn, self.ball.startMoveRight)
		self.accept(playerMoveRightOff, self.ball.stopMoveRight)
		self.accept(playerMoveLeftOn, self.ball.startMoveLeft)
		self.accept(playerMoveLeftOff, self.ball.stopMoveLeft)
		self.accept(playerJumpOn, self.ball.jumpOn)
		self.accept(playerJumpOff, self.ball.jumpOff)

		self.accept(GameControl.PLAYER_RIGHT_KEY, self.ball.arrowRightDown)
		self.accept(GameControl.PLAYER_RIGHT_KEY + "-up", self.ball.arrowRightUp)
		self.accept(GameControl.PLAYER_LEFT_KEY, self.ball.arrowLeftDown)
		self.accept(GameControl.PLAYER_LEFT_KEY + "-up", self.ball.arrowLeftUp)
		
		self.accept(EventType.CONTROL_CHANGE, self.controlLocation)
		
		self.accept(GameControl.PLAYER_UP_KEY, self.ball.arrowUpDown)
		self.accept(GameControl.PLAYER_UP_KEY + "-up", self.ball.arrowUpUp)
		self.accept(GameControl.PLAYER_DOWN_KEY, self.ball.arrowDownDown)
		self.accept(GameControl.PLAYER_DOWN_KEY + "-up", self.ball.arrowDownUp)
		
		self.accept(GameControl.PLAYER_JUMP, self.player.jumpOn)
		self.accept(GameControl.PLAYER_JUMP + "-up", self.player.jumpOff)
		
		self.accept(GameControl.TURN_GRAVITY, self.model.turnGravityTask )
		self.accept(GameControl.TURN_GRAVITY2, self.model.turnGravityTask2 )
		
		if self.TOGGLE_VERB:
			print self.ball
			print self
		
	def bStartInit(self):
		#print 'GameControl.bStartInit'
		self.accept(EventType.CONTROL_CHANGE, self.controlLocation)
	
	def controlChange(self):
		self.activeMenu = self.app.getActiveMenu()
		if self.TOGGLE_VERB:
			print self.activeMenu
			print self.ball
		print ' \n Aktiivinen menu:'
		print self.activeMenu
		
		self.ignore(GameControl.PLAYER_UP_KEY + "-up")
		self.ignore(GameControl.PLAYER_DOWN_KEY + "-up")
		self.ignore(GameControl.SELECT + "-up")
		print 'KONTROLLIT >'
		if self.activeMenu != None:
			print 'MENUSSA \n'
			self.accept(GameControl.PLAYER_UP_KEY + "-up", self.activeMenu.selectionUp)
			self.accept(GameControl.PLAYER_DOWN_KEY + "-up", self.activeMenu.selectionDown)
			self.accept(GameControl.SELECT + "-up", self.activeMenu.select)
		else:
			print 'IN-GAME \n'
			if self.TOGGLE_VERB:
				print 'Pallo on:'
				print self.ball
				print self
			self.accept(GameControl.PLAYER_UP_KEY + "-up", self.ball.arrowUpUp)
			self.accept(GameControl.PLAYER_DOWN_KEY + "-up", self.ball.arrowDownUp)
			self.accept(GameControl.SELECT + "-up",self.unbind )
	
	def controlLocation(self):
		#print 'GameControl.controlLocation'
		self.inMenu = not self.inMenu
		if self.TOGGLE_VERB:
			print self.inMenu
			print self.ball
			print self
		self.controlChange()
		
	def unbind(self):
		print "Key unbinded"
		
	def updateResources(self, model, app):
		print 'GameControl.updateResources'
		self.player = model.getPlayer()
		self.ball = model.getBall()
		self.app = app
		self.initEvents()