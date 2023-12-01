Bonjour,

L'objectif de ce projet est de rendre inaccessible un fichier quelconque en utilisant plusieurs méthodes de chiffrement telles que le SHA256 et l'AES. Je partage avec vous des informations sur les fonctionnalités et l'utilisation des différentes applications/fichiers de mon répertoire.

Installation Automatique des Dépendances :
Le script vérifie si Python, Curl, 7-Zip, cryptography et PyQt5 sont installés. S'ils ne le sont pas, le script les installe automatiquement.

Installation de PyInstaller et Pillow :
Le script installe PyInstaller pour créer des exécutables à partir des scripts Python. Il installe également Pillow, une bibliothèque pour le traitement d'images.

Téléchargement de la Police Magneto :
Le script télécharge la police Magneto-Bold depuis Internet et l'installe sur l'ordinateur.

Création d'un Installateur avec Inno Setup :
Le projet utilise Inno Setup pour créer un installateur Windows (.exe) personnalisé.

Script d'Initialisation avec Téléchargement Automatique :
Le script d'initialisation vérifie si certains fichiers nécessaires sont présents. S'ils ne le sont pas, il les télécharge automatiquement depuis Internet.

Interface Utilisateur DOOM.pyw :
Le projet inclut l'application DOOM.pyw avec une icône personnalisée sur le bureau.

Notes importantes :

Assurez-vous d'avoir une connexion Internet lors de l'installation pour le téléchargement de certains fichiers.
Respectez les lois et politiques de confidentialité lors de l'utilisation du script d'initialisation avec téléchargement automatique.
Avertissement :
L'utilisation de ce projet implique l'acceptation des conditions d'utilisation et la compréhension des actions effectuées par les scripts, en particulier le téléchargement automatique de fichiers depuis Internet.
PS : C'est pas impossible que Windows defender vous annonce que c'est un trojent // le principe d'importer des bibliotèque python n'est pas très apprecié de cette antivirus ^^.

Si vous avez trouver un moyen de l'améliorer faites moi signe <3
