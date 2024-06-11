import os, json, sys
from PyQt5.QtWidgets import QStatusBar, QMessageBox, QTextBrowser, QPlainTextEdit, QTabWidget,QLineEdit, QRadioButton, QDialog, QFileDialog, QLabel, QPushButton
from PyQt5.uic import loadUiType, loadUi
from PyQt5 import QtGui, QtCore
from utility import __version__, Res, Intercafe_File, resource_path, hash_password, check_password, Set_LineInput_Password, create_db, connect_db, fetch_data_from_db, update_db
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
        
        self.path = path

        # Items list

        self.Text_Display   :QTextBrowser
        self.Text_Edit      :QPlainTextEdit
        self.Tab            :QTabWidget
        self.Save_Button    :QPushButton
        self.Encoding_Input :QLineEdit
        self.Encoding_Label :QLabel
        self.Encoding_Radio :QRadioButton
        self.statusbar      :QStatusBar

        # Set resources element

        # Build status bar
        self.FilePathLabel = QLabel('')
        self.SaveIndicate = QLabel('')

        self.statusbar.addWidget(self.FilePathLabel)
        self.statusbar.addPermanentWidget(self.SaveIndicate)

        # Set Save_Button icon
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path(Res.SaveIcon)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Save_Button.setIcon(icon)


        # Scriptings

        self.Encoding_Radio.clicked.connect(self.Check_Encoding_Radio)
        self.Text_Edit.textChanged.connect(self.TextChange_Text_Edit)
        self.Save_Button.clicked.connect(self.Clicked_SaveButton)

        # Uncrypting

        self.db = None
        self.key = None
        self.Encrypt_Content = None
        self.hint = None
        self.hash = None
        self.Content = None
        

    def Check_Encoding_Radio(self, e:bool):
        # Si le Radio et check on mais le champ de texte en mods password

        # if e:
        #     self.Encoding_Input.setEchoMode(QtWidgets.QLineEdit.Password)
        # else:
        #     self.Encoding_Input.setEchoMode(QtWidgets.QLineEdit.Normal)

        Set_LineInput_Password(self.Encoding_Input, e)

    def TextChange_Text_Edit(self):
        text = self.Text_Edit.toPlainText()
        self.Text_Display.setMarkdown( text )
        self.Save_Button.setEnabled( text != self.Content)
    
    def show(self):
        super().show()

        if self.path is not None:   

            self.path = os.path.abspath(self.path)

            # Chargement du contenue du fichier
            self.db = connect_db(self.path)

            # Load data

            data = fetch_data_from_db(self.db)
            self.file_version = data[0]
            self.hint:str = data[1]
            self.hash:str = data[2]
            self.Encrypt_Content:str = data[3]

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

            self.FilePathLabel.setText(self.path)
        
    def Clicked_SaveButton(self):
        
        key = self.Encoding_Input.text()
        if key is "":
            QMessageBox.information(self, "WARNIG !", "You did not specify an encryption key !")
            return
        

        # self.SaveIndicate.setText("Saving...")
        # timer = QtCore.QTime()
        # timer.setSingleShot(True)  # Assurez-vous que le timer se déclenche une seule fois
        # timer.timeout.connect(lambda: self.SaveIndicate.setText(""))

        self.Save_Button.setEnabled(False)
        self.Text_Edit.setFocus()

        text = self.Text_Edit.toPlainText()


        if self.path is None:

            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getSaveFileName(self, "Save file", "", "Encryptoz file (*.eyz);;All the files (*)", options=options)
            print(fileName)
            if fileName is "":
                return

            self.db = create_db(fileName)
            self.path = fileName
            self.file_version = __version__

        else:

            if self.key != key:
                reply = QMessageBox.question(self, 'the key is different !', 'The encryption key is different. Are you sure you want to change it ?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

                if reply == QMessageBox.Yes:
                    pass
                else:
                    return
            
            
            
            
        self.hint = "h"
        self.Content = text
        self.hash = hash_password(key)
        self.Encrypt_Content = encrypt(text, key)
        self.key = key
        
        try:
            update_db(
                self.db,
                version=self.file_version,
                hint=self.hint,
                hash=self.hash,
                content=self.Encrypt_Content
            )
        except Exception as e:
            QMessageBox.information(self, "ERROR", str(e))

        # timer.start(1000)
        


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
        #self.Decrypt_Button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))

        self.Label_FileName.setText(os.path.basename(self.path))
        self.Label_FIlePath.setText(self.path)

        # Scriptings

        self.Key_Radio.clicked.connect(self.Check_Key_Radio)
        self.Decrypt_Button.clicked.connect(self.decrypt)
        self.Key_Input.textChanged.connect(self.Button_isEnabled)

    def Check_Key_Radio(self, e):
        # Si le Radio et check on mais le champ de texte en mods password
        Set_LineInput_Password(self.Key_Input, e)

    def Button_isEnabled(self):
        self.Decrypt_Button.setEnabled(self.Key_Input.text() is not "")


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
