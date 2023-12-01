import sys
import os
import zipfile
import hashlib
import zlib
from Crypto.Random import get_random_bytes
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QMessageBox, QLineEdit, QInputDialog, QHBoxLayout
)
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtCore import Qt
import urllib.request
import shutil
import tempfile
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

MAX_TENTATIVES = 3

class InterfaceChiffrementFichiers(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Outil de Chiffrement de Fichiers")

        # Chemin d'accès local à la police Magneto
        font_path_local = r'C:\Users\victo\OneDrive\Bureau\projet vicking\magneto-bold.ttf'

        # Charger la police Magneto
        font_id = QFontDatabase.addApplicationFont(font_path_local)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        magneto_font = QFont(font_family, 16, QFont.Bold)

        # Utilisation de QHBoxLayout pour centrer le texte
        layout = QVBoxLayout()

        hbox = QHBoxLayout()
        hbox.addStretch(1)  # Ajoute un espace élastique à gauche
        self.etiquette = QLabel("DOOM")
        self.etiquette.setFont(magneto_font)
        hbox.addWidget(self.etiquette)
        hbox.addStretch(1)  # Ajoute un espace élastique à droite

        layout.addLayout(hbox)

        self.bouton_chiffrer = QPushButton("Chiffrer")
        self.bouton_dechiffrer = QPushButton("Déchiffrer")

        layout.addWidget(self.bouton_chiffrer)
        layout.addWidget(self.bouton_dechiffrer)

        self.setLayout(layout)

        self.bouton_chiffrer.clicked.connect(self.chiffrer)
        self.bouton_dechiffrer.clicked.connect(self.dechiffrer)

        # Ajuster la taille de la fenêtre
        self.resize(600, 400)

    def choisir_fichier(self, operation):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        chemin_fichier, _ = QFileDialog.getOpenFileName(self, f"Choisissez le fichier à {operation}", "", "Tous les fichiers (*.*);;")

        return chemin_fichier

    def chiffrer(self):
        chemin_fichier = self.choisir_fichier('Chiffrer')
        if chemin_fichier:
            mot_de_passe, ok = QInputDialog.getText(self, 'Mot de passe', 'Entrez votre mot de passe pour chiffrer:')
            if ok:
                chiffrer_fichier(chemin_fichier, mot_de_passe)

    def dechiffrer(self):
        chemin_fichier = self.choisir_fichier('Déchiffrer')
        if chemin_fichier:
            mot_de_passe, ok = QInputDialog.getText(self, 'Mot de passe', 'Entrez votre mot de passe pour déchiffrer:')
            if ok:
                dechiffrer_fichier(chemin_fichier, mot_de_passe)

def generer_cle(mot_de_passe):
    kdf = Scrypt(
        salt=get_random_bytes(16),
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    cle = kdf.derive(mot_de_passe.encode())
    return cle

def secure_delete(filepath, passes=1):
    try:
        with open(filepath, "rb+") as f:
            size = os.path.getsize(filepath)
            for _ in range(passes):
                f.seek(0)
                f.write(os.urandom(size))
            f.truncate()
        os.remove(filepath)
    except Exception as e:
        print(f"Error securely deleting file: {e}")

def chiffrer_fichier(chemin_fichier, mot_de_passe):
    iv = get_random_bytes(16)

    cle = generer_cle(mot_de_passe)

    cipher = Cipher(algorithms.AES(cle), modes.CFB(iv), backend=default_backend())
    chiffreur = cipher.encryptor()

    with open(chemin_fichier, 'rb') as f:
        texte_clair = f.read()

    donnees_compressees = zlib.compress(texte_clair)
    texte_chiffre = chiffreur.update(donnees_compressees) + chiffreur.finalize()

    repertoire_temporaire = tempfile.mkdtemp()
    chemin_fichier_temporaire = os.path.join(repertoire_temporaire, "fichier_chiffre")

    with open(chemin_fichier_temporaire, 'wb') as f:
        f.write(iv)
        f.write(texte_chiffre)

    shutil.move(chemin_fichier_temporaire, chemin_fichier)

    QMessageBox.information(None, "Chiffrement", "Fichier chiffré avec succès.")

def dechiffrer_fichier(chemin_fichier, mot_de_passe):
    config = {"tentatives": 0}

    donnees_decompactees = None

    with open(chemin_fichier, 'rb') as f:
        iv = f.read(16)

    for tentative in range(MAX_TENTATIVES):
        with open(chemin_fichier, 'rb') as f:
            iv = f.read(16)
            cle = generer_cle(mot_de_passe)

            cipher = Cipher(algorithms.AES(cle), modes.CFB(iv), backend=default_backend())
            dechiffreur = cipher.decryptor()

            texte_chiffre = f.read()

        try:
            donnees_decompactees = zlib.decompress(dechiffreur.update(texte_chiffre) + dechiffreur.finalize())
            break
        except zlib.error:
            if tentative == MAX_TENTATIVES - 1:
                secure_delete(chemin_fichier)
                QMessageBox.critical(None, "Trop de tentatives", "Vous avez dépassé le nombre maximum de tentatives. Le fichier crypté a été supprimé de manière sécurisée.")
                return

            QMessageBox.critical(None, "Mot de passe incorrect", "Mot de passe incorrect. Veuillez réessayer.")
            mot_de_passe, ok = QInputDialog.getText(None, 'Mot de passe', 'Entrez votre mot de passe pour déchiffrer:')
            if not ok:
                return

    if donnees_decompactees is not None:
        repertoire_temporaire = tempfile.mkdtemp()
        chemin_fichier_temporaire = os.path.join(repertoire_temporaire, "fichier_dechiffre")

        with open(chemin_fichier_temporaire, 'wb') as f:
            f.write(donnees_decompactees)

        shutil.move(chemin_fichier_temporaire, chemin_fichier)
        shutil.rmtree(repertoire_temporaire)

        QMessageBox.information(None, "Déchiffrement", "Fichier déchiffré avec succès.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    interface = InterfaceChiffrementFichiers()
    interface.show()
    sys.exit(app.exec_())
