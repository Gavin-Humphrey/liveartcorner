<p align="center">
  <img src="./static/img/live-art-corner-logo.png" alt="Logo" >
</p>

<details>
<summary><strong>Table of Contents</strong></summary>

 - [LIVE-ART-CORNER](#live-art-corner)
  - [Features](#features)
  - [Prerequisites](#prerequisites)
  - [Installation and Launch](#installation-and-launch)
  - [Production](#production)
  - [Deployment](#deployment)
  - [Author](#author)

</details>

## LIVE-ART-CORNER

LIVE-ART-CORNER is a Python/Django application where artists can display and sell their artworks to users. Artists must subscribe and get verified to upload their artworks and list custom services. Only registered users can access custom services and artists' profile pages, while the marketplace is open to all clients.

### Features

- Artists can display and sell artworks.
- Subscription and verification process for artists.
- Custom services offered by artists (portrait, landscape drawings, paintings via webcam).
- Registered users can access custom services and artists' profiles.
- Marketplace open to all users; only registered users can add items to wishlist.
- Scrolling animation for popular items on the homepage.
- Items displayed in cards, each representing an artist's shop.
- Detailed view of items when clicked.

### Prerequisites

Ensure you have the following installed before proceeding:

- [Git](https://git-scm.com/)
- [Sentry](https://sentry.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Cloudinary](https://cloudinary.com/)
- [Docker](https://www.docker.com/)
- [CircleCI](https://circleci.com/)
- [Heroku](https://www.heroku.com/)

### Installation and Launch

1. **Install Python:**
   - [Python installation guide](https://www.python.org/)

2. **Clone the repository:**

   ```bash
   git clone https://github.com/Gavin-Humphrey/liveartcorner.git

<strong>Create and activate a virtual environment:</strong><br>
python -m venv env<br><br>
<strong>macOS/Linux:</strong><br>
source env/bin/activate  <br><br>
<strong>Windows:</strong><br>
env\scripts\activate.bat<br><br> 
<strong>Install required packages:</strong><br>
pip install -r requirements.txt<br><br>
<strong>Migrate the database:</strong><br>
python manage.py makemigrations<br>
python manage.py migrate<br><br>
<strong>Collect static files:</strong><br>
python manage.py collectstatic<br><br>
<strong>Launch the server:</strong><br>
python manage.py runserver,<br>
Access the application at http://127.0.0.1:8000

<strong>Unit Tests</strong><br>
**Run unit tests using Pytest:**<br>
pytest<br>


### Production
<details>
<summary><strong>CircleCI</strong></summary>
Follow these steps to configure CircleCI:

Create a CircleCI account and connect your GitHub account.
Create a new project and select your GitHub repository.
Add the required environment variables to the CircleCI project settings:
DOCKER_USERNAME: Your Docker Hub username
DOCKER_LOGIN: Your Docker Hub login email
HEROKU_APP_NAME: The name of your Heroku application
HEROKU_TOKEN: Your Heroku API key
Push a new commit to your repository to trigger a new build on CircleCI.
</details>
<details>
<summary><strong>Sentry</strong></summary>
This application uses Sentry for error tracking. To configure Sentry:

Create a Sentry account and create a new project.

Add the SENTRY_DSN environment variable to your project's .env file.

Install the Sentry SDK Python package:


pip install sentry-sdk
Add the generated code to the settings.py file.

</details>
<details>
<summary><strong>Cloudinary Configuration</strong></summary>
To use Cloudinary for image/video storage and manipulation, you need to set up Cloudinary credentials in your Django application:

Cloudinary credentials in your Django application:
  
  [Sign up](https://cloudinary.com/) for a Cloudinary account if you haven't already.
  Obtain your Cloudinary API credentials (Cloud name, API Key, API Secret).
  Set the following environment variables in your environment (local development, CI/CD):<br>
  
    - CLOUDINARY_CLOUD_NAME: Your Cloudinary cloud name  
    - CLOUDINARY_API_KEY: Your Cloudinary API key  
    - CLOUDINARY_API_SECRET: Your Cloudinary API secret  
</details>
</details><br>

### Deployment 
<br>

This app is deployed on Heroku at https://liveartcorner-5afce0fdefed.herokuapp.com/


#### Author
Gavin Humphrey

<small>&copy; All rights reserved.</small><br><br>

<details>
<summary><strong>Version Française</strong></summary>
<details>
<summary><strong>Table des matières</strong></summary>

- - [LIVE-ART-CORNER fr](#live-art-corner-fr)
  - [Fonctionnalités](#fonctionnalités)
  - [Prerequis](#prerequis)
  - [Installation et lancement](#installation-et-lancement)
  - [Production fr](#production-fr)
  - [Deploiement](#deploiement)
  - [Auteur](#auteur)

</details>

## LIVE-ART-CORNER fr
LIVE-ART-CORNER est une application Python/Django où les artistes peuvent afficher et vendre leurs œuvres d'art aux utilisateurs. Les artistes doivent s'abonner et se faire vérifier pour télécharger leurs œuvres et répertorier des services personnalisés. Seuls les utilisateurs enregistrés peuvent accéder aux services personnalisés et aux pages de profil des artistes, tandis que la place de marché est ouverte à tous les clients.

### Fonctionnalités
- Les artistes peuvent afficher et vendre des œuvres d'art.
- Processus d'abonnement et de vérification pour les artistes.
- Services personnalisés offerts par les artistes (portrait, dessins de paysages, peintures via webcam).
- Les utilisateurs enregistrés peuvent accéder aux services personnalisés et aux profils des artistes.
- La place de marché est ouverte à tous les utilisateurs ; seuls les utilisateurs enregistrés peuvent ajouter des articles à la liste de souhaits.
- Animation de défilement pour les articles populaires sur la page d'accueil.
- Articles affichés dans des cartes, chacune représentant la boutique d'un artiste.
- Vue détaillée des articles lorsqu'ils sont cliqués.

### Prerequis
Avant de commencer, assurez-vous d'avoir installé les éléments suivants :

- [Git](https://git-scm.com/)
- [Sentry](https://sentry.io/)
- [PostgreSQL](https://www.postgresql.org/)
- [Cloudinary](https://cloudinary.com/)
- [Docker](https://www.docker.com/)
- [CircleCI](https://circleci.com/)
- [Heroku](https://www.heroku.com/)

### Installation et lancement
1. **Installez Python :**

- [Guide d'installation de Python](https://www.python.org/)

2. **Clonez le dépôt :**

    ```bash 
        git clone https://github.com/Gavin-Humphrey/liveartcorner.git

<strong>Créez et activez un environnement virtuel :</strong><br>
python -m venv env<br><br>

<strong>macOS/Linux:</strong><br>
source env/bin/activate  <br><br>
<strong>Windows:</strong><br>
env\scripts\activate.bat<br><br> 
<strong>Installez les packages requis :</strong><br>
pip install -r requirements.txt<br><br>
<strong>Migrez la base de données :</strong><br>
python manage.py makemigrations<br>
python manage.py migrate<br><br>
<strong>Collectez les fichiers statiques :</strong><br>
python manage.py collectstatic<br><br>
<strong>Lancez le serveur :</strong><br>
python manage.py runserver,<br>
Access the application at http://127.0.0.1:8000

<strong>Tests unitaires</strong><br>
**Exécutez les tests unitaires à l'aide de Pytest :**<br>
pytest<br><br>

### Production fr
<details>
<summary><strong>CircleCI</strong></summary>
Suivez ces étapes pour configurer CircleCI :

Créez un compte CircleCI et connectez votre compte GitHub.
Créez un nouveau projet et sélectionnez votre dépôt GitHub.
Ajoutez les variables d'environnement requises aux paramètres du projet CircleCI :
DOCKER_USERNAME : Votre nom d'utilisateur Docker Hub
DOCKER_LOGIN : Votre adresse e-mail de connexion Docker Hub
HEROKU_APP_NAME : Le nom de votre application Heroku
HEROKU_TOKEN : Votre clé API Heroku
Poussez un nouveau commit à votre dépôt pour déclencher une nouvelle construction sur CircleCI.
</details>
<details>
<summary><strong>Sentry</strong></summary>
Ce projet utilise Sentry pour le suivi des erreurs. Pour configurer Sentry :

Créez un compte Sentry et créez un nouveau projet.

Ajoutez la variable d'environnement SENTRY_DSN au fichier .env de votre projet.

Installez le package Python Sentry SDK :


pip install sentry-sdk
Ajoutez le code généré au fichier settings.py.


</details>
<details>
<summary><strong>Configuration de Cloudinary</strong></summary>
Pour utiliser Cloudinary pour le stockage et la manipulation d'images/vidéos, vous devez configurer les identifiants Cloudinary dans votre application Django :

[Inscrivez-vous](https://cloudinary.com/) pour un compte Cloudinary si ce n'est pas déjà fait.
Obtenez vos identifiants API Cloudinary (nom du cloud, clé API, secret API).
Définissez les variables d'environnement suivantes dans votre environnement (développement local, CI/CD) :
CLOUDINARY_CLOUD_NAME : Le nom de votre cloud Cloudinary
CLOUDINARY_API_KEY : Votre clé API Cloudinary
CLOUDINARY_API_SECRET : Votre secret API Cloudinary

</details><br>

### Deploiement
<br>
Le projet est déployé sur Heroku à l'adresse https://liveartcorner-5afce0fdefed.herokuapp.com/

#### Auteur
Gavin Humphrey

<small>&copy; Tous droits réservés.</small>
</details>
