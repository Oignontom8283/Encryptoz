%~d0
cd %~dp0


python -m venv .env

.\.env\Scripts\activate

python -m pip install --upgrade pip

python -m pip install -r requirements.txt