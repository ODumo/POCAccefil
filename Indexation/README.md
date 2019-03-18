# Indexation

## Installation

Une installation par docker pourra être effectuée (une installation plus classique est toujours envisageable). Les requêtes et la configuration d'elasticseach se feront donc par l'API REST de l'image.

Installation via docker :

```
docker pull docker.elastic.co/elasticsearch/elasticsearch:6.6.2

docker run --name "elasticsearch" -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:6.6.2
```
Une fois l'image lancée, l'API elasticsearch est attaquable sur le port 9200 sur localhost. Pour l'exemple nous utilisons curl pour effectuer les requêtes. Cependant le script python _indexation.py_ se chargera d'effectuer la plupart des actions à partir de la librairie d'elasticsearch. En effet elasticsearch propose des librairies pour une multitude de langages qui permettent de faciliter les échanges.


## Utilisation

Tout d'abord, il est nécessaire de créer un index de la manière suivante :
```
curl -X PUT "localhost:9200/pocaccefil?pretty"
```
L'option "pretty" permet d'avoir le retour de la requête dans un format JSON lisible.

Les documents que nous ajouterons seront stockés à cet index.

Pour l'exemple, nous utiliserons le contenu des deux documents Bill.txt et Steve.txt. Ces textes correspondent au premier paragraphe des pages Wikipedia de Bill Gates et Steve Jobs.

Nous allons donc commencer par entrer les données dans elasticsearch. Pour cela nous allons effectuer les requêtes suivantes :
```
curl -X PUT "localhost:9200/pocaccefil/documents/bill" -H 'Content-Type: application/json' -d '{
    "path" : "Bill.txt",
    "content" : "William Henry Gates III,..."
}'

curl -X PUT "localhost:9200/pocaccefil/documents/steve" -H 'Content-Type: application/json' -d '{
    "path" : "Steve.txt",
    "content" : "Steven Paul Jobs,..."
}'
```
Ici nous utilisons des textes bruts et courts. En cas de textes plus importants, il est nécessaire d'effectuer des pré-traitements des textes comme par exemple supprimer les stopwords (articles, mots courts et courants, etc).

La recherche d'informations s'effectue simplement en utilisant leur langage de requête qui est un JSON qui se doit de correspondre à une structure attendue. Ce JSON est envoyé à une url avec le paramètre *_search* dans notre index.

```
curl -X GET "localhost:9200/pocaccefil/_search" -H 'Content-Type: application/json' -d '{
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
}'
```
Ici nous cherchons à récupérer le document discutant de Bill Gates. Nous allons donc utiliser le nom de son entreprise qui apparaît dans le paragraphe. La requête au dessus demande donc de chercher le terme *Microsoft* dans la clé *content*.

La seconde partie de la recherche permet d'ajouter un deuxième terme *Gattes* qui correspond donc au nom *Gates* mal orthographié. Pour utiliser la distance de Levenshtein, le paramètre *fuzziness* est ajouté. Ce paramètre indique la distance maximale autorisée pour considérer un mot comme acceptable.
