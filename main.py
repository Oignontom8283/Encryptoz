import sys
from interface import Main_UI
from PyQt5.QtWidgets import QApplication
import xml.etree.ElementTree as ET



if __name__ == "__main__":
    app = QApplication([])


    file_path = None
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(file_path)

    Start_UI = Main_UI(file_path)
    Start_UI.show()

    app.exec_()