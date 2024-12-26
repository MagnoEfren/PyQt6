
#  - #7f5af0
# rgb(17, 17, 17);  - #111111
# rgb(44, 44, 44);  - #2c2c2c 

from PyQt6.QtWidgets import QMainWindow, QApplication, QFileDialog
from PyQt6.uic import loadUi 
from PyQt6 import QtCore, QtWidgets,QtGui
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar   # NavigationToolbar2QT 

from PyQt6.QtCore import QUrl, Qt 
from PyQt6.QtGui import QDesktopServices, QPalette

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, pyqtProperty
from PyQt6.QtWidgets import QStackedWidget

import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import numpy as np
import cmath
import pandas as pd
import sys
###########
#from PyQt5.QtWidgets import QApplication, QMessageBox
from message_box import CustomMessageBox
from information import Ui_Informacion
from design import Ui_Design

###  evitar errores ##############
import warnings
warnings.filterwarnings('ignore')
#############################


class App(QMainWindow, Ui_Design):
	def __init__(self, usuario):
		super().__init__()
		self.setupUi(self)

		self.usuario = usuario
		self.actionInformacion.triggered.connect(self.ventana_informacion)   
		self.actionFormulario.triggered.connect(self.ventana_formulario)
		self.actionGuiaAction.triggered.connect(self.ventana_guia)


		self.bt_iniciar_animacion.clicked.connect(self.control_iniciar_animacion)
		self.bt_reiniciar_animacion.clicked.connect(self.variables_entrada)
		self.bt_detener_animacion.clicked.connect(self.control_stop_animacion)
		self.bt_guardar_animacion.clicked.connect(self.guardar_animacion)		


		self.rbt_config_abierta.setChecked(True) #configuracion OPEN default
		self.rbt_analisis_posicion.setChecked(True) #  configuracion posicion analisis default
		self.in_velocindad_angular2.setEnabled(False)   # deshabilitados
		self.in_aceleracion_angular2.setEnabled(False)  # deshabilitados
		self.bt_grafica_w3.setEnabled(False) 
		self.bt_grafica_w4.setEnabled(False) 
		self.bt_grafica_vp.setEnabled(False) 
		self.bt_grafica_a_agular3.setEnabled(False) 
		self.bt_grafica_a_agular4.setEnabled(False) 

		##########		
		self.chb_sentido_antihorario.setChecked(True)
		self.step = 0.0055 # 364 valores               
		self.Len = 0   # Longitud BP acoplador verde
		self.Len_cg = self.Len   #longitud BP   barra morada 
		self.Angle = 0   # angulo en el punto P
		self.Angle_cg = self.Angle  # angulo barra   a   eslabon bc
		self.bord = 1000 
		self.y2 = 0
		self.theta2, self.theta3, self.theta4,self.alpha3,self.alpha4  = 0,0,0,0,0
		self.w3, self.w4, self.vpx, self.vpy, self.vA,self.vB =  0,0,0,0,0,0 

		self.x1,self.x2,self.x3,self.x4 = 0,0,0,0
		self.y1,self.y2,self.y3,self.y4 = 0,0,0,0
		self.xfg, self.yfg, self.xf,self.yf = 0,0,0,0

		self.repeat = 1  #1
		self.figure = plt.figure(dpi=100, facecolor='#0f0e17',frameon=True)
		self.ani = None
		self.valor_ani = False
		self.n = 0
		self.stop_tetha2 = False
		self.enviar_data_ad = [0,0,0,0,0,0]
		self.val_punto = [0,0,0,0,0,0,0]
		
		self.canvas = FigureCanvas(self.figure)
		self.layout_grafica_cinematica.addWidget(self.canvas)
		self.toolbar = NavigationToolbar(self.canvas, self.frame_grafica_cinematico)
		self.toolbar.hide()
		self.bt_inicio.clicked.connect(lambda: self.toolbar.home())
		#self.bt_izquierda.clicked.connect(lambda: self.toolbar.back()) 
		#self.bt_derecha.clicked.connect(lambda: self.toolbar.forward()) 
		self.bt_mover.clicked.connect(lambda: self.toolbar.pan())
		self.bt_zoom.clicked.connect(lambda: self.toolbar.zoom("in"))
		#self.bt_zoom_out.clicked.connect(lambda: self.toolbar.zoom("out"))      # Zoom out
		self.bt_ajustes.clicked.connect(lambda: self.toolbar.configure_subplots())    
		self.bt_personalizar.clicked.connect(lambda: self.toolbar.edit_parameters())  
		self.bt_guardar_imagen.clicked.connect(lambda: self.toolbar.save_figure())

		########### graficas velociad ##################
		self.bt_grafica_w3.clicked.connect(self.grafica_velocidad_w3)
		self.bt_grafica_w4.clicked.connect(self.grafica_velocidad_w4)
		self.bt_grafica_vp.clicked.connect(self.grafica_velocidad_vp)  

		# aceleracion
		self.bt_grafica_a_agular3.clicked.connect(self.grafica_aceleracion_alpha3) 
		self.bt_grafica_a_agular4.clicked.connect(self.grafica_aceleracion_alpha4) 
		########### pestañas ###########


		########### gurardar datos en excel ###############
		self.bt_guardar_data.clicked.connect(self.guardar_data)
		

		#self.tabWidget.tabBarClicked.connect(self.pestanna_grashof)
		self.rbt_analisis_posicion.toggled.connect(self.seleccionar_analisis_posicion) 
		self.rbt_analisis_velocidad.toggled.connect(self.seleccionar_analisis_velocidad) 
		self.rbt_analisis_aceleracion.toggled.connect(self.seleccionar_analisis_aceleracion) 
		self.rbt_analisis_dinamico.toggled.connect(self.analisis_dinamico_check) 

		########VENTANAS CONTROL INFERIORES #####################
		self.figure_w3 = plt.figure(dpi=100, facecolor='#0f0e17',frameon=True) #dpi=100, facecolor='#0f0e17',frameon=True
		self.canvas_w3 = FigureCanvas(self.figure_w3)
		self.layout_grafica_w3.addWidget(self.canvas_w3)

		self.ax_w3 = self.figure_w3.add_subplot(111)
		self.ax_w3.set_title("Gráfica  ω3 vs  θ2", color='#7f5af0')
		self.ax_w3.set_xlabel("θ2  [°]", color ='#7f5af0' )
		self.ax_w3.set_ylabel("ω3 [ rad/s]", color ='#7f5af0')
		self.ax_w3.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 
		self.ax_w3.grid ()

		self.figure_w4 = plt.figure(dpi=100, facecolor='#0f0e17',frameon=True)
		self.canvas_w4 = FigureCanvas(self.figure_w4)
		self.layout_grafica_w4.addWidget(self.canvas_w4)
		self.ax_w4 = self.figure_w4.add_subplot(111)
		self.ax_w4.set_title("Gráfica  ω4 vs  θ2" , color='#7f5af0')
		self.ax_w4.set_xlabel("θ2  [°]", color ='#7f5af0')
		self.ax_w4.set_ylabel("ω4 [ rad/s]", color ='#7f5af0')
		self.ax_w4.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 		
		self.ax_w4.grid ()


		self.figure_vp = plt.figure(dpi=100, facecolor='#0f0e17',frameon=True)
		self.canvas_vp = FigureCanvas(self.figure_vp)
		self.layout_grafica_vp.addWidget(self.canvas_vp)
		self.ax_vp = self.figure_vp.add_subplot(111)
		self.ax_vp.set_title("Gráfica  Vp vs  θ2", color='#7f5af0')
		self.ax_vp.set_xlabel("θ2  [ ° ]", color ='#7f5af0')
		self.ax_vp.set_ylabel("Vp [ m/s]", color ='#7f5af0')	
		self.ax_vp.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 	
		self.ax_vp.grid()

		self.figure_oo3 = plt.figure(dpi=100, facecolor='#0f0e17',frameon=True)
		self.canvas_oo3 = FigureCanvas(self.figure_oo3)
		self.layout_grafica_a_agular3.addWidget(self.canvas_oo3)
		self.ax_oo3 = self.figure_oo3.add_subplot(111)
		self.ax_oo3.set_title("Gráfica  Vp vs  θ2", color='#7f5af0')
		self.ax_oo3.set_xlabel("θ2  [ ° ]", color ='#7f5af0')
		self.ax_oo3.set_ylabel("Vp [ m/s]", color ='#7f5af0')	
		self.ax_oo3.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 	
		self.ax_oo3.grid()

		self.figure_oo4 = plt.figure(dpi=100, facecolor='#0f0e17',frameon=True)
		self.canvas_oo4 = FigureCanvas(self.figure_oo4)
		self.layout_grafica_a_agular4.addWidget(self.canvas_oo4)
		self.ax_oo4 = self.figure_oo4.add_subplot(111)
		self.ax_oo4.set_title("Gráfica  Vp vs  θ2")
		self.ax_oo4.set_xlabel("θ2  [ ° ]")
		self.ax_oo4.set_ylabel("Vp [ m/s]")		
		self.ax_oo4.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 	
		self.ax_oo4.grid()		

		#self.foto_mecanismo.setScaledContents(True)
		#self.foto_mecanismo.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
		####################### GRAFICAS DINAMICA #########################################


		#self.bt_datos_dinamica.clicked.connect(lambda:Dinamica().variables_entrada_dinamica(
		#	self.spinBox_l1D.value(), self.spinBox_l2D.value(),self.spinBox_l3D.value(),
		#	self.spinBox_l4D.value(), 6))

		##### grafica #####
		self.figure_ad = plt.figure(dpi=100, facecolor='#0f0e17',frameon=True)		
		self.canvas_ad = FigureCanvas(self.figure_ad)
		self.layout_grafica_dinamico.addWidget(self.canvas_ad)	 
		self.ax_ad = self.figure_ad.add_subplot(111)
		self.ax_ad.set_title("Mecanismo", color='#7f5af0')
		self.ax_ad.set_xlabel("X [mm]", color ='#7f5af0' )
		self.ax_ad.set_ylabel("Y [mm]", color ='#7f5af0')
		self.ax_ad.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 
		self.ax_ad.grid()
		



		self.bt_graficar_ad.clicked.connect(self.grafica_analisis_dinamico)  
		self.bt_calcular_data.clicked.connect(self.calcular_analisis_dinamico) 

		

		#########################  INTRODUCCION  ################################
		self.dark_theme = False
		self.bt_cambiar_modo.clicked.connect(self.change_style)
		self.graficar_grid()
		#AnimatedStackedWidget(self.stackedWidget)
		

	def change_style(self):
		if self.dark_theme:
			self.bt_cambiar_modo.setIcon(QtGui.QIcon("images/sun.svg"))
			dark = """color:white; font: 12pt 'SansSerif'; background:#0f0e17;"""
			self.frame_introduccion.setStyleSheet(dark)
			self.dark_theme = False
		else:
			self.bt_cambiar_modo.setIcon(QtGui.QIcon("images/moon.svg"))
			ligh = """color:#0f0e17; font: 12pt 'SansSerif'; background: white;"""
			self.frame_introduccion.setStyleSheet(ligh)
			self.dark_theme = True

	def seleccionar_analisis_posicion(self, checked):
		if checked:
			self.in_velocindad_angular2.setEnabled(False)
			self.in_aceleracion_angular2.setEnabled(False)
			self.bt_grafica_w3.setEnabled(False) 
			self.bt_grafica_w4.setEnabled(False) 
			self.bt_grafica_vp.setEnabled(False) 
			self.bt_grafica_a_agular3.setEnabled(False) 
			self.bt_grafica_a_agular4.setEnabled(False) 
	def seleccionar_analisis_velocidad(self, checked):
			self.in_velocindad_angular2.setEnabled(True)
			self.in_aceleracion_angular2.setEnabled(False)			
			self.bt_grafica_w3.setEnabled(True) 
			self.bt_grafica_w4.setEnabled(True) 
			self.bt_grafica_vp.setEnabled(True) 
			self.bt_grafica_a_agular3.setEnabled(False) 
			self.bt_grafica_a_agular4.setEnabled(False) 			
	def seleccionar_analisis_aceleracion(self, checked):
			self.in_velocindad_angular2.setEnabled(True)
			self.in_aceleracion_angular2.setEnabled(True)
			self.bt_grafica_w3.setEnabled(True) 
			self.bt_grafica_w4.setEnabled(True) 
			self.bt_grafica_vp.setEnabled(True) 
			self.bt_grafica_a_agular3.setEnabled(True) 
			self.bt_grafica_a_agular4.setEnabled(True) 

	def analisis_dinamico_check(self, checked):
		self.ventan4 = CustomMessageBox('Advertencia', "Debe ingresar un valor de θ2 que se encuentre en el rango para hacer el análisis dinámico")
		self.ventan4.setWindowFlags(self.ventan4.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
		self.ventan4.show()	


	def control_stop_animacion(self):
		self.ani.event_source.stop() 
		self.bt_detener_animacion.setEnabled(False)
		self.bt_reiniciar_animacion.setEnabled(True)

	def control_iniciar_animacion(self):
		self.stop_tetha2 = False
		self.variables_entrada()
		self.iniciar_animacion()
		self.bt_detener_animacion.setEnabled(True)
		self.bt_iniciar_animacion.setEnabled(False)	
		self.bt_reiniciar_animacion.setEnabled(False)	

	def ventana_informacion(self):
		self.Informacion = QtWidgets.QWidget()
		self.ui = Ui_Informacion()
		self.ui.setupUi(self.Informacion)
		self.Informacion.show()

	def ventana_guia(self):
		url = QUrl("https://proyec4simu.herokuapp.com/")
		QDesktopServices.openUrl(url)

	def ventana_formulario(self):
		url = QUrl("https://forms.gle/gSSsYjNAdVNBMWGy5")
		QDesktopServices.openUrl(url)

	def verificar_ley_grashof(self):
		a = self.L2.value() # manivela
		b = self.L3.value()  # acoplador
		c = self.L4.value()   # balancin
		d = self.L1.value()   # bancada
		L, P, Q, S = sorted([a,b,c,d])

		max_v = max(a, b, c, d)
		if max_v == a:
			masL = "L2"
		elif max_v == b:
			masL = "L3"
		elif max_v == c:
			masL = "L4"
		else:
			masL = "L1"
		valores3 = 0
		if masL == 'L1':
			valores3 = a + b + c - 1
		elif masL == 'L2':
			valores3 = b + c + d - 1
		elif masL == 'L3':
			valores3 = a + d + c - 1
		else:
			valores3 = a + b + d - 1
		if L + S < P + Q:
			self.indicador_tipo_grasof.setText('Grashof: CLASE I')
		elif L + S == P + Q:
			self.indicador_tipo_grasof.setText('Grashof Especial : CLASE III')
		else:
			self.indicador_tipo_grasof.setText('No Grashof: CLASE II')

		if (L**2+ P**2+ Q**2 > (S**2)/3) and (L**4+P**4+Q**4 >= (S**4)/27):
			if L+P+Q == S:
				self.ventan1 = CustomMessageBox(f'Error de Parámetro', f" {self.usuario}: Es una estructura estatica {round(L,3)}+{round(P,3)}+{round(Q,3)} = {round(S,3)}")
				self.ventan1.setWindowFlags(self.ventan1.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
				self.ventan1.show()
		else:
			self.ventan2 = CustomMessageBox(f'Error de Parámetro', f" {self.usuario}:  Las longitudes de los eslabones  forman una CADENA ABIERTA, porfavor, intente con valores en este rango: {masL} <= {valores3}")
			self.ventan2.setWindowFlags(self.ventan2.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
			self.ventan2.show()

	def variables_entrada(self):
		self.bt_detener_animacion.setEnabled(True)
		self.bt_guardar_animacion.setEnabled(True)
		self.bt_iniciar_animacion.setEnabled(False)
		if self.valor_ani == True:		
			self.ani.event_source.start()
		a = self.L2.value() # manivela
		b = self.L3.value()  # acoplador
		c = self.L4.value()   # balancin
		d = self.L1.value()   # bancada
		#
		self.verificar_ley_grashof()
		self.grafica_grashof(a,b,c,d)

	def graficar_grid(self):
		temp = self.x1,self.x2,self.x3,self.x4
		xmin = np.amin([np.amin(mini) for mini in temp])
		xmax = np.amax([np.amax(mini) for mini in temp])
		temp = self.y1,self.y2,self.y3,self.y4
		ymin = np.amin([np.amin(mini) for mini in temp])
		ymax = np.amax([np.amax(mini) for mini in temp])
		self.ax = self.figure.add_subplot(1, 1, 1, autoscale_on=True , xlim=(xmin-self.bord, xmax+self.bord), 
			ylim=(ymin-self.bord, ymax+self.bord)) 
		self.ax.axhline(linewidth=2, color='#7f5af0')
		self.ax.axvline(linewidth=2, color='#7f5af0')
		self.ax.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 
		self.ax.set_title('GRAFICA MECANISMO DE 4 BARRAS', color='#7f5af0')


		self.line, = self.ax.plot([], [], marker = 'o',c = 'k',lw = 6,ms = 10)
		self.line2, = self.ax.plot([], [], marker = 'o',c = 'g',lw = 6,ms = 4)
		self.line3, = self.ax.plot([], [], marker = 'x',c = 'm',lw = 5,ms = 20)
		self.recorrido, = self.ax.plot([],[], c = 'r', lw = 2, ms = 2, linestyle='dashed')
		self.text_theta2 = self.ax.text(0.02, 0.95, '', transform = self.ax.transAxes)
		self.line.set_data([],[])
		self.line2.set_data([],[])
		self.line3.set_data([],[])	
		self.recorrido.set_data([], [])	
		#major_ticks_top=np.linspace(-self.bord,self.bord, int(self.bord/50)+1)
		#minor_ticks_top=np.linspace(-self.bord,self.bord, int(self.bord/50)+1)
		#self.ax.set_xticks(major_ticks_top)
		#self.ax.set_yticks(major_ticks_top)
		#self.ax.set_xticks(minor_ticks_top, minor=True)
		#self.ax.set_yticks(minor_ticks_top, minor=True)	
		self.ax.grid ()
		self.figure.canvas.draw()

	def grafica_grashof(self,a,b,c,d):
		if not self.chb_pausa_tetha2.isChecked():
			self.stop_tetha2 = False
		elif self.chb_pausa_tetha2.isChecked():
			self.stop_tetha2 = True

		if not self.chb_sentido_antihorario.isChecked():
			self.theta2 = np.arange(2*np.pi,0,- self.step*np.pi)
		elif self.chb_sentido_antihorario.isChecked():
			self.theta2 = np.arange(0,2*np.pi, self.step*np.pi)
		
		self.b = b
		K1 = d/a
		K2 = d/c
		K3 = (a*a -b*b +c*c +d*d )/(2.0*a*c)
		A = np.cos(self.theta2) - K1 - K2*np.cos(self.theta2) + K3
		B = -2*np.sin(self.theta2)
		C = K1 - (K2+1)*np.cos(self.theta2) + K3

		disc = (B*B)-4*A*C 
		if not(np.greater_equal(disc, 0).all()):
			condition = np.greater_equal(disc,0)

			self.theta2 = np.extract(condition, self.theta2)
			condition = np.less_equal(self.theta2, np.pi)
			self.theta2 = np.extract(condition,self.theta2)

			self.theta2 = np.tile(np.r_[self.theta2,np.flipud(self.theta2)], self.repeat)

			#ubdate A,B,C
			A = np.cos(self.theta2) - K1 - K2*np.cos(self.theta2) + K3
			B = -2*np.sin(self.theta2)
			C = K1 - (K2+1)*np.cos(self.theta2) + K3
			disc = (B*B)-4*A*C

		if self.rbt_config_abierta.isChecked():
			self.theta4 = 2*np.arctan((-B - np.sqrt((B*B)-4*A*C) )/(2*A))
		elif self.rbt_config_cruzada.isChecked(): #closed
			self.theta4 = 2*np.arctan((-B + np.sqrt((B*B)-4*A*C) )/(2*A))	

		th_d = -np.pi*np.ones(len(self.theta4))
		phase1 = [cmath.exp(1j*i) for i in self.theta2]
		phase3 = [cmath.exp(1j*i) for i in self.theta4]
		phase4 = [cmath.exp(1j*i) for i in th_d]

		R1 = a*np.array(phase1)
		R3 = c*np.array(phase3)
		R4 = -d*np.array(phase4)

		self.x1,self.y1 = np.zeros(len(R1)),np.zeros(len(R1))
		self.x2,self.y2 = np.real(R1),np.imag(R1)
		self.x3,self.y3 = np.real(R3+R4),np.imag(R3+R4)
		self.x4,self.y4 = np.real(R4),np.imag(R4)

		self.theta3 = np.arctan2((self.y3-self.y2),(self.x3-self.x2))
		phase2 = [cmath.exp(1j*i) for i in self.theta3]
		R2 = b*np.array(phase2)

		#Creando el ángulo del seguidor con respecto al suelo
		f_d = self.Angle*np.pi/180*np.ones(len(self.theta2))
		f_d += self.theta3
		f_dCG = self.Angle_cg*np.pi/180*np.ones(len(self.theta2))
		f_dCG += self.theta3
		#Tamaño del seguidor
		f = self.Len 
		fCG = self.Len_cg 

		#Fase de seguidor
		phasef = [cmath.exp(1j*i) for i in f_d]
		Rf = R1+ f*(np.array(phasef))
		self.xf, self.yf = np.real(Rf),np.imag(Rf)

		#Fase del centro de gravedad del seguidor
		phasef_CG = [cmath.exp(1j*i) for i in f_dCG]
		Rf_CG = R1 + fCG*(np.array(phasef_CG))
		self.xfg, self.yfg = np.real(Rf_CG), np.imag(Rf_CG)


		#  Calculo de la velocidades
		w2 = (self.in_velocindad_angular2.value()*2*np.pi/60)
		self._w2 = w2
		self.w3 = (a*w2*np.sin(np.subtract(self.theta4, self.theta2)))/(b*np.sin(np.subtract(self.theta3, self.theta4)))
		self.w4 = (a*w2*np.sin(np.subtract(self.theta2, self.theta3)))/(c*np.sin(np.subtract(self.theta4, self.theta3)))

		self.vpx = (w2*(a/1000)*np.sin(self.theta2)) + (-self.L_acoplador.value()/1000)*self.w3*np.sin(np.add(self.theta3, (np.pi*self.A_acoplador.value()/180) ))
		self.vpy =  (w2*(a/1000)*np.cos(self.theta2)) + (self.L_acoplador.value()/1000)*self.w3*np.cos(np.add(self.theta3, (np.pi*self.A_acoplador.value()/180) ))

		self.vA = self.theta2*(a/1000)
		self.vB =  self.theta4*(c/1000)

		#  Calculo de la aceleraciones
		A1 = (c/1000)*np.sin(self.theta4) 
		B1 = (b/1000)*np.sin(self.theta3)
		C1 = (a/1000)*(self.in_aceleracion_angular2.value())*np.sin(self.theta2) + (a/1000)*((w2)**2)*(np.cos(self.theta2)) +  (b/1000)*((self.w3)**2)*(np.cos(self.theta3)) - (c/1000)*((self.w4)**2)*(np.cos(self.theta4))

		D1 = (c/1000)*(np.cos(self.theta4))
		E1 = (b/1000)*(np.cos(self.theta3))
		F1 = (a/1000)*(self.in_aceleracion_angular2.value())*np.cos(self.theta2) - (a/1000)*((w2)**2)*(np.sin(self.theta2)) - (b/1000)*((self.w3)**2)*(np.sin(self.theta3)) + (c/1000)*((self.w4)**2)*(np.sin(self.theta4))

		self.alpha3 = (C1*D1 - A1*F1)/(E1*A1 - B1*D1)
		self.alpha4 = (C1*E1 - B1*F1)/(A1*E1 - B1*D1)

	def polar_to_cartesian(self, r, theta):
		x = r * np.cos(theta)
		y = r * np.sin(theta)
		return np.array([x, y])

	def init(self):
		self.line.set_data([],[])
		self.line2.set_data([],[])
		self.line3.set_data([],[])
		self.recorrido.set_data([], [])
		self.text_theta2.set_text('')
		return self.line,self.line2,self.line3, self.recorrido, self.text_theta2

	def animate(self,i):
		try:
			thisx = [self.x1[i],self.x2[i],self.x3[i],self.x4[i]]
			thisy = [self.y1[i],self.y2[i],self.y3[i],self.y4[i]]
			self.line.set_data(thisx,thisy)

			thisx = [self.x2[i],self.xf[i],self.x3[i]]
			thisy = [self.y2[i],self.yf[i],self.y3[i]]
			self.line2.set_data(thisx,thisy)
			thisx = [self.x2[i],self.xfg[i]]
			thisy = [self.y2[i],self.yfg[i]]			
			self.line3.set_data(thisx,thisy)

			self.recorrido.set_data(self.xfg,self.yfg)
			theta2 =  np.rad2deg(self.theta2).astype(int)
			theta3 =  np.rad2deg(self.theta3).astype(int)
			theta4 =  np.rad2deg(self.theta4).astype(int)	

			#print(theta2[0], theta2[-1])
			# posicion
			self.out_p_angular2.setText(str(f'θ2 : {theta2[i]}°'))
			self.out_p_angular3.setText(str(f'θ3 : {theta3[i]}°'))
			self.out_p_angular4.setText(str(f'θ4 : {theta4[i]}°'))
			self.out_p_punto_px.setText(str(f'Px : {round(self.xfg[i],2)}'))
			self.out_p_punto_py.setText(str(f'Py : {round(self.yfg[i],2)}'))
			## velocidad 
			self.out_v_angular3.setText(str(f'ω3 : {round(self.w3[i],2)}')) 
			self.out_v_angular4.setText(str(f'ω4 : {round(self.w4[i],2)}')) 

			self.out_v_punto_px.setText(str(f'Vpx: {round(self.vpx[i],2)}'))
			self.out_v_punto_py.setText(str(f'Vpy : {round(self.vpy[i],2)}'))

			self.out_v_linealA.setText(str(f'VA : {round(self.vA[i],2)}'))
			self.out_v_linealB.setText(str(f'VB : {round(self.vB[i],2)}'))

			# aceleracion self.alpha3
			self.out_a_angular3.setText(str(f'{round(self.alpha3[i],2)}'))
			self.out_a_angular4.setText(str(f'{round(self.alpha4[i],2)}'))

			if self.stop_tetha2:
				if int(theta2[i]) == int(self.in_tetha2.value()):
					self.ani.event_source.stop()

			#lim_in = theta2[0]
			#lim_sup = theta2[-1]
			#print(lim_in, lim_sup)

			#definimos las variables
			x = self.b/1000
			angulo = np.add(np.radians(self.A_acoplador.value()), self.theta3[i])
			R_AO = self.polar_to_cartesian(x, self.theta2[i])
			R_PA = self.polar_to_cartesian(x, angulo)			
			#Aceleracion de A
			A_A = (np.cross(np.array([0, 0, self.in_aceleracion_angular2.value()]),np.array([R_AO[0], R_AO[1], 0])))-((self._w2**2) * np.array([R_AO[0], R_AO[1], 0]))
			#Aceleracion de P respecto a A
			A_PA = (np.cross(np.array([0, 0, self.alpha3[i]]),np.array([R_PA[0], R_PA[1], 0])))-((self.w3[i]**2) * np.array([R_PA[0], R_PA[1], 0]))
			#Aceleracion de P
			A_P = A_A + A_PA
			self.Apx = A_P[0]
			self.Apy = A_P[1]
			self.out_a_px.setText(str(f'{round(self.Apx,4)}'))
			self.out_a_py.setText(str(f'{round(self.Apy,4)}'))
			#self.Ap = (self.Apx**2 + self.Apy**2)**(1/2)
			if self.rbt_analisis_dinamico.isChecked():
				if int(theta2[i]) == int(self.in_tetha2.value()):
					self.ani.event_source.stop()
					self.enviar_data_ad[0] = theta3[i]
					self.enviar_data_ad[1] = theta4[i]
					self.enviar_data_ad[2] = self.w3[i]
					self.enviar_data_ad[3] = self.w4[i]
					self.enviar_data_ad[4] = self.alpha3[i]
					self.enviar_data_ad[5] = self.alpha4[i]
		except IndexError:
			pass
			#print('ERROR EN EL INDEX')

		self.text_theta2.set_text('i = %.1f' % i)
		self.Len = self.L_acoplador.value()
		self.Angle  = self.A_acoplador.value()
		self.Len_cg = self.Len
		self.Angle_cg = self.Angle 
		return self.line, self.line2, self.line3,self.recorrido, self.text_theta2 

	def iniciar_animacion(self):
		self.valor_ani = True
		self.ani = animation.FuncAnimation(self.figure, self.animate, np.arange(1, (len(self.y2))),
                              interval=30, blit=True,init_func=self.init, save_count=10)  #, 
		#self.canvas.draw()

	def guardar_animacion(self):
		try:
			filename = QFileDialog.getSaveFileName(None,"Save File", "", "Video Files (*.mp4);;All Files (*)")[0]
			if len(filename) != 0:
				self.ani.save(filename, writer='ffmpeg')
				self.ventan5 = CustomMessageBox('Video guardado correctamente', "Datos Guardados")
				self.ventan5.setWindowFlags(self.ventan5.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
				self.ventan5.show()
			else:
				self.ventan7 = CustomMessageBox('Error al guardar', "Porfavor  escriba un nombre al video")
				self.ventan7.setWindowFlags(self.ventan7.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
				self.ventan7.show()

		except Exception as e:
			self.ventan6 = CustomMessageBox('Error al guardar', "Inicie la animación y pause y vuelva a guardar")
			self.ventan6.setWindowFlags(self.ventan6.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
			self.ventan6.show()

	def grafica_velocidad_w3(self, event):
		self.stackedWidget.setCurrentWidget(self.page_grafica_w3)	
		x = np.rad2deg(self.theta2).astype(int)
		y = self.w3
		self.ax_w3.clear()
		self.ax_w3.grid()
		self.ax_w3.set_title("Gráfica  ω3 vs  θ2", color='#7f5af0')
		self.ax_w3.set_xlabel("θ2  [°]", color ='#7f5af0' )
		self.ax_w3.set_ylabel("ω3 [ rad/s]", color ='#7f5af0')		
		self.line_w3 = self.ax_w3.plot(x, y, color ='#7f5af0')
		self.canvas_w3.draw()

	def grafica_velocidad_w4(self, event):
		self.stackedWidget.setCurrentWidget(self.page_grafica_w4)
		x = np.rad2deg(self.theta2).astype(int)
		y =  self.w4 
		self.ax_w4.clear()
		self.ax_w4.grid()
		self.ax_w4.set_title("Gráfica  ω4 vs  θ2" , color='#7f5af0')
		self.ax_w4.set_xlabel("θ2  [°]", color ='#7f5af0')
		self.ax_w4.set_ylabel("ω4 [ rad/s]", color ='#7f5af0')	
		self.ax_w4.plot(x, y, color ='#7f5af0')
		self.canvas_w4.draw()

	def grafica_velocidad_vp(self, event):
		self.stackedWidget.setCurrentWidget(self.page_grafica_vp)		
		x = np.rad2deg(self.theta2).astype(int) 
		y = ((self.vpx)**2 +(self.vpy)**2)**(1/2)
		self.ax_vp.clear()
		self.ax_vp.plot(x, y, color ='#7f5af0')
		self.ax_vp.set_title("Gráfica  Vp vs  θ2", color='#7f5af0')
		self.ax_vp.set_xlabel("θ2  [ ° ]", color ='#7f5af0')
		self.ax_vp.set_ylabel("Vp [ m/s]", color ='#7f5af0')		
		self.ax_vp.grid()
		self.canvas_vp.draw()		
	
	def grafica_aceleracion_alpha3(self, event):
		self.stackedWidget_2.setCurrentWidget(self.page_grafica_a_agular3)		
		x = np.rad2deg(self.theta2).astype(int) 
		y = self.alpha3
		self.ax_oo3.clear()
		self.ax_oo3.plot(x, y)
		self.ax_oo3.set_title("Gráfica  α3 vs  θ2", color='#7f5af0')
		self.ax_oo3.set_xlabel("θ2  [ ° ]", color ='#7f5af0')
		self.ax_oo3.set_ylabel("α3 [ rad/s2]]", color ='#7f5af0')		
		self.ax_oo3.grid()
		self.canvas_oo3.draw()
	
	def grafica_aceleracion_alpha4(self, event):
		self.stackedWidget_2.setCurrentWidget(self.page_grafica_a_agular4)		
		x = np.rad2deg(self.theta2).astype(int) 
		y = self.alpha4
		self.ax_oo4.clear()
		self.ax_oo4.plot(x, y)
		self.ax_oo4.set_title("Gráfica  α4 vs  θ2", color='#7f5af0')
		self.ax_oo4.set_xlabel("θ2  [ ° ]", color ='#7f5af0')
		self.ax_oo4.set_ylabel("α4 [ rad/s2]", color ='#7f5af0')		
		self.ax_oo4.grid()
		self.canvas_oo4.draw()	

	def guardar_data(self):
		#if not self.radioB_data_tetha2.isChecked():
		array_t2 = self.theta2
		array_t3 = self.theta3
		array_t4 = self.theta4
		array_w3 = self.w3
		array_w4 = self.w4
		array_vp = ((self.vpx)**2 +(self.vpy)**2)**(1/2)
		array_oo3 = self.alpha3
		array_oo4 = self.alpha4
		try:
			df = pd.concat([pd.DataFrame(array_t2), pd.DataFrame(array_t3), pd.DataFrame(array_t4), 
				pd.DataFrame(array_w3),pd.DataFrame(array_w4),pd.DataFrame(array_vp),
				pd.DataFrame(array_oo3),pd.DataFrame(array_oo4)], axis=1)
			# Renombrar las columnas
			df.columns = ['Theta2', 'Theta3', 'Theta4','W3', 'W4', 'Vp','Alpha3', 'Alpha3']

			try:
			
				filename = QFileDialog.getSaveFileName(None,"Save File", "", "Excel Files (*.xlsx);;All Files (*)")[0]
				if len(filename) != 0:
					df.to_excel(filename, index=True)
					self.ventan30 = CustomMessageBox('Archivo guardado correctamente', "Datos Guardados")
					self.ventan30.setWindowFlags(self.ventan30.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
					self.ventan30.show()
				else:
					self.ventan31 = CustomMessageBox('Error al guardar', "Porfavor ingrese un nombre para el archivo")
					self.ventan31.setWindowFlags(self.ventan31.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
					self.ventan31.show()
			except Exception as e:
				pass
		except Exception as e:
			self.ventan43 = CustomMessageBox('Error al guardar el archivo', "Primero Ejecute la animacion para obtener los datos")
			self.ventan43.setWindowFlags(self.ventan43.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
			self.ventan43.show()

	#####################
	def calcular_analisis_dinamico(self):
		a = self.L2.value()/1000 # manivela
		b = self.L3.value()/1000  # acoplador
		c = self.L4.value()/1000   # balancin
		d = self.L1.value()/1000   # bancada

		L = self.L_acoplador.value()/1000
		delta = self.A_acoplador.value()

		theta2 = self.in_tetha2.value()
		theta3 = self.enviar_data_ad[0]  #
		theta4 = self.enviar_data_ad[1]  #

		w2 = (self.in_velocindad_angular2.value()*2*np.pi/60)
		w3 = self.enviar_data_ad[2]  #
		w4 = self.enviar_data_ad[3]  #

		alpha2 = self.in_aceleracion_angular2.value()
		alpha3 = self.enviar_data_ad[4] # 
		alpha4 = self.enviar_data_ad[5]  #

		self.val_punto = [ theta2, theta3,theta4, w3, w4, alpha3, alpha4]

		#m1 = 0kg
		m2 = self.doubleSpinBox_l2D.value()
		m3 = self.doubleSpinBox_l3D.value()
		m4 = self.doubleSpinBox_l4D.value()

		# Fuerza en P y thetap
		thetap = self.in_anguloP.value()
		FP = self.in_FuerzaP.value()

		CG2  = (a/2)   # metros
		CG3 = ((((L)*np.cos(delta) + b)/3)**2 + (((L)*np.sin(delta))/3)**2)**(1/2)
		CG4 = (c/2)  # metros


		IG2 = round((m2/12)*(w2**2 + a**2),4)
		IG3 = round((m3/6)*(b**2 + (L*np.sin(delta))**2),4)
		IG4 = round((m4/12)*(w4**2 + c**2),4)


		RCG2 = a/2
		RCG3X = (((L)*np.cos(delta) + a)/3)**2
		RCG3Y = (((L)*np.sin(delta))/3)**2
		RCG3 = ((((L)*np.cos(delta) + b)/3)**2 + (((L)*np.sin(delta))/3)**2)**(1/2)
		RCG4 = c/2   ##  ENCONTRAR AUN

		delta33 = np.degrees(np.arctan2(RCG3X , RCG3Y)) ###### 1 #######


		self.IG2.setText(str(IG2))   # colocando los momentos de inercia en el Label
		self.IG3.setText(str(IG3))
		self.IG4.setText(str(IG4))

		######  rediovectores  ###########
		R12X = CG2*np.cos(theta2 + 180)
		R12Y = CG2*np.sin(theta2 + 180)
		R32X = CG2*np.cos(theta2)
		R32Y = CG2*np.sin(theta2)
		R23X = CG3*np.cos(theta3 + delta33 + 180)
		R23Y = CG3*np.sin(theta3 + delta33 + 180)
		R43X = b*np.cos(theta3) - CG3*np.cos(theta3 + delta33)
		R43Y = -(CG3*np.sin(theta3 + delta33)- b*np.sin(theta3))
		R34X = RCG4*np.cos(theta4)
		R34Y = RCG4*np.cos(theta4)
		R14X = RCG4*np.cos(theta4 + 180)
		R14Y = RCG4*np.cos(theta4 + 180)
		RPX = L*np.cos(theta3 + delta) - np.abs(R23X)
		RPY = L*np.sin(theta3 + delta) - np.abs(R23Y)
		########## fuerza en N aplicada en el punto P
		FPX = FP*np.cos(thetap)
		FPY = FP*np.sin(thetap)
		######  Aceleraciones  ###########
		AG2 = CG2*alpha2*(((-np.sin((theta2))))+(1j*np.cos((theta2))))-(a*(w2**2)*(np.cos((theta2))+(1j*np.sin((theta2)))))
		AG2X = np.real(AG2)
		AG2Y = np.imag(AG2)
		A_A = (a*alpha2*((-np.sin(theta2))+(1j*np.cos(theta2))))-(a*(w2**2)*(np.cos(theta2)) + 1j*np.sin((theta2)))
		ACG3_A = CG3*alpha3*((-np.sin((theta3 + delta33)))+(1j*np.cos((theta3 + delta33))))+(-CG3*(w2**2)*(np.cos((theta3 + delta33))+(1j*np.sin((theta3 + delta33)))))
		AG3 = A_A + ACG3_A
		AG3X = np.real(AG3)
		AG3Y = np.imag(AG3)
		AG4 = (CG4*alpha4*((-np.sin(theta4))+(1j*np.cos(theta4)))) - (((c*(w4**2)*(np.cos(theta4)))+(1j*np.sin(theta4))))
		AG4X = np.real(AG4)
		AG4Y = np.imag(AG4)
		########## Matrixx
		# INGRESO
		A = np.zeros([9, 9]) 
		A[0] = [1, 0, 1, 0, 0,0,0,0,0]
		A[1] = [0, 1, 0, 1, 0,0,0,0,0]
		A[2] = [-R12Y, R12X, -R32Y,R32X, 0,0,0,0,1]
		A[3] = [0, 0, -1, 0, 1,0,0,0,0]
		A[4] = [0, 0, 0, -1, 0,1,0,0,0]
		A[5] = [0, 0, R23Y,-R23X, -R43Y,R43X,0,0,0]
		A[6] = [0, 0, 0, 0, -1,0,1,0,0]
		A[7] = [0, 0, 0, 0, 0,-1,0,1,0]
		A[8] = [0, 0, 0, 0, R34Y,-R34X,-R14Y,R14X,0]

		B = np.zeros([9, 1]) 
		B[0] = m2*AG2X
		B[1] = m2*AG2Y
		B[2] = IG2*alpha2
		B[3] = m3*AG3X-FPX
		B[4] = m3*AG3Y-FPY
		B[5] = IG3*alpha3-RPX*FPY+RPY*FPX
		B[6] = m4*AG4X
		B[7] = m4*AG4Y
		B[8] = IG4*alpha4

		x = np.linalg.solve(A, B)
		x = np.split(x, 9)
        ############### GRAFICA   ############
		self.F12X.setText(str(f'F12X: {round(x[0][0][0],2)} N'))
		self.F12Y.setText(str(f'F12Y: {round(x[1][0][0],2)} N'))
		self.F32X.setText(str(f'F12X: {round(x[2][0][0],2)} N'))
		self.F32Y.setText(str(f'F32Y: {round(x[3][0][0],2)} N'))
		self.F43X.setText(str(f'F43X: {round(x[4][0][0],2)} N'))
		self.F43Y.setText(str(f'F43Y: {round(x[5][0][0],2)} N'))
		self.F14X.setText(str(f'F14X: {round(x[6][0][0],2)} N'))
		self.F14Y.setText(str(f'F14Y: {round(x[7][0][0],2)} N'))
		self.T12.setText(str(f'T12: {round(x[8][0][0],2)} N.m'))
		self.ax_ad.tick_params(color = '#16161a', labelcolor = '#7f5af0', direction='out', length=2, width=2) 
		#x1 = 1*np.cos(thetap)
		#y1 = 1*np.sin(thetap)
		self.ax_ad.set_title("Variables de entrada", color='#7f5af0')
		self.ax_ad.set_xlabel("θ2 [°]", color ='#7f5af0')
		self.ax_ad.set_ylabel("", color ='#7f5af0')


	def grafica_analisis_dinamico(self):
		x = np.rad2deg(self.theta2).astype(int) 
		y1 = np.rad2deg(self.theta3).astype(int) 
		y2 = np.rad2deg(self.theta4).astype(int) 
		y3 = self.w3
		y4 = self.w4
		y5 = self.alpha3
		y6 = self.alpha4
		pos =  self.val_punto
		self.ax_ad.clear()
		self.ax_ad.plot(x, y1, label='θ3')
		self.ax_ad.plot(x, y2, label='θ4')
		self.ax_ad.plot(x, y3, label='ω3')
		self.ax_ad.plot(x, y4, label='ω4')
		self.ax_ad.plot(x, y5, label='α3')
		self.ax_ad.plot(x, y6, label='α4')
		self.ax_ad.scatter(pos[0], pos[1], marker='o')
		self.ax_ad.scatter(pos[0], pos[2], marker='o')
		self.ax_ad.scatter(pos[0], pos[3], marker='o')
		self.ax_ad.scatter(pos[0], pos[4], marker='o')
		self.ax_ad.scatter(pos[0], pos[5], marker='o')
		self.ax_ad.scatter(pos[0], pos[6], marker='o')
		self.ax_ad.set_autoscale_on(True)
		self.ax_ad.legend()
		self.ax_ad.grid()
		self.canvas_ad.draw()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	my_app = App()
	my_app.show()
	sys.exit(app.exec_())

