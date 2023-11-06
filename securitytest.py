from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(898, 629)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Kevin - Copy.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Dialog.setWindowIcon(icon)
        Dialog.setStyleSheet("background-color: rgb(0, 0, 0);\n"
                            "border : 1px solid white;\n"
                            "")

        self.login_button = QtWidgets.QPushButton(Dialog)
        self.login_button.setGeometry(QtCore.QRect(200, 400, 200, 40))
        self.login_button.setObjectName("login_button")
        self.login_button.setText("Login")
        self.login_button.clicked.connect(self.login_attempt)

        self.signup_button = QtWidgets.QPushButton(Dialog)
        self.signup_button.setGeometry(QtCore.QRect(400, 400, 200, 40))
        self.signup_button.setObjectName("signup_button")
        self.signup_button.setText("Signup")
        self.signup_button.clicked.connect(self.show_signup)

        self.retry_button = QtWidgets.QPushButton(Dialog)
        self.retry_button.setGeometry(QtCore.QRect(300, 450, 200, 40))
        self.retry_button.setObjectName("retry_button")
        self.retry_button.setText("Retry")
        self.retry_button.clicked.connect(self.login_retry)
        self.retry_button.hide()  # Initially hide the retry button

        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(0, 480, 491, 111))
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(490, 260, 411, 221))
        self.label_4.setScaledContents(True)
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(310, 0, 331, 271))
        self.label_5.setScaledContents(True)
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(0, 270, 491, 211))
        self.label_6.setScaledContents(True)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Create QMovie objects for your labels
        self.movie3 = QtGui.QMovie("../00545cb7179c504433d4c8f5e845f286.gif")
        self.movie4 = QtGui.QMovie("../../Downloads/Hero_Template.gif")
        self.movie5 = QtGui.QMovie("../../Downloads/7gQj (1).gif")
        self.movie6 = QtGui.QMovie("../../Downloads/Earth.gif")

        # Set QMovies for your labels
        self.label_3.setMovie(self.movie3)
        self.label_4.setMovie(self.movie4)
        self.label_5.setMovie(self.movie5)
        self.label_6.setMovie(self.movie6)

        # Start QMovies
        self.movie3.start()
        self.movie4.start()
        self.movie5.start()
        self.movie6.start()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "KEVIN-SECURITY SYSTEM"))
        self.signup_button.setText(_translate("Dialog", "Sign"))
        self.login_button.setText(_translate("Dialog", "Login"))

        # Other UI elements...

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())