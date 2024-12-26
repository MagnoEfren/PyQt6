# Form implementation generated from reading ui file 'message.ui'
#
# Created by: PyQt6 UI code generator 6.5.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(425, 266)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("Images/logo_App.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(parent=self.centralwidget)
        self.frame.setStyleSheet("QFrame{\n"
"border: 2px solid #0f0e17;\n"
"background-color: #ffffff;\n"
"color: #0f0e17;\n"
"border-radius: 10px;\n"
"}\n"
"QLabel{\n"
"background-color: #ffffff;\n"
"font: 15pt \"Lato\";\n"
"color: #7f5af0;\n"
"border: None;\n"
"}\n"
"\n"
"QPushButton {\n"
"    color: white;\n"
"    font: 12pt \"Lato\";\n"
"     border-radius: 10px;\n"
"     background-color:      #7f5af0;\n"
"    width:                 24px;\n"
"    height:                 24px;\n"
"    border: 3px solid  #0f0e17;\n"
"    }\n"
"\n"
"\n"
" QPushButton:hover {\n"
"        background-color:#0f0e17;\n"
"        color: #ffffff;\n"
"        border: 3px solid  #7f5af0;\n"
"    }\n"
"\n"
"    QPushButton:disabled {\n"
"        background-color: #0f0e17;\n"
"        color: grey;\n"
"        border: 3px solid  grey;\n"
"    }\n"
"\n"
"\n"
"")
        self.frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Shadow.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(20, 10, 20, 10)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.titulo_label_aviso = QtWidgets.QLabel(parent=self.frame)
        self.titulo_label_aviso.setText("")
        self.titulo_label_aviso.setObjectName("titulo_label_aviso")
        self.horizontalLayout.addWidget(self.titulo_label_aviso)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton.setStyleSheet("QPushButton{\n"
"border-radius:20px;\n"
"font: 75 20pt \"MS Sans Serif\";\n"
"background-color: rgba(0, 0, 0,0%);\n"
"border:  None;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"border:0px;\n"
"color: rgb(0, 0, 0);\n"
"border: 2px solid #0f0e17;\n"
"}\n"
"\n"
"")
        self.pushButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("Images/x.svg"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.pushButton.setIcon(icon1)
        self.pushButton.setIconSize(QtCore.QSize(36, 36))
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(26)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.frame)
        self.label_2.setMaximumSize(QtCore.QSize(120, 120))
        self.label_2.setStyleSheet("font: 75 14pt \"MS Shell Dlg 2\";\n"
"background-color: rgba(0,0,0,0%);\n"
"border:0px;")
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("Images/logo_App.png"))
        self.label_2.setScaledContents(True)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.label_texto_aviso = QtWidgets.QLabel(parent=self.frame)
        self.label_texto_aviso.setTabletTracking(False)
        self.label_texto_aviso.setAcceptDrops(False)
        self.label_texto_aviso.setStyleSheet("")
        self.label_texto_aviso.setText("")
        self.label_texto_aviso.setTextFormat(QtCore.Qt.TextFormat.AutoText)
        self.label_texto_aviso.setScaledContents(False)
        self.label_texto_aviso.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_texto_aviso.setWordWrap(True)
        self.label_texto_aviso.setOpenExternalLinks(False)
        self.label_texto_aviso.setObjectName("label_texto_aviso")
        self.horizontalLayout_2.addWidget(self.label_texto_aviso)
        self.horizontalLayout_2.setStretch(0, 1)
        self.horizontalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.frame)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 35))
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(1, 5)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton.clicked.connect(MainWindow.close) # type: ignore
        self.pushButton_2.clicked.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Mecanismo de 4 barras"))
        self.pushButton_2.setText(_translate("MainWindow", "Aceptar"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())