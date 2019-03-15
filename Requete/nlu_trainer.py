from rasa_nlu.training_data import load_data
from rasa_nlu import config
from rasa_nlu.components import ComponentBuilder
from rasa_nlu.model import Trainer

#Permet quelques économies de performances
builder = ComponentBuilder(use_cache=True)

#Chargement des données d'entrainement
training_data = load_data('data/nlu')
#Création de l'entraineur associé à la configuration
trainer = Trainer(config.load("./nlu_config.yml"), builder)
#Entrainement
trainer.train(training_data)
#Sauvegarde du modèle entrainé
model_directory = trainer.persist('./projects/default/', fixed_model_name="model")