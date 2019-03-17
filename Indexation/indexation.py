from elasticsearch import Elasticsearch

es = Elasticsearch()

#Récupération du contenu Bill Gates
with open("Bill.txt") as f :
    bill_data = f.read()
f.close()
bill = {
    "path" : "Bill.txt",
    "content" : bill_data
}

#Récupération du contenu Steve Jobs
with open("Steve.txt") as f :
    steve_data = f.read()
f.close()
steve = {
    "path" : "Steve.txt",
    "content" : steve_data
}

print("Création des documents (ou mise à jour si existant)")
#Insertion des données dans l'index
res = es.index(index="pocaccefil", doc_type='document', id="bill", body=bill)
print(res["result"])
res = es.index(index="pocaccefil", doc_type='document', id="steve", body=steve)
print(res["result"])

"""
Recherche dans l'index pocaccefil.
Dans cet exemple on match les document qui ont obligatoirement Microsoft
dans leur contenu. L'autre partie de la requête effectue la même chose avec le mot "Gattes"
qui correspond à une erreur d'écriture. Le paramètre fuzziness permet l'utilisation de la
distance de Levenshtein et indique la distance maximale autorisée pour considérer un match.
"""
print("Recherche dans l'index")
res = es.search(index="pocaccefil", body={
    "query": {
        "bool":{
            "must":{
                "match": {
                    "content": "Microsoft"
                },
                "match": {
                    "content": {
                        "query": "Gattes",
                        "fuzziness": 2
                    }
                }
            }
        }
    }
})


print("Chemin du fichier retourné :",res["hits"]["hits"][0]["_source"]["path"])