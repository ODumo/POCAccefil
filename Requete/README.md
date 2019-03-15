# Module de requête
## Installation
### Via python  :
Pour une installation via package python les commandes suivantes doivent être exécutées.

Dans la racine du projet, pour installer l'environnement virtuel :
```
virtualenv venv

#sous linux
source venv/bin/activate

#sous windows
source venv/Scripts/activate
```

Une fois dans l'environnement, il est nécessaire d'y installer les packets python requis:

```
# Installation de rasa_nlu
pip install rasa_nlu

# Installation des éléments nécessaires pour faire communiquer rasa et spacy
pip install rasa_nlu[spacy]
```
Pour la suite, il faut télécharger les modèles de spacy dont nous nous servons pour entrainer les données.

```
python -m spacy download fr_core_news_md
python -m spacy link fr_core_news_md fr
```

La commande link permet d'utiliser "fr" à la place du nom complet du modèle.
