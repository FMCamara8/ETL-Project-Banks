# ETL-Project-Banks
# Présentation
Ce projet est un pipeline de données automatisé qui récupère les informations sur les plus grandes banques mondiales par capitalisation boursière. L'objectif est de centraliser des données provenant du web, de les convertir en plusieurs devises et de les organiser pour qu'elles soient prêtes à être analysées.

# Fonctionnement du code
Le script suit trois étapes principales (ETL) :

- Extraction : le code va chercher les données sur une page Wikipédia (archive) en utilisant le Web Scraping.

- Transformation :
    Nettoyage des données pour qu'elles soient exploitables par Python.
    Conversion de la valeur boursière (USD) en GBP, EUR et INR grâce à un fichier de taux de change externe     (exchange_rate.csv).
    Arrondi des chiffres à deux décimales.

- Chargement :
    Création d'un fichier de sortie au format CSV.
    Insertion automatique dans une base de données SQL (Banks.db).

# Outils utilisés
- Langage : Python

# Bibliothèques :
- Pandas et NumPy pour la gestion des tableaux de données.
- BeautifulSoup pour l'extraction web.
- SQLite3 pour la partie base de données.
- IDE :  Visual Studio Code

# Comment lancer le projet
1. Téléchargez les fichiers banks_project.py et exchange_rate.csv dans le même dossier.
2. Installez les bibliothèques nécessaires avec la commande : pip install pandas beautifulsoup4 requests.
3. Exécutez le script : python banks_project.py.
4. Consultez le fichier code_log.txt pour voir l'historique d'exécution.
