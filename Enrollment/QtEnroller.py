# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'QtEnroller.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(911, 609)
        Form.setStyleSheet("    background-color: #ecf5fd; /* Light blue background color */")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(702, 280, 180, 15))
        self.label_11.setMinimumSize(QtCore.QSize(15, 15))
        self.label_11.setMaximumSize(QtCore.QSize(16777215, 15))
        self.label_11.setObjectName("label_11")
        self.layoutWidget = QtWidgets.QWidget(Form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 691, 591))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_view_cam = QtWidgets.QLabel(self.layoutWidget)
        self.label_view_cam.setMinimumSize(QtCore.QSize(680, 460))
        self.label_view_cam.setMaximumSize(QtCore.QSize(682, 460))
        self.label_view_cam.setStyleSheet("    background-color: #d3f8d3; /* Light green background color */\n"
"    border: 2px solid #006400; /* Dark green border color */")
        self.label_view_cam.setText("")
        self.label_view_cam.setObjectName("label_view_cam")
        self.verticalLayout.addWidget(self.label_view_cam)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_face_1 = QtWidgets.QLabel(self.layoutWidget)
        self.label_face_1.setMinimumSize(QtCore.QSize(110, 110))
        self.label_face_1.setMaximumSize(QtCore.QSize(110, 110))
        self.label_face_1.setStyleSheet("    background-color: #d3f8d3; /* Light green background color */\n"
"    border: 2px solid #006400; /* Dark green border color */")
        self.label_face_1.setText("")
        self.label_face_1.setObjectName("label_face_1")
        self.horizontalLayout.addWidget(self.label_face_1)
        self.label_face_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_face_2.setMinimumSize(QtCore.QSize(110, 110))
        self.label_face_2.setMaximumSize(QtCore.QSize(110, 110))
        self.label_face_2.setStyleSheet("    background-color: #d3f8d3; /* Light green background color */\n"
"    border: 2px solid #006400; /* Dark green border color */")
        self.label_face_2.setText("")
        self.label_face_2.setObjectName("label_face_2")
        self.horizontalLayout.addWidget(self.label_face_2)
        self.label_face_3 = QtWidgets.QLabel(self.layoutWidget)
        self.label_face_3.setMinimumSize(QtCore.QSize(110, 110))
        self.label_face_3.setMaximumSize(QtCore.QSize(110, 110))
        self.label_face_3.setStyleSheet("    background-color: #d3f8d3; /* Light green background color */\n"
"    border: 2px solid #006400; /* Dark green border color */")
        self.label_face_3.setText("")
        self.label_face_3.setObjectName("label_face_3")
        self.horizontalLayout.addWidget(self.label_face_3)
        self.label_face_4 = QtWidgets.QLabel(self.layoutWidget)
        self.label_face_4.setMinimumSize(QtCore.QSize(110, 110))
        self.label_face_4.setMaximumSize(QtCore.QSize(110, 110))
        self.label_face_4.setStyleSheet("    background-color: #d3f8d3; /* Light green background color */\n"
"    border: 2px solid #006400; /* Dark green border color */")
        self.label_face_4.setText("")
        self.label_face_4.setObjectName("label_face_4")
        self.horizontalLayout.addWidget(self.label_face_4)
        self.label_face_5 = QtWidgets.QLabel(self.layoutWidget)
        self.label_face_5.setMinimumSize(QtCore.QSize(110, 110))
        self.label_face_5.setMaximumSize(QtCore.QSize(110, 110))
        self.label_face_5.setStyleSheet("    background-color: #d3f8d3; /* Light green background color */\n"
"    border: 2px solid #006400; /* Dark green border color */")
        self.label_face_5.setText("")
        self.label_face_5.setObjectName("label_face_5")
        self.horizontalLayout.addWidget(self.label_face_5)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.layoutWidget1 = QtWidgets.QWidget(Form)
        self.layoutWidget1.setGeometry(QtCore.QRect(700, 510, 201, 91))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.button_start = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_start.setStyleSheet("QPushButton {\n"
"    font-weight: bold;\n"
"    font-size: 14px; /* Set your desired font size */\n"
"    color: #ffffff; /* Set your desired text color */\n"
"    background-color: #007bff; /* Set your desired background color */\n"
"    border: 2px solid #006400; /* Dark green border color */    border-radius: 5px; /* Set your desired border radius */\n"
"    padding: 5px 10px; /* Set your desired padding */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #0056b3; /* Set your desired hover background color */\n"
"    border: 1px solid #0056b3; /* Set your desired hover border color */\n"
"}")
        self.button_start.setObjectName("button_start")
        self.verticalLayout_3.addWidget(self.button_start)
        self.button_verify = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_verify.setStyleSheet("QPushButton {\n"
"    font-weight: bold;\n"
"    font-size: 14px; /* Set your desired font size */\n"
"    color: #ffffff; /* Set your desired text color */\n"
"    background-color: #007bff; /* Set your desired background color */\n"
"    border: 2px solid #006400; /* Dark green border color */    border-radius: 5px; /* Set your desired border radius */\n"
"    padding: 5px 10px; /* Set your desired padding */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #0056b3; /* Set your desired hover background color */\n"
"    border: 1px solid #0056b3; /* Set your desired hover border color */\n"
"}")
        self.button_verify.setObjectName("button_verify")
        self.verticalLayout_3.addWidget(self.button_verify)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.button_enroll = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_enroll.setStyleSheet("QPushButton {\n"
"    font-weight: bold;\n"
"    font-size: 14px; /* Set your desired font size */\n"
"    color: #ffffff; /* Set your desired text color */\n"
"    background-color: #007bff; /* Set your desired background color */\n"
"    border: 2px solid #006400; /* Dark green border color */    border-radius: 5px; /* Set your desired border radius */\n"
"    padding: 5px 10px; /* Set your desired padding */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #0056b3; /* Set your desired hover background color */\n"
"    border: 1px solid #0056b3; /* Set your desired hover border color */\n"
"}")
        self.button_enroll.setObjectName("button_enroll")
        self.verticalLayout_4.addWidget(self.button_enroll)
        self.button_reset = QtWidgets.QPushButton(self.layoutWidget1)
        self.button_reset.setStyleSheet("QPushButton {\n"
"    font-weight: bold;\n"
"    font-size: 14px; /* Set your desired font size */\n"
"    color: #ffffff; /* Set your desired text color */\n"
"    background-color: #007bff; /* Set your desired background color */\n"
"    border: 2px solid #006400; /* Dark green border color */    border-radius: 5px; /* Set your desired border radius */\n"
"    padding: 5px 10px; /* Set your desired padding */\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #0056b3; /* Set your desired hover background color */\n"
"    border: 1px solid #0056b3; /* Set your desired hover border color */\n"
"}")
        self.button_reset.setObjectName("button_reset")
        self.verticalLayout_4.addWidget(self.button_reset)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.layoutWidget2 = QtWidgets.QWidget(Form)
        self.layoutWidget2.setGeometry(QtCore.QRect(701, 11, 202, 261))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_7 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_7.setMinimumSize(QtCore.QSize(200, 0))
        self.label_7.setMaximumSize(QtCore.QSize(200, 16777215))
        self.label_7.setStyleSheet("font-weight: bold;\n"
"        font-size: 25px;\n"
"        color: #ffffff;\n"
"        background-color: #007bff;\n"
"    border: 2px solid #006400; /* Dark green border color */    border-radius: 5px; /* Set your desired border radius */\n"
"        padding: 5px 10px;")
        self.label_7.setObjectName("label_7")
        self.verticalLayout_2.addWidget(self.label_7)
        self.label_8 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_8.setStyleSheet("font: 15pt \"Ubuntu\";")
        self.label_8.setObjectName("label_8")
        self.verticalLayout_2.addWidget(self.label_8)
        self.line_edit_name = QtWidgets.QLineEdit(self.layoutWidget2)
        self.line_edit_name.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"QLineEdit {\n"
"    color: #555555; /* Set your desired text color */\n"
"}\n"
"\n"
"QLineEdit:placeholder {\n"
"    color: #999999; /* Set your desired placeholder text color */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    color: #000000; /* Set your desired text color when focused */\n"
"}")
        self.line_edit_name.setObjectName("line_edit_name")
        self.verticalLayout_2.addWidget(self.line_edit_name)
        self.label_9 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_9.setStyleSheet("font: 15pt \"Ubuntu\";")
        self.label_9.setObjectName("label_9")
        self.verticalLayout_2.addWidget(self.label_9)
        self.line_edit_phone = QtWidgets.QLineEdit(self.layoutWidget2)
        self.line_edit_phone.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"QLineEdit {\n"
"    color: #555555; /* Set your desired text color */\n"
"}\n"
"\n"
"QLineEdit:placeholder {\n"
"    color: #999999; /* Set your desired placeholder text color */\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    color: #000000; /* Set your desired text color when focused */\n"
"}")
        self.line_edit_phone.setObjectName("line_edit_phone")
        self.verticalLayout_2.addWidget(self.line_edit_phone)
        self.label_10 = QtWidgets.QLabel(self.layoutWidget2)
        self.label_10.setStyleSheet("font: 15pt \"Ubuntu\";")
        self.label_10.setObjectName("label_10")
        self.verticalLayout_2.addWidget(self.label_10)
        self.line_edit_email = QtWidgets.QLineEdit(self.layoutWidget2)
        self.line_edit_email.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.line_edit_email.setObjectName("line_edit_email")
        self.verticalLayout_2.addWidget(self.line_edit_email)
        self.text_edit_output = QtWidgets.QTextEdit(Form)
        self.text_edit_output.setGeometry(QtCore.QRect(700, 300, 201, 200))
        self.text_edit_output.setMinimumSize(QtCore.QSize(0, 160))
        self.text_edit_output.setMaximumSize(QtCore.QSize(16777215, 200))
        self.text_edit_output.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.text_edit_output.setObjectName("text_edit_output")

        self.retranslateUi(Form)
        self.button_reset.clicked.connect(self.label_face_1.clear)
        self.button_reset.clicked.connect(self.label_view_cam.clear)
        self.button_reset.clicked.connect(self.text_edit_output.clear)
        self.button_reset.clicked.connect(self.line_edit_email.clear)
        self.button_reset.clicked.connect(self.line_edit_phone.clear)
        self.button_reset.clicked.connect(self.line_edit_name.clear)
        self.button_reset.clicked.connect(self.label_face_2.clear)
        self.button_reset.clicked.connect(self.label_face_3.clear)
        self.button_reset.clicked.connect(self.label_face_4.clear)
        self.button_reset.clicked.connect(self.label_face_5.clear)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        Form.setToolTip(_translate("Form", "<html><head/><body><p>Enroll App</p></body></html>"))
        self.label_11.setText(_translate("Form", "Output:"))
        self.button_start.setToolTip(_translate("Form", "<html><head/><body><p>Start the Camera feed</p></body></html>"))
        self.button_start.setText(_translate("Form", "Start"))
        self.button_verify.setText(_translate("Form", "Verify"))
        self.button_enroll.setText(_translate("Form", "Enroll"))
        self.button_reset.setText(_translate("Form", "Reset"))
        self.label_7.setText(_translate("Form", "Face Enroller"))
        self.label_8.setText(_translate("Form", "Name"))
        self.label_9.setText(_translate("Form", "Phone Number"))
        self.label_10.setText(_translate("Form", "Email Address"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
