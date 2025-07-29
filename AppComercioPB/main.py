import sys
from PyQt6.QtWidgets import  QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor
from  design import Ui_MainWindow
from PyQt6 import QtCore, QtWidgets,QtGui
from fpdf import FPDF
import datetime
# pyinstaller --windowed --onefile --icon=./images/icono.ico main.py
# pyuic6 -x design.ui -o design.py

class PDF(FPDF):
    def header(self):
        self.set_font( "Arial", "B", 12)
        self.cell(0, 10, "Tabla de datos", 0,1, "C")

    def footer(self):
        self.set_y(-10)
        self.set_font("Arial", "I", 8)
        self.cell(0, 10, f"Pagina {self.page_no()}", 0, 0, "C")


class MiApp(QMainWindow):
    def __init__(self):
        super(MiApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.dark_theme = False
        self.change_style()

        self.ui.BT_CALCULAR.clicked.connect(self.calculate_values)
        self.ui.BT_LIMPIAR.clicked.connect(self.clear_values)        
        self.ui.bt_mode_theme.clicked.connect(self.change_style)
        self.ui.bt_export_pdf.clicked.connect(self.save_pdf)

        self.ui.BT_CALCULAR.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.BT_LIMPIAR.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_mode_theme.setCursor(Qt.CursorShape.PointingHandCursor)
        self.ui.bt_export_pdf.setCursor(Qt.CursorShape.PointingHandCursor)

    def calculate_values(self):
        self.PB_LEYES =  (self.ui.PB_LEYES.value())
        self.AG_LEYES =  self.ui.AG_LEYES.value()  
        self.AU_LEYES =  self.ui.AU_LEYES.value()
        self.AS_LEYES =  (self.ui.AS_LEYES.value())
        self.SB_LEYES =  (self.ui.SB_LEYES.value()) 
        self.BI_LEYES =  (self.ui.BI_LEYES.value())  
        self.ZN_LEYES =  (self.ui.ZN_LEYES.value())
        self.produccion_LEYES =  self.ui.produccion_LEYES.value() 
        self.humedad_LEYES =  (self.ui.humedad_LEYES.value()) 
        self.maquila_LEYES =  self.ui.maquila_LEYES.value()  
        self.preciobase_LEYES =  self.ui.preciobase_LEYES.value()
        self.upscale_LEYES =  self.ui.upscale_LEYES.value() 

        self.PB_PRECIO = self.ui.PB_PRECIO.value() 
        self.AG_PRECIO = self.ui.AG_PRECIO.value() 
        self.AU_PRECIO = self.ui.AU_PRECIO.value() 

        self.PB_R = self.ui.PB_R.value() 
        self.AG_R = self.ui.AG_R.value()  
        self.AU_R = self.ui.AU_R.value()  

        self.PB_DM = self.ui.PB_DM.value()  
        self.AG_DM = self.ui.AG_DM.value() 
        self.AU_DM = self.ui.AU_DM.value() 

        #self.PB_refinacion = self.ui.PB_refinacion.value() 
        self.AG_refinacion = self.ui.AG_refinacion.value() 
        self.AU_refinacion = self.ui.AU_refinacion.value() 

        self.escalador = self.ui.escalador.value() 

        #######################################################
        opcion11 = self.PB_LEYES - self.PB_DM
        opcion21 = round((self.PB_LEYES*self.PB_R)/100, 3)
        ley_pagable = min(opcion11, opcion21)
        Pb = round((ley_pagable*self.PB_PRECIO)/100, 3)

        DM2 = round(self.AG_DM*0.035273962, 3)
        opcion12 = self.AG_LEYES - DM2
        opcion22 = round((self.AG_LEYES*self.AG_R)/100, 3)
        ley_pagable2 = min(opcion12, opcion22)
        Ag = round(ley_pagable2*self.AG_PRECIO, 3)

        DM3 = round(self.AU_DM*0.035273962, 3)
        opcion13 = self.AU_LEYES - DM3
        opcion23 = round((self.AU_LEYES*self.AU_R)/100, 3)
        ley_pagable3 = min(opcion13, opcion23)
        Au = round(ley_pagable3*self.AU_PRECIO, 3)


        self.ui.S_pagables_Pb.setText(f"{Pb} $/TM")
        self.ui.S_pagables_Ag.setText(f"{Ag} $/TM")
        self.ui.S_pagables_Au.setText(f"{Au} $/TM")
        S_pagables_total = Pb+Ag+Au
        self.ui.S_pagables_total.setText(f"{S_pagables_total} $/TM")
        
        #######################################################
        self.ui.S_deducciones_maquila.setText(f"{self.maquila_LEYES} $/TM")
        
        factor_multiplicador = round((self.PB_PRECIO - self.preciobase_LEYES)/self.escalador, 3)
        deduccionesE = round(factor_multiplicador*self.upscale_LEYES, 3)

        self.ui.S_deducciones_escalador.setText(f"{deduccionesE} $/TM")

        sum1 = self.AG_refinacion*ley_pagable2
        sum2 = self.AU_refinacion*ley_pagable3
        deduccionesR = round((sum1 + sum2), 3)
        self.ui.S_deducciones_refinacion.setText(f"{deduccionesR} $/TM")
        deducciones_total = round((self.maquila_LEYES+ deduccionesE+deduccionesR),3 )
        self.ui.S_deducciones_total.setText(f"{deducciones_total} $/TM") ########TOTAL ############
        ############################# PENALIDADES ###################
        contenido_penaliza_AS = self.AS_LEYES - self.ui.AS_limite.value() #  limites 
        contenido_penaliza_SB = self.SB_LEYES - self.ui.SB_limite.value() #  limites 
        contenido_penaliza_BI = self.BI_LEYES - self.ui.BI_limite.value() #  limites 
        contenido_penaliza_ZN = self.ZN_LEYES - self.ui.ZN_limite.value() #  limites 
     #   print("contenido_penaliza_ZN", contenido_penaliza_ZN, self.ui.ZN_limite.value())

        por_cada_AS = self.ui.AS_pc.value()
        por_cada_SB = self.ui.SB_pc.value()
        por_cada_BI = self.ui.BI_pc.value()
        por_cada_ZN = self.ui.ZN_pc.value()

        factor_AS  = 0
        factor_SB = 0
        factor_BI  = 0
        factor_ZN  = 0

        if contenido_penaliza_AS >0:
            factor_AS = contenido_penaliza_AS/por_cada_AS #APLICA
        if contenido_penaliza_SB >0:
            factor_SB = contenido_penaliza_SB/por_cada_SB
        if contenido_penaliza_BI >0:
            factor_BI = contenido_penaliza_BI/por_cada_BI
        if contenido_penaliza_ZN >0:
            factor_ZN = contenido_penaliza_ZN/por_cada_ZN
        
       # print(factor_ZN)
        penalidad_AS = self.ui.AS_penalidad.value()*factor_AS
        penalidad_SB = self.ui.SB_penalidad.value()*factor_SB
        penalidad_BI = self.ui.BI_penalidad.value()*factor_BI
        penalidad_ZN = self.ui.ZN_penalidad.value()*factor_ZN
      #  print("penalidad_ZN", penalidad_ZN, self.ui.ZN_penalidad.value())
        # Reemplazar valores cero con "No Aplica"
        penalidad_AS = penalidad_AS if penalidad_AS != 0 else "0" #No Aplica
        penalidad_SB = penalidad_SB if penalidad_SB != 0 else "0" #No Aplica
        penalidad_BI = penalidad_BI if penalidad_BI != 0 else "0" #No Aplica
        penalidad_ZN = penalidad_ZN if penalidad_ZN != 0 else "0" #No Aplica

        # Crear una lista de penalidades numéricas
        penalidades = [
            penalidad_AS if isinstance(penalidad_AS, (int, float)) else 0,
            penalidad_SB if isinstance(penalidad_SB, (int, float)) else 0,
            penalidad_BI if isinstance(penalidad_BI, (int, float)) else 0,
            penalidad_ZN if isinstance(penalidad_ZN, (int, float)) else 0,
        ]


    # Sumar las penalidades numéricas
        totalP = sum(penalidades)

        self.ui.S_penalidad_as.setText(f"{penalidad_AS} $/TM")
        self.ui.S_penalidad_sb.setText(f"{penalidad_SB} $/TM")
        self.ui.S_penalidad_bi.setText(f"{penalidad_BI} $/TM")
        self.ui.S_penalidad_zn.setText(f"{penalidad_ZN} $/TM")
        self.ui.S_penalidad_total.setText(f"{totalP} $/TM")

    # operaciones finales 
        valorpRMSdc  = S_pagables_total - (self.maquila_LEYES + deduccionesE + deduccionesR) - totalP
        self.ui.S_valorpRMSdc.setText(f"{round(valorpRMSdc, 3)} $/TM")
        self.ui.S_pesohumedoc.setText(f"{round(self.produccion_LEYES, 3)} TMH")
       
        pesosc = self.produccion_LEYES*(1- self.humedad_LEYES/100)
        self.ui.S_pesosc.setText(f"{round(pesosc, 3)} TMS")

        valor_concentrado = round(valorpRMSdc*pesosc, 3)
        self.ui.S_valor_concentrado.setText(f"{round(valor_concentrado, 3)} $")
             

    def clear_values(self):
        # limpiar entradas 
        self.ui.PB_LEYES.setValue(0.000)
        self.ui.AG_LEYES.setValue(0.000)
        self.ui.AU_LEYES.setValue(0.000)
        self.ui.AS_LEYES.setValue(0.000)
        self.ui.SB_LEYES.setValue(0.000)
        self.ui.BI_LEYES.setValue(0.000)
        self.ui.ZN_LEYES.setValue(0.000)
        self.ui.produccion_LEYES.setValue(0.000) 
        self.ui.humedad_LEYES.setValue(0.000) 
        self.ui.maquila_LEYES.setValue(0.000)  
        self.ui.preciobase_LEYES.setValue(0.000)
        self.ui.upscale_LEYES.setValue(0.000)
        self.ui.upscale_LEYES.setValue(0.000)

        self.ui.PB_PRECIO.setValue(0.000)
        self.ui.AG_PRECIO.setValue(0.000)
        self.ui.AU_PRECIO.setValue(0.000)

        self.ui.PB_R.setValue(0.000)
        self.ui.AG_R.setValue(0.000)
        self.ui.AU_R.setValue(0.000)

        self.ui.PB_DM.setValue(0.000)
        self.ui.AG_DM.setValue(0.000)
        self.ui.AU_DM.setValue(0.000)

  
        self.ui.AG_refinacion.setValue(0.000)
        self.ui.AU_refinacion.setValue(0.000)
        self.ui.escalador.setValue(0.000)

        self.ui.AS_penalidad.setValue(0.000) #PB_refinacion
        self.ui.SB_penalidad.setValue(0.000)
        self.ui.BI_penalidad.setValue(0.000)
        self.ui.ZN_penalidad.setValue(0.000)
        self.ui.AS_limite.setValue(0.000)
        self.ui.SB_limite.setValue(0.000)
        self.ui.BI_limite.setValue(0.000)
        self.ui.ZN_limite.setValue(0.000)
        self.ui.AS_pc.setValue(0.000)
        self.ui.SB_pc.setValue(0.000)
        self.ui.BI_pc.setValue(0.000)
        self.ui.ZN_pc.setValue(0.000)

        # limpiar salidas
        self.ui.S_valorpRMSdc.setText(f"{0.000} $/TM")
        self.ui.S_pesohumedoc.setText(f"{0.000} TMH")
        self.ui.S_pesosc.setText(f"{0.000} TMS")
        self.ui.S_valor_concentrado.setText(f"{0.000} $")
                       
        self.ui.S_pagables_Pb.setText(f"{0.000} $/TM")
        self.ui.S_pagables_Ag.setText(f"{0.000} $/TM")
        self.ui.S_pagables_Au.setText(f"{0.000} $/TM")
        self.ui.S_pagables_total.setText(f"{0.000} $/TM")
        self.ui.S_deducciones_maquila.setText(f"{0.000} $/TM")     

        self.ui.S_deducciones_escalador.setText(f"{0.000} $/TM")
        self.ui.S_deducciones_refinacion.setText(f"{0.000} $/TM")

        self.ui.S_penalidad_as.setText(f"{0.000} $/TM")
        self.ui.S_penalidad_sb.setText(f"{0.000} $/TM")
        self.ui.S_penalidad_bi.setText(f"{0.000} $/TM")
        self.ui.S_penalidad_zn.setText(f"{0.000} $/TM")
        self.ui.S_penalidad_total.setText(f"{0.000} $/TM")

        

    def change_style(self):
        if self.dark_theme:
            self.ui.bt_mode_theme.setIcon(QtGui.QIcon("images/sun.svg"))
            dark = """color:#e5e2c3;  background:#0f0e17;"""
            self.ui.centralwidget.setStyleSheet(dark)
            self.dark_theme = False
        else:
            self.ui.bt_mode_theme.setIcon(QtGui.QIcon("images/moon.svg"))
            ligh = """color:#0f0e17; background: #e5e2c3;"""
            self.ui.centralwidget.setStyleSheet(ligh)
            self.dark_theme = True


    def save_pdf(self, e):
        # Crear el PDF
        pdf = PDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        # Título
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, "Resultados Calculados", 0, 1, "C")
        pdf.ln(2)

        # Sección de Datos Pagables
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Datos Pagables:", 0, 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Pb: {self.ui.S_pagables_Pb.text()}", 0, 1)
        pdf.cell(0, 10, f"Ag: {self.ui.S_pagables_Ag.text()}", 0, 1)
        pdf.cell(0, 10, f"Au: {self.ui.S_pagables_Au.text()}", 0, 1)
        pdf.cell(0, 10, f"Total: {self.ui.S_pagables_total.text()}", 0, 1)
        pdf.ln(2)

        # Sección de Deducciones
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Deducciones:", 0, 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"Maquila: {self.ui.S_deducciones_maquila.text()} ", 0, 1)
        pdf.cell(0, 10, f"Escalador: {self.ui.S_deducciones_escalador.text()} ", 0, 1)
        pdf.cell(0, 10, f"Refinación: {self.ui.S_deducciones_refinacion.text()} ", 0, 1)
        pdf.ln(2)

        # Sección de Penalidades
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "Penalidades:", 0, 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"As: {self.ui.S_penalidad_as.text()} ", 0, 1)
        pdf.cell(0, 10, f"Sb: {self.ui.S_penalidad_sb.text()}", 0, 1)
        pdf.cell(0, 10, f"Bi: {self.ui.S_penalidad_bi.text()}", 0, 1)
        pdf.cell(0, 10, f"Zn: {self.ui.S_penalidad_zn.text()}", 0, 1)
        pdf.cell(0, 10, f"Total: {self.ui.S_penalidad_total.text()}", 0, 1)
        pdf.ln(2)

        # Operaciones finales
        pdf.set_font("Arial", "B", 12)
        pdf.cell(0, 10, "-------------------------------", 0, 1)
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 10, f"VALOR POR TMS DE CONCENTRADO: {self.ui.S_valorpRMSdc.text()}", 0, 1)
        pdf.cell(0, 10, f"Peso Humedo de concentrado: {self.ui.S_pesohumedoc.text()}", 0, 1)
        pdf.cell(0, 10, f"Peso Seco del Concentrado: {self.ui.S_pesosc.text()}", 0, 1)
        pdf.cell(0, 10, f"Valor del  Concentrado: {self.ui.S_valor_concentrado.text()}", 0, 1)

        file_name = datetime.datetime.now()
        file_name = file_name.strftime("DATA %Y-%m-%d_%H-%M-%S") + ".pdf"
        pdf.output(file_name)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MiApp()
    window.show()
    sys.exit(app.exec())