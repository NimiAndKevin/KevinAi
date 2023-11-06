from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(910, 640)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(0, 50, 901, 591))
        self.label.setStyleSheet("background-color: rgb(0, 0, 0);")
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(619, 543, 221, 71))
        self.pushButton.setText("")
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setIcon(QtGui.QIcon("C:\\Users\\surface\\Downloads\\Start.png"))
        self.pushButton.setIconSize(QtCore.QSize(200, 200))

        self.pushButton.clicked.connect(self.start_animation)

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(180, 120, 511, 411))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("../../Downloads/Ntuks.gif"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(50, 480, 261, 141))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("../../Downloads/Earth.gif"))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")
        
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(620, 90, 261, 231))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("../../Downloads/Hero_Template.gif"))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")
        
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(30, 70, 261, 271))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("../../Downloads/7gQj (1).gif"))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "WELCOME TO KEVIN"))
        self.label.setText(_translate("Dialog", "TextLabel"))

    def start_animation(self):
        self.movie1 = QtGui.QMovie("../../Downloads/Ntuks.gif")
        self.label_2.setMovie(self.movie1)
        self.movie1.start()

        self.movie2 = QtGui.QMovie("../../Downloads/Earth.gif")
        self.label_3.setMovie(self.movie2)
        self.movie2.start()

        self.movie3 = QtGui.QMovie("../../Downloads/Hero_Template.gif")
        self.label_4.setMovie(self.movie3)
        self.movie3.start()

        self.movie4 = QtGui.QMovie("../../Downloads/7gQj (1).gif")
        self.label_5.setMovie(self.movie4)
        self.movie4.start()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())