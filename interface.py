from PyQt5.QtWidgets import QMessageBox, QTextBrowser, QPlainTextEdit, QTabWidget,QLineEdit, QRadioButton, QDialog, QFileDialog, QComboBox, QLabel, QPushButton, QCheckBox, QScrollArea, QWidget, QVBoxLayout
from PyQt5.uic import loadUiType, loadUi
from PyQt5 import QtGui, QtWidgets, QtCore
import os, json, sys
from utility import resource_path, Res, Intercafe_File, hash_password, check_password
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
        
        self.path = os.path.abspath(path)

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
        self.Save_Button.clicked.connect(self.Clicked_SaveButton)

        # Uncrypting

        self.key = None
        self.Encrypt_Content = None
        self.hint = None
        self.hash = None
        self.Content = None
        

    def Check_Encoding_Radio(self, e:bool):
        # Si le Radio et check on mais le champ de texte en mods password

        if e:
            self.Encoding_Input.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.Encoding_Input.setEchoMode(QtWidgets.QLineEdit.Normal)

    def TextChange_Text_Edit(self):

        self.Text_Display.setMarkdown(
            self.Text_Edit.toPlainText()
        )
    
    def show(self):
        super().show()

        if self.path is not None:

            # Chargement du contenue du fichier
            with open(self.path, "r", encoding="utf-8") as self.file:
                root = json.load(self.file)

            # Load data
            self.Encrypt_Content:str = root["content"]
            self.hint:str = root["hint"]
            self.hash:str = root["hash"]

            if self.Encrypt_Content is None or self.hint is None:
                raise IndexError()


            # Ouvre une popup pour demander la clé a l'utilisateur

            dialoge = KeyInput_UI(self, hash=self.hash, path=self.path) # Open popup

            # Attendre que l'utilisateur et valider la popup
            if dialoge.exec_() == QDialog.Accepted:
                self.key = dialoge.key


            # Uncrypt content

            self.Content = decrypt(
                encrypted_text= self.Encrypt_Content,
                key= self.key
            )

            # Charger les info dans la fenetre
            self.Text_Edit.setPlainText(self.Content)
            self.Text_Display.setMarkdown(self.Content)
            self.Encoding_Input.setText(self.key)
        
    def Clicked_SaveButton(self):
        
        if self.path is None:
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Encryptoz file (*.eyz);;All the files (*)", options=options)
            print(fileName)

class KeyInput_UI(QDialog, Window_KeyInput[1], Window_KeyInput[0]):
    
    def __init__(self, parent, hash:str, path:str) -> None:
        super(KeyInput_UI, self).__init__(parent)
        self.setupUi(self)

        self.hash = hash
        self.path = path

        # Items list

        self.Key_Input:QLineEdit
        self.Key_Label:QLabel
        self.Key_Radio:QRadioButton
        self.Decrypt_Button:QPushButton
        self.Label_FileName:QLabel
        self.Label_FIlePath:QLabel

        # Builds

        self.Decrypt_Button.setEnabled(False)
        self.Decrypt_Button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        self.Label_FileName.setText(os.path.basename(self.path))
        self.Label_FIlePath.setText(self.path)

        # Scriptings

        self.Key_Radio.clicked.connect(self.Check_Key_Radio)
        self.Decrypt_Button.clicked.connect(self.decrypt)
        self.Key_Input.textChanged.connect(self.Button_isEnabled)

    def Check_Key_Radio(self, e):
        # Si le Radio et check on mais le champ de texte en mods password

        if e:
            self.Key_Input.setEchoMode(QtWidgets.QLineEdit.Password)
        else:
            self.Key_Input.setEchoMode(QtWidgets.QLineEdit.Normal)

    def Button_isEnabled(self):
        if self.Key_Input.text() == "":
            self.Decrypt_Button.setEnabled(False)
            self.Decrypt_Button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
        else:
            self.Decrypt_Button.setEnabled(True)
            self.Decrypt_Button.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def decrypt(self):
        
        self.key = self.Key_Input.text()

        if check_password(self.key, self.hash):
            self.accept()
        else:
            QMessageBox.information(self, "Warning !", "The Decryption Key is incorrect!")

        #self.close()

    def closeEvent(self, event):

        # reply = QMessageBox.question(self, 'Confirmation', 'Êtes-vous sûr de vouloir fermer la fenêtre?',
        #                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
        #     sys.exit()
        # else:
        #     event.ignore()  # Empêche la fermeture de la fenêtre

        sys.exit()
