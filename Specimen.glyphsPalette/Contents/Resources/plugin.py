# encoding: utf-8

from __future__ import division, print_function, unicode_literals
import objc
from GlyphsApp import *
from GlyphsApp.plugins import *
from vanilla import *
import os, random, json

class Specimen (PalettePlugin):
	
	dialog = objc.IBOutlet()
	textField = objc.IBOutlet()
	
	@objc.python_method
	def settings(self):
		self.name = 'Specimen'
	
	@objc.python_method
	def start(self):
		width = 150
		height = 300
		halfwidth = 75
		self.paletteView = Window((width, height))
		self.paletteView.group = Group((0, 0, width, height))
		self.paletteView.group.myTextBox = TextBox((10, 5, -10, 20), "Words length", sizeStyle='mini',)
		self.paletteView.group.slider = Slider((10, 20, -10, 20),value=10, minValue=3, maxValue=25, sizeStyle='mini', continuous=False, callback=self.update)
		self.paletteView.group.myTextBox2 = TextBox((10, 50, -10, 20), "Lines count", sizeStyle='mini',)
		self.paletteView.group.slider2 = Slider((10, 65, -10, 20),value=10, minValue=3, maxValue=18, sizeStyle='mini', tickMarkCount=18,stopOnTickMarks =True,continuous=False, callback=self.update)
		self.paletteView.group.radioGroup = RadioGroup((10, 100, -10, 20), ["lower", "UPPER", "Caps"],isVertical=False, callback=self.update)
		self.paletteView.group.radioGroup.set(0)
		self.paletteView.group.title = TextBox((10, 130, -10, 20), "Tolerance", sizeStyle="mini")
		self.paletteView.group.slider3 = Slider((10, 145, -10, 20),value=200, minValue=50, maxValue=2000, sizeStyle='mini',continuous=False, callback=self.update)
		self.paletteView.group.titleleftcar = TextBox((10, 170, halfwidth, 20), "Left glyph", sizeStyle="mini")
		self.paletteView.group.titlerightcar = TextBox(((halfwidth+20), 170, halfwidth, 20), "Right glyph", sizeStyle="mini")
		self.paletteView.group.carLeft = EditText((10, 190, halfwidth, 20), sizeStyle='regular', callback=self.update)
		self.paletteView.group.carRight = EditText(((halfwidth+20), 190, halfwidth, 20), sizeStyle='regular', callback=self.update)
		self.paletteView.group.myList = PopUpButton((10, 220, -10, 18),["English", "French"],sizeStyle='small', callback=self.update)
		self.paletteView.group.myButton = Button((10, 250, -10, 20), "Generate", callback=self.update)
		self.dialog = self.paletteView.group.getNSView()
	
	@objc.python_method
	def __del__(self):
		Glyphs.removeCallback(self.update)
	
	@objc.python_method
	def update( self, sender ):
		lang = self.paletteView.group.myList.getItem()
		lang = str(lang).replace('[{','').replace('}]','').replace(';','').replace('\n','').replace('value = ', '')
		with open(os.path.join(os.path.dirname(__file__), "dico_"+lang+".json"), "r") as read_file:
			dictionary = json.load(read_file)
		wordcase = self.paletteView.group.radioGroup.get()
		wordlength = int(self.paletteView.group.slider.get())
		lineslength = int(self.paletteView.group.slider2.get())
		tolerance = int(self.paletteView.group.slider3.get())
		beforecar = str(self.paletteView.group.carLeft.get())
		aftercar = str(self.paletteView.group.carRight.get())
		tabText = ''
		desiredLength = wordlength*400
		line = 0
		while line < lineslength:
			randomchoice = random.sample(list(dictionary['1']), k=1 )
			for word in randomchoice:
				if wordcase == 0:
					word = word.lower()
				elif wordcase == 1:
					word = word.upper()
				else:
					word = word.capitalize()
				wordwidth = 0
				for letter in list(word):
					letterwWidth = Glyphs.font.glyphs[str(letter)].layers[Glyphs.font.selectedFontMaster.id].width
					wordwidth += letterwWidth
				if wordwidth >= desiredLength and wordwidth < desiredLength+tolerance:
					tabText += str(beforecar)+word+str(aftercar)+'\n'
					line += 1
				else:
					continue
		Glyphs.font.currentTab.text = tabText

	@objc.python_method
	def __file__(self):
		"""Please leave this method unchanged"""
		return __file__
	
	# Temporary Fix
	# Sort ID for compatibility with v919:
	_sortID = 4
	@objc.python_method
	def setSortID_(self, id):
		try:
			self._sortID = id
		except Exception as e:
			self.logToConsole( "setSortID_: %s" % str(e) )
	
	@objc.python_method
	def sortID(self):
		return self._sortID
	