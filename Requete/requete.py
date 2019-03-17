from rasa_nlu.model import Interpreter
from operator import itemgetter

if __name__ == "__main__":

    print("Chargement du modèle, cette action peut prendre du temps.")
    interpreter = Interpreter.load("./projects/default/default/model")

    """
    La structure context correspond à l'ensemble des intents permettant de déterminer
    un type de document. Un classement est effectué en fonction du score de chaque élément.
    Le score correspond à la valeur "confidence" retournée par l'interpréteur de RASA.
    Si deux phrase retourne le même intent, son score dans intent_ranking sera la somme 
    des valeurs de "confidence" de RASA. Celà permet d'affiner la recherche et limiter
    les erreurs au fil de la conversation.

    On pourra associer à chaque intent de cette structure une liste de mots correspondant
    au document et qui seront utilisés pour la recherche dans les documents indexés.
    """
    context = {
        "hospitalisation": {"score":0, "mots":["hospitalisation","service"]},
        "remboursement": {"score":0, "mots":["remboursement","client"]},
        "analyse_sang": {"score":0, "mots":["lipide","analyse"]}
    }

    #Ensemble des entités récupérées.
    entities = []

    #Boucle d'inputs
    ipt = input("Entrer l'expression à analyser ou exit pour quitter : ")
    while ipt != "exit":
        parsed = interpreter.parse(ipt)
        """
        Modification du context seulement si l'intent en fait parti et si sa valeur "confidence" est supérieure 
        au palier établi arbitrairement.
        """
        if parsed["intent"]["confidence"] > 0.4 and parsed["intent"]["name"] in context :
            #Incrémentation du score de l'intent
            context[parsed["intent"]["name"]]["score"]+=parsed["intent"]["confidence"]
        
        for entity in parsed["entities"]:
            entities.append(entity)

        ipt = input("Entrer l'expression à analyser ou exit pour quitter : ")

    #Tri en fonction du score
    ranked_context = sorted(list(context.values()),key= lambda x: x["score"], reverse=True)

    #Affichage de l'intent en tête : Score et mots associés pour la recherche dans les documents
    print("Intent le mieux classé :",ranked_context[0])
    #Affichage des entités récupérées
    print("Entités :",entities)