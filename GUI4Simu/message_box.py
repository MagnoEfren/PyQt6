
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6.uic import loadUi 
from PyQt6 import QtCore, QtWidgets
import sys

from message import Ui_MainWindow

class CustomMessageBox(QMainWindow,Ui_MainWindow):
	def __init__(self,titulo, texto):
		super().__init__()
		self.setupUi(self)
		# Eliminar barra de titulo y opacidad
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setWindowOpacity(1)
		self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.label_texto_aviso.setText(texto)
		self.titulo_label_aviso.setText(titulo)

			
if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_app = CustomMessageBox()
	my_app.show()	
	sys.exit(app.exec_())
