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

## Code
### Requete.py

Ce code s'occupe de lire l'input ( pour le moment, l'implémentation pour lire un fichier .txt est tout à fait viable ),
qui le parsera à l'interpreter pour trouver un intent présent à la fois dans l'input et dans les training models du model.

```
ipt = input("Entrer l'expression à analyser ou exit pour quitter : ")
    while ipt != "exit":
        parsed = interpreter.parse(ipt)
```

Si le score de confidence attribué par RASA sur l'intent trouvé est assez élevé et qu'il est présent dans la structure
de donnée alors le score de l'intent est augmenté de sa confidence.

```
if parsed["intent"]["confidence"] > 0.4 and parsed["intent"]["name"] in context :
            context[parsed["intent"]["name"]]["score"]+=parsed["intent"]["confidence"]
```

Ensuite, on sauvegarde les entities trouvé s'il y en a.

```
for entity in parsed["entities"]:
            entities.append(entity)

```

Et finalement, on classe les contexts en fonction de le leur score afin de faire ressortir le sujet de discussion le plus probable.

```
ranked_context = sorted(list(context.values()),key= lambda x: x["score"], reverse=True)
```

### nlu_config.yml

Ici, il est très simple, il configure le langage et les entraineurs nécéssaires.

```
language: "fr"
pipeline: "spacy_sklearn"
```

### nlu_trainer.py

Permet quelques économies de performances.

```
builder = ComponentBuilder(use_cache=True)
```

Chargement des données d'entrainement.

```
training_data = load_data('data/nlu')
```

Création de l'entraineur associé à la configuration.

```
trainer = Trainer(config.load("./nlu_config.yml"), builder)
```

Entrainement.

```
trainer.train(training_data)
```

Sauvegarde du modèle entrainé.

```
model_directory = trainer.persist('./projects/default/', fixed_model_name="model")
```
