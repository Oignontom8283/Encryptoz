import sys, argparse
from interface import Main_UI
from PyQt5.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication([])

    # file_path = None
    # if len(sys.argv) > 1:
    #     file_path = sys.argv[1]
    #     print(f"File_path : ${file_path}")

    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument('file_path', nargs='?', default=None, help="Path to file")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    
    args = parser.parse_args()

    # Récupération des valeurs des arguments
    file_path, debug_mode = args.file_path, args.debug


    Start_UI = Main_UI(file_path)
    Start_UI.show()

    app.exec_()