
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi 
from PyQt6 import QtCore, QtWidgets
import sys
import time 
from main_window_adc import App
import os
from start import Ui_MainWindow
#pyinstaller --windowed --onefile --icon=./icono.ico main.py

#  pyuic6 -x design.ui -o design.py
# pyuic6 -x information.ui -o information.py  
# pyuic6 -x message.ui -o message.py   
# pyuic6 -x start.ui -o start.py   


class MainApp(QMainWindow, Ui_MainWindow):
	def __init__(self):
		super().__init__()
		self.setupUi(self)
		self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
		self.setWindowOpacity(1)
		self.setWindowFlags(QtCore.Qt.WindowType.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)
		self.usuario = 'Usuario'
		self.bt_ingresar.clicked.connect(self.iniciar_sesion)
	
	def iniciar_sesion(self):
		self.usuario = self.nombre_usuario.text()
		for i in range(0,100):
			time.sleep(0.02)
			self.progressBar.setValue(i)
			if self.usuario == '':
				try:
					self.usuario = os.environ.get("USERNAME")
				except Exception as e:
					self.usuario = 'Usuario'
		self.hide()
		self.ventana = App(self.usuario)
		self.ventana.show() 
					
if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_app = MainApp()
	my_app.show()
	sys.exit(app.exec())

