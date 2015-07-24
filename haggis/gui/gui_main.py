import sys
from PyQt4 import QtGui, QtCore, uic

class gui_main(object):
    """description of class"""

 
class TestApp(QtGui.QMainWindow):
	def __init__(self):
		QtGui.QMainWindow.__init__(self)
		self.ui = uic.loadUi('hag/gui/test.ui')
		self.ui.show()


