from PyQt5.QtWidgets import QTextBrowser, QPlainTextEdit, QTabWidget,QLineEdit, QRadioButton, QDialog, QFileDialog, QComboBox, QLabel, QPushButton, QCheckBox, QScrollArea, QWidget, QVBoxLayout
from PyQt5.uic import loadUiType, loadUi
from PyQt5 import QtGui, QtWidgets
import os
from utility import resource_path, Res, Intercafe_File
from crypting import encrypt, decrypt
import xml.etree.ElementTree as ET

# Load global resources
# App_Icon = resource_path('./resources/icon/icon.ico')


# Load UI
Window_Main =  loadUiType(resource_path(Intercafe_File.main))
Window_KeyInput =  loadUiType(resource_path(Intercafe_File.key_input))


# Builds interfaces

class Main_UI(Window_Main[1], Window_Main[0]):
    def __init__(self, path) -> None:
        super(Main_UI, self).__init__()
        self.setupUi(self)


        # Items list

        self.Text_Display   :QTextBrowser
        self.Text_Edit      :QPlainTextEdit
        self.Tab            :QTabWidget
        self.Save_Button    :QPushButton
        self.Encoding_Input :QLineEdit
        self.Encoding_Label :QLabel
        self.Encoding_Radio :QRadioButton

        # Set resources element

        # Set Save_Button icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path(Res.SaveIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Save_Button.setIcon(icon)


        # Scriptings

        self.Encoding_Radio.clicked.connect(self.Check_Encoding_Radio)
        self.Text_Edit.textChanged.connect(self.TextChange_Text_Edit)

        # Uncrypting

        self.key = None
        if path is not None:

            # Load file
            tree = ET.parse(path)
            root = tree.getroot()

            # Load data
            self.Encrypt_Content = root.find('.//content')
            self.hint = root.find(".//hint")

            if self.Encrypt_Content is None or self.hint is None:
                raise IndexError()


            # Launch input key ui
            dialoge = KeyInput_UI(self)

            if dialoge.exec_() == QDialog.Accepted:
                self.key = dialoge.key

            # Uncrypt content

            self.Content = decrypt(
                encrypted_text=self.Encrypt_Content,
                key=self.key
            )

            print(self.Encrypt_Content)
            print(self.key)
            print(self.Content)

            self.Text_Edit.setPlainText(self.Content)
            self.Text_Display.setMarkdown(self.Content)


            



    def Check_Encoding_Radio(self, e):
        # Si le Radio et check on mais le champ de texte en mods password

        if e:
            self.Encoding_Input.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.Encoding_Input.setEchoMode(QtWidgets.QLineEdit.Normal)

    def TextChange_Text_Edit(self):

        self.Text_Display.setMarkdown(
            self.Text_Edit.toPlainText()
        )

class KeyInput_UI(QDialog, Window_KeyInput[1], Window_KeyInput[0]):
    
    def __init__(self, parent=None) -> None:
        super(KeyInput_UI, self).__init__(parent)
        self.setupUi(self)

        # Items list

        self.Key_Input:QLineEdit
        self.Key_Label:QLabel
        self.Key_Radio:QRadioButton
        self.Decrypt_Button:QPushButton
        self.Label_FileName:QLabel
        self.Label_FIlePath:QLabel

        # Scriptings

        self.Key_Radio.clicked.connect(self.Check_Key_Radio)
        self.Decrypt_Button.clicked.connect(self.decrypt)

    def Check_Key_Radio(self, e):
        # Si le Radio et check on mais le champ de texte en mods password

        if e:
            self.Key_Input.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.Key_Input.setEchoMode(QtWidgets.QLineEdit.Normal)

    def decrypt(self):
        
        self.key = self.Key_Input.text()

        self.accept()
        #self.close()
