import sys, argparse, configparser
from interface import Main_UI
from PyQt5.QtWidgets import QApplication
from utility import console, config, absolute_path, end

if __name__ == "__main__":
    app = QApplication([])

    # ARGUMENT GET

    parser = argparse.ArgumentParser(description="")
    
    parser.add_argument('file_path', nargs='?', default=None, help="Path to file")
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    
    args = parser.parse_args()

    # Récupération des valeurs des arguments
    file_path, debug_mode = args.file_path, args.debug


    # LOAD CONFIG

    config(absolute_path("./.config"))


    # INIT LOG SYSTEM

    console(
        LogsDirectory = config.get("Log", "directory"),
        LogDirectory_max_memory = config.get("Log", "max_memory"),
        LogDirectory_max_age = config.get("Log", "max_age"),
        Console_Log_Level = console.Level.CRITICAL if debug_mode == False else console.Level.DEBUG,
        File_Log_Level = console.Level.INFO if debug_mode == False else console.Level.DEBUG
    )


    # START UI

    Start_UI = Main_UI(file_path)
    Start_UI.show()
    
    
    app.exec_()
    end(reason="Normal end")