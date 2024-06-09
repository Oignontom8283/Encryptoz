%~d0
cd %~dp0

pyinstaller --distpath "./bin/windows/onedir/" --name "Encryptoz" --noconfirm --onedir --windowed --add-data "./interface;interface/" --add-data "./resources;resources/" "./main.py"
pyinstaller --distpath "./bin/windows/onefile/" --name "Encryptoz" --noconfirm --onefile --windowed --add-data "./interface;interface/" --add-data "./resources;resources/" "./main.py"


rd /s /q build
rd /s /q build